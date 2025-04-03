# Market Sentiment Analysis

This project investigates how Twitter sentiment related to Tesla can be transformed into **adaptive trading signals**. Rather than relying on correlation analysis, we explore how tuning and optimizing model parameters can reveal predictive insights from online discourse.

---

## Project Overview

### **Objective**
- **Develop** an adaptive model that transforms Twitter sentiment into trading signals.
- **Optimize** model parameters to maximize return using historical data.
- **Assess** whether public sentiment can be used to construct actionable strategies.

### **Data Sources**
- **Twitter Data:** Collected via Selenium using the Nitter interface.  
- **Stock Market Data:** Retrieved from Yahoo Finance.

---

## Workflow

### **1. Data Preparation**

#### **Data Collection**
- **Twitter Sentiment:** Scraped daily from Nitter using Selenium and rotating proxies.  
- **Financial Data:** Extracted from Yahoo Finance (TSLA).

#### **Data Cleaning**
- Remove duplicate tweets to ensure uniqueness.  
- Clean text (remove URLs, mentions, numbers, punctuation).  
- Filter only English tweets.  

#### **Sentiment Analysis**
- **VADER:** Scores sentiment from -1 to 1.  
- **BERT-based Models:** Classify tweets as positive, negative, or neutral.  
- **Multiple Models Compared:** FinancialBERT, DistilRoBERTa, DeBERTa.  
- Tweets with neutral scores are excluded from trading simulations.

---

### **2. Data Analysis**

#### **Exploratory Data Analysis (EDA)**
- Visualize distribution of sentiment scores across models.  
- Highlight dominance of neutral sentiment and its implications.  
- Filter and retain only impactful sentiment signals (above a threshold).

#### **Daily Aggregation**
- Sentiment scores averaged by day.  
- Split between verified and non-verified user tweets.  
- Weighted aggregation allows flexible contribution control from each group.  

#### **Sentiment Calibration**
- Sentiment time series are normalized and smoothed.  
- Rolling averages applied to capture trends and reduce noise.  

---

### **3. Trading Strategy Development**

#### **Signal Generation**
- Buy/sell decisions based on thresholds applied to smoothed sentiment signals.  
- Trades executed at daily open, exits on sentiment reversal.  
- Portfolio return is tracked over time.

#### **Parameter Optimization**
- Grid search over multiple configurations:
  - Sentiment model choice
  - Rolling window size
  - Buy/sell thresholds  
- Best-performing combination is selected based on return.

---

## References

> Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14).  
> HuggingFace Transformers — Financial Sentiment Models

---
