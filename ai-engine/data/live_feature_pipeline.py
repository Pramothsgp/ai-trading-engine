import pandas as pd
from features.technical import add_technical_features
from features.market_context import add_trend_context


def build_live_features(raw_path):
    # Handle complex CSV format with merged cells
    df = pd.read_csv(raw_path, header=None)
    # Find the first row with actual date data (starts with YYYY-MM-DD)
    date_row = df[df[0].str.contains(r"\d{4}-\d{2}-\d{2}", na=False)].index
    if len(date_row) == 0:
        raise ValueError(f"No valid data found in {raw_path}")
    start_row = date_row[0]

    # Read from the first data row
    df = pd.read_csv(raw_path, header=None, skiprows=start_row)
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
        raise ValueError(f"No valid data rows found in {raw_path}")

    df = pd.DataFrame(
        data_rows, columns=["Date", "Close", "High", "Low", "Open", "Volume"]
    )

    df["Date"] = pd.to_datetime(df["Date"])
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(inplace=True)

    df = add_technical_features(df)
    df = add_trend_context(df)

    df.dropna(inplace=True)

    return df
