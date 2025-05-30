# 🐦 Tweet Scraper & Sentiment Pipeline (Nitter Edition)

Scrape **public tweets** through [Nitter](https://github.com/zedeus/nitter) (no Twitter API required) and attach **multi-model sentiment scores** in one go.  
Designed for daily, proxy-rotated harvesting of any ticker or keyword (e.g. `Tesla`).

---

## Key Features
* **Headless Selenium** + automatic **HTTPS-proxy rotation** to dodge rate limits.  
* **Four sentiment models out-of-the-box**  
  * VADER (*compound* score –1…1)  
  * `ahmedrachid/FinancialBERT-Sentiment-Analysis`  
  * `mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis`
  * `mrm8488/deberta-v3-ft-financial-news-sentiment-analysis`  
* **Language filter** – keeps English tweets only.  
* **Rolling month buffer** – writes one CSV per month plus a final global file in the event of a crash.

---

## Quick Start

```bash
# activate your project venv first
python main.py \
  --company "Tesla" \
  --start "2025-04-15" \
  --end   "2025-04-19" \
  --min_daily 50
```

The command above scrapes 15-19 Apr 2025 and produces:

```
data/Tesla/raw/   Data_for_2025-04.csv
data/Tesla/global Data_Tesla.csv
```

### CLI Flags (`python main.py --help`)
| Flag               | Default      | Description                          |
|--------------------|--------------|--------------------------------------|
| `--company`        | Tesla        | Keyword searched on Nitter           |
| `--start / --end`  | last 5 days  | Date range (YYYY-MM-DD)              |
| `--min_daily`      | 50          | Minimum tweets per day; if fewer than 50 exist, the scraper collects whatever is available      |
| `--proxy_retries`  | 20           | Max proxy swaps              |

---

## Installation

```bash
pip install -r requirements.txt
# or, standalone:
pip install selenium webdriver-manager pandas langdetect beautifulsoup4 requests vaderSentiment transformers
```
*Python 3.9+ recommended.*

---

## Output Schema

| Column               | Example                         | Notes                              |
|----------------------|---------------------------------|------------------------------------|
| `id`                 | `1658327123456789`              | Tweet ID                           |
| `query_date`         | `2025-04-15`                    | Day the tweet was scraped          |
| `text`               | raw tweet text                  |                                    |
| `verified`           | `True`                          | Blue-check status                  |
| `cleaned_tweet`      | text without URLs, mentions…    |                                    |
| `sentiment_vader`    | `0.63`                          | VADER compound                     |
| `sentiment_{hf_model}`  | `1` (`-1,0,1`)                  | One column **per** HF model:<br>  • `financialbert`<br>  • `distilroberta_fin` <br>  • `deberta_v3_fin`|

* HF : Hugging Face

---

## File Layout

```
Data_preparation/
├── main.py               # CLI orchestrator
├── scrape.py             # Nitter navigation & extraction
├── driver.py             # Chrome initialisation with proxy
├── sentiment.py          # VADER + HF pipelines
└── utils.py              # dates, proxy pool, text cleaning
```

---

## Error Handling

* **Proxy pool** downloaded from *sslproxies.org* and validated in parallel.  
* Automatic proxy swap on HTTP errors / empty pages (up to `proxy_retries`).  
* Daily scrape retried three times before the date is skipped.
