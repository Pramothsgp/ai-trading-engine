# NOTE: features + forward return , currently using score as target so it is not used

import pandas as pd
from features.technical import add_technical_features
from features.market_context import add_trend_context
from labeling.labels import create_forward_return
import glob

all_data = []

for path in glob.glob("data/raw/*.csv"):
    symbol = path.split("/")[-1].replace(".csv", "")
    # Handle complex CSV format with merged cells
    df = pd.read_csv(path, header=None)
    # Find the first row with actual date data (starts with YYYY-MM-DD)
    date_row = df[df[0].str.contains(r"\d{4}-\d{2}-\d{2}", na=False)].index
    if len(date_row) == 0:
        continue
    start_row = date_row[0]

    # Read from the first data row
    df = pd.read_csv(path, header=None, skiprows=start_row)
    # Extract columns - data is in pairs (date,OHLCV)
    data_rows = []
    for i, row in df.iterrows():
        if pd.isna(row[0]) or not str(row[0]).startswith("20"):
            continue
        # Extract date and OHLCV data
        date_str = row[0]
        # OHLCV data is in the next columns, need to parse carefully
        try:
            close = float(row[1].split(",")[0] if "," in str(row[1]) else row[1])
            high = float(row[2].split(",")[0] if "," in str(row[2]) else row[2])
            low = float(row[3].split(",")[0] if "," in str(row[3]) else row[3])
            open_price = float(row[4].split(",")[0] if "," in str(row[4]) else row[4])
            volume = int(row[5].split(",")[0] if "," in str(row[5]) else row[5])

            data_rows.append([date_str, close, high, low, open_price, volume])
        except (ValueError, IndexError):
            continue

    if not data_rows:
        continue

    df = pd.DataFrame(
        data_rows, columns=["Date", "Close", "High", "Low", "Open", "Volume"]
    )
    df["Date"] = pd.to_datetime(df["Date"])

    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(inplace=True)

    # --- features ---
    df = add_technical_features(df)
    df = add_trend_context(df)

    # --- target ---
    df = create_forward_return(df, horizon=10)

    df["symbol"] = symbol

    df.dropna(inplace=True)

    all_data.append(df)

# Combine all stocks
final_df = pd.concat(all_data, ignore_index=True)

final_df.to_csv("data/processed/cross_sectional_dataset.csv", index=False)

print("Final dataset shape:", final_df.shape)
print(final_df.head())
