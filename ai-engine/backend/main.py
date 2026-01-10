from fastapi.middleware.cors import CORSMiddleware



from fastapi import FastAPI
from backend.api.backtest import router as backtest_router
from backend.api.signals import router as signals_router
from backend.api.alphas import router as alphas_router
from backend.api.strategies import router as strategies_router
from backend.api.walkforward import router as walkforward_router

app = FastAPI(title="AI Trading Strategy Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(backtest_router, prefix="/api")
app.include_router(signals_router, prefix="/api")
app.include_router(alphas_router, prefix="/api")
app.include_router(strategies_router, prefix="/api")
app.include_router(walkforward_router, prefix="/api")

@app.get("/")
def health():
    return {"status": "running"}
