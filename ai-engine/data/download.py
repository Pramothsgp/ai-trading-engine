import yfinance as yf
import pandas as pd

def fetch_data(symbol):
    df = yf.download(
        f"{symbol}.NS",
        start="2018-01-01",
        interval="1d",
        auto_adjust=True
    )
    df.dropna(inplace=True)
    return df

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

    # for s in symbols:
        # df = fetch_data(s)
        # df.to_csv(f"data/raw/{s}.csv")
    download_nifty()
