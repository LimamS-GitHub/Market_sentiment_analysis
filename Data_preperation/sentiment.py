from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment_vader(tweet):
    score = SentimentIntensityAnalyzer().polarity_scores(tweet)
    return score['compound']
