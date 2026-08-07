import json
import os

PORTFOLIO_FILE = "history/portfolio.json"


def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=4, default=str)


def load_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        return []

    with open(PORTFOLIO_FILE, "r") as f:
        return json.load(f)
        