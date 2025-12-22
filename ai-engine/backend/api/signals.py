from fastapi import APIRouter, Query
from backend.schemas.strategy import StrategyConfig
from typing import Optional
import pandas as pd
from engine.alpha_engine import build_alpha_score, rank_alpha_score
from backend.core.live_engine import generate_live_signals
import os
from datetime import datetime

router = APIRouter(prefix="/signals", tags=["Signals"])

DATA_PATH = os.path.join("data", "processed", "live_cross_sectional.csv")


@router.post("/date")
def generate_signals(
    strategy: StrategyConfig,
    date: Optional[str] = Query(
        None,
        description="Date in YYYY-MM-DD format. If not provided, uses latest available data",
    ),
):
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])

    if date:
        # Use specific date if provided
        target_date = pd.to_datetime(date)
        available_dates = df["Date"].unique()

        # Find the closest available date on or before the target date
        valid_dates = available_dates[available_dates <= target_date]
        if len(valid_dates) == 0:
            return {"error": f"No data available on or before {date}"}

        latest_date = valid_dates.max()
        today = df[df["Date"] == latest_date]
    else:
        # Use latest available data (live behavior)
        latest_date = df["Date"].max()
        today = df[df["Date"] == latest_date]

    alpha_cfg = {k: v.dict() for k, v in strategy.alphas.items()}

    today["final_score"] = build_alpha_score(today, alpha_cfg)
    today["rank"] = rank_alpha_score(today, "final_score")

    picks = today[today["rank"] <= strategy.top_k].sort_values("rank")[
        ["symbol", "final_score", "rank"]
    ]

    return {"date": str(latest_date.date()), "signals": picks.to_dict(orient="records")}


@router.post("/live")
def live_signals(strategy: StrategyConfig, top_k: int = 200):
    return generate_live_signals(strategy, top_k)
