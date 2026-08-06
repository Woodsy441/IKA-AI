from datetime import datetime

portfolio = []


def add_trade(trade):
    portfolio.append(trade)


def show_portfolio():

    print("\n==============================")
    print("IKA AI PORTFOLIO")
    print("==============================")

    if len(portfolio) == 0:
        print("No open trades.\n")
        return

    for i, trade in enumerate(portfolio, start=1):

        print(
            f"{i}. "
            f"{trade['asset']}  "
            f"{trade['action']}  "
            f"Entry: {trade['entry']:.2f}  "
            f"SL: {trade['stop_loss']:.2f}  "
            f"TP: {trade['take_profit']:.2f}  "
            f"Size: {trade['position_size']}"
        )

    print("==============================\n")
    