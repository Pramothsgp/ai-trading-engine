import pandas as pd
import joblib

MODEL_PATH = "models/xgb_reliance.pkl"
FEATURES = ["rsi", "ema_20", "ema_50", "atr", "returns", "trend", "volatility"]

THRESHOLD = 0.70  # this is the key

model = joblib.load(MODEL_PATH)


def generate_signal(row):
    X = row[FEATURES].values.reshape(1, -1)
    prob = model.predict_proba(X)[0, 1]

    if prob >= THRESHOLD:
        return "BUY", prob
    return "NO_TRADE", prob
