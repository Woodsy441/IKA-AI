from config import ACCOUNT_SIZE


class TradingAccount:

    def __init__(self):

        self.starting_balance = ACCOUNT_SIZE
        self.balance = ACCOUNT_SIZE

        self.open_profit = 0.0
        self.closed_profit = 0.0

    def update(self, portfolio):

        self.open_profit = sum(
            trade.get("profit_loss", 0)
            for trade in portfolio
            if trade["status"] == "OPEN"
        )

    def close_trade(self, trade):

        profit = trade.get("profit_loss", 0)

        self.closed_profit += profit
        self.balance += profit

        print(
            f"\nAccount updated: "
            f"{trade['asset']} closed "
            f"({trade['close_reason']}) "
            f"P/L: £{profit:.2f}"
        )

    def show(self):

        equity = self.balance + self.open_profit

        print("\n==============================")
        print("IKA AI ACCOUNT")
        print("==============================")
        print(f"Starting Balance : £{self.starting_balance:,.2f}")
        print(f"Current Balance  : £{self.balance:,.2f}")
        print(f"Open P/L         : £{self.open_profit:,.2f}")
        print(f"Closed P/L       : £{self.closed_profit:,.2f}")
        print(f"Equity           : £{equity:,.2f}")
        print("==============================\n")


account = TradingAccount()
