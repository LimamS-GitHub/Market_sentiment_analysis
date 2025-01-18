import pandas as pd

# Charger le fichier CSV dans un DataFrame
file_path = 'data/data.csv'  # Remplace par le chemin réel
data = pd.read_csv(file_path)

# Suppression des colonnes inutiles
columns_to_drop = [
    'Unnamed: 0', 'LAST_PRICE', '1_DAY_RETURN', '2_DAY_RETURN', 
    '3_DAY_RETURN', '7_DAY_RETURN', 'PX_VOLUME', 'VOLATILITY_10D', 
    'VOLATILITY_30D', 'LSTM_POLARITY', 'TEXTBLOB_POLARITY'
]
data.drop(columns=columns_to_drop, inplace=True, errors='ignore')

# Convertir la colonne DATE en datetime et supprimer les dates invalides
data['DATE'] = pd.to_datetime(data['DATE'], format='%d/%m/%Y', errors='coerce')
invalid_dates_count = data['DATE'].isnull().sum()
data = data.dropna(subset=['DATE'])
print(f"Dates invalides supprimées : {invalid_dates_count}")

# Vérifier et corriger les valeurs uniques dans la colonne STOCK
data['STOCK'] = data['STOCK'].str.strip().str.upper()  # Uniformiser les valeurs
print("Valeurs uniques dans STOCK :")
print(data['STOCK'].unique())

# Identifier et supprimer les doublons
duplicates_count = data.duplicated(subset=['TWEET', 'STOCK', 'DATE']).sum()
data.drop_duplicates(subset=['TWEET', 'STOCK', 'DATE'], inplace=True)
print(f"Nombres de doublons supprimés : {duplicates_count}")

# Supprimer les lignes avec des valeurs manquantes dans les colonnes essentielles
essential_columns = ['TWEET', 'STOCK', 'DATE']
initial_row_count = data.shape[0]
data.dropna(subset=essential_columns, inplace=True)
cleaned_row_count = data.shape[0]
removed_rows_count = initial_row_count - cleaned_row_count
print(f"Lignes supprimées pour valeurs manquantes : {removed_rows_count}")

# Supprimer les passages à la ligne dans la colonne 'TWEET'
data['TWEET'] = data['TWEET'].replace(r'\n', ' ', regex=True)
data['TWEET'] = data['TWEET'].replace(r'\r', ' ', regex=True)

# Sauvegarde des données nettoyées
output_file = 'data/data_cleaned.csv'
data.to_csv(output_file, index=False)
print(f"Données nettoyées sauvegardées dans : {output_file}")

# Résumé final
print(f"Données nettoyées : {data.shape[0]} lignes restantes")
