import random
import numpy as np


class SentimentTradingModel:
    """
    Modèle de trading basé sur l'analyse des sentiments.
    Il combine plusieurs modèles de sentiment pour générer des signaux d'achat et de vente pour une action donnée.
    Paramètres du modèle:
    - weights : liste de poids pour chaque modèle de sentiment
    - buy_threshold : seuil pour générer un signal d'achat
    - sell_threshold : seuil pour générer un signal de vente
    - sentiment_cols : liste des colonnes de sentiment à utiliser
    - initial_cash : montant initial en espèces pour le trading (par défaut 1000)
    - weight_verified : poids pour le modèle de sentiment vérifié
    - weight_non_verified : poids pour le modèle de sentiment non vérifié

    Méthodes principales:
    - combine_sentiments : combine les sentiments en utilisant la moyenne pondérée
    - generate_signal : génère les signaux d'achat/vente/attente selon les sentiments combinés
    - apply_sentiment_weights : applique la pondération verified / non_verified pour chaque modèle de sentiment
    - train : optimise les hyperparamètres avec une recherche aléatoire
    - test : teste le modèle sur un ensemble de données donné
    - print_model_params : affiche les paramètres actuels du modèle
    """

    def __init__(self, weights, buy_threshold, sell_threshold, sentiment_cols,weight_verified, initial_cash=1000):
        """
        Initialise le modèle avec les paramètres fournis.
        """
        self.weights = weights
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.initial_cash = initial_cash
        self.sentiment_cols = sentiment_cols
        self.weight_verified = weight_verified
        self.weight_non_verified = 1 - weight_verified
        
    def print_model_params(self):
        """
        Affiche les paramètres actuels du modèle.
        """
        print(f"Poids : {self.weights}")
        print(f'sentiment_cols : {self.sentiment_cols}')
        print(f"Seuil d'achat : {self.buy_threshold}")
        print(f"Seuil de vente : {self.sell_threshold}")
        
    
    def return_model_params(self):
        """
        Retourne les paramètres actuels du modèle sous forme de dictionnaire.
        """
        return {
            'weights': self.weights,
            'buy_threshold': self.buy_threshold,
            'sell_threshold': self.sell_threshold,
            'sentiment_cols': self.sentiment_cols,
        }

    def combine_sentiments(self, df):
        """
        Combine les sentiments en utilisant la moyenne pondérée.
        """
        df_combined = df[self.sentiment_cols].copy()
        df_combined['combined_sentiment'] = np.dot(df_combined, self.weights)
        return df_combined

    def generate_signal(self, df):
        """
        Génère les signaux d'achat/vente/attente selon les sentiments combinés.
        """
        df = df.copy()
        df['combined_sentiment'] = sum(w * df[col] for w, col in zip(self.weights, self.sentiment_cols))

        df['signal'] = 0
        df.loc[df['combined_sentiment'] > self.buy_threshold, 'signal'] = 1
        df.loc[df['combined_sentiment'] < self.sell_threshold, 'signal'] = -1
        return df
    
    def apply_sentiment_weights(self, df):
        """
        Applique la pondération verified / non_verified pour chaque modèle de sentiment.
        """
        df = df.copy()
        for col in self.sentiment_cols:
            verified_col = f"{col}_verified"
            non_verified_col = f"{col}_non_verified"
            
            df[col] = (
                (self.weight_verified * df[verified_col] +
                self.weight_non_verified * df[non_verified_col])*(np.exp(df["coefficient"])-1)/(np.exp(1)-1)
            )
        return df
    
    def train(self, df_train, n_iter=100):
        """
        Optimisation des hyperparamètres avec une recherche aléatoire.
        """
        best_return = -np.inf
        best_params = {}
        
        for _ in range(n_iter):
            
            df_weighted = self.apply_sentiment_weights(df_train)
            df_signals = self.generate_signal(df_weighted)

            position = 0
            cash = self.initial_cash

            for _, row in df_signals.iterrows():
                price = row['Close']
                if row['signal'] == 1 and position == 0:
                    position = (cash-1) / price
                    cash = 0
                elif row['signal'] == -1 and position > 0:
                    cash = position * price - 1
                    position = 0

            final_value = cash + position * df_signals.iloc[-1]['Close']
            ret = final_value - self.initial_cash

            if ret > best_return:
                best_return = ret
                best_params = {
                    'buy_threshold': self.buy_threshold,
                    'sell_threshold': self.sell_threshold,
                    'weights': self.weights,
                    'weight_verified': self.weight_verified
                }
            
            # Choix aléatoire des hyperparamètres
            buy = random.uniform(0, 1)
            sell = random.uniform(-1, 0)
            weights = random.choice([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
                (0.5 * np.array([1, 1, 0, 0])).tolist(),
                (0.5 * np.array([1, 0, 1, 0])).tolist(),
                (0.5 * np.array([0, 1, 1, 0])).tolist(),
                (0.5 * np.array([1, 0, 0, 1])).tolist(),
                (0.5 * np.array([0, 1, 0, 1])).tolist(),
                (1/3 * np.array([1, 1, 1, 0])).tolist(),
                (1/3 * np.array([1, 0, 1, 1])).tolist(),
                (1/3 * np.array([0, 1, 1, 1])).tolist(),
                (1/3 * np.array([1, 1, 0, 1])).tolist(),
                (0.5 * np.array([0, 0, 1, 1])).tolist()
            ])
            self.weight_verified = random.uniform(0, 1)
            self.weight_non_verified = 1 - self.weight_verified

            # Appliquer les poids verified

            self.buy_threshold = buy
            self.sell_threshold = sell
            self.weights = weights

        # Mise à jour des meilleurs paramètres
        self.buy_threshold = best_params['buy_threshold']
        self.sell_threshold = best_params['sell_threshold']
        self.weights = best_params['weights']
        self.weight_verified = best_params['weight_verified']
        self.weight_non_verified = 1 - self.weight_verified

    def test (self, df_test):
        """
        Teste le modèle sur un ensemble de données donné.
        """
        df_signals = df_test.copy()

        df_signals['signal'] = df_signals.apply(
            lambda row: self.generate_signal(
                np.dot(row[self.sentiment_cols], self.weights)
            ), axis=1
        )

        position = 0
        cash = self.initial_cash

        for _, row in df_signals.iterrows():
            price = row['Close']
            if row['signal'] == 1 and position == 0:
                position = (cash-1) / price
                cash = 0
            elif row['signal'] == -1 and position > 0:
                cash = position * price - 1
                position = 0

        final_value = cash + position * df_signals.iloc[-1]['Close']
        ret = final_value - self.initial_cash

        return ret
