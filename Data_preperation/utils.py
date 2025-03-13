import re
from datetime import timedelta
from langdetect import detect

#------------------------------------------------------------------------------------------------------------------

def is_english_text(text):
    try:
        language = detect(text)
        return language == 'en'
    except:
        return False

#------------------------------------------------------------------------------------------------------------------

def clean_tweet(tweet):
    """Cleans a tweet by removing mentions, links, special characters, and numbers."""
    tweet = re.sub(r'@', '', tweet)
    tweet = re.sub(r'http\S+|www\S+', '', tweet)
    tweet = re.sub(r'[^\w\s]', '', tweet)
    tweet = re.sub(r'\d+', '', tweet)
    tweet = re.sub(r'\n', '', tweet)
    tweet = tweet.strip()
    
    return tweet

#------------------------------------------------------------------------------------------------------------------

def generate_date_list(start_date, end_date):
    """Generates a list of dates between start_date and end_date."""
    return [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
