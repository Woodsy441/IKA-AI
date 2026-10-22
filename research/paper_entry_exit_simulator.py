"""Offline, no-lookahead paper entry/exit simulator.

Each CSV row is one completed OHLC bar with:
timestamp,open,high,low,close,signal
signal: 1 for long candidate, 0 otherwise. A signal on bar N may only
enter at bar N+1 open. Stop/take-profit levels are evaluated from that bar
onward; if both touch in the same bar, assume STOP first (conservative).
Single long position; no shorting, leverage, live data or broker connectivity.
Research only. Not a production trading engine.
"""
import argparse
import csv
import json
import math
from datetime import datetime


def simulate(rows, stop_pct=0.02, target_pct=0.04, max_bars=12, fee_bps=5, slippage_bps=5):
    if not (0 < stop_pct < 1 and 0 < target_pct < 1 and max_bars >= 1
            and fee_bps >= 0 and slippage_bps >= 0):
        raise ValueError("invalid simulation parameters")
    bars = []
    last_time = None
    for i, row in enumerate(rows, 2):
        stamp = datetime.fromisoformat(row["timestamp"].strip().replace("Z", "+00:00"))
        if stamp.utcoffset() is None or (last_time is not None and stamp <= last_time):
            raise ValueError(f"line {i}: invalid or unordered timezone-aware timestamp")
        last_time = stamp
        o, h, l, c = (float(row[k]) for k in ("open", "high", "low", "close"))
        if not all(map(math.isfinite, (o, h, l, c))) or l <= 0 or not (l <= o <= h and l <= c <= h):
            raise ValueError(f"line {i}: invalid OHLC")
        signal = int(row["signal"])
        if signal not in (0, 1):
            raise ValueError(f"line {i}: signal must be 0 or 1")
        bars.append((stamp, o, h, l, c, signal))
    trades = []
    position = None
    pending = False
    for index, (stamp, o, h, l, c, signal) in enumerate(bars):
        if position is None and pending:
            entry = o * (1 + slippage_bps / 10000)
            position = {"entry_time": stamp.isoformat(), "entry": entry,
                        "entry_index": index}
            pending = False
        if position is not None:
            entry = position["entry"]
            stop = entry * (1 - stop_pct)
            target = entry * (1 + target_pct)
            # Opening gaps can fill beyond stops/targets; do not assume the stop price.
            if o <= stop:
                raw_exit, reason = o, "gap_stop"
            elif o >= target:
                raw_exit, reason = target, "target_open"
            elif l <= stop:
                raw_exit, reason = stop, "stop"
            elif h >= target:
                raw_exit, reason = target, "target"
            elif index - position["entry_index"] + 1 >= max_bars:
                raw_exit, reason = c, "time"
            else:
                raw_exit, reason = None, None
            if raw_exit is not None:
                exit_price = raw_exit * (1 - slippage_bps / 10000)
                net_return = (exit_price / entry - 1) * 100 - 2 * fee_bps / 100
                trades.append({
                    "entry_time": position["entry_time"],
                    "exit_time": stamp.isoformat(),
                    "entry_price": round(entry, 8),
                    "exit_price": round(exit_price, 8),
                    "exit_reason": reason,
                    "net_return_pct": round(net_return, 6),
                })
                position = None
        # A signal cannot enter until next bar; do not enter while already occupied.
        if position is None and signal and index + 1 < len(bars):
            pending = True
    return {
        "closed_trades": trades,
        "trade_count": len(trades),
        "mean_net_return_pct": (sum(t["net_return_pct"] for t in trades) / len(trades)
                                if trades else None),
        "open_position_at_end": position is not None,
        "limitations": [
            "Synthetic bar fills, no order book or real market liquidity.",
            "Intrabar path unknown; simultaneous stop/target assumes stop first.",
            "No portfolio sizing, overnight corporate actions, borrow costs or taxes.",
            "Trade mean is not compounded portfolio P/L.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file")
    parser.add_argument("--stop-pct", type=float, default=0.02)
    parser.add_argument("--target-pct", type=float, default=0.04)
    parser.add_argument("--max-bars", type=int, default=12)
    parser.add_argument("--fee-bps", type=float, default=5)
    parser.add_argument("--slippage-bps", type=float, default=5)
    args = parser.parse_args()
    with open(args.csv_file, newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"timestamp", "open", "high", "low", "close", "signal"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            parser.error("missing columns: " + ", ".join(sorted(missing)))
        result = simulate(reader, args.stop_pct, args.target_pct,
                          args.max_bars, args.fee_bps, args.slippage_bps)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
