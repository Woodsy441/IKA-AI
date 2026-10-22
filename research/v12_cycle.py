"""Safe periodic offline research cycle: explicit invocation, no daemon.

Run from a local scheduler if desired. Never launches trades or network calls.
Only reads evidence CSV and writes isolated research ledger/dashboard files.
"""
import argparse
import csv
import json
from pathlib import Path

from research.v12_agents import evaluate
from research.v12_dashboard import render
from research.v12_research_runner import run
from research.v12_agent_coordinator import propose


def cycle(database, dashboard, evidence=None):
    rows = []
    if evidence:
        with Path(evidence).open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
    ledger = run(database, rows)
    index = {p["proposal_id"]: p for p in propose()}
    handoffs = []
    for row in rows:
        p = index.get(row.get("proposal_id"))
        if p is not None:
            handoffs.append(evaluate(p["market"], p["symbol"], p["strategy"], row))
    Path(dashboard).parent.mkdir(parents=True, exist_ok=True)
    Path(dashboard).write_text(render(database), encoding="utf-8")
    return {
        "status": "completed",
        "execution_enabled": False,
        "evidence_rows": len(rows),
        "handoffs": handoffs,
        "ledger": ledger,
        "dashboard": str(dashboard),
        "warning": "This is an on-demand cycle, not continuous background execution.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--dashboard", type=Path, required=True)
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args()
    print(json.dumps(cycle(args.database, args.dashboard, args.evidence), indent=2))


if __name__ == "__main__":
    main()
