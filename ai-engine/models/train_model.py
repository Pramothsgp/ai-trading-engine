import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, precision_score, confusion_matrix

# ==============================
# CONFIGURATION
# ==============================

DATA_PATH = "data/processed/RELIANCE_processed.csv"
MODEL_PATH = "models/xgb_reliance.pkl"

FEATURES = ["rsi", "ema_20", "ema_50", "atr", "returns", "trend", "volatility"]

TEST_SPLIT_RATIO = 0.20
RANDOM_STATE = 42

# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv(DATA_PATH)
df = df.sort_values("Date").reset_index(drop=True)

X = df[FEATURES]
y = df["label"]

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
# HANDLE CLASS IMBALANCE
# ==============================

pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

# ==============================
# MODEL DEFINITION
# ==============================

model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=pos_weight,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=RANDOM_STATE,
)

# ==============================
# TRAIN
# ==============================

model.fit(X_train, y_train)

# ==============================
# EVALUATION
# ==============================

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

precision = precision_score(y_test, y_pred)

print("\n==============================")
print("MODEL EVALUATION")
print("==============================")
print(f"Precision (Class 1): {precision:.4f}\n")

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

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


thresholds = [0.55, 0.60, 0.65, 0.70, 0.75]

print("\nPrecision by probability threshold:")
for t in thresholds:
    preds = (y_prob >= t).astype(int)
    if preds.sum() < 10:
        continue
    p = precision_score(y_test, preds)
    print(f"Threshold {t:.2f} → Precision: {p:.3f}, Trades: {preds.sum()}")
