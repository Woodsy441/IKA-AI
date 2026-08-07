import yfinance as yf

from trading.storage import save_portfolio


def update_trade(trade):

    ticker_map = {
        "Gold": "GC=F",
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "NVIDIA": "NVDA",
        "Amazon": "AMZN",
        "Meta": "META",
        "Google": "GOOGL",
        "Tesla": "TSLA"
    }

    ticker = ticker_map.get(trade["asset"])

    if ticker is None:
        return trade

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

    # -------- AUTO CLOSE --------

    if trade["action"] == "BUY":

        if current_price <= trade["stop_loss"]:
            trade["status"] = "STOP LOSS"

        elif current_price >= trade["take_profit"]:
            trade["status"] = "TAKE PROFIT"

    else:

        if current_price >= trade["stop_loss"]:
            trade["status"] = "STOP LOSS"

        elif current_price <= trade["take_profit"]:
            trade["status"] = "TAKE PROFIT"

    return trade
    