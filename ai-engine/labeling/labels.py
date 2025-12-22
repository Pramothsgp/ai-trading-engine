import numpy as np


def create_score_labels(df, horizon=5):
    """
    Creates a continuous trade-quality score.

    score = max_future_return - |max_future_drawdown|
    """

    scores = []
    max_returns = []
    max_drawdowns = []

    closes = df["Close"].values

    for i in range(len(df)):
        if i + horizon >= len(df):
            scores.append(np.nan)
            max_returns.append(np.nan)
            max_drawdowns.append(np.nan)
            continue

        entry = closes[i]
        future = closes[i + 1 : i + horizon + 1]

        max_future_return = (future.max() - entry) / entry
        max_future_drawdown = (future.min() - entry) / entry  # negative

        score = max_future_return - abs(max_future_drawdown)

        scores.append(score)
        max_returns.append(max_future_return)
        max_drawdowns.append(max_future_drawdown)

    df["future_max_return"] = max_returns
    df["future_max_drawdown"] = max_drawdowns
    df["score"] = scores

    return df


def create_forward_return(df, horizon=10):
    """
    Forward N-day return as regression target
    """

    future_returns = []

    closes = df["Close"].values

    for i in range(len(df)):
        if i + horizon >= len(df):
            future_returns.append(np.nan)
            continue

        ret = (closes[i + horizon] - closes[i]) / closes[i]
        future_returns.append(ret)

    df["forward_return"] = future_returns
    return df


def create_binary_labels(df, target=0.02, stop=-0.01, horizon=5):
    labels = []

    for i in range(len(df) - horizon):
        entry = df["Close"].iloc[i]
        future = df["Close"].iloc[i + 1 : i + horizon + 1]

        max_gain = (future.max() - entry) / entry
        max_loss = (future.min() - entry) / entry

        if max_gain >= target and max_loss > stop:
            labels.append(1)
        else:
            labels.append(0)

    labels += [0] * horizon
    df["label"] = labels
    return df
