import pandas as pd
import numpy as np

DATA_PATH = "data/processed/cross_sectional_dataset.csv"
SIGNAL_PATH = "signals/signals.csv"

HOLD_DAYS = 10
CAPITAL = 1_000_000
POSITION_SIZE = 0.1  # 10% per position

# -------------------------
# LOAD DATA
# -------------------------

df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(["symbol", "Date"]).reset_index(drop=True)

signals = pd.read_csv("signals/signals.csv")
signals["Date"] = pd.to_datetime(signals["Date"])

df = df.merge(signals[["Date", "symbol", "signal"]], on=["Date", "symbol"], how="left")

df["signal"] = df["signal"].fillna(0)

# -------------------------
# SIMULATE TRADES
# -------------------------

trades = []

for _, row in df[df["signal"] == 1].iterrows():
    entry_date = row["Date"]
    symbol = row["symbol"]
    entry_price = row["Close"]

    future = df[(df["symbol"] == symbol) & (df["Date"] > entry_date)].head(HOLD_DAYS)

    if len(future) < HOLD_DAYS:
        continue

    exit_price = future.iloc[-1]["Close"]
    ret = (exit_price - entry_price) / entry_price

    trades.append(ret)

# -------------------------
# RESULTS
# -------------------------

trades = np.array(trades)

print("\n===== BACKTEST RESULTS =====")
print(f"Trades: {len(trades)}")
print(f"Win rate: {(trades > 0).mean():.2%}")
print(f"Average return per trade: {trades.mean():.4f}")
print(f"Total return (no compounding): {trades.sum():.4f}")
