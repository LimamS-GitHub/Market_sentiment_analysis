# Market Sentiment-Driven Strategy

This project explores how public sentiment on Twitter—specifically regarding Tesla—can be transformed into **adaptive trading signals** using Natural Language Processing (NLP) models.

---

## Project Objective

- Build a **dynamic sentiment-based trading model** that adapts to market behavior over time.
- Replace traditional correlation studies with **parameter optimization and calibration loops**.
- Leverage verified vs. non-verified user sentiment with adjustable weightings.

---

## Data Sources

- **Twitter Data**: Scraped from [Nitter](https://nitter.net) using Selenium and proxies to bypass limitations.
- **Market Data**: Fetched from [Yahoo Finance](https://finance.yahoo.com) for Tesla (TSLA) stock.

---

## Workflow

### 1. Sentiment Data Collection & Preprocessing
- Tweets are scraped daily from Nitter for a given period.
- Cleaned (URLs, mentions, numbers, punctuation removed).
- Filtered for English language and verified users.

### 2. Sentiment Analysis
- Four models used for comparative robustness:
  - VADER
  - FinancialBERT
  - DistilRoBERTa (finetuned)
  - DeBERTa (finetuned)
- Sentiment scores standardized between -1 (negative) and +1 (positive).
- Neutral tweets (score ≈ 0) excluded from signal construction.

### 3. Daily Aggregation & Weighting
- Sentiment scores are averaged per day.
- Separate aggregation for **verified vs. non-verified** accounts.
- User-defined weight (`α`) adjusts the impact of each group.

### 4. Trading Strategy Simulation
- A buy/sell simulation is executed using:
  - Smoothed sentiment scores (rolling average).
  - Buy/sell thresholds (tunable).
  - Cash tracking and position management.
- Strategy performance is measured by portfolio return.

### 5. Adaptive Optimization
- A parameter sweep is performed to identify the **optimal configuration**:
  - Model choice
  - Rolling window size
  - Buy threshold
  - Sell threshold
- This replaces fixed-rule strategies with a data-driven adaptive method.

---

## Example Result

Using 2022 sentiment data, the best configuration achieved:

- **Model**: FinancialBERT  
- **Buy Threshold**: 0.3  
- **Sell Threshold**: -0.5  
- **Rolling Window**: 1  
- **Return**: +75.86%

---

## Next Steps

- Incorporate live updates and adaptive retraining.
- Introduce reinforcement learning or Bayesian optimization.
- Expand to multiple assets or broader market indicators.

---

## References

> Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. *ICWSM-14*.  
> Ahmed Rachid, HuggingFace: FinancialBERT Sentiment Models.

---
