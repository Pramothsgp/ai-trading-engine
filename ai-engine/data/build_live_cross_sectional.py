# NOTE: Live cross-sectional dataset, used for retriving live data for backtesting

import glob
import pandas as pd
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from data.live_feature_pipeline import build_live_features

# Load environment variables
load_dotenv()

# Get number of workers from environment
MAX_WORKERS = int(os.getenv("DATA_MAX_WORKERS", "4"))
THREAD_SLEEP = float(os.getenv("DATA_THREAD_SLEEP", "0.1"))

def process_file(path, sleep_time=0):
    """Process a single file with optional sleep"""
    if sleep_time > 0:
        time.sleep(sleep_time)
    
    try:
        symbol = path.split("/")[-1].replace(".csv", "")
        df = build_live_features(path)
        df["symbol"] = symbol
        return df
    except Exception as e:
        print(f"❌ Error processing {path}: {e}")
        return None

if __name__ == "__main__":
    files = glob.glob("data/raw/*.csv")
    print(f"🚀 Processing {len(files)} files with {MAX_WORKERS} workers...")
    
    dfs = []
    success_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all processing tasks with staggered sleep
        futures = {
            executor.submit(process_file, path, THREAD_SLEEP): path 
            for i, path in enumerate(files)
        }
        
        # Process completed tasks
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                dfs.append(result)
                success_count += 1
                if success_count % 50 == 0:
                    print(f"✅ Processed {success_count}/{len(files)} files...")
    
    print(f"\n✅ Processing complete: {success_count}/{len(files)} files")
    
    live_df = pd.concat(dfs, ignore_index=True)

    live_df.to_csv("data/processed/live_cross_sectional.csv", index=False)
