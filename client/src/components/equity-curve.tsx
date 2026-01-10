import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

interface Point {
  date: string;
  equity: number;
  drawdown: number;
}

interface Props {
  data: Point[];
}

export function EquityCurve({ data }: Props) {
  if (!data || data.length === 0) {
    return <div>No equity data</div>;
  }

  return (
    <div className="border rounded-xl p-6 bg-white shadow-sm">
      <h2 className="font-semibold text-lg mb-4">Equity Curve</h2>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />

            <XAxis
              dataKey="date"
              tick={{ fontSize: 12 }}
              tickFormatter={(d) => d.slice(0, 10)}
            />

            <YAxis
              yAxisId="equity"
              tick={{ fontSize: 12 }}
              tickFormatter={(v) => `₹${(v / 1_000_000).toFixed(1)}M`}
            />

            <YAxis
              yAxisId="drawdown"
              orientation="right"
              domain={[-1, 0]}
              tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
              tick={{ fontSize: 12 }}
            />

            <Tooltip
              formatter={(value: number | undefined, name: string) => {
                if (value === undefined) return [0, name];
                if (name === "Equity")
                  return [`₹${value.toLocaleString()}`, "Equity"];
                if (name === "Drawdown")
                  return [`${(value * 100).toFixed(2)}%`, "Drawdown"];
                return value;
              }}
              labelFormatter={(label) => `Date: ${label.slice(0, 10)}`}
            />

            <Legend />

            <Line
              yAxisId="equity"
              type="monotone"
              dataKey="equity"
              name="Equity"
              stroke="#2563eb"
              strokeWidth={2}
              dot={false}
            />

            <Line
              yAxisId="drawdown"
              type="monotone"
              dataKey="drawdown"
              name="Drawdown"
              stroke="#dc2626"
              strokeWidth={1.5}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
