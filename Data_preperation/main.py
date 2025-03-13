import pandas as pd
from driver import initialize_driver
from scrape import scrape_nitter_date_range
from utils import generate_date_list, clean_tweet
from datetime import date
from sentiment import analyze_sentiment_vader, models_sentiment, sentiment

def main():
    start_date = date(2023, 4, 3)
    end_date = date(2023, 4, 5)
    date_list = generate_date_list(start_date, end_date)
    models = models_sentiment()
    driver = initialize_driver()
    try:
        minimum_number_tweets_per_day = 10
        all_tweets = []

        for single_date in date_list:
            try:
                tweet_data = scrape_nitter_date_range(driver, [single_date], minimum_number_tweets_per_day)
                df_tweet = pd.DataFrame(tweet_data)
                
                if not df_tweet.empty:
                    df_tweet['CLEANED_TWEET'] = df_tweet['text'].apply(clean_tweet)
                    df_tweet['SENTIMENT_VADER'] = df_tweet['text'].apply(analyze_sentiment_vader)
                    for model in models:
                        df_tweet[f'SENTIMENT_{model.model.name_or_path.split('/')[-1]}'] = df_tweet['CLEANED_TWEET'].apply(lambda x: sentiment(x, model))
                    all_tweets.append(df_tweet)
                    print(f'Total number of tweets for {single_date}: {len(df_tweet)}')
            except Exception as e:
                print(f"Error for {single_date}: {e}")

        if all_tweets:
            final_df = pd.concat(all_tweets, ignore_index=True)
            final_df.to_csv("tweets.csv", index=False, encoding="utf-8-sig")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

