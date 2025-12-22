import { useState } from "react";
import { AlphaSelector } from "../components/alpha-selector";
import { BacktestSummary } from "../components/backtest-summary";
import { EquityCurve } from "../components/equity-curve";
import { api } from "../lib/api";
import { Play, LineChart } from "lucide-react";
import type { AlphaConfigMap, BacktestResult } from "../types";

export default function BacktestPage() {
  const [alphaConfig, setAlphaConfig] = useState<AlphaConfigMap>({
    ml: { enabled: true, weight: 0.4 },
    momentum: { enabled: true, weight: 0.4 },
    breakout: { enabled: false, weight: 0.2 },
  });

  const [strategyConfig, setStrategyConfig] = useState({
    top_k: 3,
    hold_days: 10,
    trade_notional: 100000,
    round_trip_cost: 0.003,
    use_trend_filter: true,
    use_vol_filter: true,
    no_trade_lookback: 20,
  });

  const [backtestResult, setBacktestResult] = useState<BacktestResult | null>(
    null
  );
  const [loading, setLoading] = useState(false);

  const runBacktest = async () => {
    setLoading(true);
    try {
      const response = await api.post("/backtest/run", {
        alphas: alphaConfig,
        ...strategyConfig,
      });
      setBacktestResult(response.data);
    } catch (error) {
      console.error("Error running backtest:", error);
    } finally {
      setLoading(false);
    }
  };

const getEquityCurve = async () => {
  try {
    const response = await api.post("/backtest/equity", {
      alphas: alphaConfig,
      ...strategyConfig,
    });

    if (response.data?.equity_curve) {
      const normalized = response.data.equity_curve.map((p: any) => ({
        date: p.Date,
        equity: p.Equity,
        drawdown: p.Drawdown,
      }));

      setBacktestResult((prev) =>
        prev
          ? { ...prev, equity_curve: normalized }
          : {
              trades: 0,
              win_rate: 0,
              avg_return: 0,
              final_equity: 0,
              max_drawdown: 0,
              equity_curve: normalized,
            }
      );
    }
  } catch (error) {
    console.error("Error fetching equity curve:", error);
  }
};


  return (
    <div className="space-y-8">
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-8">
        <div className="flex items-center space-x-3 mb-8">
          <div className="w-10 h-10 bg-linear-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
            <LineChart className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">Backtest Engine</h1>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <AlphaSelector
              alphaConfig={alphaConfig}
              onChange={setAlphaConfig}
            />
          </div>

          <div className="space-y-6">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                <Play className="w-4 h-4 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900">
                Strategy Parameters
              </h3>
            </div>

            <div className="bg-gray-50 rounded-lg p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Top K
                  </label>
                  <input
                    type="number"
                    value={strategyConfig.top_k}
                    onChange={(e) =>
                      setStrategyConfig({
                        ...strategyConfig,
                        top_k: parseInt(e.target.value),
                      })
                    }
                    className="block w-full px-4 py-3 rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition-all duration-200"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Hold Days
                  </label>
                  <input
                    type="number"
                    value={strategyConfig.hold_days}
                    onChange={(e) =>
                      setStrategyConfig({
                        ...strategyConfig,
                        hold_days: parseInt(e.target.value),
                      })
                    }
                    className="block w-full px-4 py-3 rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition-all duration-200"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Trade Notional
                  </label>
                  <input
                    type="number"
                    value={strategyConfig.trade_notional}
                    onChange={(e) =>
                      setStrategyConfig({
                        ...strategyConfig,
                        trade_notional: parseFloat(e.target.value),
                      })
                    }
                    className="block w-full px-4 py-3 rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition-all duration-200"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Round Trip Cost
                  </label>
                  <input
                    type="number"
                    step="0.001"
                    value={strategyConfig.round_trip_cost}
                    onChange={(e) =>
                      setStrategyConfig({
                        ...strategyConfig,
                        round_trip_cost: parseFloat(e.target.value),
                      })
                    }
                    className="block w-full px-4 py-3 rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition-all duration-200"
                  />
                </div>
              </div>

              <div className="space-y-3 pt-4">
                <label className="flex items-center p-3 bg-white rounded-lg border border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors duration-200">
                  <input
                    type="checkbox"
                    checked={strategyConfig.use_trend_filter}
                    onChange={(e) =>
                      setStrategyConfig({
                        ...strategyConfig,
                        use_trend_filter: e.target.checked,
                      })
                    }
                    className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                  />
                  <span className="ml-3 text-sm font-medium text-gray-700">
                    Use Trend Filter
                  </span>
                </label>

                <label className="flex items-center p-3 bg-white rounded-lg border border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors duration-200">
                  <input
                    type="checkbox"
                    checked={strategyConfig.use_vol_filter}
                    onChange={(e) =>
                      setStrategyConfig({
                        ...strategyConfig,
                        use_vol_filter: e.target.checked,
                      })
                    }
                    className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                  />
                  <span className="ml-3 text-sm font-medium text-gray-700">
                    Use Volatility Filter
                  </span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8 flex gap-4">
          <button
            onClick={runBacktest}
            disabled={loading}
            className="px-6 py-3 bg-linear-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-lg hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-md hover:shadow-lg flex items-center space-x-2"
          >
            <Play className="w-5 h-5" />
            <span>{loading ? "Running..." : "Run Backtest"}</span>
          </button>

          <button
            onClick={getEquityCurve}
            // onClick={() => console.log("clicked")}
            className="px-6 py-3 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-700 transition-all duration-200 shadow-md hover:shadow-lg flex items-center space-x-2"
          >
            <LineChart className="w-5 h-5" />
            <span>Get Equity Curve</span>
          </button>
        </div>
      </div>

      {backtestResult && (
        <>
          <h1>sdvvkjnkvfnk</h1>
          <BacktestSummary
            trades={backtestResult.trades}
            winRate={backtestResult.win_rate}
            avgReturn={backtestResult.avg_return}
            finalEquity={backtestResult.final_equity}
            maxDrawdown={backtestResult.max_drawdown}
          />

          {backtestResult.equity_curve && (
            <EquityCurve data={backtestResult.equity_curve} />
          )}
        </>
      )}
    </div>
  );
}
