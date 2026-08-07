from datetime import datetime

from trading.portfolio import add_trade, trade_exists


def open_trade(signal):

    if trade_exists(signal["asset"]):
        print(f"{signal['asset']} already has an open trade.")
        return None

    trade = {
        "asset": signal["asset"],
        "action": signal["rating"],
        "entry": signal["price"],
        "stop_loss": signal["stop_loss"],
        "take_profit": signal["take_profit"],
        "position_size": signal["position_size"],
        "opened": datetime.now(),
        "status": "OPEN"
    }

    add_trade(trade)

    print("\n==============================")
    print("IKA AI PAPER TRADE")
    print("==============================")
    print(f"Asset: {trade['asset']}")
    print(f"Action: {trade['action']}")
    print(f"Entry: {trade['entry']:.2f}")
    print(f"Stop Loss: {trade['stop_loss']:.2f}")
    print(f"Take Profit: {trade['take_profit']:.2f}")
    print(f"Position Size: {trade['position_size']}")
    print("==============================\n")

    return trade
    