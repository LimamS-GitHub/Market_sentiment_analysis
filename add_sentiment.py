import re
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

file_path = 'data/data_cleaned.csv'  # Remplace par le chemin réel
data = pd.read_csv(file_path)

# Afficher quelques tweets pour analyser leur structure
print(data['TWEET'].head(10))
def clean_tweet(tweet):
    # 1. Retirer les mentions (@username)
    tweet = re.sub(r'@', '', tweet)
    
    # 3. Retirer les liens (http:// ou https://)
    tweet = re.sub(r'http\S+|www\S+', '', tweet)
    
    # 4. Retirer les caractères spéciaux
    tweet = re.sub(r'[^\w\s]', '', tweet)  # Garde seulement les lettres, chiffres et espaces
    
    # 5. Retirer les chiffres
    tweet = re.sub(r'\d+', '', tweet)
    
    # 6. Retirer les espaces en trop
    tweet = tweet.strip()
    
    return tweet

# Appliquer le nettoyage à tous les tweets
data['CLEANED_TWEET'] = data['TWEET'].apply(clean_tweet)

# Afficher les tweets avant et après nettoyage
print(data[['TWEET', 'CLEANED_TWEET']].head(10))

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_vader(tweet):
    score = analyzer.polarity_scores(tweet)
    return score['compound']

data['SENTIMENT'] = data['CLEANED_TWEET'].apply(analyze_sentiment_vader)
output_file_path = 'data/sentiment_data_cleaned.csv'  # Remplace par le chemin désiré
data.to_csv(output_file_path, index=False)

print(f"Fichier nettoyé enregistré sous : {output_file_path}")
