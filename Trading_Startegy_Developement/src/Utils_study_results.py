import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import os
from src.model import *
from src.Utils_simulations import *

def analyser_performance_portefeuille(historique, cash_initial=1000):
    # Convertir en DataFrame et trier par date
    df = pd.DataFrame(historique).copy()
    df = df.sort_values(by='date')

    # Colonnes numériques
    df['valeur_portefeuille'] = df['valeur_portefeuille'].astype(float)
    df['Close'] = df['Close'].astype(float)

    # Rendements journaliers
    df['rendement_journalier'] = df['valeur_portefeuille'].pct_change()
    df['rendement_action'] = df['Close'].pct_change()

    # Rendements totaux
    rendement_portefeuille_total = (df['valeur_portefeuille'].iloc[-1] / cash_initial) - 1
    rendement_action_total = (df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1

    # Rendements annualisés
    nb_jours = len(df)
    rendement_annuel_portefeuille = (1 + rendement_portefeuille_total)**(252 / nb_jours) - 1
    rendement_annuel_action = (1 + rendement_action_total)**(252 / nb_jours) - 1

    # Volatilité annualisée
    volatilite_annuelle = df['rendement_journalier'].std() * np.sqrt(252)

    # Max Drawdown
    cumulative = df['valeur_portefeuille'].cummax()
    drawdown = (df['valeur_portefeuille'] - cumulative) / cumulative
    max_drawdown = drawdown.min()

    # Surperformance totale (annualisée)
    surperformance_annuelle = (rendement_annuel_portefeuille - rendement_annuel_action) * 100

    # Surperformance moyenne journalière
    df['surperformance_journaliere'] = df['valeur_portefeuille'] - df['Close']/df['Close'].iloc[0]*cash_initial
    surperformance_journaliere_moyenne = df['surperformance_journaliere'].mean()/cash_initial * 100

    # Résumé
    stats = {
        "Rendement total (%)": rendement_portefeuille_total * 100,
        "Rendement annualisé (%)": rendement_annuel_portefeuille * 100,
        "Volatilité annualisée (%)": volatilite_annuelle * 100,
        "Max Drawdown (%)": max_drawdown * 100,
        "Écart annuel de performance (%)": surperformance_annuelle,
        "Écart moyen (vs action) / capital initial (%)": surperformance_journaliere_moyenne
    }

    return stats, df


def plot_hyperparams_over_time(model_historique, dates):
    """
    Affiche l'évolution des hyperparamètres du modèle au fil du temps.
    """
    df = pd.DataFrame(model_historique)
    df['date'] = pd.to_datetime(dates)

    # Séparer les weights
    poids = pd.DataFrame(df['weights'].tolist(), columns=[
        'weight_model_1', 'weight_model_2', 'weight_model_3', 'weight_model_4'
    ])
    df = pd.concat([df, poids], axis=1)

    params_to_plot = ['buy_threshold', 'sell_threshold', 'weight_verified', 'weight_non_verified', 'weight_model_1', 'weight_model_2', 'weight_model_3', 'weight_model_4']

    fig, axs = plt.subplots(len(params_to_plot), 1, figsize=(12, 10), sharex=True)

    for i, param in enumerate(params_to_plot):
        axs[i].plot(df['date'], df[param], marker='o', label=param)
        axs[i].set_ylabel(param)
        axs[i].legend()
        axs[i].grid()

    # Subplot pour les weights
    plt.suptitle("Évolution des hyperparamètres du modèle")
    plt.tight_layout()
    plt.show()


def plot_historique(df):
    fig, axs = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    if 'date' in df.columns:
        df['Date'] = df['date']
        df['Date'] = pd.to_datetime(df['Date'])
        df.drop(columns=['date'], inplace=True)
    # ==== 1. PRIX DE FERMETURE + SIGNES ====
    axs[0].plot(df['Date'], df['Close'], label="Prix de fermeture", color='orange', linewidth=1.5)

    # Signaux d'achat
    if 'signal' in df.columns:
        df_achat = df[df['signal'] == 1]
        axs[0].scatter(df_achat['Date'], df_achat['Close'], color='green', marker='^', label='Achat', s=60)

    # Signaux de vente
    if 'signal' in df.columns:
        df_vente = df[df['signal'] == -1]
        axs[0].scatter(df_vente['Date'], df_vente['Close'], color='red', marker='v', label='Vente', s=60)

    axs[0].set_title("Prix de fermeture avec signaux d'achat/vente")
    axs[0].set_ylabel("Prix (€)")
    axs[0].legend()
    axs[0].grid(alpha=0.3)

    # ==== 2. VALEUR DU PORTEFEUILLE ====
    axs[1].plot(df['Date'], df['Close']/df['Close'][0]*df['valeur_portefeuille'][0], label="Stratégie buy & hold", color='orange', linewidth=1)
    axs[1].plot(df['Date'], df['valeur_portefeuille'], label="Valeur du portefeuille", color='blue', linewidth=1.5)
    axs[1].axhline(y=df['valeur_portefeuille'][0], color='gray', linestyle='--', linewidth=1, label="Cash départ")

    axs[1].set_title("Évolution de la valeur du portefeuille")
    axs[1].set_ylabel("Valeur (€)")
    axs[1].legend()
    axs[1].grid(alpha=0.3)

    # ==== FORMAT DES DATES ====
    axs[1].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(axs[1].xaxis.get_majorticklabels(), rotation=45, ha="right")

    plt.tight_layout()
    plt.show()

def simulation_download_results(date_debut, date_fin, nb_iterations_list, nb_mois_entrainements_list, sentiment_cols,data_path=r'C:\Users\selim\Desktop\Data_total\Data_Tesla_2022_2025.csv',market_path = r'C:\Users\selim\Desktop\Data_total\TSLA_market.csv'):
    
    # Créer les dossiers si besoin
    os.makedirs("df_historique_saves", exist_ok=True)
    os.makedirs("df_global", exist_ok=True)
    os.makedirs("df_historique_param", exist_ok=True)

    df_evolution = pd.DataFrame(columns=[
        'nb_iterations',
        'nb_mois_entrainement',
        'Rendement total (%)',
        'Rendement annualisé (%)',
        'Volatilité annualisée (%)',
        'Max Drawdown (%)',
        'Écart annuel de performance (%)',
        'Écart moyen (vs action) / capital initial (%)',
        'resultats_path',
        'param_path'
    ])

    for nb_iterations in nb_iterations_list:
        for nb_mois_entrainements in nb_mois_entrainements_list:
            # Initialiser le modèle
            weight_1 = random.uniform(0, 1)
            weight_2 = random.uniform(0, 1 - weight_1)
            weight_3 = random.uniform(0, 1 - weight_1 - weight_2)
            weight_4 = 1 - weight_1 - weight_2 - weight_3
            weights = [weight_1, weight_2, weight_3, weight_4]
            model = SentimentTradingModel(
                weights=weights,
                buy_threshold=random.uniform(0, 1),
                sell_threshold=random.uniform(-1, 0),
                weight_verified=random.uniform(0, 1),
                sentiment_cols=sentiment_cols
            )
            
            # Simulation
            resultats_historique, model_historique = simuler_marche_journalier(
                1000,
                model,
                date_debut,
                date_fin,
                sentiment_cols,
                nb_iterations,
                nb_mois_entrainements,
                data_path,
                market_path
            )
            
            # Évaluation
            stats, _ = analyser_performance_portefeuille(resultats_historique, cash_initial=1000)

            # Noms de fichiers
            filename = f"df_{nb_iterations}_iter_{nb_mois_entrainements}_mois.csv"
            filename2 = f"df_params_{nb_iterations}_iter_{nb_mois_entrainements}_mois.csv"
            resultats_path = os.path.join("df_historique_saves", filename)
            param_path = os.path.join("df_historique_param", filename2)


            # Sauvegardes
            pd.DataFrame(resultats_historique).to_csv(resultats_path, index=False)
            pd.DataFrame(model_historique).to_csv(param_path, index=False)

            # Ajout à df_evolution
            df_evolution.loc[len(df_evolution)] = {
                'nb_iterations': nb_iterations,
                'nb_mois_entrainement': nb_mois_entrainements,
                'Rendement total (%)': stats['Rendement total (%)'],
                'Rendement annualisé (%)': stats['Rendement annualisé (%)'],
                'Volatilité annualisée (%)': stats['Volatilité annualisée (%)'],
                'Max Drawdown (%)': stats['Max Drawdown (%)'],
                'Écart annuel de performance (%)': stats['Écart annuel de performance (%)'],
                'Écart moyen (vs action) / capital initial (%)': stats['Écart moyen (vs action) / capital initial (%)'],
                'resultats_path': resultats_path,
                'param_path': param_path
            }
            print(f"Rendement total : {stats['Rendement total (%)']} --- Écart moyen (vs strategie buy & hold ) / capital initial (%)': {stats['Écart moyen (vs action) / capital initial (%)']}% avec {nb_iterations} iterations et {nb_mois_entrainements} mois")
            
    # Sauvegarde globale
    df_evolution.to_csv("df_global/resultats_global.csv", index=False)
    
