"""Offline paper strategy experiment grid with chronological holdout.

Input OHLCV-free CSV: timestamp,open,high,low,close,signal.
Candidate parameter selection uses training bars only. Holdout is evaluated
once with the selected settings; no broker connectivity or deployment.
NOTE: Each partition is independently simulated; trades crossing boundary
are discarded to prevent using holdout prices during selection.
"""
import argparse
import csv
import itertools
import json
from datetime import datetime

from research.paper_entry_exit_simulator import simulate


def experiment(rows, train_fraction=0.7, stops=(0.01, 0.02),
               targets=(0.02, 0.04), holding_bars=(6, 12),
               fee_bps=5, slippage_bps=5, minimum_train_trades=10):
    bars = list(rows)
    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1")
    if minimum_train_trades < 1:
        raise ValueError("minimum_train_trades must be positive")
    # Parse and validate timestamps before splitting; the simulator validates OHLC.
    times = [datetime.fromisoformat(b["timestamp"].replace("Z", "+00:00")) for b in bars]
    if any(t.utcoffset() is None for t in times) or any(
            a >= b for a, b in zip(times, times[1:])):
        raise ValueError("timestamps must be timezone-aware and strictly increasing")
    if len(bars) < 4:
        raise ValueError("at least four bars required")
    cut = max(2, min(len(bars) - 2, int(len(bars) * train_fraction)))
    training, holdout = bars[:cut], bars[cut:]
    candidates = []
    for stop, target, holding in itertools.product(stops, targets, holding_bars):
        params = {"stop_pct": stop, "target_pct": target, "max_bars": holding,
                  "fee_bps": fee_bps, "slippage_bps": slippage_bps}
        result = simulate(training, **params)
        # Do not score an unclosed position at the training boundary.
        if result["trade_count"] >= minimum_train_trades:
            candidates.append((result["mean_net_return_pct"], params, result["trade_count"]))
    if not candidates:
        return {"status": "insufficient_training_trades", "training_bars": len(training),
                "holdout_bars": len(holdout), "candidate_count": 0}
    # Deterministic tie-break; candidate search is explicitly in-sample.
    candidates.sort(key=lambda item: (-item[0], item[1]["stop_pct"],
                                      item[1]["target_pct"], item[1]["max_bars"]))
    train_score, params, train_count = candidates[0]
    test = simulate(holdout, **params)
    return {
        "status": "research_only",
        "training_bars": len(training),
        "holdout_bars": len(holdout),
        "evaluated_candidates": len(candidates),
        "selected_parameters": params,
        "training_closed_trades": train_count,
        "training_mean_net_return_pct": train_score,
        "holdout_closed_trades": test["trade_count"],
        "holdout_mean_net_return_pct": test["mean_net_return_pct"],
        "holdout_open_position_at_end": test["open_position_at_end"],
        "warnings": [
            "Exploratory single split: selection bias remains; use rolling walk-forward folds.",
            "No candidate is approved for deployment, even if holdout results are positive.",
            "Trade averages are not compounded account returns.",
            "No market-impact, corporate-action or portfolio capital model.",
            "Boundary-crossing trades excluded; open holdout positions not marked to market.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file")
    parser.add_argument("--min-train-trades", type=int, default=10)
    args = parser.parse_args()
    with open(args.csv_file, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"timestamp", "open", "high", "low", "close", "signal"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            parser.error("missing columns: " + ", ".join(sorted(missing)))
        result = experiment(reader, minimum_train_trades=args.min_train_trades)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
