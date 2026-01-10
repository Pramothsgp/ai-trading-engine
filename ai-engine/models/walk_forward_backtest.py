import pandas as pd
import numpy as np

from engine.alpha_engine import build_alpha_score, rank_alpha_score
from features.market_regime import add_market_regime


def walk_forward_run(
    data_path: str = "data/processed/cross_sectional_dataset.csv",
    nifty_path: str = "data/nifty/NIFTY.csv",
    window_train_days: int = 504,
    window_test_days: int = 126,
    top_k: int = 3,
    hold_days: int = 10,
    initial_capital: int = 1_000_000,
    trade_notional: int = 100_000,
    round_trip_cost: float = 0.003,
    no_trade_lookback: int = 20,
    alpha_config: dict | None = None,
):
    if alpha_config is None:
        alpha_config = {
            "ml": {"enabled": True, "weight": 0.5},
            "momentum": {"enabled": True, "weight": 0.3},
            "breakout": {"enabled": True, "weight": 0.2},
        }

    # -------------------------
    # LOAD DATA
    # -------------------------
    df = pd.read_csv(data_path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["Date", "symbol"]).reset_index(drop=True)

    dates = sorted(df["Date"].unique())

    # -------------------------
    # MARKET REGIME
    # -------------------------
    nifty = pd.read_csv(nifty_path)
    nifty = nifty.iloc[2:].reset_index(drop=True)
    nifty.columns = ["Date", "Close", "High", "Low", "Open", "Volume"]
    nifty["Date"] = pd.to_datetime(nifty["Date"])

    for c in ["Open", "High", "Low", "Close", "Volume"]:
        nifty[c] = pd.to_numeric(nifty[c], errors="coerce")

    nifty.dropna(subset=["Close"], inplace=True)

    nifty_regime = add_market_regime(nifty)
    df = df.merge(nifty_regime, on="Date", how="left")
    df[["bull_regime", "low_vol_regime"]] = df[
        ["bull_regime", "low_vol_regime"]
    ].fillna(0)

    # -------------------------
    # WALK-FORWARD LOOP
    # -------------------------
    results = []
    start_idx = window_train_days

    while start_idx + window_test_days < len(dates):
        test_dates = dates[start_idx : start_idx + window_test_days]
        test_df = df[df["Date"].isin(test_dates)].copy()

        test_df["final_score"] = build_alpha_score(
            test_df, alpha_config, date_col="Date"
        )
        test_df["rank"] = rank_alpha_score(test_df, "final_score")

        price_lookup = test_df.set_index(["Date", "symbol"])["Close"]

        cash = initial_capital
        open_positions = []
        trade_returns = []

        for i, date in enumerate(test_dates):
            # EXIT
            still_open = []
            for pos in open_positions:
                if pos["exit_idx"] == i:
                    try:
                        price = price_lookup.loc[(date, pos["symbol"])]
                    except KeyError:
                        still_open.append(pos)
                        continue

                    gross = (price - pos["entry_price"]) / pos["entry_price"]
                    net = gross - round_trip_cost
                    cash += trade_notional * (1 + net)
                    trade_returns.append(net)
                else:
                    still_open.append(pos)

            open_positions = still_open

            todays = test_df[test_df["Date"] == date]

            if (
                len(trade_returns) >= no_trade_lookback
                and np.mean(trade_returns[-no_trade_lookback:]) < 0
            ):
                continue

            if (
                todays["bull_regime"].iloc[0] == 0
                or todays["low_vol_regime"].iloc[0] == 0
            ):
                continue

            for _, row in todays[todays["rank"] <= top_k].iterrows():
                if len(open_positions) >= top_k:
                    break
                if cash < trade_notional:
                    break

                exit_idx = i + hold_days
                if exit_idx >= len(test_dates):
                    continue

                cash -= trade_notional
                open_positions.append(
                    {
                        "symbol": row["symbol"],
                        "entry_price": row["Close"],
                        "exit_idx": exit_idx,
                    }
                )

        results.append(
            {
                "start": str(test_dates[0]),
                "end": str(test_dates[-1]),
                "trades": len(trade_returns),
                "avg_return": float(np.mean(trade_returns)) if trade_returns else 0,
                "win_rate": (
                    float(np.mean([r > 0 for r in trade_returns]))
                    if trade_returns
                    else 0
                ),
                "final_equity": float(cash),
            }
        )

        start_idx += window_test_days

    return results

if __name__ == "__main__":
    results = walk_forward_run()
    print(results)