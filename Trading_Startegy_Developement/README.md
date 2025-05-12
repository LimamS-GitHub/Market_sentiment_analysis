# Trading_Strategy_Development

Back-testing engine that **adapts day-by-day**:  
for each trading date it re-trains on the *N* previous months of data, picks the best sentiment mix via random search, executes the next-day trade, and records full performance stats.

---

## What it does
1. **Daily random search** – finds the best weights (VADER + 4 HF models), buy/sell thresholds, and verified-account factor on the training window that ends the day before.  
2. **Walk-forward simulation** – moves one day ahead, sends the trade, updates cash & position.  
3. **Detailed KPI dump** – Total Return, CAGR, annual volatility, max drawdown, yearly out-performance vs buy-and-hold, mean € gap vs stock.

*(No rolling averages or technical indicators are used inside the model — only the daily sentiment features you provide.)*

---

## Daily Adaptive Loop

```mermaid
flowchart TD
    subgraph DAILY_LOOP["Repeat for each trading day t"]
        A1[Select training window\\n(last N months)]
        A2[Random search\\nweights & thresholds]
        A3[Keep best parameters]
        A4[Generate sentiment\\nsignal for day t]
        A5[Execute trade\\n(open of day t+1)]
        A6[Update cash and position]
        A7[Log KPIs\\nReturn, CAGR, Vol, DD]
    end
    A1 --> A2 --> A3 --> A4 --> A5 --> A6 --> A7
    A7 -->|next day| DAILY_LOOP
```

---

## Folder layout
```
Trading_Strategy_Development/
├── src/
│   ├── model.py               # SentimentTradingModel class
│   ├── Utils_simulations.py   # simuler_marche_journalier()
│   └── Utils_study_results.py # KPI calc + batch runner
├── Notebooks/
│   ├── TSD.ipynb              # step-by-step example
│   └── Study_results.ipynb    # aggregate & plot batch runs
└── README.md
```

---

## Quick start

```bash
# Single adaptive run on Tesla
python src/Utils_simulations.py \
  --sentiment_csv ../../data/processed/tsla_sentiment.csv \
  --price_csv     ../../data/market/TSLA.csv \
  --lookback_months 6 \
  --n_iter 200 \
  --capital 10000 \
  --out_dir results/tsla_run

# Batch scan: 3 look-back lengths × 2 search sizes
python src/Utils_study_results.py \
  --sentiment_csv ../../data/processed/tsla_sentiment.csv \
  --price_csv     ../../data/market/TSLA.csv \
  --train_lengths 3 6 12 \
  --n_iter_list   100 250 \
  --capital 10000 \
  --out_root results/batch
```

### Key outputs

| Path | Purpose |
|------|---------|
| `history.csv` | Daily equity, cash, position, signal, price |
| `kpi.json` | Summary KPIs (Total Return, CAGR, Vol, Max DD, etc.) |
| `parameters.json` | Weights, thresholds and verified factors chosen each day |
| `Notebooks/df_global/results_global.csv` | One line per batch run (overall leaderboard) |
| `Notebooks/df_global/results_global_mois_1.csv` | KPIs aggregated month-by-month (example) |

> **Where exactly are they stored?**  
> All artifacts live under **`Notebooks/df_global/`** so you can explore them directly in Jupyter:
>
> ```
> Notebooks/df_global/
> ├── results_global.csv            # leaderboard of every run
> ├── results_global_mois_1.csv     # monthly slice KPIs
> ├── df_historique_param/          # ⤷ daily hyper-parameter trajectories
> └── df_historique_saves/          # ⤷ full equity curves & trade logs
> ```
>
> Open **`Study_results.ipynb`** to load these CSVs, rank strategies, and visualise the parameter evolution.

---

## Main pieces

| File / Function | Role |
|-----------------|------|
| **`model.py` / `SentimentTradingModel`** | Combines the five sentiment columns with custom weights; random-searches hyper-parameters; outputs buy / sell / hold signal. |
| **`Utils_simulations.py` / `simuler_marche_journalier`** | Daily loop → train, signal, trade, log. |
| **`Utils_study_results.py` / `analyser_performance_portefeuille`** | Computes KPIs and plots equity curve. |
| `simulation_download_results()` | Runs hundreds of experiments and aggregates results. |

---

## Key parameters

| Arg / Attr | Controls | Typical values |
|------------|----------|----------------|
| `lookback_months` | Training window length | 3 / 6 / 12 |
| `n_iter` | Random-search iterations per day | 100 – 500 |
| `buy_threshold / sell_threshold` | Entry / exit cut-offs | sampled in [0, 1] / [-1, 0] |
| `weights` | 4-tuple (VADER + 3 HF) — Σ = 1 | auto-sampled |
| `weight_verified` | Extra weight for verified accounts | 0 – 1 |

---

## Interpreting KPIs

| Metric | Meaning |
|--------|---------|
| **Total Return** | overall % gain |
| **CAGR** | compound annual growth rate |
| **Annual Volatility** | σ of daily returns × √252 |
| **Max Drawdown** | worst peak-to-trough drop |
| **Annual Out-perf.** | CAGR(strategy) – CAGR(stock) |
| **Avg € gap vs stock** | mean daily € difference vs buy-and-hold (scaled to initial capital) |

Aim for high Total Return & CAGR with low Max DD and acceptable volatility.

---

## Roadmap

* Replace random search with **Optuna Bayesian optimisation**.  
* Add stop-loss / take-profit logic.  
* Scale to **multi-asset** portfolios.  
* Expose the loop as a **FastAPI** service for live paper trading.

Questions or suggestions? Open an issue or PR — contributions welcome!
