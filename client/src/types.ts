export type AlphaConfig = {
  enabled: boolean;
  weight: number;
};

export type AlphaConfigMap = Record<string, AlphaConfig>;

export type StrategyConfig = {
  alphas: AlphaConfigMap;
  top_k: number;
  hold_days: number;
  trade_notional: number;
  round_trip_cost: number;
  use_trend_filter: boolean;
  use_vol_filter: boolean;
  no_trade_lookback: number;
};

export type Signal = {
  symbol: string;
  rank: number;
  final_score: number;
  net_return?: number;
};

export type BacktestResult = {
  trades: number;
  win_rate: number;
  avg_return: number;
  final_equity: number;
  max_drawdown: number;
  equity_curve: Array<{ date: string; equity: number; drawdown: number }>;
};

export type Strategy = {
  id: string;
  name: string;
  alphas: AlphaConfigMap;
  execution: {
    top_k: number;
    hold_days: number;
    round_trip_cost: number;
    no_trade_lookback: number;
  };
};

export type Alpha = {
  key: string;
  name: string;
  requires_model: boolean;
};
