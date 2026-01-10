

# 📘 backend/README.md (FastAPI + Trading Engine)

## Backend – Trading & Strategy Engine

The backend provides a **stateless, deterministic API** for:

* Strategy backtesting
* Walk-forward validation
* Live signal generation
* Alpha configuration

Built using **FastAPI**, designed for low latency and future WebSocket support.

---

## 📁 Directory Structure

```
backend/
├── api/                # HTTP endpoints
├── core/               # Execution engines
├── schemas/            # Pydantic request/response models
├── main.py             # App entrypoint
```

---

## 🔌 API Endpoints

### `/api/backtest/run`

Runs a full historical backtest.

**Input**

```json
{
  "alphas": {...},
  "top_k": 3,
  "hold_days": 10,
  "trade_notional": 100000
}
```

**Output**

* Trades
* Win rate
* Avg return
* Equity curve
* Drawdown

---

### `/api/backtest/equity`

Returns equity curve only (used for charts).

---

### `/api/walkforward/run`

Performs walk-forward evaluation using rolling windows.

Used to validate **strategy robustness**, not profitability.

---

### `/api/signals/live`

Generates live ranked signals using:

* Latest available date
* Live feature dataset
* Loaded ML model

---

## 🧠 Alpha Engine

Located in `engine/alpha_engine.py`

### Responsibilities:

* Enable/disable alphas
* Normalize alpha scores cross-sectionally
* Weight and aggregate final score

```python
final_score = Σ(weight_i × zscore(alpha_i))
```

---

## 📊 Alphas

| Alpha         | Type | Description            |
| ------------- | ---- | ---------------------- |
| MLAlpha       | ML   | XGBoost rank predictor |
| MomentumAlpha | Rule | Trend continuation     |
| BreakoutAlpha | Rule | Volatility expansion   |

Each alpha is **independent and pluggable**.

---

## 🤖 ML Alpha Lifecycle

### Training

* Uses labeled CSD
* Predicts `score` or `forward_return`
* Saved via `joblib`

### Inference

* Loaded once at startup
* Used only in:

  * live signals
  * backtests
  * walk-forward

Fails fast if model not loaded.

---

## 🛑 Safety Rules

* Live engine never uses labels
* Backtest uses historical prices only
* No implicit defaults (explicit config required)

---

## ▶️ Running Backend

```bash
export PYTHONPATH=$(pwd)
uvicorn backend.main:app --reload
```

---
