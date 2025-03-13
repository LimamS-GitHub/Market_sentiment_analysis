from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

#--------------------------------------------------------------------------------------------------------------------

def analyze_sentiment_vader(tweet):
    score = SentimentIntensityAnalyzer().polarity_scores(tweet)
    return score['compound']

#--------------------------------------------------------------------------------------------------------------------

def models_sentiment():
    models = [
        pipeline("text-classification", model="ahmedrachid/FinancialBERT-Sentiment-Analysis"),
        pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"),
        pipeline("text-classification", model="mrm8488/deberta-v3-ft-financial-news-sentiment-analysis"),
        pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
    ]
    return models

#--------------------------------------------------------------------------------------------------------------------

def sentiment(tweet, model):
    result = model(tweet)[0]
    label = result['label'].upper()
    return 1 if label == 'POSITIVE' else -1 if label == 'NEGATIVE' else 0