from fastapi import APIRouter

router = APIRouter(prefix="/alphas", tags=["Alphas"])


@router.get("")
def list_alphas():
    return {
        "alphas": [
            {
                "key": "ml",
                "name": "Machine Learning Alpha",
                "requires_model": True,
            },
            {
                "key": "momentum",
                "name": "Momentum Alpha",
                "requires_model": False,
            },
            {
                "key": "breakout",
                "name": "Breakout Alpha",
                "requires_model": False,
            },
        ]
    }
