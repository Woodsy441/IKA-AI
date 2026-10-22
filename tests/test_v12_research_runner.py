import sqlite3
import tempfile
import unittest
from pathlib import Path
from research.v12_agent_coordinator import propose
from research.v12_research_runner import run


class RunnerTests(unittest.TestCase):
    def test_persistent_idempotent_audit_and_no_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "research.sqlite"
            evidence = [{
                "proposal_id": propose()[0]["proposal_id"],
                "train_trades": "100",
                "holdout_trades": "50",
                "holdout_mean_net_return_pct": "1",
                "max_drawdown_pct": "5",
                "data_quality_errors": "0",
            }]
            first = run(db, evidence)
            second = run(db, evidence)
            self.assertFalse(first["execution_enabled"])
            self.assertEqual(first["reviews"][0]["experiment_id"],
                             second["reviews"][0]["experiment_id"])
            with sqlite3.connect(db) as conn:
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM experiments").fetchone()[0], 1)
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM agent_events").fetchone()[0], 5)

    def test_unknown_proposal_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run(Path(tmp) / "ledger.db", [{"proposal_id": "unknown"}])
            self.assertEqual(result["reviews"][0]["decision"], "UNKNOWN_PROPOSAL")


if __name__ == "__main__":
    unittest.main()
