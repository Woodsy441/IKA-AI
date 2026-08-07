import yfinance as yf


def update_trade(trade):

    ticker = trade["ticker"]

    data = yf.download(
        ticker,
        period="5d",
        interval="1d",
        progress=False
    )

    if data.empty:
        return trade

    close = data["Close"]

    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    current_price = float(close.iloc[-1])

    trade["current_price"] = round(current_price, 2)

    if trade["action"] == "BUY":
        pnl = (current_price - trade["entry"]) * trade["position_size"]
    else:
        pnl = (trade["entry"] - current_price) * trade["position_size"]

    trade["profit_loss"] = round(pnl, 2)

    # Stop Loss
    if trade["action"] == "BUY" and current_price <= trade["stop_loss"]:
        trade["status"] = "CLOSED"
        trade["close_reason"] = "STOP LOSS"

    # Take Profit
    elif trade["action"] == "BUY" and current_price >= trade["take_profit"]:
        trade["status"] = "CLOSED"
        trade["close_reason"] = "TAKE PROFIT"

    return trade
    