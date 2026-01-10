## AI Trading Strategy Engine – System Overview

This repository implements a **multi-alpha quantitative trading system** with:

* Cross-sectional alpha modeling
* ML-based ranking (XGBoost)
* Rule-based alphas (Momentum, Breakout)
* Event-driven backtesting
* Walk-forward validation
* Live signal generation
* Frontend trading dashboard

The system is **modular, extensible, and production-oriented**, designed to scale from **daily equity strategies → intraday → derivatives (options)**.

---

## 🧠 Core Design Philosophy

1. **Cross-Sectional Ranking (not prediction)**

   * The model does NOT predict price
   * It predicts **relative attractiveness among stocks on the same date**

2. **Alpha Ensemble**

   * Multiple independent alphas
   * Normalized cross-sectionally
   * Weighted aggregation

3. **Separation of Concerns**

   * Data pipeline
   * Alpha computation
   * Execution logic
   * API layer
   * UI layer

Each layer can evolve independently.

---

## 🏗️ High-Level Architecture

```
┌────────────┐
│ Market Data│
│ (CSV / API)│
└─────┬──────┘
      ↓
┌──────────────────────────┐
│ Feature Engineering      │
│ (Technical + Context)    │
└─────┬────────────────────┘
      ↓
┌──────────────────────────┐
│ Labeling (Training Only) │
│ - forward_return         │
│ - score                  │
└─────┬────────────────────┘
      ↓
┌──────────────────────────┐
│ ML Model Training        │
│ (XGBoost Cross-Sectional)│
└─────┬────────────────────┘
      ↓
┌──────────────────────────┐
│ Alpha Engine             │
│ - ML Alpha               │
│ - Momentum               │
│ - Breakout               │
└─────┬────────────────────┘
      ↓
┌──────────────────────────┐
│ Backtest / Walk-Forward  │
│ / Live Signal Engine     │
└─────┬────────────────────┘
      ↓
┌──────────────────────────┐
│ FastAPI Backend          │
└─────┬────────────────────┘
      ↓
┌──────────────────────────┐
│ React Client Dashboard   │
└──────────────────────────┘
```

---

## 📊 Key Concepts

### Cross-Sectional Dataset (CSD)

* One row = one stock on one date
* Many stocks share the same date
* Used for:

  * ML training
  * Backtesting
  * Walk-forward
* **Not used directly for live inference**

### Live Cross-Sectional Dataset (LCD)

* Latest available day only
* Built separately
* Used exclusively for **live signals**

---

## ⚠️ Important Distinction

| Dataset                     | Purpose              | Contains Labels |
| --------------------------- | -------------------- | --------------- |
| cross_sectional_dataset.csv | Training & backtests | Yes             |
| live_cross_sectional.csv    | Live signals         | No              |

They **must never overwrite each other**.

---

## 🧩 Execution Order (End-to-End)

1. Download market data
2. Build features
3. Create labels (training only)
4. Build cross-sectional dataset
5. Train ML alpha model
6. Start backend API
7. Use UI for:

   * Backtest
   * Walk-forward
   * Live signals

---

## 🚀 System Guarantees

* No look-ahead bias
* Date-safe cross-sectional normalization
* ML model never sees future data
* Live mode never depends on labels

---

## 🧠 Extensibility Roadmap

* Replace CSV with broker API
* Switch daily → intraday
* Add options greeks
* Plug RL agents
* Stream live updates via WebSockets

---

---