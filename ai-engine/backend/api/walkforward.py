from fastapi import APIRouter
from backend.schemas.strategy import StrategyConfig
from backend.core.walkforward_engine import run_walkforward

router = APIRouter(prefix="/walkforward", tags=["WalkForward"])


@router.post("/run")
def walkforward_run(strategy: StrategyConfig):
    return run_walkforward(strategy)
