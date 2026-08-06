import yfinance as yf


def get_market_prices():
    assets = {
        "Gold": "GC=F",
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "NVIDIA": "NVDA",
        "Amazon": "AMZN"
    }

    print("\n==============================")
    print("      LIVE MARKET DATA")
    print("==============================")

    for name, ticker in assets.items():
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="1d")

            if not history.empty:
                price = history["Close"].iloc[-1]
                print(f"{name:<12} {price:.2f}")
            else:
                print(f"{name:<12} No data")
        except Exception as e:
            print(f"{name:<12} Error: {e}")
            