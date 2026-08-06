from ta.volatility import AverageTrueRange


def calculate_risk(data, current_price):
    """
    Calculates ATR, stop loss and take profit.
    """

    high = data["High"]
    low = data["Low"]
    close = data["Close"]

    # Convert DataFrames to Series if needed
    if hasattr(high, "columns"):
        high = high.iloc[:, 0]

    if hasattr(low, "columns"):
        low = low.iloc[:, 0]

    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    atr = AverageTrueRange(
        high=high,
        low=low,
        close=close,
        window=14
    ).average_true_range().iloc[-1]

    stop_loss = current_price - (atr * 2)
    take_profit = current_price + (atr * 3)

    return {
        "atr": round(float(atr), 2),
        "stop_loss": round(float(stop_loss), 2),
        "take_profit": round(float(take_profit), 2)
    }
    