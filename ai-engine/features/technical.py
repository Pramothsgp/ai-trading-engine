import pandas_ta as ta
import pandas as pd


def add_technical_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["rsi"] = ta.rsi(df["Close"], length=14)

    df["ema_20"] = ta.ema(df["Close"], length=20)
    df["ema_50"] = ta.ema(df["Close"], length=50)
    df["ema_100"] = ta.ema(df["Close"], length=100)  # ✅ NEW

    df["atr"] = ta.atr(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        length=14,
    )

    df["returns"] = df["Close"].pct_change()

    df["volatility"] = df["returns"].rolling(20).std()

    return df
