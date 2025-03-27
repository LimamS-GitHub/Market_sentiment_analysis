import pandas as pd
from driver import initialize_driver
from scrape import scrape_nitter_date_range
from utils import generate_date_list, clean_tweet,valid_proxy
from datetime import date, datetime
from sentiment import analyze_sentiment_vader, models_sentiment, sentiment

def main():
    start_date = date(2022, 1, 2)
    end_date = date(2025, 1, 2)
    date_list = generate_date_list(start_date, end_date)
    models = models_sentiment()

    minimum_number_tweets_per_day = 50
    all_tweets = []
    current_month = None
    monthly_dfs = {}  # Pour la sauvegarde par mois

    for single_date in date_list:
        valide = 1
        attempt = 0

        while valide:
            print(f'📅 {single_date} | Attempt: {attempt}')
            current_month_ = datetime.strptime(single_date, "%Y-%m-%d").date().month
            if current_month_ != current_month or attempt > 0:
                current_month = current_month_
                proxy = valid_proxy()

            driver = None
            try:
                driver = initialize_driver(proxy)
                tweet_data = scrape_nitter_date_range(driver, [single_date], minimum_number_tweets_per_day)
                df_tweet = pd.DataFrame(tweet_data)

                if not df_tweet.empty:
                    df_tweet['CLEANED_TWEET'] = df_tweet['text'].apply(clean_tweet)
                    df_tweet['SENTIMENT_VADER'] = df_tweet['text'].apply(analyze_sentiment_vader)

                    for model in models:
                        df_tweet[f'SENTIMENT_{model.model.name_or_path.split("/")[-1]}'] = df_tweet['CLEANED_TWEET'].apply(
                            lambda x: sentiment(x, model)
                        )

                    all_tweets.append(df_tweet)
                    month_key = single_date[:7]  # Format 'YYYY-MM'

                    if month_key not in monthly_dfs:
                        monthly_dfs[month_key] = []

                    monthly_dfs[month_key].append(df_tweet)
                    valide = 0
                    print(f"✅ {len(df_tweet)} tweets collectés pour {single_date}")
                else:
                    attempt += 1

            except Exception as e:
                print(f"❌ Erreur pour {single_date} : {e}")
                attempt += 1

            finally:
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass

    # Sauvegarde générale
    if all_tweets:
        final_df = pd.concat(all_tweets, ignore_index=True)
        final_df.to_csv("C:\\Users\\selim\\Desktop\\Market_sentiment_analysis\\Data_preperation\\All_tweets.csv", index=False, encoding="utf-8-sig")
        print(f"\n💾 Fichier global : {len(final_df)} tweets enregistrés.")

    # Sauvegarde par mois
    for month_key, dfs in monthly_dfs.items():
        monthly_df = pd.concat(dfs, ignore_index=True)
        filename = f"tweets_{month_key}.csv"
        monthly_df.to_csv("C:\\Users\\selim\\Desktop\\Market_sentiment_analysis\\Data_preperation\\"+filename, index=False, encoding="utf-8-sig")
        print(f"📁 Sauvegardé : {filename} ({len(monthly_df)} tweets)")

if __name__ == "__main__":
    main()

