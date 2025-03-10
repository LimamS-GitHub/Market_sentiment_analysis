# Market Sentiment Analysis

This project investigates the relationship between Twitter sentiment and Tesla's stock performance. By analyzing public sentiment, we aim to determine whether trends in online discourse can be leveraged to inform trading strategies.

---

## Project Overview

### **Objective**
- **Analyze** the correlation between Twitter sentiment and Tesla’s stock movements.
- **Evaluate** the potential of sentiment data as a predictive signal for trading decisions.

### **Data Sources**
- **Twitter Data:** Collected via Selenium using the Nitter interface.  
- **Stock Market Data:** Retrieved from Yahoo Finance.

---

## Workflow

### **1. Data Preparation**

#### **Data Collection**
- **Twitter Sentiment:** Scraped from Nitter using Selenium.  
- **Financial Data:** Extracted from Yahoo Finance.  

#### **Data Cleaning**
- Remove duplicate tweets to ensure uniqueness.  
- Filter out URLs, special characters, and irrelevant content.  
- Normalize text (e.g., lowercase conversion, punctuation removal) to optimize sentiment analysis.  

#### **Sentiment Analysis**
- **VADER (Valence Aware Dictionary and sEntiment Reasoner):** Computes sentiment scores ranging from -1 (negative) to +1 (positive).  
- **BERT-based Model:** Classifies sentiment into discrete categories (-1 for negative, +1 for positive).  
- **Additional Models:** Test alternative sentiment analysis approaches to enhance accuracy.  

---

### **2. Data Analysis**

#### **Exploratory Data Analysis (EDA)**
- Visualize the distribution of sentiment scores.  
- Identify sentiment trends over time.  
- Compare sentiment variations across different timeframes.  

#### **Correlation with Market Data**
- Examine relationships between sentiment scores and key stock market indicators.  
- Investigate whether social media sentiment can anticipate market fluctuations.  
- Develop predictive models to assess the influence of sentiment on Tesla's stock price.  

#### **Refining Sentiment Analysis**
- Implement a **sentiment calibration method** to better align sentiment scores with stock market movements.  

---

### **3. Trading Strategy Development**

#### **Signal Generation**
- Convert refined sentiment scores and financial indicators (e.g., MACD, moving averages) into actionable buy/sell signals.  
- Assess the effectiveness of these signals through backtesting.  

---

## Referances

> Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

---
