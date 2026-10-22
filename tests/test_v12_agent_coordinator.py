import unittest
from research.v12_agent_coordinator import AGENTS, MARKETS, propose, report, review


class CoordinatorTests(unittest.TestCase):
    def test_all_markets_and_agents_present(self):
        self.assertEqual(set(MARKETS), {"stocks", "crypto", "forex"})
        self.assertEqual(len(AGENTS), 10)
        self.assertEqual(len(propose()), 8 * 4)
        self.assertTrue(all(p["status"] == "RESEARCH_ONLY" for p in propose()))

    def test_fail_closed_without_evidence(self):
        p = propose()[0]
        self.assertEqual(review(p, {})["decision"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(review(p, {"train_trades": "x"})["decision"], "INSUFFICIENT_EVIDENCE")

    def test_candidate_never_activates_trading(self):
        p = propose()[0]
        evidence = dict(train_trades=100, holdout_trades=50,
                        holdout_mean_net_return_pct=1.5,
                        max_drawdown_pct=5, data_quality_errors=0)
        result = review(p, evidence)
        self.assertEqual(result["decision"], "SHADOW_REVIEW_CANDIDATE")
        self.assertFalse(result["execution_enabled"])
        self.assertEqual(result["approval"], "NONE")

    def test_report_has_no_execution(self):
        result = report()
        self.assertFalse(result["trading_execution_enabled"])
        self.assertEqual(result["monitor"], "STOPPED")


if __name__ == "__main__":
    unittest.main()
