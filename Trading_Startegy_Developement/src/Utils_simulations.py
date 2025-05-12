import pandas as pd
import yfinance as yf
from tqdm.notebook import tqdm

def charger_donnees_traitees(date_debut, date_fin, sentiment_cols,data_path,market_path):
    """
    Charge et prépare les données entre deux dates données, filtre les tweets neutres,
    et retourne les sentiments séparés (_verified, _non_verified), le nombre de tweets, et les données boursières.
    La pondération des sentiments est désormais effectuée par le modèle.
    """
    # 1. Chargement et prétraitement des données brutes
    df = pd.read_csv(data_path)
    df = df.drop_duplicates(subset="id")
    df['query_date'] = pd.to_datetime(df['query_date'])
    df['year'] = df['query_date'].dt.year
    df['month'] = df['query_date'].dt.month
    df = df.sort_values(by='query_date').reset_index(drop=True)

    # 2. Filtrage selon les dates spécifiées
    date_debut = pd.to_datetime(date_debut)
    date_fin = pd.to_datetime(date_fin)
    df = df[(df['query_date'] >= date_debut) & (df['query_date'] <= date_fin)]

    # 3. Filtrage des tweets neutres
    for col in sentiment_cols:
        df = df[df[col].abs() >= 0.1]

    # 4. Nombre de tweets par jour (après filtrage)
    df_nb_tweets = df.groupby('query_date').size().rename('Nb_tweets').to_frame()

    # 5. Séparation verified / non_verified
    df_verified = df[df['verified']]
    df_non_verified = df[~df['verified']]

    # 6. Agrégation journalière des sentiments
    daily_verified = df_verified.groupby(['query_date', 'year', 'month'])[sentiment_cols].mean()
    daily_non_verified = df_non_verified.groupby(['query_date', 'year', 'month'])[sentiment_cols].mean()

    # 7. Fusion des sentiments (conserve les colonnes _verified et _non_verified)
    df_combined = pd.merge(daily_verified, daily_non_verified, 
                           left_index=True, right_index=True, 
                           suffixes=('_verified', '_non_verified'))

    # 8. Construction du DataFrame final de sentiment
    df_combined.reset_index(inplace=True)
    df_combined.rename(columns={'query_date': 'date'}, inplace=True)
    df_combined['date'] = pd.to_datetime(df_combined['date'])

    # 9. Ajout du nombre de tweets
    df_combined = df_combined.merge(df_nb_tweets, left_on='date', right_index=True, how='left')
    df_combined['coefficient'] = df_combined['Nb_tweets'] / df_combined['Nb_tweets'].max()

    # 10. Téléchargement des données boursières
    df_market = pd.read_csv(market_path)
    # Forcer les noms de colonnes à être simples si MultiIndex
    if isinstance(df_market.columns, pd.MultiIndex):
        df_market.columns = df_market.columns.get_level_values(0)

    # Conversion explicite de la colonne date si elle existe
    if 'date' not in df_market.columns:
        df_market['date'] = pd.to_datetime(df_market['date'], errors='coerce')
    else:
        df_market['date'] = pd.to_datetime(df_market['date'], errors='coerce')

    # Nettoyage : retirer les lignes dont la date est manquante
    df_market = df_market[df_market['date'].notna()]

    # Calcul de la variation journalière en %
    df_market["Daily_Change_%"] = df_market["Close"].pct_change() * 100

    # Réorganisation des colonnes
    df_market = df_market[["date", "Open", "High", "Low", "Close", "Volume", "Daily_Change_%"]]

    # Normalisation de la date pour éviter les fuseaux horaires et heures
    df_market['date'] = df_market['date'].dt.floor('D')

    # Tri et réindexation
    df_market = df_market.sort_values("date").reset_index(drop=True)

    # 11. Fusion finale avec les données de marché
    df_final = pd.merge(df_combined, df_market, on="date", how="inner")

    return df_final

def simuler_marche_journalier(cash, model, date_debut,date_fin, sentiment_cols, Nb_iter = 100, nombre_mois_entrainement = 2,data_path = r'C:\Users\selim\Desktop\Data_total\Data_Tesla_2022_2025.csv',market_path = r'C:\Users\selim\Desktop\Data_total\TSLA_market.csv'):
    """
    Simule les décisions d'achat/vente jour après jour en recalibrant le modèle à chaque nouvelle journée.
    """
    # 1. Charger les données pour toutes les années demandées
    df = charger_donnees_traitees(date_debut,date_fin, sentiment_cols,data_path,market_path)

    premier_mois = df['date'].min()
    premiere_annee = df['date'].min().year

    jours_test = df[
        (df['date'].dt.year > premiere_annee) | 
        ((df['date'].dt.year == premiere_annee) & (df['date'].dt.month > premier_mois.month))
    ]['date'].unique()

    position = 0
    historique = {
        'date': [],
        'signal': [],
        'position': [],
        'valeur_portefeuille': [],
        'Close': [],
        'Signal': []
    }

    historique_model = {
        'weights': [],
        'buy_threshold': [],
        'sell_threshold': [],
        'weight_verified': [],
        'weight_non_verified': []
    }

    for jour in tqdm(jours_test, desc="⏳ Simulation en cours"):
        df_train = df[(df['date'] < jour) & (df['date'] >= (jour - pd.DateOffset(months=nombre_mois_entrainement)))]
        df_today = df[df['date'] == jour]

        if df_today.empty or df_train.empty:
            continue

        # Entraînement et génération du signal
        
        model.train(df_train,Nb_iter)
        df_today = model.apply_sentiment_weights(df_today)
        df_signal = model.generate_signal(df_today)
        
        historique_model['weights'].append(model.weights)
        historique_model['buy_threshold'].append(model.buy_threshold)
        historique_model['sell_threshold'].append(model.sell_threshold)
        historique_model['weight_verified'].append(model.weight_verified)
        historique_model['weight_non_verified'].append(model.weight_non_verified)

        if df_signal.empty:
            continue

        signal = df_signal['signal'].iloc[0]
        prix = df_signal['Close'].iloc[0]

        # Exécution du trade selon le signal
        if signal == 1 and position == 0:
            cash -= 1
            position = cash / prix
            cash = 0
            historique['signal'].append(1)
        elif signal == -1 and position > 0:
            cash = position * prix - 1
            position = 0
            historique['signal'].append(-1)
        else:
            historique['signal'].append(0)

        # Enregistrement dans l'historique
        historique['Signal'].append(signal)
        historique['date'].append(jour)
        historique['position'].append(position)
        historique['Close'].append(prix)
        historique['valeur_portefeuille'].append(cash + position * prix)

    return historique, historique_model

