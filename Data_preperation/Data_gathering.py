import time
import pandas as pd
import re
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from langdetect import detect
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#------------------------------------------------------------------------------------------------------------------

def initialize_driver():
    """Initializes and returns a Selenium driver in headless mode."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Silent mode
    return webdriver.Chrome(service=service, options=options)

#------------------------------------------------------------------------------------------------------------------

def scroll_page(driver, scroll_attempts=3):
    """Scrolls down the page to load more tweets."""
    prev_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(scroll_attempts):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == prev_height:
            break
        prev_height = new_height

#------------------------------------------------------------------------------------------------------------------

def click_load_more(driver):
    """Clicks only on the 'Load more' button and ignores 'Load newest'."""
    try:
        load_more_buttons = driver.find_elements(By.CSS_SELECTOR, "div.show-more a")
        for button in load_more_buttons:
            if "Load more" in button.text:  # Checks if it's indeed 'Load more'
                button.click()
                time.sleep(2)  # Wait for new tweets to load
                return True
        return False  # No 'Load more' button found
    except Exception as e:
        print(f"Error clicking 'Load more': {e}")
        return False

#------------------------------------------------------------------------------------------------------------------

def is_english_text(text):
    try:
        language = detect(text)
        return language == 'en'
    except:
        return False
    
#------------------------------------------------------------------------------------------------------------------

def extract_tweets(driver, date_):
    """Extracts the tweets present on the page and returns a list of dictionaries."""
    tweet_data = []
    tweet_divs = driver.find_elements(By.CSS_SELECTOR, "div.timeline-item")


    for div in tweet_divs:
        tweet_text = div.find_element(By.CSS_SELECTOR, ".tweet-content").text if div.find_elements(By.CSS_SELECTOR, ".tweet-content") else ""
        tweet_id = div.find_element(By.CSS_SELECTOR, ".tweet-date a").get_attribute("href").split("/")[-1] if div.find_elements(By.CSS_SELECTOR, ".tweet-date a") else ""
        verified = div.find_elements(By.CSS_SELECTOR, "span.icon-ok.verified-icon.blue[title='Verified blue account']")
        if is_english_text(tweet_text):
            tweet_data.append({"id": tweet_id, "query_date": date_, "text": tweet_text, "verified": bool(verified)})
            
    print(f"{len(tweet_divs)} tweets found for {date_} with {len(tweet_data)} in English")
    return tweet_data, len(tweet_divs)


#------------------------------------------------------------------------------------------------------------------

def analyze_sentiment_vader(tweet):
    score = SentimentIntensityAnalyzer().polarity_scores(tweet)
    return score['compound']

#------------------------------------------------------------------------------------------------------------------

def clean_tweet(tweet):
    """Cleans a tweet by removing mentions, links, special characters, and numbers."""
    tweet = re.sub(r'@', '', tweet)
    tweet = re.sub(r'http\S+|www\S+', '', tweet)
    #tweet = re.sub(r'[^\w\s]', '', tweet)
    tweet = re.sub(r'\d+', '', tweet)
    tweet = re.sub(r'\n', '', tweet)
    tweet = tweet.strip()
    
    return tweet

#------------------------------------------------------------------------------------------------------------------

def scrape_nitter_date_range(driver, date_list, number_tweets_per_day):
    """Iterates through a list of dates and retrieves the corresponding tweets."""
    all_data = []
    
    for date_ in date_list:
        print("Processing date:", date_)
        total_tweets_day = 0
        try:
            url = f"https://nitter.net/search?f=tweets&q=Tesla&until={date_}"
            driver.get(url)
            
            # Wait for tweets to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.timeline-item"))
            )

            while click_load_more(driver) and total_tweets_day < number_tweets_per_day:
                tweet_data, number_tweets = extract_tweets(driver, date_)
                all_data.extend(tweet_data)
                total_tweets_day += number_tweets
                scroll_page(driver) 
                
        except Exception as e:
            print(f"Error for {date_}: {str(e)}")
        
    return all_data

#------------------------------------------------------------------------------------------------------------------

def generate_date_list(start_date, end_date):
    """Generates a list of dates between start_date and end_date."""
    return [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]

#------------------------------------------------------------------------------------------------------------------

def save_to_csv(data, filename="tweets.csv"):
    """Saves the collected data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")

#------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    start_date = date(2023, 11, 4)
    end_date = date(2023, 11, 5)
    date_list = generate_date_list(start_date, end_date)
    
    driver = initialize_driver()
    try:
        minimum_number_tweets_per_day = 5

        tweet_data = scrape_nitter_date_range(driver, date_list, minimum_number_tweets_per_day)
        df_tweet = pd.DataFrame(tweet_data)
        
        if not df_tweet.empty:
            df_tweet['CLEANED_TWEET'] = df_tweet['text'].apply(clean_tweet)
            df_tweet['SENTIMENT'] = df_tweet['text'].apply(analyze_sentiment_vader)
            print(f'Total number of tweets: {len(df_tweet)}')
            save_to_csv(df_tweet)
    finally:
        driver.quit()
