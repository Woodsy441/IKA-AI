import yfinance as yf
from ta.momentum import RSIIndicator


def analyse_asset(name, ticker):
    data = yf.download(ticker, period="3mo", progress=False)

    if data.empty:
        print(f"{name}: No data")
        return

    close = data["Close"]

    rsi = RSIIndicator(close).rsi().iloc[-1]

    print("-" * 40)
    print(name)
    print(f"Current RSI: {rsi:.2f}")

    if rsi > 70:
        print("Status: Overbought")
    elif rsi < 30:
        print("Status: Oversold")
    else:
        print("Status: Neutral")
        