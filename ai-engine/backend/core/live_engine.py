import pandas as pd
from engine.alpha_engine import build_alpha_score, rank_alpha_score

DATA_PATH = "data/processed/live_cross_sectional.csv"


def generate_live_signals(strategy, top_k):
    df = pd.read_csv(DATA_PATH)
    print(len(df))
    df["Date"] = pd.to_datetime(df["Date"])
    alpha_config = {k: v.dict() for k, v in strategy.alphas.items()}

    df["final_score"] = build_alpha_score(df, alpha_config)
    df["rank"] = rank_alpha_score(df, "final_score")

    latest = df["Date"].max()

    signals = (
        df[df["Date"] == latest]
        .sort_values("final_score", ascending=False)
        .head(top_k)[["symbol", "final_score", "rank"]]
        .to_dict(orient="records")
    )
    result = pd.DataFrame(signals)
    # Format datetime for valid filename (replace spaces and colons)
    filename = latest.strftime("%Y-%m-%d_%H-%M-%S")
    result.to_csv(f"data/result/{filename}.csv")

    return {
        "mode": "LIVE",
        "date": str(latest),
        "signals": signals,
    }
