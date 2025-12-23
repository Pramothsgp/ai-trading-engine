import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import os


def fetch_data(symbol):
    df = yf.download(
        f"{symbol}.NS", start="2018-01-01", interval="1d", auto_adjust=True
    )
    df.dropna(inplace=True)
    return df


def download_single_symbol(symbol):
    """Download data for a single symbol and save to CSV."""
    try:
        print(f"Downloading {symbol}...")
        df = fetch_data(symbol)
        os.makedirs("data/raw", exist_ok=True)
        df.to_csv(f"data/raw/{symbol}.csv")
        print(f"✓ Completed {symbol}")
        return symbol, True
    except Exception as e:
        print(f"✗ Failed {symbol}: {e}")
        return symbol, False


def download_nifty():
    print("Downloading NIFTY index...")
    nifty = yf.download("^NSEI", start="2010-01-01")
    os.makedirs("data/nifty", exist_ok=True)
    nifty.to_csv("data/nifty/NIFTY.csv")
    print("✓ Completed NIFTY")


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

    print(f"Starting download of {len(symbols)} symbols using 8 threads...")

    # Download symbols in parallel
    successful_downloads = 0
    failed_downloads = 0

    with ThreadPoolExecutor(max_workers=8) as executor:
        # Submit all download tasks
        future_to_symbol = {
            executor.submit(download_single_symbol, symbol): symbol
            for symbol in symbols
        }

        # Process completed downloads
        for future in as_completed(future_to_symbol):
            symbol, success = future.result()
            if success:
                successful_downloads += 1
            else:
                failed_downloads += 1

    print(f"\nDownload Summary:")
    print(f"✓ Successful: {successful_downloads}")
    print(f"✗ Failed: {failed_downloads}")

    # Download NIFTY index
    download_nifty()
