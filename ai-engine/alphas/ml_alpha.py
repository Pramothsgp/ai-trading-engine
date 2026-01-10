import pandas as pd
import joblib
from features.ml_features import ML_FEATURES

class MLAlpha:

    def __init__(self, model_path="models/cross_sectional_xgb.pkl"):
        self.model = joblib.load(model_path)
        self.FEATURES = ML_FEATURES

    def compute(self, df, mode="backtest"):
        missing = [c for c in self.FEATURES if c not in df.columns]
        if missing:
            raise ValueError(f"Missing ML features: {missing}")

        preds = self.model.predict(df[self.FEATURES])

        # IMPORTANT: return raw prediction (ranking happens later)
        return pd.Series(preds, index=df.index)
