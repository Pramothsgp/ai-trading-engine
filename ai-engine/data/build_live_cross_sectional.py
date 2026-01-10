# NOTE: Live cross-sectional dataset, used for retriving live data for backtesting

import glob
import pandas as pd
from data.live_feature_pipeline import build_live_features

dfs = []

for path in glob.glob("data/raw/*.csv"):
    try:
        symbol = path.split("/")[-1].replace(".csv", "")
        print("Processing:", symbol)
        df = build_live_features(path)
        df["symbol"] = symbol
        dfs.append(df)
    except Exception as e:
        print(f"Error processing {path}: {e}")
        continue

live_df = pd.concat(dfs, ignore_index=True)

live_df.to_csv("data/processed/live_cross_sectional.csv", index=False)
