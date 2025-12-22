import type { AlphaConfigMap } from "../types";
import { Brain, Zap, Target } from "lucide-react";

interface Props {
  alphaConfig: AlphaConfigMap;
  onChange: (config: AlphaConfigMap) => void;
}

export function AlphaSelector({ alphaConfig, onChange }: Props) {
  const updateAlpha = (
    key: string,
    field: "enabled" | "weight",
    value: boolean | number
  ) => {
    onChange({
      ...alphaConfig,
      [key]: {
        ...alphaConfig[key],
        [field]: value,
      },
    });
  };

  const getIcon = (key: string) => {
    switch (key) {
      case "ml":
        return Brain;
      case "momentum":
        return Zap;
      case "breakout":
        return Target;
      default:
        return Brain;
    }
  };

  return (
    <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 space-y-6">
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 bg-linear-to-r from-purple-600 to-indigo-600 rounded-lg flex items-center justify-center">
          <Brain className="w-5 h-5 text-white" />
        </div>
        <h2 className="text-xl font-bold text-gray-900">Alpha Selection</h2>
      </div>

      <div className="space-y-4">
        {Object.entries(alphaConfig).map(([key, cfg]) => {
          const Icon = getIcon(key);
          return (
            <div
              key={key}
              className={`bg-gray-50 rounded-lg p-4 border transition-all duration-200 ${
                cfg.enabled
                  ? "border-indigo-200 bg-indigo-50"
                  : "border-gray-200"
              }`}
            >
              <div className="flex items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div
                    className={`w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-200 ${
                      cfg.enabled ? "bg-indigo-600" : "bg-gray-400"
                    }`}
                  >
                    <Icon className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <span className="font-semibold text-gray-900 capitalize">
                      {key} Alpha
                    </span>
                    <div className="text-xs text-gray-500 mt-1">
                      {cfg.enabled ? "Active" : "Inactive"}
                    </div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={cfg.enabled}
                      onChange={(e) =>
                        updateAlpha(key, "enabled", e.target.checked)
                      }
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                  </label>
                </div>

                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <div className="text-xs text-gray-500 mb-1">Weight</div>
                    <div className="font-semibold text-gray-900">
                      {cfg.weight.toFixed(2)}
                    </div>
                  </div>
                  <div className="relative">
                    <input
                      type="range"
                      min={0}
                      max={1}
                      step={0.05}
                      value={cfg.weight}
                      disabled={!cfg.enabled}
                      onChange={(e) =>
                        updateAlpha(key, "weight", Number(e.target.value))
                      }
                      className={`w-24 h-2 rounded-lg appearance-none cursor-pointer ${
                        cfg.enabled
                          ? "bg-indigo-200 accent-indigo-600"
                          : "bg-gray-200 accent-gray-400"
                      }`}
                    />
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
