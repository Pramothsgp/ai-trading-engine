# NOTE: Score labels currently in use

import pandas as pd
from features.technical import add_technical_features
from features.market_context import add_trend_context
from labeling.labels import create_score_labels
import glob
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

RAW_PATH = "data/raw"
OUT_PATH = "data/processed/cross_sectional_labeled.csv"


def process_single_file(file_path):
    """Process a single CSV file and return the processed DataFrame."""
    try:
        symbol = os.path.basename(file_path).replace(".csv", "")
        print(f"Processing {symbol}...")

        # Handle complex CSV format with merged cells
        df = pd.read_csv(file_path, header=None)
        # Find the first row with actual date data (starts with YYYY-MM-DD)
        date_row = df[df[0].str.contains(r"\d{4}-\d{2}-\d{2}", na=False)].index
        if len(date_row) == 0:
            return None

        start_row = date_row[0]

        # Read from the first data row
        df = pd.read_csv(file_path, header=None, skiprows=start_row)
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
                open_price = float(
                    row[4].split(",")[0] if "," in str(row[4]) else row[4]
                )
                volume = int(row[5].split(",")[0] if "," in str(row[5]) else row[5])

                data_rows.append([date_str, close, high, low, open_price, volume])
            except (ValueError, IndexError):
                continue

        if not data_rows:
            return None

        df = pd.DataFrame(
            data_rows, columns=["Date", "Close", "High", "Low", "Open", "Volume"]
        )

        df["Date"] = pd.to_datetime(df["Date"])
        for c in ["Open", "High", "Low", "Close", "Volume"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        df.dropna(inplace=True)

        df = add_technical_features(df)
        df = add_trend_context(df)

        # ⭐ CREATE SCORE
        df = create_score_labels(df, horizon=5)

        df.dropna(inplace=True)
        df["symbol"] = symbol

        print(f"✓ Completed {symbol}")
        return df

    except Exception as e:
        print(f"✗ Failed {symbol}: {e}")
        return None


if __name__ == "__main__":
    # Get all CSV files to process
    csv_files = glob.glob(f"{RAW_PATH}/*.csv")
    print(f"Found {len(csv_files)} CSV files to process")

    all_dfs = []
    successful_processes = 0
    failed_processes = 0

    # Process files in parallel using 4 threads (adjust based on CPU cores)
    with ThreadPoolExecutor(max_workers=8) as executor:
        # Submit all processing tasks
        future_to_file = {
            executor.submit(process_single_file, file_path): file_path
            for file_path in csv_files
        }

        # Process completed tasks
        for future in as_completed(future_to_file):
            result = future.result()
            if result is not None:
                all_dfs.append(result)
                successful_processes += 1
            else:
                failed_processes += 1

    print(f"\nProcessing Summary:")
    print(f"✓ Successful: {successful_processes}")
    print(f"✗ Failed: {failed_processes}")

    if not all_dfs:
        print("No data to save!")
        exit(1)

    # =========================
    # COMBINE ALL STOCKS
    # =========================
    final_df = pd.concat(all_dfs, ignore_index=True)

    final_df = final_df.sort_values(["Date", "symbol"]).reset_index(drop=True)

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    final_df.to_csv(OUT_PATH, index=False)

    print("Saved:", OUT_PATH)
    print(final_df.columns)
    print(final_df[["symbol", "Date", "score"]].head())
