import subprocess
import sys
import os
import shutil
from datetime import datetime

RAW_DIR = "data/raw"
ARCHIVE_DIR = "data/archive"
LIVE_FILE = "data/processed/live_cross_sectional.csv"


def run(cmd: list[str], desc: str):
    print(f"\n=== {desc} ===")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"FAILED: {desc}")
        sys.exit(1)


def archive_raw_data():
    month = datetime.now().strftime("%Y_%m")
    dest = os.path.join(ARCHIVE_DIR, f"raw_{month}")
    os.makedirs(dest, exist_ok=True)

    for f in os.listdir(RAW_DIR):
        if f.endswith(".csv"):
            shutil.move(
                os.path.join(RAW_DIR, f),
                os.path.join(dest, f),
            )

    print(f"Archived raw data to {dest}")


def cleanup_live_files():
    if os.path.exists(LIVE_FILE):
        os.remove(LIVE_FILE)
        print("Removed old live cross-sectional file")


if __name__ == "__main__":

    # Clean old live snapshot
    cleanup_live_files()

    run(["python", "-m", "data.download"], "Downloading data")
    run(["python", "-m", "data.feature_pipeline"], "Feature engineering")
    run(["python", "-m", "data.label_pipeline"], "Label generation")
    run(["python", "-m", "data.build_cross_sectional_dataset"], "Build CSD")
    run(["python", "-m", "scripts.train_ml_alpha_xgb"], "Train ML model")
    run(["python", "-m", "data.build_live_cross_sectional"], "Build LIVE CSD")

    # Archive raw CSVs (optional daily / weekly)
    # archive_raw_data()

    print("\n✅ PIPELINE COMPLETED & CLEANED")

# export PYTHONPATH=$(pwd)   
# uvicorn backend.main:app --reload
