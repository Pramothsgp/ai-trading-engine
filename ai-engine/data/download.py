import yfinance as yf
import pandas as pd
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get number of workers from environment
MAX_WORKERS = int(os.getenv("DATA_MAX_WORKERS", "4"))
THREAD_SLEEP = float(os.getenv("DATA_THREAD_SLEEP", "0.1"))

def fetch_data(symbol, sleep_time=0):
    """Fetch data for a single symbol with optional sleep"""
    if sleep_time > 0:
        time.sleep(sleep_time)
    # print("Downloading:", symbol)
    try:
        df = yf.download(
            f"{symbol}.NS",
            start="2018-01-01",
            interval="1d",
            auto_adjust=True,
            progress=False
        )
        df.dropna(inplace=True)
        return symbol, df, None
    except Exception as e:
        return symbol, None, str(e)

def download_nifty():
    nifty = yf.download("^NSEI", start="2010-01-01")
    nifty.to_csv("data/nifty/NIFTY.csv")

if __name__ == "__main__":
    symbols = [
        "RELIANCE",
        "TCS",
        "INFY",
        "HDFCBANK",
        "ICICIBANK",
        "LT",
        "AXISBANK",
        "SBIN",
        "ITC",
        "HINDUNILVR",
        "BEL",
        "COFORGE",
        "SHRIRAMFIN",
        "BIOCON",
        "JIOFIN",
        "TITAN",
        "JKCEMENT",
        "MUTHOOTFIN",
        "PRESTIGE",
        "ANGELONE",
        "BRITANNIA",
        "NITINSPIN",
        "KSL",
        "GODFRYPHLP",
        "BSE",
        "INDOTHAI",
        # NIFTY 50 Stocks (added)
        "ADANIENT",
        "ADANIPORTS",
        "APOLLOHOSP",
        "ASIANPAINT",
        "BAJAJ-AUTO",
        "BAJFINANCE",
        "BAJAJFINSV",
        "BHARTIARTL",
        "COALINDIA",
        "CIPLA",
        "EICHERMOT",
        "GRASIM",
        "HCLTECH",
        "HDFCLIFE",
        "HINDALCO",
        "INDIGO",
        "KOTAKBANK",
        "M&M",
        "MARUTI",
        "MAXHEALTH",
        "NESTLEIND",
        "NTPC",
        "ONGC",
        "POWERGRID",
        "SBILIFE",
        "SUNPHARMA",
        "TATACONSUM",
        "TATAMOTORS",
        "TATASTEEL",
        "TECHM",
        "TRENT",
        "ULTRACEMCO",
        "WIPRO",
    ]

    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

    # Read CSV
    df = pd.read_csv(url)

    # Extract SYMBOL column
    symbols = df["SYMBOL"].dropna().unique().tolist()
    
    print(f"🚀 Downloading {len(symbols)} symbols with {MAX_WORKERS} workers...")
    
    # Download with multithreading
    success_count = 0
    error_count = 0
    os.makedirs("data/raw", exist_ok=True)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all download tasks with staggered sleep
        futures = {
            executor.submit(fetch_data, symbol, THREAD_SLEEP): symbol 
            for i, symbol in enumerate(symbols)
        }
        
        # Process completed downloads
        for future in as_completed(futures):
            symbol, data, error = future.result()
            if error:
                print(f"❌ Error downloading {symbol}: {error}")
                error_count += 1
            elif data is not None and not data.empty:
                data.to_csv(f"data/raw/{symbol}.csv")
                success_count += 1
                if success_count % 50 == 0:
                    print(f"✅ Downloaded {success_count}/{len(symbols)} symbols...")
            else:
                error_count += 1
    
    print(f"\n✅ Download complete: {success_count} success, {error_count} errors")
    download_nifty()
