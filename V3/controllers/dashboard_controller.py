"""
Dashboard Controller

Provides live dashboard data to the UI.
"""

from pathlib import Path
import sys

# -------------------------------------------------
# Add the original IKA AI project to Python's path
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from trading.account import account
from trading.storage import load_portfolio


class DashboardController:

    def __init__(self):
        self.portfolio = []
        self.refresh()

    def refresh(self):

        self.portfolio = load_portfolio()

        account.update(self.portfolio)

        # ------------------------------
        # Debug (temporary)
        # ------------------------------

        print("\n========== DASHBOARD ==========")
        print("Balance      :", account.balance)
        print("Open Profit  :", account.open_profit)
        print("Open Trades  :", len(self.portfolio))
        print("Portfolio    :", self.portfolio)
        print("===============================\n")

    def get_balance(self):
        return account.balance

    def get_equity(self):
        return account.balance + account.open_profit

    def get_open_profit(self):
        return account.open_profit

    def get_open_trades(self):

        return sum(
            1
            for trade in self.portfolio
            if trade.get("status") == "OPEN"
        )
        