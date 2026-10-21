"""Offline walk-forward evaluation of paired paper-trading opportunities.

CSV: opportunity_id,signal_time,variant,net_return_pct,entry_delay_seconds
Exactly one baseline and candidate row per opportunity. Signal timestamps must
be timezone-aware ISO-8601. Chronological train/test split by opportunity.
No trading execution, model fitting, or automatic strategy promotion.
"""
import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path


def evaluate(rows, train_fraction=0.7):
    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1")
    grouped = {}
    errors = []
    for line, row in enumerate(rows, 2):
        try:
            key = (row.get("opportunity_id") or "").strip()
            variant = (row.get("variant") or "").strip().lower()
            stamp = datetime.fromisoformat((row.get("signal_time") or "").replace("Z", "+00:00"))
            if not key or variant not in ("baseline", "candidate") or stamp.utcoffset() is None:
                raise ValueError("invalid id, variant or timezone")
            ret = float(row["net_return_pct"])
            delay = float(row["entry_delay_seconds"])
            if not math.isfinite(ret) or not math.isfinite(delay) or delay < 0:
                raise ValueError("invalid return or delay")
            record = grouped.setdefault(key, {"time": stamp, "variants": {}})
            if record["time"] != stamp:
                raise ValueError("mismatched signal times for opportunity")
            if variant in record["variants"]:
                raise ValueError("duplicate variant")
            record["variants"][variant] = (ret, delay)
        except (ValueError, TypeError, KeyError) as exc:
            errors.append({"line": line, "error": str(exc)})
    complete = [(v["time"], k, v["variants"]) for k, v in grouped.items()
                if set(v["variants"]) == {"baseline", "candidate"}]
    complete.sort(key=lambda item: (item[0], item[1]))
    # Keep same-time opportunities in the same partition to avoid timestamp leakage.
    unique_times = sorted({item[0] for item in complete})
    if len(unique_times) < 2:
        return {"error": "need at least two distinct paired signal timestamps",
                "paired_opportunities": len(complete), "invalid_rows": errors}
    cut = max(1, min(len(unique_times) - 1, int(len(unique_times) * train_fraction)))
    boundary = unique_times[cut]
    train = [x for x in complete if x[0] < boundary]
    test = [x for x in complete if x[0] >= boundary]

    def summarise(partition):
        deltas = [x[2]["candidate"][0] - x[2]["baseline"][0] for x in partition]
        faster = sum(x[2]["candidate"][1] < x[2]["baseline"][1] for x in partition)
        return {
            "opportunities": len(partition),
            "mean_candidate_minus_baseline_net_return_pct": sum(deltas) / len(deltas),
            "fraction_candidate_entries_faster": faster / len(partition),
            "candidate_outperformed_fraction": sum(x > 0 for x in deltas) / len(deltas),
        }
    return {
        "train": summarise(train),
        "out_of_sample": summarise(test),
        "split_boundary_utc": boundary.isoformat(),
        "unpaired_opportunities": len(grouped) - len(complete),
        "invalid_rows": errors,
        "limitations": [
            "Exploratory comparison; training split is not a substitute for multiple rolling folds.",
            "Returns must include fees/slippage; matching opportunities must use no lookahead.",
            "Trade-level averages are not portfolio returns; overlapping positions matter.",
            "No statistical significance, regime robustness, or promotion decision is implied.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--train-fraction", type=float, default=0.7)
    args = parser.parse_args()
    with args.csv_file.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"opportunity_id", "signal_time", "variant", "net_return_pct", "entry_delay_seconds"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            parser.error("missing columns: " + ", ".join(sorted(missing)))
        report = evaluate(reader, args.train_fraction)
    print(json.dumps(report, indent=2))
    if report.get("error") or report["invalid_rows"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
