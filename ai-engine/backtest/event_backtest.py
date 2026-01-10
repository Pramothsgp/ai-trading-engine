import pandas as pd
import numpy as np

from engine.alpha_engine import build_alpha_score, rank_alpha_score
from features.market_regime import add_market_regime


# =========================
# MAIN ENGINE
# =========================


def run_event_backtest(
    data_path: str = "data/processed/cross_sectional_dataset.csv",
    nifty_path: str = "data/nifty/NIFTY.csv",
    alpha_config: dict | None = None,
    top_k: int = 3,
    hold_days: int = 10,
    initial_capital: float = 1_000_000,
    trade_notional: float = 100_000,
    round_trip_cost: float = 0.003,
    no_trade_lookback: int = 20,
):
    """
    Multi-alpha event-driven backtest engine.
    Safe to import, API-ready.
    """

    if alpha_config is None:
        alpha_config = {
            "ml": {"enabled": True, "weight": 0.5},
            "momentum": {"enabled": True, "weight": 0.3},
            "breakout": {"enabled": True, "weight": 0.2},
        }

    # =========================
    # LOAD DATA
    # =========================

    df = pd.read_csv(data_path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["Date", "symbol"]).reset_index(drop=True)

    # =========================
    # MARKET REGIME
    # =========================

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

    # =========================
    # BUILD MULTI-ALPHA SCORE
    # =========================

    df["final_score"] = build_alpha_score(
        df,
        alpha_config,
        date_col="Date",
    )

    df["rank"] = rank_alpha_score(
        df,
        score_col="final_score",
        date_col="Date",
    )

    price_lookup = df[["Date", "symbol", "Close"]].set_index(["Date", "symbol"])
    dates = list(df["Date"].unique())

    # =========================
    # STATE
    # =========================

    cash = initial_capital
    open_positions = []
    trade_log = []
    equity_curve = []
    recent_trade_returns = []

    def safe_price(date, symbol):
        try:
            return price_lookup.loc[(date, symbol), "Close"]
        except KeyError:
            return None

    # =========================
    # EVENT LOOP
    # =========================

    for i, date in enumerate(dates):

        # ---- EXIT ----
        still_open = []
        for pos in open_positions:
            if pos["exit_idx"] == i:
                price = safe_price(date, pos["symbol"])
                if price is None:
                    still_open.append(pos)
                    continue

                gross_ret = (price - pos["entry_price"]) / pos["entry_price"]
                net_ret = gross_ret - round_trip_cost
                pnl = trade_notional * net_ret

                cash += trade_notional + pnl
                recent_trade_returns.append(net_ret)

                if len(recent_trade_returns) > no_trade_lookback:
                    recent_trade_returns = recent_trade_returns[-no_trade_lookback:]

                trade_log.append(
                    {
                        "symbol": pos["symbol"],
                        "entry_date": pos["entry_date"],
                        "exit_date": date,
                        "return": net_ret,
                        "pnl": pnl,
                    }
                )
            else:
                still_open.append(pos)

        open_positions = still_open

        # ---- ENTRY ----
        todays = df[df["Date"] == date]

        # NO-TRADE STATE
        if (
            len(recent_trade_returns) >= no_trade_lookback
            and np.mean(recent_trade_returns) < 0
        ):
            equity_curve.append(
                {"Date": date, "Equity": cash + len(open_positions) * trade_notional}
            )
            continue

        # REGIME FILTERS
        if todays["bull_regime"].iloc[0] == 0 or todays["low_vol_regime"].iloc[0] == 0:
            equity_curve.append(
                {"Date": date, "Equity": cash + len(open_positions) * trade_notional}
            )
            continue

        candidates = todays[todays["rank"] <= top_k].sort_values("rank")

        for _, row in candidates.iterrows():
            if len(open_positions) >= top_k:
                break
            if cash < trade_notional:
                break
            if any(p["symbol"] == row["symbol"] for p in open_positions):
                continue

            exit_idx = i + hold_days
            if exit_idx >= len(dates):
                continue

            cash -= trade_notional
            open_positions.append(
                {
                    "symbol": row["symbol"],
                    "entry_date": date,
                    "exit_idx": exit_idx,
                    "entry_price": row["Close"],
                }
            )

        equity_curve.append(
            {"Date": date, "Equity": cash + len(open_positions) * trade_notional}
        )

    # =========================
    # METRICS
    # =========================

    eq = pd.DataFrame(equity_curve).set_index("Date")
    eq["Peak"] = eq["Equity"].cummax()
    eq["Drawdown"] = (eq["Equity"] - eq["Peak"]) / eq["Peak"]

    trades = pd.DataFrame(trade_log)

    return {
        "trades": int(len(trades)),
        "win_rate": float((trades["return"] > 0).mean()) if len(trades) else 0.0,
        "avg_return": float(trades["return"].mean()) if len(trades) else 0.0,
        "final_equity": float(eq["Equity"].iloc[-1]),
        "max_drawdown": float(eq["Drawdown"].min()),
        "equity_curve": eq.reset_index().to_dict(orient="records"),
        "trade_log": trades.to_dict(orient="records"),
        "equity": eq.reset_index().to_dict(orient="records"),
    }


# =========================
# SCRIPT ENTRY (OPTIONAL)
# =========================

if __name__ == "__main__":
    result = run_event_backtest()
    print("\n===== FINAL MULTI-ALPHA BACKTEST =====")
    print(f"Trades: {result['trades']}")
    print(f"Win rate: {result['win_rate']:.2%}")
    print(f"Avg return / trade: {result['avg_return']:.4f}")
    print(f"Final equity: {result['final_equity']:,.0f}")
    print(f"Max drawdown: {result['max_drawdown']:.2%}")
