# NOTE: Score labels currently in use

import pandas as pd
from features.technical import add_technical_features
from features.market_context import add_trend_context
from labeling.labels import create_score_labels
import glob
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get number of workers from environment
MAX_WORKERS = int(os.getenv("DATA_MAX_WORKERS", "4"))
THREAD_SLEEP = float(os.getenv("DATA_THREAD_SLEEP", "0.1"))

RAW_PATH = "data/raw"
OUT_PATH = "data/processed/cross_sectional_labeled.csv"

def process_file(file, sleep_time=0):
    """Process a single file with optional sleep"""
    if sleep_time > 0:
        time.sleep(sleep_time)
    
    symbol = os.path.basename(file).replace(".csv", "")
    # Handle complex CSV format with merged cells
    try:
        df = pd.read_csv(file, header=None)
        # Find the first row with actual date data (starts with YYYY-MM-DD)
        date_row = df[df[0].str.contains(r"\d{4}-\d{2}-\d{2}", na=False)].index
        if len(date_row) == 0:
            return None
        start_row = date_row[0]

        # Read from the first data row
        df = pd.read_csv(file, header=None, skiprows=start_row)
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
                return None

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

        return df
    except Exception as e:
        print(f"❌ Error processing {file}: {e}")
        return None

if __name__ == "__main__":
    files = glob.glob(f"{RAW_PATH}/*.csv")
    print(f"🚀 Processing {len(files)} files with {MAX_WORKERS} workers...")
    
    all_dfs = []
    success_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all processing tasks with staggered sleep
        futures = {
            executor.submit(process_file, file, THREAD_SLEEP): file 
            for i, file in enumerate(files)
        }
        
        # Process completed tasks
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                all_dfs.append(result)
                success_count += 1
                if success_count % 50 == 0:
                    print(f"✅ Processed {success_count}/{len(files)} files...")
    
    print(f"\n✅ Processing complete: {success_count}/{len(files)} files")
    
    # =========================
    # COMBINE ALL STOCKS
    # =========================
    final_df = pd.concat(all_dfs, ignore_index=True)

    final_df = final_df.sort_values(["Date", "symbol"]).reset_index(drop=True)

    final_df.to_csv(OUT_PATH, index=False)

    print("Saved:", OUT_PATH)
    print(final_df.columns)
    print(final_df[["symbol", "Date", "score"]].head())
