# 🐦 Tweet Scraper via Nitter + Sentiment Analysis

Ce projet permet de **scraper des tweets publics** depuis [Nitter](https://nitter.net), une alternative sans JavaScript à Twitter, et d'appliquer plusieurs **modèles d'analyse de sentiment**. Il est conçu pour contourner les limitations d'accès via un système de **rotation de proxies HTTPS**.

## Objectif

- Récupérer quotidiennement des tweets liés à une entreprise donnée (ex : `Tesla`).
- Appliquer 4 modèles de sentiment (VADER + 3 Transformers financiers).
- Sauvegarder les résultats par mois et dans un fichier global, pour analyse de tendance ou backtest boursier.

---

## Dépendances

```bash
pip install selenium webdriver-manager pandas langdetect beautifulsoup4 requests vaderSentiment transformers
```

Python 3.8+ recommandé.

---

## Lancer le scraping

```bash
python main.py
```

Cela lance le scraping pour la plage de dates définie dans `main.py`, par défaut entre le 15 et 19 avril 2025.

---

## Paramètres configurables (`main.py`)

- `start_date` / `end_date` : plage de dates à scraper
- `company_name` : mot-clé recherché dans les tweets (par défaut : "Tesla")
- `minimum_number_tweets_per_day` : nombre minimum de tweets à collecter par jour

---

## Fonctionnement (étapes principales)

1. **Initialisation des dates, modèles de sentiment et proxies**
2. **Pour chaque jour :**
   - Ouverture d'un navigateur avec proxy
   - Scraping sur Nitter
   - Nettoyage et filtrage des tweets en anglais
   - Analyse de sentiment avec VADER et 3 modèles Transformers
   - Enregistrement dans un buffer mensuel et global
3. **À chaque changement de mois :**
   - Écriture dans un fichier `Data_for_YYYY-MM.csv`
4. **À la fin du script :**
   - Fusion et sauvegarde finale dans `Data_<company>.csv`

---

## Schéma du processus de scraping

```mermaid
graph TD
    Start[Start script] --> LoadParams[Load parameters]
    LoadParams --> LoopDates[Loop through dates]
    LoopDates --> GetProxy[Select random valid proxy]
    GetProxy --> LaunchDriver[Init WebDriver with proxy]
    LaunchDriver --> AccessNitter[Access Nitter & search tweets]
    AccessNitter --> Extract[Extract & filter English tweets]
    Extract --> Clean[Clean tweet text]
    Clean --> Analyze[Sentiment analysis: VADER + models]
    Analyze --> MonthCheck{Month changed?}
    MonthCheck -- Yes --> SaveMonth[Save monthly CSV]
    MonthCheck -- No --> ContinueDate[Next date]
    SaveMonth --> ContinueDate
    ContinueDate --> FinalCheck{Last date?}
    FinalCheck -- No --> Retry{Retry needed?}
    Retry -- Yes --> GetProxy
    Retry -- No --> LoopDates
    FinalCheck -- Yes --> SaveAll[Save final CSV]
    SaveAll --> End[Done]
```

---

## Structure des fichiers

- `main.py` : script principal de scraping et orchestration
- `scrape.py` : logique de navigation sur Nitter, extraction des tweets
- `driver.py` : initialisation du navigateur Chrome avec proxy
- `utils.py` : génération de dates, gestion des proxies, nettoyage texte
- `sentiment.py` : analyse de sentiment avec VADER + Transformers

---

## Format de sortie

Les tweets sont sauvegardés dans :

- des fichiers mensuels : `Data_for_2025-04.csv`
- un fichier global : `Data_Tesla.csv`

Colonnes principales :

| id        | query\_date | text             | verified   | CLEANED\_TWEET | SENTIMENT\_VADER | SENTIMENT\_ModelName |
| --------- | ----------- | ---------------- | ---------- | -------------- | ---------------- | -------------------- |
| tweet\_id | yyyy-mm-dd  | contenu du tweet | True/False | tweet nettoyé  | score [-1 à 1]   | score du modèle NLP  |

---

## Gestion des erreurs & contournement

- **Proxies HTTPS dynamiques** : Récupérés depuis `sslproxies.org` puis filtrés grâce à `valid_proxies()` pour ne garder que ceux qui fonctionnent.
- **Test unitaire de validité** : Chaque proxy est testé individuellement via une requête HTTPS vers Nitter (`test_https_proxy`).
- **Rotation intelligente** : Pour chaque tentative, un proxy est sélectionné au hasard parmi la liste des valides. Une fois utilisé, il est retiré temporairement pour éviter les blocages.
- \*\*Retries\*\*: Jusqu'à **10 tentatives par jour**, avec changement de proxy après chaque tentative échouée.
- **Filtrage linguistique** : Seuls les tweets détectés comme étant en anglais sont conservés (`langdetect`).Seuls les tweets détectés comme étant en anglais sont conservés (`langdetect`).

---

## 📬 Contact

Pour toute amélioration ou suggestion, n'hésite pas à ouvrir une *issue* ou à me contacter directement.

