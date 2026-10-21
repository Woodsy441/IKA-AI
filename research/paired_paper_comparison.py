"""Compare paired baseline/candidate PAPER research outcomes, offline only.

CSV columns: opportunity_id,variant,net_return_pct,entry_delay_seconds
variant must be baseline or candidate. One row per opportunity and variant.
Returns are already net of realistic costs, and expressed as percentages.
This tool does not select or promote strategies or place orders.
"""
import argparse
import csv
import json
import math
from pathlib import Path


def compare(rows):
    paired = {}
    errors = []
    for line, row in enumerate(rows, 2):
        try:
            key = (row.get("opportunity_id") or "").strip()
            variant = (row.get("variant") or "").strip().lower()
            if not key or variant not in ("baseline", "candidate"):
                raise ValueError("invalid opportunity_id or variant")
            net = float(row["net_return_pct"])
            delay = float(row["entry_delay_seconds"])
            if not all(map(math.isfinite, (net, delay))) or delay < 0:
                raise ValueError("non-finite return or invalid delay")
            bucket = paired.setdefault(key, {})
            if variant in bucket:
                raise ValueError("duplicate variant for opportunity")
            bucket[variant] = (net, delay)
        except (ValueError, TypeError, KeyError) as exc:
            errors.append({"line": line, "error": str(exc)})
    complete = [pair for pair in paired.values()
                if set(pair) == {"baseline", "candidate"}]
    unmatched = sum(set(pair) != {"baseline", "candidate"} for pair in paired.values())
    def metrics(variant):
        returns = [pair[variant][0] for pair in complete]
        delays = [pair[variant][1] for pair in complete]
        wins = sum(x > 0 for x in returns)
        return {
            "count": len(returns),
            "mean_net_return_pct": sum(returns) / len(returns) if returns else None,
            "win_rate": wins / len(returns) if returns else None,
            "mean_entry_delay_seconds": sum(delays) / len(delays) if delays else None,
            "total_net_return_pct_points": sum(returns),
        }
    baseline = metrics("baseline")
    candidate = metrics("candidate")
    return {
        "paired_opportunities": len(complete),
        "unmatched_opportunities": unmatched,
        "baseline": baseline,
        "candidate": candidate,
        "candidate_minus_baseline_mean_net_return_pct": (
            candidate["mean_net_return_pct"] - baseline["mean_net_return_pct"]
            if complete else None),
        "invalid_rows": errors,
        "warning": (
            "Diagnostic comparison only. Summed trade returns are NOT portfolio P/L. "
            "Paired opportunities must be generated with identical timestamps, "
            "universe and non-lookahead assumptions. No automatic promotion."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()
    with args.csv_file.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"opportunity_id", "variant", "net_return_pct", "entry_delay_seconds"}
        if not required.issubset(set(reader.fieldnames or [])):
            parser.error("missing columns: " + ", ".join(sorted(required - set(reader.fieldnames or []))))
        report = compare(reader)
    print(json.dumps(report, indent=2))
    if report["invalid_rows"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
