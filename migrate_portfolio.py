import json

TICKERS = {
    "Gold": "GC=F",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Meta": "META",
    "Google": "GOOGL",
    "Tesla": "TSLA"
}

with open("history/portfolio.json", "r") as f:
    portfolio = json.load(f)

updated = 0

for trade in portfolio:

    if "ticker" not in trade:

        trade["ticker"] = TICKERS.get(trade["asset"])

        updated += 1

with open("history/portfolio.json", "w") as f:
    json.dump(portfolio, f, indent=4)

print(f"Updated {updated} trade(s).")
