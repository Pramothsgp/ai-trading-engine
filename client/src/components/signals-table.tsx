import { TrendingUp, TrendingDown, Minus } from "lucide-react";

interface Signal {
  symbol: string;
  final_score: number;
  rank?: number;
  current_price?: number;
  max_change_pct?: number;
  min_change_pct?: number;
  [key: `price_${string}`]: number | undefined;
}

interface Props {
  signals: Signal[];
  date?: string;
}

export function SignalsTable({ signals, date }: Props) {
  if (!signals || signals.length === 0) {
    return (
      <div className="bg-white rounded-xl p-8 shadow-lg border border-gray-100 text-center">
        <Minus className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <div className="text-gray-500 font-medium">No signals available</div>
      </div>
    );
  }

  // Extract price columns (current_price and price_YYYY-MM-DD columns)
  const priceColumns = new Set<string>();
  signals.forEach((signal) => {
    if (signal.current_price !== undefined) {
      priceColumns.add("current_price");
    }
    Object.keys(signal).forEach((key) => {
      if (key.startsWith("price_")) {
        priceColumns.add(key);
      }
    });
  });

  const sortedPriceColumns = Array.from(priceColumns).sort();

  // Check if we have max/min change data (historical analysis)
  const hasChangeData = signals.some((s) => s.max_change_pct !== undefined);

  const formatChangePct = (value?: number) => {
    if (value === undefined || value === null) return "-";
    const prefix = value > 0 ? "+" : "";
    return `${prefix}${value.toFixed(2)}%`;
  };

  const getChangeColor = (value?: number) => {
    if (value === undefined || value === null) return "text-gray-500";
    if (value > 0) return "text-green-600";
    if (value < 0) return "text-red-600";
    return "text-gray-500";
  };

  const getTrendIcon = (score: number) => {
    if (score > 0.5) return <TrendingUp className="w-4 h-4 text-green-500" />;
    if (score < 0) return <TrendingDown className="w-4 h-4 text-red-500" />;
    return <Minus className="w-4 h-4 text-gray-400" />;
  };

  const getScoreColor = (score: number) => {
    if (score > 0.5) return "text-green-600 font-semibold";
    if (score < 0) return "text-red-600 font-semibold";
    return "text-gray-600";
  };

  const formatPrice = (price: number | undefined) => {
    if (price === undefined || price === null) return "-";
    return `₹${price.toFixed(2)}`;
  };

  const formatDate = (dateStr: string) => {
    // Convert YYYY-MM-DD to DD/MM/YYYY
    if (!dateStr) return dateStr;
    const match = dateStr.match(/^(\d{4})-(\d{2})-(\d{2})/);
    if (match) {
      return `${match[3]}/${match[2]}/${match[1]}`;
    }
    return dateStr;
  };

  const formatColumnHeader = (column: string) => {
    if (column === "current_price") return "Current Price";
    if (column.startsWith("price_")) {
      const dateStr = column.replace("price_", "");
      return formatDate(dateStr);
    }
    return column;
  };

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
      <div className="bg-linear-to-r from-indigo-50 to-purple-50 px-6 py-4 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <h2 className="text-xl font-bold text-gray-900">Trading Signals</h2>
          </div>
          {date && (
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-600 font-medium">
                {formatDate(date)}
              </span>
            </div>
          )}
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Rank
              </th>
              <th className="text-left px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Symbol
              </th>
              <th className="text-right px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Score
              </th>
              <th className="text-center px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Trend
              </th>
              {hasChangeData && (
                <>
                  <th className="text-right px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Max ↑
                  </th>
                  <th className="text-right px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Min ↓
                  </th>
                </>
              )}
              {sortedPriceColumns.map((column) => (
                <th
                  key={column}
                  className="text-right px-6 py-4 text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {formatColumnHeader(column)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {signals.map((s, i) => (
              <tr
                key={s.symbol}
                className="hover:bg-gray-50 transition-colors duration-150"
              >
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                        (s.rank ?? i + 1) <= 3
                          ? "bg-indigo-100 text-indigo-800"
                          : "bg-gray-100 text-gray-600"
                      }`}
                    >
                      {s.rank ?? i + 1}
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-bold text-gray-900">
                    {s.symbol}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right">
                  <div className={`text-sm ${getScoreColor(s.final_score)}`}>
                    {s.final_score.toFixed(4)}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-center">
                  <div className="flex justify-center">
                    {getTrendIcon(s.final_score)}
                  </div>
                </td>
                {hasChangeData && (
                  <>
                    <td className="px-6 py-4 whitespace-nowrap text-right">
                      <span
                        className={`text-sm font-mono font-semibold ${getChangeColor(
                          s.max_change_pct
                        )}`}
                      >
                        {formatChangePct(s.max_change_pct)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right">
                      <span
                        className={`text-sm font-mono font-semibold ${getChangeColor(
                          s.min_change_pct
                        )}`}
                      >
                        {formatChangePct(s.min_change_pct)}
                      </span>
                    </td>
                  </>
                )}
                {sortedPriceColumns.map((column) => (
                  <td
                    key={column}
                    className="px-6 py-4 whitespace-nowrap text-right"
                  >
                    <div className="text-sm text-gray-900 font-mono">
                      {formatPrice(s[column as keyof typeof s] as number)}
                    </div>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
