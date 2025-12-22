# NOTE: This is not used in the backtest. It is just for reference.

import pandas as pd
from features.technical import add_technical_features
from features.market_context import add_trend_context

# ---- LOAD CSV ----
df = pd.read_csv("data/raw/RELIANCE.csv")

# ---- DROP YFINANCE METADATA ROWS ----
df = df.iloc[2:].reset_index(drop=True)

# ---- FIX COLUMN NAMES ----
df.columns = ["Date", "Close", "High", "Low", "Open", "Volume"]

# ---- TYPE CONVERSION ----
df["Date"] = pd.to_datetime(df["Date"])

numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---- DROP BAD ROWS ----
df.dropna(inplace=True)

# ---- ADD FEATURES ----
df = add_technical_features(df)
df = add_trend_context(df)

df.dropna(inplace=True)

print(df.tail())
print(df.dtypes)
