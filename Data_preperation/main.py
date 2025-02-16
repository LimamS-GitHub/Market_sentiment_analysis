import pandas as pd
from driver import initialize_driver
from scrape import scrape_nitter_date_range
from utils import generate_date_list
from datetime import date
from utils import clean_tweet
from sentiment import analyze_sentiment_vader

def main():
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
            df_tweet.to_csv("tweets.csv", index=False, encoding="utf-8-sig")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
