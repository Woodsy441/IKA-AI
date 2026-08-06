import csv
from datetime import datetime


def log_trade(result):

    with open("history/trade_history.csv", "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            result["asset"],
            result["rating"],
            result["price"],
            result["score"],
            result["take_profit"],
            result["stop_loss"]
        ])