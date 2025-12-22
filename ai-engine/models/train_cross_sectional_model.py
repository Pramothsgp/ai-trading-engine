import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from scipy.stats import spearmanr

FEATURES = ["rsi", "ema_20", "ema_50", "atr", "returns", "trend", "volatility"]

df = pd.read_csv("data/processed/cross_sectional_dataset.csv")
df = df.sort_values("Date").reset_index(drop=True)

X = df[FEATURES]
y = df["forward_return"]

# Time-based split
split = int(len(df) * 0.8)

X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

model = XGBRegressor(
    n_estimators=500,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

rank_corr, _ = spearmanr(y_test, y_pred)

print("\nSpearman Rank Correlation:", rank_corr)

# Top-percentile evaluation
test = X_test.copy()
test["true"] = y_test.values
test["pred"] = y_pred

for pct in [90, 95]:
    cutoff = np.percentile(test["pred"], pct)
    sel = test[test["pred"] >= cutoff]
    print(
        f"Top {100-pct}% | "
        f"Count={len(sel)} | "
        f"Avg Forward Return={sel['true'].mean():.4f}"
    )

joblib.dump(model, "models/cross_sectional_xgb.pkl")
