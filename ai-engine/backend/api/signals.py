from fastapi import APIRouter, Query
from backend.schemas.strategy import StrategyConfig
from typing import Optional
from backend.core.live_engine import generate_live_signals, generate_date_signals

router = APIRouter(prefix="/signals", tags=["Signals"])


@router.post("/date")
def generate_signals(
    strategy: StrategyConfig,
    date: Optional[str] = Query(
        None,
        description="Date in YYYY-MM-DD format. If not provided, uses latest available data",
    ),
    top_k: int = Query(
        20,
        description="Number of top signals to return",
        ge=1,
        le=500,
    ),
    min_price: float = Query(
        0.0,
        description="Minimum stock price filter",
        ge=0.0,
    ),
    min_volume: int = Query(
        0,
        description="Minimum trading volume filter",
        ge=0,
    ),
):
    return generate_date_signals(strategy, top_k, date, min_price, min_volume)


@router.post("/live")
def live_signals(
    strategy: StrategyConfig,
    top_k: int = Query(
        20,
        description="Number of top signals to return",
        ge=1,
        le=500,
    ),
    min_price: float = Query(
        0.0,
        description="Minimum stock price filter",
        ge=0.0,
    ),
    min_volume: int = Query(
        0,
        description="Minimum trading volume filter",
        ge=0,
    ),
):
    return generate_live_signals(strategy, top_k, min_price, min_volume)
