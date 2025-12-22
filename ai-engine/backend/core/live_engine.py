import pandas as pd
from engine.alpha_engine import build_alpha_score, rank_alpha_score

DATA_PATH = "data/processed/live_cross_sectional.csv"


def generate_live_signals(strategy, top_k):
    df = pd.read_csv(DATA_PATH)
    print(len(df))
    df["Date"] = pd.to_datetime(df["Date"])
    alpha_config = {k: v.dict() for k, v in strategy.alphas.items()}

    df["final_score"] = build_alpha_score(df, alpha_config)
    df["rank"] = rank_alpha_score(df, "final_score")

    latest = df["Date"].max()

    # Get top signals with current prices from the latest available data
    latest_data = df[df["Date"] == latest]
    signals = (
        latest_data.sort_values("final_score", ascending=False)
        .head(top_k)[["symbol", "final_score", "rank", "Close"]]
        .rename(columns={"Close": "current_price"})
        .to_dict(orient="records")
    )

    result = pd.DataFrame(signals)

    # Format datetime for valid filename (replace spaces and colons)
    filename = latest.strftime("%Y-%m-%d_%H-%M-%S")
    result.to_csv(f"data/result/{filename}.csv", index=False)

    # Convert result to list of dicts for API response
    signals_with_prices = result.to_dict(orient="records")

    return {
        "mode": "LIVE",
        "date": str(latest),
        "signals": signals_with_prices,
    }


def generate_date_signals(strategy, top_k, target_date=None):
    df = pd.read_csv(DATA_PATH)
    print(len(df))
    df["Date"] = pd.to_datetime(df["Date"])

    if target_date:
        target_date = pd.to_datetime(target_date)
        available_dates = df["Date"].unique()

        # Find the closest available date on or before the target date
        valid_dates = available_dates[available_dates <= target_date]
        if len(valid_dates) == 0:
            return {"error": f"No data available on or before {target_date.date()}"}

        calculation_date = valid_dates.max()
    else:
        # Use latest available data
        calculation_date = df["Date"].max()

    # Calculate alpha scores for the entire dataset
    alpha_config = {k: v.dict() for k, v in strategy.alphas.items()}
    df["final_score"] = build_alpha_score(df, alpha_config)
    df["rank"] = rank_alpha_score(df, "final_score")

    # Get top signals from the calculation date
    calculation_data = df[df["Date"] == calculation_date]
    signals = (
        calculation_data.sort_values("final_score", ascending=False)
        .head(top_k)[["symbol", "final_score", "rank", "Close"]]
        .rename(columns={"Close": "current_price"})
        .to_dict(orient="records")
    )

    result = pd.DataFrame(signals)

    # If the latest date in CSV is ahead of the target date, add remaining closing prices as columns
    latest_date = df["Date"].max()
    if target_date and latest_date > target_date:
        # Calculate how many days to include (max 10 days or difference between dates)
        days_difference = (latest_date - target_date).days
        days_to_include = min(10, days_difference)

        end_date = target_date + pd.Timedelta(days=days_to_include)

        print(
            f"Latest data is ahead of target date. Adding price columns from {target_date + pd.Timedelta(days=1)} to {min(end_date, latest_date)} (max 10 days)"
        )

        # Get unique symbols from top signals
        top_symbols = [signal["symbol"] for signal in signals]

        # Get data for these symbols from target_date+1 to end_date (limited to available data)
        future_data = df[
            (df["Date"] > target_date)
            & (df["Date"] <= min(end_date, latest_date))
            & (df["symbol"].isin(top_symbols))
        ][["Date", "symbol", "Close"]].copy()

        # Create a dictionary to hold future prices for each symbol
        future_prices = {}
        for _, row in future_data.iterrows():
            symbol = row["symbol"]
            date_str = row["Date"].strftime("%Y-%m-%d")
            price = row["Close"]

            if symbol not in future_prices:
                future_prices[symbol] = {}
            future_prices[symbol][f"price_{date_str}"] = price

        # Add future price columns to the result DataFrame
        for symbol in result["symbol"]:
            if symbol in future_prices:
                for col_name, price in future_prices[symbol].items():
                    result.loc[result["symbol"] == symbol, col_name] = price

    # Remove any Date column that might exist from previous operations
    if "Date" in result.columns:
        result = result.drop(columns=["Date"])

    # Format datetime for valid filename
    filename = calculation_date.strftime("%Y-%m-%d_%H-%M-%S")
    result.to_csv(f"data/result/{filename}.csv", index=False)

    # Convert result back to list of dicts for API response
    signals_with_prices = result.to_dict(orient="records")

    return {
        "mode": "DATE",
        "date": str(calculation_date.date()),
        "target_date": str(target_date.date()) if target_date else None,
        "signals": signals_with_prices,
    }
