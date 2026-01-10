from fastapi import APIRouter
from backend.schemas.strategy import StrategyConfig
from backend.core.backtest_engine import run_backtest

router = APIRouter(prefix="/backtest", tags=["Backtest"])


@router.post("/run")
def backtest_run(strategy: StrategyConfig):
    return run_backtest(strategy)


@router.post("/equity")
def backtest_equity(strategy: StrategyConfig):
    print(strategy)
    result = run_backtest(strategy, return_equity=True)
    return {"equity_curve": result["equity_curve"]}
