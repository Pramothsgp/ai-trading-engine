import pandas as pd
from engine.alpha_engine import build_alpha_score, rank_alpha_score
from features.market_regime import add_market_regime
import os

DATA_PATH = os.path.join("data", "processed", "live_cross_sectional.csv")


def run_backtest(strategy):
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["Date", "symbol"]).reset_index(drop=True)

    # --- market regime ---
    nifty = pd.read_csv(os.path.join("data", "nifty", "NIFTY.csv"))
    nifty = nifty.iloc[2:].reset_index(drop=True)
    nifty.columns = ["Date", "Close", "High", "Low", "Open", "Volume"]
    nifty["Date"] = pd.to_datetime(nifty["Date"])
    nifty["Close"] = pd.to_numeric(nifty["Close"], errors="coerce")
    nifty.dropna(inplace=True)

    regime = add_market_regime(nifty)
    df = df.merge(regime, on="Date", how="left")
    df.fillna(0, inplace=True)

    # --- alpha config ---
    alpha_cfg = {k: v.dict() for k, v in strategy.alphas.items()}

    df["final_score"] = build_alpha_score(df, alpha_cfg)
    df["rank"] = rank_alpha_score(df, "final_score")

    # --- simple evaluation (summary only) ---
    trades = df[df["rank"] <= strategy.top_k]

    avg_score = trades["final_score"].mean()
    count = len(trades)

    return {
        "trades": int(count),
        "avg_score": float(avg_score),
    }
