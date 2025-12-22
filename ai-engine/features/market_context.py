def add_trend_context(df):
    df["trend"] = (df["ema_20"] > df["ema_50"]).astype(int)
    df["volatility"] = df["returns"].rolling(14).std()
    return df
