interface WalkForwardRow {
  start: string;
  end: string;
  trades: number;
  avg_return: number;
  win_rate: number;
  final_equity: number;
}

interface Props {
  rows: WalkForwardRow[];
}

export function WalkForwardTable({ rows }: Props) {
  return (
    <div className="border rounded p-4">
      <h2 className="font-semibold text-lg mb-3">Walk-Forward Results</h2>

      <table className="w-full text-sm">
        <thead>
          <tr className="border-b">
            <th>Period</th>
            <th>Trades</th>
            <th>Avg Return</th>
            <th>Win Rate</th>
            <th>Final Equity</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i} className="border-b">
              <td>
                {r.start} → {r.end}
              </td>
              <td>{r.trades}</td>
              <td>{r.avg_return.toFixed(4)}</td>
              <td>{(r.win_rate * 100).toFixed(1)}%</td>
              <td>₹ {r.final_equity.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
