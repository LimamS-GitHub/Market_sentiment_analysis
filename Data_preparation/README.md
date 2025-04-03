# 🐦 Tweet Scraper via Nitter

Ce script permet de **scraper quotidiennement des tweets publics** depuis [Nitter](https://nitter.net), une alternative sans JavaScript à Twitter, en utilisant Selenium. Il s’appuie sur des **proxies HTTPS** pour éviter les blocages IP.

## Objectif

Récupérer des tweets liés à un mot-clé donné (par défaut : `tesla`) sur une plage de dates donnée, en contournant les limites d'accès grâce à des proxies publics.

Les données collectées peuvent ensuite être utilisées pour des analyses de sentiment, d'opinion ou de tendance dans le temps.

---

## Dépendances

Voici les principales bibliothèques utilisées :

```bash
pip install selenium webdriver-manager pandas langdetect beautifulsoup4 requests
```

Python 3.8+ recommandé.

---

## Exécution

### Lancer le scraping

```bash
python main.py
```

Cela lance un scraping de tweets pour chaque jour entre le 2 janvier 2023 et le 2 janvier 2025 (modifiable dans `main.py`).

---

## Paramètres configurables

Modifiables directement dans `main.py` :

- `start_date` / `end_date` : plage de dates à scraper
- `keyword` : mot-clé recherché (par défaut `"tesla"`)
- `max_tweets_per_day` : nombre de tweets max par jour (par défaut `30`)

---

## Format de sortie

Chaque jour donne lieu à un fichier `.csv` :

```bash
tesla_tweets_2023-01-02.csv
```

Format des colonnes :

| id         | query_date | text               | verified |
|------------|------------|--------------------|----------|
| tweet_id   | date-1     | contenu du tweet   | True/False |

---

## Conseils & Limites

- **Erreurs 429 / Captchas** : Nitter peut bloquer les requêtes si trop nombreuses. C'est pour cela que le script utilise :
  - des pauses aléatoires entre les jours (`time.sleep`)
  - des **proxies HTTPS** automatiquement récupérés depuis `sslproxies.org`
- **Retry automatique** : jusqu’à 10 tentatives par jour si le scraping échoue.
- **Langue filtrée** : seuls les tweets détectés en anglais (`langdetect`) sont conservés.

---

## 🧪 Exemple de proxy utilisé

Les proxies sont automatiquement testés via :

```python
test_https_proxy(proxy)
```

Et initialisés dans Chrome headless via :

```python
initialize_driver(proxy)
```

---

## 📁 Structure des fichiers

- `main.py` : script principal de scraping
- `scrape.py` : logique de collecte via Selenium
- `driver.py` : configuration du navigateur
- `utils.py` : outils proxy, nettoyage texte, etc.

---

## 📬 Contact

Pour toute amélioration ou question, n'hésitez pas à ouvrir une *issue* ou à me contacter directement.
