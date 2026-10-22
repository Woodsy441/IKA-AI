"""Offline, read-only analysis of paper-trade signal and entry timestamps.

CSV input columns: symbol,signal_time,entry_time,status,reason
Optional: opportunity_id, strategy. Times must be ISO-8601 with explicit timezone.
No broker integration, order placement, or modification of risk settings.
"""
import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


def timestamp(value):
    if not value:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamps must include UTC offset")
    return parsed


def audit(rows):
    seen = set()
    counts = Counter()
    reasons = Counter()
    delays = []
    errors = []
    for line, row in enumerate(rows, start=2):
        try:
            symbol = (row.get("symbol") or "").strip().upper()
            status = (row.get("status") or "").strip().lower()
            signal = timestamp((row.get("signal_time") or "").strip())
            entry = timestamp((row.get("entry_time") or "").strip())
            if not symbol or not signal or status not in {"entered", "rejected", "missed", "pending"}:
                raise ValueError("missing symbol/signal_time or invalid status")
            key = (row.get("opportunity_id") or "").strip()
            if key:
                key = ("id", key)
            else:
                key = ("fallback", symbol, signal.isoformat(), (row.get("strategy") or "").strip())
            if key in seen:
                raise ValueError("duplicate opportunity")
            seen.add(key)
            if status == "entered":
                if entry is None:
                    raise ValueError("entered opportunity missing entry_time")
                delay = (entry - signal).total_seconds()
                if delay < 0:
                    raise ValueError("entry precedes signal")
                delays.append(delay)
            elif entry is not None:
                raise ValueError("non-entered opportunity has entry_time")
            counts[status] += 1
            if status in {"rejected", "missed"}:
                reasons[(row.get("reason") or "").strip() or "UNSPECIFIED"] += 1
        except (ValueError, TypeError) as exc:
            errors.append({"line": line, "error": str(exc)})
    delays.sort()
    n = len(delays)
    return {
        "valid_opportunities": sum(counts.values()),
        "status_counts": dict(sorted(counts.items())),
        "rejection_and_missed_reasons": dict(reasons.most_common()),
        "entry_delay_seconds": {
            "count": n,
            "median": (delays[(n - 1) // 2] + delays[n // 2]) / 2 if n else None,
            "p90": delays[max(0, (9 * n + 9) // 10 - 1)] if n else None,
            "maximum": delays[-1] if n else None,
        },
        "invalid_rows": errors,
        "limitations": [
            "Descriptive metrics only: no evidence of profitability or optimal entry timing.",
            "Missed-trade labels must be defined without future-price lookahead.",
            "Results depend on timestamp accuracy and completeness of input.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    args = parser.parse_args()
    with args.csv_file.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        required = {"symbol", "signal_time", "entry_time", "status", "reason"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            parser.error("missing CSV columns: " + ", ".join(sorted(missing)))
        report = audit(reader)
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    if report["invalid_rows"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
