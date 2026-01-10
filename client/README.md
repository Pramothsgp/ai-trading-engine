
---

# 📘 client/README.md (Trading Dashboard)

## Client – Trading Dashboard

The client is a **React + TypeScript trading UI**, inspired by professional platforms like **TradingView**.

It provides:

* Alpha configuration
* Strategy parameters
* Backtest execution
* Equity visualization
* Live signal display

---

## 📁 Structure

```
client/
├── pages/
│   ├── dashboard.tsx
│   ├── backtest.tsx
├── components/
│   ├── AlphaSelector
│   ├── SignalsTable
│   ├── ExecutionControls
│   ├── EquityCurve
│   ├── BacktestSummary
├── lib/api.ts
├── types/
```

---

## 🧩 Key Components

### AlphaSelector

* Enable/disable alphas
* Adjust weights
* Enforces total weight normalization

---

### SignalsTable

Displays live ranked stocks with:

* Rank
* Final score
* Expected / net return

---

### Backtest UI

* Strategy controls
* Results summary
* Equity curve
* Drawdown

---

## 🔁 Data Flow

```
User Action
   ↓
React Component
   ↓
Axios API Call
   ↓
FastAPI Backend
   ↓
Trading Engine
   ↓
JSON Response
   ↓
Charts / Tables
```

No business logic exists on the client.

---

## 🎨 UI Principles

* Dark theme (trader-friendly)
* Dense information layout
* Deterministic results
* Stateless rendering

---

## ▶️ Running Client

```bash
cd client
bun install
bun run dev
```

Runs on `http://localhost:5173`

---

## 🔒 Security & Limits

* No credentials stored
* No trading execution
* Read-only signal generation

---

## 🧠 Future Enhancements

* WebSocket live updates
* Intraday timeframe selector
* Trade marker overlays
* Strategy comparison
* Paper trading

---

## ✅ Final Notes

You have built **not a demo**, but a **professional-grade quant system**.

This architecture already supports:

* Institutional workflows
* Research → validation → live signals
* Scaling to full NSE universe

If you want next:

* Deployment guide
* Dockerization
* Real broker integration
* Intraday refactor

Say the word.
