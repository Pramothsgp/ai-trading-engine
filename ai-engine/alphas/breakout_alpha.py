import pandas as pd
from .base import Alpha


class BreakoutAlpha(Alpha):
    name = "breakout_alpha"

    def compute(self, df: pd.DataFrame, mode="live") -> pd.Series:
        high_20 = df["High"].rolling(20).max()
        atr = df["atr"]

        breakout = (df["Close"] > high_20).astype(int)
        volatility_adj = atr / df["Close"]

        score = breakout * volatility_adj
        return score
