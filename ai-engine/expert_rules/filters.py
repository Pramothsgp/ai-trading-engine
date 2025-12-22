def expert_filter(row, prediction, prob):
    if row["trend"] == 0:
        return "NO_TRADE"
    if row["volatility"] < 0.01:
        return "NO_TRADE"
    if prob < 0.65:
        return "NO_TRADE"
    return "BUY"
