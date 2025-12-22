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
):
    return generate_date_signals(strategy, top_k, date)


@router.post("/live")
def live_signals(
    strategy: StrategyConfig,
    top_k: int = Query(
        20,
        description="Number of top signals to return",
        ge=1,
        le=500,
    ),
):
    return generate_live_signals(strategy, top_k)
