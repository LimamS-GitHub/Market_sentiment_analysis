# 🐦 Collecte & Préparation des Tweets
---

## 🗂️ Sommaire

- [Pourquoi Twitter ?](#pourquoi-twitter-)
- [Objectif de cette section](#objectif-de-cette-section)
- [Aperçu technique](#aperçu-technique)
- [Schéma des données exportées](#schéma-des-données-exportées)
- [🧠 Détail conceptuel des étapes](#-détail-conceptuel-des-étapes)
- [⚠️ Limites rencontrées](#️-limites-rencontrées)
- [🔗 Pour aller plus loin](#-pour-aller-plus-loin)

## Pourquoi Twitter ?

Twitter est une plateforme où l'information circule vite, brute et en grande quantité.  
C’est un véritable flux continu d’opinions, de réactions et de spéculations, souvent en lien direct avec l’actualité économique ou les entreprises cotées en bourse.

Dans notre cas, nous nous intéressons à **Tesla ($TSLA)**.  
Notre hypothèse : les messages postés quotidiennement au sujet de Tesla pourraient refléter, voire anticiper, les mouvements de son cours boursier.

---

## Objectif de cette section

Avant d’analyser ou de modéliser quoi que ce soit, il faut construire une **base de données propre, fiable et exploitable**.  
Dans ce chapitre, nous allons donc :

- **Scraper automatiquement** des tweets à l’aide de [Nitter](https://nitter.net), une alternative à Twitter sans JavaScript ni authentification API.
- **Nettoyer les textes** : suppression des liens, mentions, ponctuations, etc.
- **Filtrer les langues** pour ne garder que les tweets en anglais.
- **Analyser le sentiment** de chaque tweet avec plusieurs modèles NLP.
- **Sauvegarder** les données propres pour les futures étapes.

---

## Aperçu technique

Le scraping est réalisé en Python avec **Selenium**, et utilise une **rotation automatique de proxies HTTPS** afin de contourner les restrictions d’accès aux contenus Twitter.

Chaque tweet est ensuite enrichi par **5 scores de sentiment** :  
- 1 issu de **VADER** (modèle lexical basé sur des règles),
- 3 provenant de **modèles Transformers spécialisés dans le domaine financier**.

Les résultats sont sauvegardés dans des fichiers CSV organisés **par mois**, ainsi qu’un **fichier global** regroupant toutes les données.

---

## Schéma des données exportées

| Colonne                | Exemple                         | Description                                 |
|------------------------|----------------------------------|---------------------------------------------|
| `id`                   | `1658327123456789`              | Identifiant unique du tweet                 |
| `query_date`           | `2025-04-15`                    | Date de récupération du tweet               |
| `text`                 | Texte brut                      | Contenu original du tweet                   |
| `verified`             | `True`                          | Statut vérifié (compte certifié ou non)     |
| `cleaned_tweet`        | Texte nettoyé                   | Sans liens, mentions, ponctuation, etc.     |
| `sentiment_vader`      | `0.63`                          | Score de sentiment (composé VADER)          |
| `sentiment_{hf_model}` | `1` (`-1`, `0`, `1`)            | Une colonne **par modèle HF** :<br> • `financialbert`<br> • `distilroberta_fin`<br> • `deberta_v3_fin` |

---

## Schéma de récupération des données

Le diagramme ci-dessous illustre le processus complet de collecte et de traitement des tweets, depuis le lancement du script jusqu’à la sauvegarde des fichiers CSV :

![Distribution sentiment](schema_scraping.svg)

---

##  Détail conceptuel des étapes

###  1. Scraping sans API

Nous avons choisi **Nitter**, une interface alternative à Twitter, pour contourner les restrictions de l’API officielle (limites, coût, authentification).  
Le scraping consiste à :

- Formuler une requête par mot-clé (`Tesla`, `TSLA`, etc.) et par jour ;
- Naviguer automatiquement dans les pages pour extraire le contenu des tweets visibles ;
- Stocker les résultats dans un format brut, avec des métadonnées (date, utilisateur, texte, etc.).

Pour automatiser cela, nous utilisons un outil de navigation sans interface visuelle (**navigateur headless**) avec gestion de délais et rotation de connexions (**proxies**) pour éviter d’être bloqués.

---

###  2. Nettoyage et filtrage linguistique

Les tweets récupérés sont très bruts : liens, mentions, hashtags, emojis, etc.  
Avant toute analyse, chaque texte est **nettoyé** pour retirer ces éléments parasites.

Ensuite, un filtre de langue est appliqué pour ne garder que les tweets **en anglais**, car les modèles NLP utilisés sont spécifiquement entraînés sur ce langage.

---

###  3. Analyse de sentiment multi-modèle

Chaque tweet nettoyé est passé à travers plusieurs modèles de **sentiment analysis** :

| Type de modèle           | Exemple utilisé         | Caractéristiques                                               |
|--------------------------|--------------------------|----------------------------------------------------------------|
| **Lexical**              | VADER                    | Basé sur des règles, rapide, mais limité face au langage complexe |
| **Transformers généralistes** | DistilRoBERTa         | Plus fins, mais parfois surentraînés sur du texte non-financier |
| **Transformers spécialisés** | FinancialBERT, DeBERTa-v3-fin | Entraînés sur des actualités boursières, mieux adaptés à notre contexte |

Chaque modèle attribue un **score de polarité** : positif, neutre ou négatif (souvent transformé en valeurs −1, 0 ou +1).

---

###  4. Stockage mensuel et structuration

Les résultats sont organisés :

- Par **mois civil** (ex. : `tweets_2022_01.csv`) pour faciliter l’analyse temporelle ;
- Avec un **fichier global fusionné** (`tweets_with_sentiment.csv`) utilisé dans les notebooks suivants.

Chaque ligne de ce fichier correspond à un tweet unique enrichi de métadonnées et de scores.

---

##  Limites rencontrées

- **Qualité des tweets** : bruit, ironie, contenu peu informatif, spam…
- **Langue détectée automatiquement** → erreurs possibles.
- **Modèles de sentiment divergents** : certaines phrases ambigües sont classées différemment selon le modèle.
- **Instabilité de Nitter** : indisponibilités ponctuelles → recours à des solutions de contournement techniques.

---

##  Pour aller plus loin

👉 Dans la prochaine section, nous croiserons ces tweets enrichis avec les **cours boursiers de Tesla** pour étudier les corrélations et construire des indicateurs de sentiment agrégé.

➡️ Accéder à la suite : [Analyse exploratoire des données](EDA.html)
