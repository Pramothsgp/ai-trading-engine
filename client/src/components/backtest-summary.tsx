interface Props {
  trades: number;
  winRate: number;
  avgReturn: number;
  finalEquity: number;
  maxDrawdown: number;
}

export function BacktestSummary({
  trades,
  winRate,
  avgReturn,
  finalEquity,
  maxDrawdown,
}: Props) {
  const Metric = ({
    label,
    value,
    trend,
  }: {
    label: string;
    value: string;
    trend?: "up" | "down" | "neutral";
  }) => (
    <div className="bg-white rounded-xl p-4 shadow-md hover:shadow-lg transition-shadow duration-200 border border-gray-100">
      <div className="flex items-center justify-between mb-2">
        <div className="text-xs font-medium text-gray-500 uppercase tracking-wider">
          {label}
        </div>
        {trend && (
          <div
            className={`w-2 h-2 rounded-full ${
              trend === "up"
                ? "bg-green-500"
                : trend === "down"
                ? "bg-red-500"
                : "bg-gray-400"
            }`}
          ></div>
        )}
      </div>
      <div className="text-xl font-bold text-gray-900">{value}</div>
    </div>
  );

  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
      <Metric label="Trades" value={String(trades)} />
      <Metric label="Win Rate" value={`${(winRate * 100).toFixed(1)}%`} />
      <Metric label="Avg Return / Trade" value={avgReturn.toFixed(4)} />
      <Metric
        label="Final Equity"
        value={`₹ ${finalEquity.toLocaleString()}`}
      />
      <Metric
        label="Max Drawdown"
        value={`${(maxDrawdown * 100).toFixed(2)}%`}
      />
    </div>
  );
}
