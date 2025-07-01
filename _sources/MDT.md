# Méthode de travail

Ce projet a été mené selon une approche structurée, progressive et orientée expérimentation. Chaque étape a été pensée pour construire un pipeline robuste, itératif et réutilisable. Voici la démarche suivie :

## 1. Définir un objectif clair

L’objectif initial était de tester une hypothèse simple mais ambitieuse :  
**peut-on exploiter le sentiment exprimé sur Twitter pour anticiper le mouvement d’un actif financier, et générer des signaux de trading ?**

Cet objectif, bien qu’audacieux, a guidé toutes les décisions méthodologiques prises par la suite.

## 2. Se documenter et analyser l’existant

Avant toute implémentation, une phase de **recherche exploratoire** a été menée pour :
- Comprendre les travaux académiques et industriels sur le **sentiment analysis appliqué aux marchés financiers**.
- Comparer les approches existantes : lexicon-based (VADER), transformer-based (FinBERT, DeBERTa…), ou hybrides.
- Identifier les limites (bruit, ironie, bulles spéculatives, sur-apprentissage) et les bonnes pratiques (agrégation temporelle, filtrage de bruit, tests robustes).

## 3. Découper le projet en sous-problèmes

Le projet a été scindé en modules indépendants mais complémentaires :

1. **Collecte des données Twitter** via Nitter + Selenium
2. **Nettoyage et scoring des textes** avec VADER et 3 modèles spécialisés
3. **Agrégation journalière des scores**
4. **Téléchargement des prix marchés (Investing.com)**
5. **Mise en relation Sentiment ↔ Variation de l’actif**
6. **Génération de signaux d’achat/vente**
7. **Backtesting et évaluation de la performance**

## 4. Commencer par des prototypes simples dans des notebooks

Chaque bloc a été initialement développé dans un **Jupyter Notebook** pour :

- Pouvoir tester rapidement des idées.
- Visualiser les outputs à chaque étape.
- Corriger plus facilement les erreurs.
- Itérer vite sur les paramètres (fenêtre temporelle, poids, seuils...).

Par exemple :
- Le scraping de Nitter a d’abord été testé sur un seul actif et une seule journée.
- Le scoring a été validé manuellement sur un petit set de tweets.

## 5. Passer en mode production dès qu’un bloc devient stable

Une fois une partie du pipeline validée (fonctionnelle, utile, robuste), elle a été **restructurée dans un fichier Python autonome** (`.py`), avec :

- Gestion des erreurs,
- Logs clairs,
- Modularisation (fonctions réutilisables),
- Intégration dans un pipeline quotidien (scraping + scoring + agrégation).

Exemple :  
Le module de collecte des tweets fonctionne de manière automatisée avec rotation de proxies, gestion des captchas et filtrage de langue.

## 6. Tester la relation sentiment ↔ marché

Une fois les séries temporelles en main, plusieurs tests statistiques ont été menés :

- **Corrélation linéaire** (Pearson, Spearman) entre le score de sentiment journalier et la variation de prix du lendemain.
- **Cross-correlation** avec différents décalages temporels.
- **Tests de causalité de Granger** pour évaluer la prédictivité.

Résultat :  
Aucune **corrélation directe robuste** n’a été observée de manière stable sur la période étudiée.

## 7. Passer à une stratégie concrète de signaux

Face à l'absence de lien direct, une approche plus pragmatique a été adoptée :
- Générer un **signal Buy/Sell** lorsque le score agrégé dépasse certains seuils (optimisés par random search).
- Simuler une stratégie de trading où l’on achète ou vend l’actif à l’ouverture du lendemain.
- Réévaluer les seuils et poids chaque jour via **une fenêtre glissante d'entraînement** (stratégie adaptative).

## 8. Itérations et extensions

Le pipeline a ensuite été étendu :
- Ajout de lissage, normalisation, distinction utilisateurs vérifiés / non vérifiés.
- Log systématique des performances (rendement, volatilité, Sharpe ratio, drawdown).
- Réflexion sur la généralisation à un **portefeuille multi-actifs**.

---

Cette méthode de travail a permis d’avancer de manière incrémentale, en assurant la robustesse de chaque étape avant de passer à la suivante. Elle laisse aussi place à l’expérimentation et à l'amélioration continue.
