import pandas as pd
import numpy as np


def add_market_regime(nifty_df):
    nifty_df = nifty_df.copy()

    # Trend
    nifty_df["ema_50"] = nifty_df["Close"].ewm(span=50, adjust=False).mean()
    nifty_df["ema_200"] = nifty_df["Close"].ewm(span=200, adjust=False).mean()
    nifty_df["bull_regime"] = (nifty_df["ema_50"] > nifty_df["ema_200"]).astype(int)

    # Volatility (20-day realized)
    nifty_df["returns"] = nifty_df["Close"].pct_change()
    nifty_df["vol_20"] = nifty_df["returns"].rolling(20).std()

    # Rolling volatility threshold (adaptive)
    nifty_df["vol_threshold"] = nifty_df["vol_20"].rolling(252).quantile(0.75)

    nifty_df["low_vol_regime"] = (
        nifty_df["vol_20"] < nifty_df["vol_threshold"]
    ).astype(int)

    return nifty_df[["Date", "bull_regime", "low_vol_regime"]]
