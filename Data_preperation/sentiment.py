from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# --------------------------------------------------------------------------------------------------------------------

def analyze_sentiment_vader(tweet):
    score = SentimentIntensityAnalyzer().polarity_scores(tweet)
    return score['compound']

# --------------------------------------------------------------------------------------------------------------------

def models_sentiment():
    models = [
        pipeline("text-classification", model="ahmedrachid/FinancialBERT-Sentiment-Analysis", truncation=True),
        pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis", truncation=True),
        pipeline("text-classification", model="mrm8488/deberta-v3-ft-financial-news-sentiment-analysis", truncation=True),
        pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis", truncation=True)
    ]
    return models

# --------------------------------------------------------------------------------------------------------------------

def sentiment(tweet, model):
    # Tronquer le texte en caractères (sécurité + performance)
    tweet = tweet[:2000]
    try:
        result = model(tweet)[0]
        label = result['label'].upper()
        return 1 if label == 'POSITIVE' else -1 if label == 'NEGATIVE' else 0
    except Exception as e:
        print(f"❌ Erreur d'analyse de sentiment : {e}")
        return 0  # Neutre en cas d'échec
