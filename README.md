# Market Sentiment Analysis – *Tesla Case Study*

This project shows how **Twitter sentiment** can be turned into **adaptive trading signals** for $TSLA.  
Instead of static correlation checks, we **re-train and re-optimize** the model as new data arrives, mimicking what would happen in real-time trading.

---

## Project Overview

### **Objective**
- **Build** a fully-adaptive pipeline that converts tweet sentiment into daily buy/sell signals.  
- **Optimize** model hyper-parameters on a rolling window to maximise risk-adjusted return.  
- **Evaluate** whether public mood provides actionable alpha beyond buy-and-hold.

### **Data Sources**
| Source | Details |
|--------|---------|
| **Twitter** | Scraped with headless Selenium via the *Nitter* front-end (no Twitter API needed). |
| **Market**  | Downloaded from https://fr.investing.com/equities/tesla-motors-historical-data |

---

## Workflow 🛠️

```mermaid
flowchart LR
    subgraph Prep["1 · Data Preparation"]
        A[Scrape Nitter<br/>+ proxy rotation] --> B[Clean text<br/>+ deduplicate]
        B --> C[Sentiment scoring<br/>VADER & HF models]
        C --> D[Daily aggregation<br/>verified vs non-verified]
    end
    subgraph EDA["2 · Feature Engineering & EDA"]
        D --> E[Visualise & filter]
        E --> F[Normalise & smooth<br/>rolling windows]
    end
    subgraph Trade["3 · Adaptive Strategy"]
        F --> G[Random search<br/>best weights & thresholds]
        G --> H[Rolling simulation<br/>adaptive portfolio]
        H --> I[Performance report<br/>(Total Return, Ann. Volatility,<br/>Max Drawdown, Ann. Outperformance,<br/>Avg Gap vs stock / initial capital)]
    end
```

### 1. Data Preparation
* Scrape tweets (headless Selenium + rotating proxies).  
* Clean text, keep English only, score with **VADER** + 3 HF models (FinancialBERT, DistilRoBERTa-FinNews, DeBERTa v3-FinNews).  
* Aggregate daily sentiment for verified vs non-verified users.

### 2. Feature Engineering & EDA
* Filter low-signal tweets, visualise distributions.  
* Normalise series and apply 1–7 day rolling averages.

### 3. Adaptive Strategy
* Daily **random search** on the last *N* months to find optimal weights & thresholds.  
* Roll-forward simulation: trade next-day open based on sentiment signal.  
* Log KPIs (total return, annual volatility, max drawdown, etc.) to `/results/`.


---

## References

* **Nitter** – <https://github.com/zedeus/nitter>  
* **Selenium** – browser automation for scraping  
* **VADER** – Hutto & Gilbert (2014) “VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text”  
* **FinancialBERT-SA** – <https://huggingface.co/ahmedrachid/FinancialBERT-Sentiment-Analysis>  
* **DistilRoBERTa-FinNews** – <https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis>  
* **DeBERTa v3-FinNews** – <https://huggingface.co/mrm8488/deberta-v3-ft-financial-news-sentiment-analysis>  

> **Disclaimer:** Educational use only. Nothing here is financial advice.
