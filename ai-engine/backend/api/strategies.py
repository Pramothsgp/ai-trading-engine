from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/strategies", tags=["Strategies"])


@router.get("/")
def list_strategies() -> Dict[str, Any]:
    """
    List available strategy templates / alpha presets.
    Used by UI dropdowns.
    """
    return {
        "strategies": [
            {
                "id": "multi_alpha_default",
                "name": "Multi-Alpha (ML + Momentum + Breakout)",
                "alphas": {
                    "ml": {"enabled": True, "weight": 0.5},
                    "momentum": {"enabled": True, "weight": 0.3},
                    "breakout": {"enabled": True, "weight": 0.2},
                },
                "execution": {
                    "top_k": 3,
                    "hold_days": 10,
                    "round_trip_cost": 0.003,
                    "no_trade_lookback": 20,
                },
            }
        ]
    }
