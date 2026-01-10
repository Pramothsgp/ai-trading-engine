import { type AlphaConfigMap } from "../types";

type Props = {
  config: AlphaConfigMap;
  onChange: (cfg: AlphaConfigMap) => void;
};

export function AlphaControls({ config, onChange }: Props) {
  const update = (key: string, field: string, value: any) => {
    onChange({
      ...config,
      [key]: {
        ...config[key],
        [field]: value,
      },
    });
  };

  return (
    <div className="space-y-4">
      {Object.entries(config).map(([key, cfg]) => (
        <div key={key} className="border rounded p-4 flex items-center gap-4">
          <input
            type="checkbox"
            checked={cfg.enabled}
            onChange={(e) => update(key, "enabled", e.target.checked)}
          />

          <div className="w-32 font-semibold capitalize">{key}</div>

          <input
            type="range"
            min={0}
            max={1}
            step={0.05}
            disabled={!cfg.enabled}
            value={cfg.weight}
            onChange={(e) => update(key, "weight", Number(e.target.value))}
            className="flex-1"
          />

          <div className="w-16 text-right">{cfg.weight.toFixed(2)}</div>
        </div>
      ))}
    </div>
  );
}
