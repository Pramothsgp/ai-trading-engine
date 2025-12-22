# from fastapi import APIRouter
# import pandas as pd
# from engine.alpha_engine import build_alpha_score, rank_alpha_score
# from backend.core.execution import apply_costs_and_tax
# import os

# router = APIRouter()

# DATA_PATH = os.path.join("data", "processed", "live_cross_sectional.csv")


# @router.post("/signals/live")
# def live_signals(payload: dict, top_k: int = 3):
#     alpha_config = payload["alpha_config"]
#     execution = payload["execution"]

#     df = pd.read_csv(DATA_PATH)

#     df["final_score"] = build_alpha_score(
#         df,
#         alpha_config,
#         date_col="Date",
#     )

#     df["rank"] = rank_alpha_score(
#         df,
#         score_col="final_score",
#         date_col="Date",
#     )

#     latest_date = df["Date"].max()

#     signals = (
#         df[df["Date"] == latest_date]
#         .sort_values("final_score", ascending=False)
#         .head(top_k)
#     )

#     # Placeholder expected return (until real execution engine)
#     signals["expected_return"] = signals["final_score"] * 0.02

#     signals["net_return"] = signals["expected_return"].apply(
#         lambda r: apply_costs_and_tax(
#             r,
#             execution["transaction_cost"],
#             execution["tax"],
#         )
#     )

#     return {
#         "mode": "LIVE",
#         "date": str(latest_date),
#         "signals": signals[["symbol", "rank", "final_score", "net_return"]].to_dict(
#             orient="records"
#         ),
#     }
