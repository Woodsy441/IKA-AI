import traceback

from analysis.technical_analysis import analyse_asset
from utils.trade_logger import log_trade
from trading.paper_trader import open_trade

# Assets IKA AI will scan
ASSETS = {
    "Gold": "GC=F",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Meta": "META",
    "Google": "GOOGL",
    "Tesla": "TSLA"
}


def scan_markets():
    print(">>> NEW MARKET SCANNER IS RUNNING <<<")
    print("\nScanning Markets...\n")

    results = []

    for name, ticker in ASSETS.items():

        try:
            print(f"Scanning {name}...")

            result = analyse_asset(name, ticker)

            if result:
                print(result)

                log_trade(result)

                if result["rating"] == "BUY":
                    print("Opening paper trade...")
                    open_trade(result)

                results.append(result)

        except Exception:
            traceback.print_exc()

    return results