import { useState } from "react";
import { api } from "../lib/api";
import { AlphaSelector } from "../components/alpha-selector";
import { SignalsTable } from "../components/signals-table";
import { Play, Calendar, TrendingUp } from "lucide-react";
import type { AlphaConfigMap } from "../types";

export default function Dashboard() {
  const [alphaConfig, setAlphaConfig] = useState<AlphaConfigMap>({
    ml: { enabled: true, weight: 0.4 },
    momentum: { enabled: true, weight: 0.4 },
    breakout: { enabled: false, weight: 0.2 },
  });

  const [signals, setSignals] = useState<any[]>([]);
  const [date, setDate] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  const [loading, setLoading] = useState(false);
  const [rowCount, setRowCount] = useState(5);
  const [minPrice, setMinPrice] = useState(0);
  const [minVolume, setMinVolume] = useState(0);

  const runLive = async () => {
    setLoading(true);

    const payload = {
      alphas: alphaConfig,
    };

    try {
      const res = await api.post(`/signals/live?top_k=${rowCount}&min_price=${minPrice}&min_volume=${minVolume}`, payload);
      setSignals(res.data.signals);
      setDate(res.data.date);
    } catch (error) {
      console.error("Error running live signals:", error);
    } finally {
      setLoading(false);
    }
  };

  const runWithDate = async () => {
    setLoading(true);

    const payload = {
      alphas: alphaConfig,
    };

    const params = selectedDate
      ? { date: selectedDate, top_k: rowCount, min_price: minPrice, min_volume: minVolume }
      : { top_k: rowCount, min_price: minPrice, min_volume: minVolume };

    try {
      const res = await api.post("/signals/date", payload, { params });
      setSignals(res.data.signals);
      setDate(res.data.date);
    } catch (error) {
      console.error("Error running signals with date:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center space-x-4">
        <div className="w-12 h-12 bg-linear-to-r from-green-600 to-emerald-600 rounded-xl flex items-center justify-center">
          <TrendingUp className="w-7 h-7 text-white" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Multi-Alpha Trading Dashboard
          </h1>
          <p className="text-gray-600 mt-1">
            Real-time trading signals and alpha strategy analysis
          </p>
        </div>
      </div>

      <AlphaSelector alphaConfig={alphaConfig} onChange={setAlphaConfig} />

      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Number of Signals to Generate
          </label>
          <div className="flex items-center space-x-3">
            <input
              type="number"
              min="1"
              max="50"
              value={rowCount}
              onChange={(e) =>
                setRowCount(
                  Math.max(1, Math.min(50, parseInt(e.target.value) || 5))
                )
              }
              className="w-24 px-3 py-2 rounded-lg border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition-all duration-200"
              placeholder="Rows"
            />
            <span className="text-sm text-gray-500">
              Generate top {rowCount} trading signals (max 50)
            </span>
          </div>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            Filters
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-600 mb-1">
                Minimum Price (₹)
              </label>
              <input
                type="number"
                min="0"
                step="0.01"
                value={minPrice}
                onChange={(e) => setMinPrice(parseFloat(e.target.value) || 0)}
                className="w-full px-3 py-2 rounded-lg border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition-all duration-200"
                placeholder="0"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">
                Minimum Volume
              </label>
              <input
                type="number"
                min="0"
                value={minVolume}
                onChange={(e) => setMinVolume(parseInt(e.target.value) || 0)}
                className="w-full px-3 py-2 rounded-lg border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition-all duration-200"
                placeholder="0"
              />
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Filter stocks by minimum price and trading volume. Set to 0 to disable filters.
          </p>
        </div>

        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900">Signal Generation</h2>
          {loading && (
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
              <div
                className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
                style={{ animationDelay: "0.1s" }}
              ></div>
              <div
                className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
                style={{ animationDelay: "0.2s" }}
              ></div>
              <span className="text-sm text-gray-600 ml-2">Processing...</span>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            <button
              onClick={runLive}
              disabled={loading}
              className="w-full px-6 py-4 bg-linear-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-xl hover:from-green-700 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-md hover:shadow-lg flex items-center justify-center space-x-3"
            >
              <Play className="w-5 h-5" />
              <span>
                {loading ? "Running Live Analysis..." : "Run Live Signals"}
              </span>
            </button>
            <p className="text-sm text-gray-500 text-center">
              Generate signals using current market data
            </p>
          </div>

          <div className="space-y-4">
            <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                <Calendar className="w-4 h-4 inline mr-2" />
                Historical Analysis (Optional)
              </label>
              <div className="flex gap-3">
                <input
                  type="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  className="flex-1 px-4 py-3 rounded-lg border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition-all duration-200"
                  placeholder="Select date"
                />
                <button
                  onClick={runWithDate}
                  disabled={loading}
                  className="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-md hover:shadow-lg flex items-center space-x-2"
                >
                  <Calendar className="w-4 h-4" />
                  <span>{loading ? "Running..." : "Analyze"}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {signals.length > 0 && (
        <div className="animate-fade-in">
          <SignalsTable signals={signals} date={date} />
        </div>
      )}

      {signals.length === 0 && !loading && (
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-12 text-center">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <TrendingUp className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            No Signals Generated
          </h3>
          <p className="text-gray-600">
            Configure your alpha strategies and run signal generation to see
            results.
          </p>
        </div>
      )}
    </div>
  );
}
