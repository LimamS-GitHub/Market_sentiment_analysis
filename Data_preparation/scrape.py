import pandas as pd
from driver import scroll_page, click_load_more
from utils import is_english_text
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import timedelta,datetime
from selenium.webdriver.support import expected_conditions as EC

#----------------------------------------------------------------------------------------------------------------------------

def extract_tweets(driver, date_):
    """Extracts tweets from the current Nitter page and returns a list of dictionaries."""
    tweet_data = []
    tweet_divs = driver.find_elements(By.CSS_SELECTOR, "div.timeline-item")

    for div in tweet_divs:
        # Get tweet content and ID if available
        tweet_text = div.find_element(By.CSS_SELECTOR, ".tweet-content").text if div.find_elements(By.CSS_SELECTOR, ".tweet-content") else ""
        tweet_id = div.find_element(By.CSS_SELECTOR, ".tweet-date a").get_attribute("href").split("/")[-1] if div.find_elements(By.CSS_SELECTOR, ".tweet-date a") else ""
        
        # Check if account is verified
        verified = div.find_elements(By.CSS_SELECTOR, "span.icon-ok.verified-icon.blue[title='Verified blue account']")

        # Keep only English tweets
        if is_english_text(tweet_text):
            tweet_data.append({
                "id": tweet_id,
                "query_date": datetime.strptime(date_, "%Y-%m-%d") - timedelta(days=1),
                "text": tweet_text,
                "verified": bool(verified)
            })
            
    print(f"{len(tweet_divs)} tweets found for {date_} with {len(tweet_data)} in English")
    return tweet_data, len(tweet_divs)

#----------------------------------------------------------------------------------------------------------------------------

def scrape_nitter_date_range(driver, date_list, number_tweets_per_day,company_name="tesla"):
    """Goes through a list of dates and collects tweets from each day."""
    all_data = []
    
    for date_ in date_list:
        print("Processing date:", date_)
        total_tweets_day = 0

        try:
            #url = f"https://lightbrd.com/search?f=tweets&q={company_name}&f-verified=on&since=&until={date_}&near="
            url = f"https://nitter.net/search?f=tweets&q={company_name}&f-verified=on&since={(pd.to_datetime(date_) - pd.DateOffset(days=1)).strftime("%Y-%m-%d")}&until={date_}"
            driver.get(url)
            
            # Wait for tweets to appear on the page
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.timeline-item"))
            )

            # Keep scrolling and loading tweets until the desired amount is reached
            while click_load_more(driver) and total_tweets_day < number_tweets_per_day:
                tweet_data, number_tweets = extract_tweets(driver, date_)
                all_data.extend(tweet_data)
                total_tweets_day += number_tweets
                scroll_page(driver)
                
        except Exception as e:
            print(f"Error for {date_}: {str(e)}")
        
    return all_data