import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from scipy.stats import spearmanr
from pathlib import Path
from features.ml_features import ML_FEATURES



# # =========================
# # CONFIG
# # =========================

# DATA_PATH = "data/processed/cross_sectional_labeled.csv"
# MODEL_PATH = "models/cross_sectional_xgb.pkl"


# TARGET = "score"  # ✅ CORRECT TARGET

# # =========================
# # LOAD DATA
# # =========================

# df = pd.read_csv(DATA_PATH)
# df["Date"] = pd.to_datetime(df["Date"])
# df = df.sort_values("Date").reset_index(drop=True)

# df = df.dropna(subset=ML_FEATURES + [TARGET])

# X = df[ML_FEATURES]
# y = df[TARGET]

# # =========================
# # TIME-BASED SPLIT
# # =========================

# split = int(len(df) * 0.8)

# X_train, X_test = X.iloc[:split], X.iloc[split:]
# y_train, y_test = y.iloc[:split], y.iloc[split:]

# # =========================
# # MODEL
# # =========================

# model = XGBRegressor(
#     n_estimators=500,
#     max_depth=5,
#     learning_rate=0.05,
#     subsample=0.8,
#     colsample_bytree=0.8,
#     objective="reg:squarederror",
#     random_state=42,
# )

# model.fit(X_train, y_train)

# # =========================
# # EVALUATION (RANK IC)
# # =========================

# y_pred = model.predict(X_test)

# rank_ic, _ = spearmanr(y_test, y_pred)
# print(f"\nSpearman Rank IC: {rank_ic:.4f}")

# test = X_test.copy()
# test["true"] = y_test.values
# test["pred"] = y_pred

# for pct in [90, 95]:
#     cutoff = np.percentile(test["pred"], pct)
#     sel = test[test["pred"] >= cutoff]
#     print(
#         f"Top {100-pct}% | "
#         f"Count={len(sel)} | "
#         f"Avg True Score={sel['true'].mean():.4f}"
#     )

# # =========================
# # SAVE MODEL
# # =========================

# Path("models").mkdir(exist_ok=True)
# joblib.dump(model, MODEL_PATH)

# print(f"\nModel saved → {MODEL_PATH}")


import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from scipy.stats import spearmanr

TARGET = "score"

DATA_PATH = "data/processed/cross_sectional_labeled.csv"
MODEL_PATH = "models/cross_sectional_xgb.pkl"

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv(DATA_PATH)
df = df.sort_values(["Date", "symbol"]).reset_index(drop=True)

# Ensure required columns exist
missing = set(ML_FEATURES + [TARGET]) - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {missing}")

df = df.dropna(subset=ML_FEATURES + [TARGET])

X = df[ML_FEATURES]
y = df[TARGET]

# -------------------------
# TIME-BASED SPLIT
# -------------------------
split = int(len(df) * 0.8)

X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

# -------------------------
# TRAIN MODEL
# -------------------------
model = XGBRegressor(
    n_estimators=500,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)

# -------------------------
# EVALUATION
# -------------------------
y_pred = model.predict(X_test)

rank_corr, _ = spearmanr(y_test, y_pred)
print(f"\nSpearman Rank Correlation: {rank_corr:.4f}")

# Top percentile check
test = X_test.copy()
test["true"] = y_test.values
test["pred"] = y_pred

for pct in [90, 95]:
    cutoff = np.percentile(test["pred"], pct)
    sel = test[test["pred"] >= cutoff]
    print(
        f"Top {100-pct}% | "
        f"Count={len(sel)} | "
        f"Avg True Score={sel['true'].mean():.4f}"
    )

# -------------------------
# SAVE MODEL
# -------------------------
joblib.dump(model, MODEL_PATH)
print(f"\nSaved model to {MODEL_PATH}")
