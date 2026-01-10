import { useState } from "react";
import { AlphaSelector } from "../components/alpha-selector";
import { WalkForwardTable } from "../components/walkforward-table";
import { api } from "../lib/api";
import type { AlphaConfigMap } from "../types";

export default function WalkforwardPage() {
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

  const [walkforwardResult, setWalkforwardResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runWalkforward = async () => {
    setLoading(true);
    try {
      const response = await api.post("/walkforward/run", {
        alphas: alphaConfig,
        ...strategyConfig,
      });
      setWalkforwardResult(response.data);
    } catch (error) {
      console.error("Error running walk-forward analysis:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-2xl font-semibold text-gray-900 mb-6">
          Walk-Forward Analysis
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <AlphaSelector
              alphaConfig={alphaConfig}
              onChange={setAlphaConfig}
            />
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-medium">Strategy Parameters</h3>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
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
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
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
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
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
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
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
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={strategyConfig.use_trend_filter}
                  onChange={(e) =>
                    setStrategyConfig({
                      ...strategyConfig,
                      use_trend_filter: e.target.checked,
                    })
                  }
                  className="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
                <span className="ml-2 text-sm text-gray-700">
                  Use Trend Filter
                </span>
              </label>

              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={strategyConfig.use_vol_filter}
                  onChange={(e) =>
                    setStrategyConfig({
                      ...strategyConfig,
                      use_vol_filter: e.target.checked,
                    })
                  }
                  className="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                />
                <span className="ml-2 text-sm text-gray-700">
                  Use Volatility Filter
                </span>
              </label>
            </div>
          </div>
        </div>

        <div className="mt-6">
          <button
            onClick={runWalkforward}
            disabled={loading}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
          >
            {loading ? "Running..." : "Run Walk-Forward Analysis"}
          </button>
        </div>
      </div>

      {walkforwardResult && <WalkForwardTable rows={walkforwardResult} />}
    </div>
  );
}
