import csv
import os


TRADE_HISTORY = "history/trade_history.csv"


def log_trade(trade):
    """
    Log every market scan to the CSV history file.
    """

    file_exists = os.path.isfile(TRADE_HISTORY)

    with open(TRADE_HISTORY, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Asset",
                "Rating",
                "Score",
                "Price",
                "Stop Loss",
                "Take Profit"
            ])

        writer.writerow([
            trade["asset"],
            trade["rating"],
            trade["score"],
            trade["price"],
            trade["stop_loss"],
            trade["take_profit"]
        ])


def log_closed_trade(trade):
    """
    Placeholder for logging closed trades.
    We'll expand this in Version 2.1.
    """

    print(
        f"Closed Trade: "
        f"{trade['asset']} "
        f"P/L £{trade['profit_loss']:.2f}"
    )
    