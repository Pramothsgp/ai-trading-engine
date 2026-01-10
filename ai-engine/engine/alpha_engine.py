import pandas as pd
import numpy as np
from scipy.stats import zscore

from alphas.ml_alpha import MLAlpha
from alphas.momentum_alpha import MomentumAlpha
from alphas.breakout_alpha import BreakoutAlpha


# =========================
# ALPHA REGISTRY
# =========================

ALPHA_REGISTRY = {
    "ml": MLAlpha(),
    "momentum": MomentumAlpha(),
    "breakout": BreakoutAlpha(),
}


# =========================
# NORMALIZATION
# =========================


def cross_sectional_zscore(series: pd.Series, dates: pd.Series) -> pd.Series:
    df = pd.DataFrame({"date": dates, "value": series})

    def _z(x):
        if x.std(ddof=0) == 0 or len(x) < 2:
            return pd.Series(0.0, index=x.index)
        return pd.Series(zscore(x, nan_policy="omit"), index=x.index)

    return df.groupby("date")["value"].transform(_z)


# =========================
# MAIN ENGINE
# =========================


def build_alpha_score(
    df: pd.DataFrame,
    alpha_config: dict,
    date_col: str = "Date",
    mode: str = "live",  # <-- FIX
) -> pd.Series:
    """
    mode:
      - "train"
      - "backtest"
      - "live"
    """

    if date_col not in df.columns:
        raise ValueError(f"Missing required column: {date_col}")

    combined_score = pd.Series(0.0, index=df.index)
    total_weight = 0.0
    enabled_any = False

    for alpha_key, cfg in alpha_config.items():
        if not cfg.get("enabled", False):
            continue

        if alpha_key not in ALPHA_REGISTRY:
            raise ValueError(f"Unknown alpha: {alpha_key}")

        enabled_any = True
        alpha = ALPHA_REGISTRY[alpha_key]

        # ---- compute raw alpha safely ----
        raw_score = alpha.compute(df, mode=mode)

        if not isinstance(raw_score, pd.Series):
            raise TypeError(f"{alpha_key} did not return pd.Series")

        # ---- normalize cross-sectionally ----
        norm_score = cross_sectional_zscore(raw_score, df[date_col])

        weight = float(cfg.get("weight", 1.0))
        combined_score += weight * norm_score
        total_weight += weight

    if not enabled_any:
        raise ValueError("No alphas enabled")

    if total_weight == 0:
        raise ValueError("Total alpha weight is zero")

    return combined_score / total_weight


# =========================
# RANKING
# =========================


def rank_alpha_score(
    df: pd.DataFrame,
    score_col: str,
    date_col: str = "Date",
    ascending: bool = False,
) -> pd.Series:
    return (
        df.groupby(date_col)[score_col]
        .rank(method="first", ascending=ascending)
        .astype(int)
    )
