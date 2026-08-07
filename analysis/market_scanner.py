import traceback

from config import ASSETS
from analysis.technical_analysis import analyse_asset
from utils.trade_logger import log_trade
from trading.paper_trader import open_trade


def scan_markets():

    print("\nScanning Markets...\n")

    results = []

    for name, ticker in ASSETS.items():

        try:

            print(f"Scanning {name}...")

            result = analyse_asset(name, ticker)

            if result:

                log_trade(result)

                if result["rating"] == "BUY":
                    open_trade(result)

                results.append(result)

        except Exception:

            print(f"{name} failed.")
            traceback.print_exc()

    return results
    