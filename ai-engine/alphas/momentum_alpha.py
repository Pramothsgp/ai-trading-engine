import pandas as pd
from .base import Alpha


class MomentumAlpha(Alpha):
    name = "momentum_alpha"

    def compute(self, df: pd.DataFrame, mode="live") -> pd.Series:
        # Simple medium-term momentum
        momentum = df["Close"] / df["ema_100"] - 1
        return momentum
