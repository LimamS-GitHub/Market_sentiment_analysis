# EDA & Sentiment-Driven Trading — *Tesla 2022*

This notebook begins by exploring sentiment data and investigates whether daily Twitter mood can help anticipate — and trade — Tesla's price movements.

---

## Goals
* Inspect the sentiment distribution produced by four models (VADER + FinancialBERT + DistilRoBERTa + DeBERTa).  
* Prototype a simple long/flat strategy based on sentiment thresholds.  
* Tune the strategy’s hyper-parameters.

---

## Data
| Source / File | Content |
|---------------|---------|
| `Data_Tesla_2022_2025.csv` | Tweets with cleaned text, verified flag, five sentiment columns |
|  `TSLA_market.csv`  | **Daily OHLCV for TSLA (2022 → 2025)** |

---

## Notebook Flow

1. **Load & tidy**  
   Import the tweet CSV and TSLA price series, drop duplicates, convert `query_date` to `datetime`, then keep only the **1 Jan → 31 Dec 2022** slice.

2. **Histogram sentiment**  
   Plot a histogram for each model (VADER, FinancialBERT, DistilRoBERTa-Fin, DeBERTa-v3-Fin) and highlight a huge spike at **0** ⇒ most tweets are neutral.

3. **Filter & aggregate**  
   Discard tweets with |score| <= 0.1 — these are considered too neutral to drive reliable buy/sell decisions.
   Split **verified** vs **non-verified** accounts and compute a daily weighted mean: **25 % verified / 75 % non-verified**.

4. **Merge market data**  
   Pull TSLA data via `TSLA_market.csv` and merge with the sentiment table on `date`.

5. **Normalise & smooth**  
   Z-score the closing price and scale each sentiment series to its max absolute value.  
   Add a rolling mean (window **1 → 7 days**) to reduce noise.

6. **Visualise**  
   Plot the normalised price curve plus a colour band (green / amber / red) keyed to the smoothed sentiment level—quickly shows price-mood divergences.

7. **Baseline strategy**  
   Fixed rules: **long** if sentiment > 0.2, **flat** if sentiment < –0.2.  
   Simulate a \$10 000 account and chart the equity curve vs buy-and-hold.

8. **Grid search**  
   Sweep:  
   * sentiment model (4 variants)  
   * rolling window (1 → 7 d)  
   * Buy/sell thresholds are selected from the range [0, 1] × [–1, 0]
   **Best 2022 run:** **+75.9 %** with *FinancialBERT*, 1-day window, buy = 0.3, sell = –0.5.

---

## Takeaways
Even a naïve threshold rule on daily sentiment outperformed buy-and-hold in 2022, suggesting real predictive value when signals are properly filtered and weighted.

---

## Next step  
Feed these sentiment features into the **adaptive trading engine** in `Trading_Strategy_Development`, which retrains each day on the last *N* months and rolls forward while logging full KPIs.

---

> **Note — OHLCV:**  
> *Open* (first price of the day), *High* (intraday maximum), *Low* (intraday minimum), *Close* (last price of the day), and *Volume* (shares traded). These five fields summarise each trading session and are standard in market data files.
