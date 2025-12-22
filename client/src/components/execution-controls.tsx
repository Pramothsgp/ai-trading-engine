type Props = {
  transactionCost: number;
  tax: number;
  onChange: (v: { transactionCost: number; tax: number }) => void;
};

export function ExecutionControls({ transactionCost, tax, onChange }: Props) {
  return (
    <div className="border rounded p-4 space-y-4">
      <h2 className="font-semibold">Execution Settings</h2>

      <div>
        <label className="block text-sm">Transaction Cost (% per trade)</label>
        <input
          type="range"
          min={0}
          max={0.01}
          step={0.0005}
          value={transactionCost}
          onChange={(e) =>
            onChange({
              transactionCost: Number(e.target.value),
              tax,
            })
          }
          className="w-full"
        />
        <div className="text-right text-sm">
          {(transactionCost * 100).toFixed(2)}%
        </div>
      </div>

      <div>
        <label className="block text-sm">Tax on Profits (%)</label>
        <input
          type="range"
          min={0}
          max={0.3}
          step={0.01}
          value={tax}
          onChange={(e) =>
            onChange({
              transactionCost,
              tax: Number(e.target.value),
            })
          }
          className="w-full"
        />
        <div className="text-right text-sm">{(tax * 100).toFixed(0)}%</div>
      </div>
    </div>
  );
}
