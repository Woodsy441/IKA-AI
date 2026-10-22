"""Read-only V12 research run: agent handoffs and persistent experiment ledger.

Offline only. Never places orders, alters the V11 runtime or auto-promotes.
Input CSV is optional; with no evidence all proposals remain unvalidated.
"""
import argparse
import csv
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from research.v12_agent_coordinator import propose, review

SCHEMA = """
CREATE TABLE IF NOT EXISTS experiments (
  experiment_id TEXT PRIMARY KEY,
  proposal_id TEXT NOT NULL,
  evidence_hash TEXT NOT NULL,
  decision TEXT NOT NULL,
  created_utc TEXT NOT NULL,
  review_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS agent_events (
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  experiment_id TEXT NOT NULL,
  agent TEXT NOT NULL,
  finding TEXT NOT NULL,
  created_utc TEXT NOT NULL
);
"""


def run(database, evidence_rows=()):
    """Record research stages transactionally. Repeat evidence is idempotent."""
    database = Path(database)
    database.parent.mkdir(parents=True, exist_ok=True)
    registry = {p["proposal_id"]: p for p in propose()}
    now = datetime.now(timezone.utc).isoformat()
    output = []
    with sqlite3.connect(database) as conn:
        conn.executescript(SCHEMA)
        for row in evidence_rows:
            proposal_id = row.get("proposal_id", "")
            canonical = json.dumps(row, sort_keys=True, separators=(",", ":"))
            evidence_hash = hashlib.sha256(canonical.encode()).hexdigest()
            experiment_id = hashlib.sha256((proposal_id + ":" + evidence_hash).encode()).hexdigest()
            if proposal_id not in registry:
                decision = {"proposal_id": proposal_id, "decision": "UNKNOWN_PROPOSAL"}
            else:
                decision = review(registry[proposal_id], row)
            conn.execute(
                "INSERT OR IGNORE INTO experiments VALUES (?,?,?,?,?,?)",
                (experiment_id, proposal_id, evidence_hash,
                 decision["decision"], now, json.dumps(decision, sort_keys=True)),
            )
            if conn.execute("SELECT changes()").fetchone()[0]:
                stages = (
                    ("market_scanner", "Research universe membership checked"),
                    ("strategy_discovery", "Hypothesis registered; not a trade signal"),
                    ("backtesting", "Externally supplied evidence received; not independently verified"),
                    ("risk", "Evidence reviewed with fail-closed gates"),
                    ("strategy_selection", "No automatic strategy promotion"),
                )
                for agent, finding in stages:
                    conn.execute(
                        "INSERT INTO agent_events (experiment_id,agent,finding,created_utc) VALUES (?,?,?,?)",
                        (experiment_id, agent, finding, now),
                    )
            output.append({"experiment_id": experiment_id, **decision})
    return {
        "mode": "OFFLINE_RESEARCH_ONLY",
        "execution_enabled": False,
        "proposals_available": len(registry),
        "reviewed_rows": len(output),
        "reviews": output,
        "database": str(database),
        "caveat": "Agent stages are deterministic audit records, not autonomous AI services.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args()
    rows = []
    if args.evidence:
        with args.evidence.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
    print(json.dumps(run(args.database, rows), indent=2))


if __name__ == "__main__":
    main()
