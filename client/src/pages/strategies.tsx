import { useState, useEffect } from "react";
import { api } from "../lib/api";
import type { Strategy, Alpha } from "../types";

export default function StrategiesPage() {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [alphas, setAlphas] = useState<Alpha[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [strategiesRes, alphasRes] = await Promise.all([
          api.get("/strategies"),
          api.get("/alphas"),
        ]);

        setStrategies(strategiesRes.data.strategies || []);
        setAlphas(alphasRes.data.alphas || []);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-gray-600">Loading strategies...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <h1 className="text-2xl font-semibold text-gray-900 mb-6">
          Strategy Templates
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {strategies.map((strategy) => (
            <div
              key={strategy.id}
              className="border rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <h3 className="font-semibold text-lg mb-2">{strategy.name}</h3>
              <div className="space-y-2">
                <div className="text-sm text-gray-600">
                  <span className="font-medium">ID:</span> {strategy.id}
                </div>

                <div className="text-sm">
                  <span className="font-medium">Alphas:</span>
                  <ul className="mt-1 space-y-1">
                    {Object.entries(strategy.alphas).map(([key, config]) => (
                      <li key={key} className="flex justify-between">
                        <span className="capitalize">{key}:</span>
                        <span>
                          {config.enabled
                            ? `${config.weight.toFixed(2)}`
                            : "disabled"}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="text-sm text-gray-600 space-y-1">
                  <div>Top K: {strategy.execution.top_k}</div>
                  <div>Hold Days: {strategy.execution.hold_days}</div>
                  <div>
                    Cost:{" "}
                    {(strategy.execution.round_trip_cost * 100).toFixed(2)}%
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Available Alpha Strategies
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {alphas.map((alpha) => (
            <div key={alpha.key} className="border rounded p-4">
              <h3 className="font-medium">{alpha.name}</h3>
              <p className="text-sm text-gray-600 mt-1">Key: {alpha.key}</p>
              <div className="mt-2">
                <span
                  className={`inline-flex px-2 py-1 text-xs rounded ${
                    alpha.requires_model
                      ? "bg-yellow-100 text-yellow-800"
                      : "bg-green-100 text-green-800"
                  }`}
                >
                  {alpha.requires_model ? "Requires Model" : "Ready to Use"}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
