from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# --------------------------------------------------------------------------------------------------------------------

def analyze_sentiment_vader(tweet):
    """Sentiment analysis using VADER (returns compound score between -1 and 1)"""
    score = SentimentIntensityAnalyzer().polarity_scores(tweet)
    return score['compound']

# --------------------------------------------------------------------------------------------------------------------

def models_sentiment():
    """Load pre-trained sentiment analysis models focused on financial text"""
    models = [
        pipeline("text-classification", model="ahmedrachid/FinancialBERT-Sentiment-Analysis", truncation=True),
        pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis", truncation=True),
        pipeline("text-classification", model="mrm8488/deberta-v3-ft-financial-news-sentiment-analysis", truncation=True),
        pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis", truncation=True)
    ]
    return models

# --------------------------------------------------------------------------------------------------------------------

def sentiment(tweet, model):
    """Truncate text and apply sentiment model"""
    tweet = tweet[:2000]
    try:
        result = model(tweet)[0]
        label = result['label'].upper()
        return 1 if label == 'POSITIVE' else -1 if label == 'NEGATIVE' else 0
    except Exception as e:
        print(f"❌ Sentiment analysis error: {e}")
        return 0
