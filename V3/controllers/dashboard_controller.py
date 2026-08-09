"""
IKA AI v3
Dashboard Controller

Connects the dashboard UI to the paper-trading engine.
"""

from pathlib import Path
import sys


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# TRADING ENGINE
# ============================================================

from trading.account import account
from trading.storage import load_portfolio


class DashboardController:

    def __init__(self):

        self.portfolio = []

        self.refresh()

    # ========================================================
    # Refresh account / portfolio data
    # ========================================================

    def refresh(self):

        self.portfolio = load_portfolio()

        account.update(self.portfolio)

    # ========================================================
    # Account information
    # ========================================================

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

    # ========================================================
    # Open positions
    # ========================================================

    def get_open_positions(self):

        return [
            trade
            for trade in self.portfolio
            if trade.get("status") == "OPEN"
        ]
        