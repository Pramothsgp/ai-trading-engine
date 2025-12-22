import pandas as pd
import numpy as np
import joblib

from xgboost import XGBRegressor
from scipy.stats import spearmanr

# ==============================
# CONFIG
# ==============================

DATA_PATH = "data/processed/RELIANCE_scored.csv"
MODEL_PATH = "models/xgb_reliance_regressor.pkl"

FEATURES = ["rsi", "ema_20", "ema_50", "atr", "returns", "trend", "volatility"]

TEST_SPLIT_RATIO = 0.20
RANDOM_STATE = 42

# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv(DATA_PATH)
df = df.sort_values("Date").reset_index(drop=True)

X = df[FEATURES]
y = df["score"]

# ==============================
# TIME-SERIES SPLIT
# ==============================

split_idx = int(len(df) * (1 - TEST_SPLIT_RATIO))

X_train = X.iloc[:split_idx]
y_train = y.iloc[:split_idx]

X_test = X.iloc[split_idx:]
y_test = y.iloc[split_idx:]

print(f"Train samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")

# ==============================
# MODEL
# ==============================

model = XGBRegressor(
    n_estimators=400,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=RANDOM_STATE,
)

# ==============================
# TRAIN
# ==============================

model.fit(X_train, y_train)

# ==============================
# EVALUATION — RANKING QUALITY
# ==============================

y_pred = model.predict(X_test)

# Spearman rank correlation
rank_corr, _ = spearmanr(y_test, y_pred)

print("\n==============================")
print("REGRESSION MODEL EVALUATION")
print("==============================")
print(f"Spearman Rank Correlation: {rank_corr:.4f}")

# ==============================
# TOP-PERCENTILE ANALYSIS
# ==============================

test_results = X_test.copy()
test_results["true_score"] = y_test.values
test_results["pred_score"] = y_pred

for pct in [90, 95, 97]:
    cutoff = np.percentile(test_results["pred_score"], pct)
    selected = test_results[test_results["pred_score"] >= cutoff]

    avg_true_score = selected["true_score"].mean()
    print(
        f"Top {100-pct}% trades → "
        f"Count: {len(selected)}, "
        f"Avg True Score: {avg_true_score:.4f}"
    )

# ==============================
# FEATURE IMPORTANCE
# ==============================

importance = pd.Series(model.feature_importances_, index=FEATURES).sort_values(
    ascending=False
)

print("\nFeature Importance:")
print(importance)

# ==============================
# SAVE MODEL
# ==============================

joblib.dump(model, MODEL_PATH)
print(f"\nModel saved to: {MODEL_PATH}")
