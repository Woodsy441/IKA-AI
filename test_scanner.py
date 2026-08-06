from analysis.market_scanner import scan_markets
from trading.portfolio import show_portfolio

results = scan_markets()

results = sorted(results, key=lambda x: x["score"], reverse=True)

print("\n" + "=" * 50)
print("        IKA AI Market Scanner")
print("=" * 50)

for i, asset in enumerate(results, start=1):
    print(
        f"{i}. {asset['asset']:<12}"
        f"{asset['rating']:<8}"
        f"{asset['score']}%   "
        f"Entry: {asset['price']:.2f}   "
        f"SL: {asset['stop_loss']:.2f}   "
        f"TP: {asset['take_profit']:.2f}   "
        f"Size: {asset['position_size']}"
    )

show_portfolio()
