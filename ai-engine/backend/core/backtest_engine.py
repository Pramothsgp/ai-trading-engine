from backtest.event_backtest import run_event_backtest


def run_backtest(strategy, return_equity=False):
    alpha_config = {k: v.dict() for k, v in strategy.alphas.items()}

    result = run_event_backtest(
        alpha_config=alpha_config,
        top_k=strategy.top_k,
        hold_days=strategy.hold_days,
        trade_notional=strategy.trade_notional,
        round_trip_cost=strategy.round_trip_cost,
        no_trade_lookback=strategy.no_trade_lookback,
    )

    if not return_equity:
        result.pop("equity_curve", None)

    return result
