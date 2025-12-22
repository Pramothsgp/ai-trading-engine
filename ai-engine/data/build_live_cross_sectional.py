# NOTE: Live cross-sectional dataset, used for retriving live data for backtesting

import glob
import pandas as pd
from data.live_feature_pipeline import build_live_features

dfs = []

for path in glob.glob("data/raw/*.csv"):
    symbol = path.split("/")[-1].replace(".csv", "")
    df = build_live_features(path)
    df["symbol"] = symbol
    dfs.append(df)

live_df = pd.concat(dfs, ignore_index=True)

live_df.to_csv("data/processed/live_cross_sectional.csv", index=False)
