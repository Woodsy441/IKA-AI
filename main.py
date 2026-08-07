"""
IKA AI
Version 1.0
Main Program
"""

from analysis.market_scanner import scan_markets
from trading.portfolio import show_portfolio
from trading.account import account


def display_market_results(results):

    print("\n" + "=" * 50)
    print("        IKA AI Market Scanner")
    print("=" * 50)

    for i, asset in enumerate(results, start=1):

        print(
            f"{i}. "
            f"{asset['asset']:<12}"
            f"{asset['rating']:<8}"
            f"{asset['score']}%   "
            f"Entry: {asset['price']:.2f}   "
            f"SL: {asset['stop_loss']:.2f}   "
            f"TP: {asset['take_profit']:.2f}   "
            f"Size: {asset['position_size']}"
        )


def main():

    print("\n" + "=" * 50)
    print("               IKA AI")
    print("      Intelligent Trading Assistant")
    print("=" * 50)

    results = scan_markets()

    results.sort(
        key=lambda asset: asset["score"],
        reverse=True
    )

    display_market_results(results)

    show_portfolio()

    account.show()


if __name__ == "__main__":
    main()
    