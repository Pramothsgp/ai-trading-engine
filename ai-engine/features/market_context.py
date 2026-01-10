import pandas as pd

def add_trend_context(df):
    # Ensure EMA columns are numeric and handle None/NaN values
    df["ema_20"] = pd.to_numeric(df["ema_20"], errors="coerce")
    df["ema_50"] = pd.to_numeric(df["ema_50"], errors="coerce")
    
    # Perform comparison, NaN values will be preserved and then converted to 0
    df["trend"] = (df["ema_20"] > df["ema_50"]).fillna(0).astype(int)
    df["volatility"] = df["returns"].rolling(14).std()
    return df
