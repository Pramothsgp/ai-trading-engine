import pandas as pd
import numpy as np
import joblib

MODEL_PATH = "models/cross_sectional_xgb.pkl"
DATA_PATH = "data/processed/cross_sectional_dataset.csv"

FEATURES = ["rsi", "ema_20", "ema_50", "atr", "returns", "trend", "volatility"]

TOP_K = 3  # number of stocks to buy each day
HOLD_DAYS = 10  # holding period

# -------------------------
# LOAD DATA & MODEL
# -------------------------

df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(["Date", "symbol"]).reset_index(drop=True)

model = joblib.load(MODEL_PATH)

# -------------------------
# PREDICT SCORES
# -------------------------

df["predicted_return"] = model.predict(df[FEATURES])

# -------------------------
# DAILY RANKING
# -------------------------

df["daily_rank"] = df.groupby("Date")["predicted_return"].rank(
    ascending=False, method="first"
)

df["signal"] = (df["daily_rank"] <= TOP_K).astype(int)

print(df[df["signal"] == 1].head())

df[["Date", "symbol", "signal"]].to_csv("signals/signals.csv", index=False)
