from pydantic import BaseModel
from typing import Dict, Optional


class AlphaConfig(BaseModel):
    enabled: bool
    weight: Optional[float] = 1.0


class StrategyConfig(BaseModel):
    alphas: Dict[str, AlphaConfig]

    top_k: int = 3
    hold_days: int = 10

    trade_notional: float = 100000
    round_trip_cost: float = 0.003

    use_trend_filter: bool = True
    use_vol_filter: bool = True

    no_trade_lookback: int = 20
