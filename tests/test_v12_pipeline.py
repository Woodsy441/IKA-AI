import tempfile
import unittest
from pathlib import Path
from research.v12_agents import AGENTS, evaluate
from research.v12_cycle import cycle


class V12PipelineTests(unittest.TestCase):
    def test_all_ten_agents_run_on_supported_research(self):
        result = evaluate("stocks", "AAPL", "momentum")
        self.assertEqual(len(AGENTS), 10)
        self.assertEqual(len(result["agent_findings"]), 10)
        self.assertFalse(result["execution_enabled"])
        self.assertFalse(result["auto_promotion"])

    def test_unsupported_market_stops(self):
        result = evaluate("unsupported", "AAPL", "momentum")
        self.assertEqual(len(result["agent_findings"]), 1)
        self.assertEqual(result["agent_findings"][0]["finding"], "unsupported_universe")

    def test_cycle_generates_ledger_and_dashboard_without_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "ledger.db"
            page = Path(tmp) / "report.html"
            result = cycle(db, page)
            self.assertTrue(db.exists())
            self.assertTrue(page.exists())
            self.assertFalse(result["execution_enabled"])
            self.assertIn("IKA AI V12", page.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
