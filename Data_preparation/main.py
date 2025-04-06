import pandas as pd
from driver import initialize_driver
from scrape import scrape_nitter_date_range
from utils import generate_date_list, clean_tweet, valid_proxy, list_proxies
from datetime import date, datetime
from sentiment import analyze_sentiment_vader, models_sentiment, sentiment

def save_month(monthly_buffer, month_key):
    """Save monthly tweets to CSV."""
    if monthly_buffer:
        df = pd.concat(monthly_buffer, ignore_index=True)
        path = f"C:\\Users\\selim\\Desktop\\Market_sentiment_analysis\\Data_preperation\\{month_key}.csv"
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"💾 Month {month_key} saved with {len(df)} tweets.")

def process_tweet_data(df_tweet, models):
    """Clean and analyze sentiment on tweet DataFrame."""
    df_tweet['CLEANED_TWEET'] = df_tweet['text'].apply(clean_tweet)
    df_tweet['SENTIMENT_VADER'] = df_tweet['text'].apply(analyze_sentiment_vader)
    for model in models:
        name = model.model.name_or_path.split("/")[-1]
        df_tweet[f'SENTIMENT_{name}'] = df_tweet['CLEANED_TWEET'].apply(lambda x: sentiment(x, model))
    return df_tweet

def main(start_date, end_date, minimum_number_tweets_per_day):
    date_list = generate_date_list(start_date, end_date)
    models = models_sentiment()
    all_tweets, monthly_buffer = [], []
    ip_list = list_proxies()
    proxy, _ = valid_proxy(ip_list)
    current_month = None

    for date_str in date_list:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        month_key = date_obj.strftime("%Y-%m")

        # Save previous month if changed
        if current_month and month_key != current_month:
            save_month(monthly_buffer, current_month)
            monthly_buffer = []

        current_month = month_key
        success, attempt = False, 0

        while not success:
            print(f'📅 {date_str} | Attempt {attempt}')
            if attempt > 2:
                if not ip_list:
                    print("❌ No valid proxies left.")
                    ip_list = list_proxies()
                    break
                proxy, _ = valid_proxy(ip_list)
                attempt = 0

            try:
                driver = initialize_driver(proxy)
                tweet_data = scrape_nitter_date_range(driver, [date_str], minimum_number_tweets_per_day)
                driver.quit()

                df = pd.DataFrame(tweet_data)
                if not df.empty:
                    df = process_tweet_data(df, models)
                    all_tweets.append(df)
                    monthly_buffer.append(df)
                    print(f"✅ {len(df)} tweets collected for {date_str}")
                    success = True
                else:
                    attempt += 1

            except Exception as e:
                print(f"❌ Error on {date_str}: {e}")
                attempt += 1
                try:
                    driver.quit()
                except:
                    pass
    # Save all data
    if all_tweets:
        final_df = pd.concat(all_tweets, ignore_index=True)
        final_df.to_csv("C:\\Users\\selim\\Desktop\\Market_sentiment_analysis\\Data_preperation\\All_tweets.csv", index=False, encoding="utf-8-sig")
        print(f"\n📦 Global file saved with {len(final_df)} tweets.")

if __name__ == "__main__":
    start_date = date(2022, 1, 2)
    end_date = date(2025, 1, 2)
    minimum_number_tweets_per_day = 5
    main(start_date, end_date, minimum_number_tweets_per_day)
