from trading.storage import save_portfolio, load_portfolio
from trading.trade_manager import update_trade
from trading.account import account

portfolio = load_portfolio()


def trade_exists(asset):

    for trade in portfolio:

        if trade["asset"] == asset and trade["status"] == "OPEN":
            return True

    return False


def add_trade(trade):

    portfolio.append(trade)
    save_portfolio(portfolio)


def show_portfolio():

    print("\n==============================")
    print("IKA AI PORTFOLIO")
    print("==============================")

    if len(portfolio) == 0:
        print("No open trades.\n")
        return

    closed_trades = []

    for i, trade in enumerate(portfolio, start=1):

        trade = update_trade(trade)

        if trade["status"] == "CLOSED":

            account.close_trade(trade)

            print(
                f"{trade['asset']} CLOSED "
                f"({trade['close_reason']}) "
                f"P/L: £{trade['profit_loss']:.2f}"
            )

            closed_trades.append(trade)

        else:

            print(
                f"{i}. "
                f"{trade['asset']}  "
                f"{trade['action']}  "
                f"Entry: {trade['entry']:.2f}  "
                f"Current: {trade['current_price']:.2f}  "
                f"P/L: £{trade['profit_loss']:.2f}  "
                f"Status: {trade['status']}  "
                f"Size: {trade['position_size']}"
            )

    for trade in closed_trades:
        portfolio.remove(trade)

    save_portfolio(portfolio)

    print("==============================\n")
    