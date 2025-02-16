# Market Sentiment Analysis !

This project explores the relationship between Twitter sentiment and Tesla's stock performance. By analyzing public sentiment, we investigate whether trends in online discourse can be leveraged to inform trading strategies.

---

## Project Overview

### Objective
- **Analyze** how sentiment expressed on Twitter correlates with Tesla's stock performance.
- **Evaluate** the potential of using sentiment data as a signal for trading decisions.

### Data Sources
- **Twitter Data:** Scraped via Selenium using the Nitter interface.
- **Stock Market Data:** Retrieved from Yahoo Finance.

---

## Workflow

### 1. Data Preparation

- **Data Collection**
  - **Twitter:** Scrape tweets from Nitter with Selenium.
  - **Financial Data:** Fetch stock market info from Yahoo Finance.

- **Data Cleaning**
  - Remove duplicates for unique entries.
  - Eliminate URLs and special characters to refine the text.
  - Normalize the text (e.g., lowercasing, punctuation handling) to prepare for analysis.

- **Sentiment Analysis**
  - Utilize **VADER (Valence Aware Dictionary and sEntiment Reasoner)** to compute sentiment scores for each tweet on a scale from -1 (negative) to +1 (positive).

---

### 2. Data Analysis

- **Exploratory Data Analysis (EDA)**
  - Visualize the distribution of sentiment scores.
  - Identify the most frequently mentioned companies.
  - Chart sentiment trends over time.

- **Correlation with Market Data**
  - Compare sentiment scores with key stock market indicators.
  - Investigate possible relationships between social media sentiment and market performance.

---

### 3. Trading Strategy Development

- **Signal Generation**
  - Transform sentiment analysis and financial indicators into potential buy/sell signals.
  - Evaluate the efficiency of these signals through backtesting.

---

## Get Involved

Feel free to explore the code, data, and visualizations in this repository. Your feedback is welcome—if you have questions or suggestions, please reach out!

---
