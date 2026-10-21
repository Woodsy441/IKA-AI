"""Offline, deterministic paper-trade risk diagnostics; never executes trades.

CSV columns: timestamp,equity,position_value
Use ordered UTC/offset-aware ISO timestamps and account equity in the same currency.
No strategy changes or orders are generated.
"""
import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path


def analyse(rows):
    peak = None
    previous_time = None
    max_drawdown = 0.0
    max_exposure = 0.0
    last_equity = None
    count = 0
    errors = []
    for line, row in enumerate(rows, 2):
        try:
            timestamp = datetime.fromisoformat(row["timestamp"].strip().replace("Z", "+00:00"))
            if timestamp.utcoffset() is None:
                raise ValueError("timestamp must contain timezone")
            equity = float(row["equity"])
            position = float(row["position_value"])
            if not all(map(math.isfinite, (equity, position))) or equity <= 0 or position < 0:
                raise ValueError("equity must be positive; position_value nonnegative; both finite")
            if previous_time is not None and timestamp <= previous_time:
                raise ValueError("timestamps must increase strictly")
            previous_time = timestamp
            peak = max(peak or equity, equity)
            max_drawdown = max(max_drawdown, (peak - equity) / peak)
            max_exposure = max(max_exposure, position / equity)
            last_equity = equity
            count += 1
        except (ValueError, TypeError, KeyError) as exc:
            errors.append({"line": line, "error": str(exc)})
    return {
        "valid_snapshots": count,
        "last_equity": last_equity,
        "maximum_observed_drawdown_pct": round(max_drawdown * 100, 6) if count else None,
        "maximum_observed_gross_exposure_pct": round(max_exposure * 100, 6) if count else None,
        "invalid_rows": errors,
        "limitations": [
            "Snapshot-only metrics; intraperiod drawdown and leverage can be worse.",
            "Position values must represent total gross exposure, including short positions.",
            "No evidence of strategy profitability or suitability for live trading.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()
    with args.csv_file.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"timestamp", "equity", "position_value"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            parser.error("missing columns: " + ", ".join(sorted(missing)))
        report = analyse(reader)
    print(json.dumps(report, indent=2))
    if report["invalid_rows"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
