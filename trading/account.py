from config import ACCOUNT_SIZE


class TradingAccount:

    def __init__(self):

        self.starting_balance = ACCOUNT_SIZE
        self.balance = ACCOUNT_SIZE

        self.open_profit = 0.0
        self.closed_profit = 0.0

    def show(self):

        print("\n==============================")
        print("IKA AI ACCOUNT")
        print("==============================")
        print(f"Starting Balance : £{self.starting_balance:,.2f}")
        print(f"Current Balance  : £{self.balance:,.2f}")
        print(f"Open P/L         : £{self.open_profit:,.2f}")
        print(f"Closed P/L       : £{self.closed_profit:,.2f}")
        print("==============================\n")


account = TradingAccount()
