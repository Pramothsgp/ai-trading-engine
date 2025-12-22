from models.walk_forward_backtest import walk_forward_run


def run_walkforward(strategy):
    alpha_config = {k: v.dict() for k, v in strategy.alphas.items()}

    return walk_forward_run(
        alpha_config=alpha_config,
        top_k=strategy.top_k,
        hold_days=strategy.hold_days,
        trade_notional=strategy.trade_notional,
        round_trip_cost=strategy.round_trip_cost,
        no_trade_lookback=strategy.no_trade_lookback,
    )
