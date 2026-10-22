import unittest
from research.paper_risk_audit import analyse


class PaperRiskAuditTests(unittest.TestCase):
    def test_drawdown_and_exposure(self):
        rows = [
            {"timestamp": "2026-10-20T10:00:00Z", "equity": "1000", "position_value": "500"},
            {"timestamp": "2026-10-20T11:00:00Z", "equity": "900", "position_value": "450"},
            {"timestamp": "2026-10-20T12:00:00Z", "equity": "1100", "position_value": "220"},
        ]
        result = analyse(rows)
        self.assertEqual(result["valid_snapshots"], 3)
        self.assertEqual(result["maximum_observed_drawdown_pct"], 10)
        self.assertEqual(result["maximum_observed_gross_exposure_pct"], 50)

    def test_reject_out_of_order_and_bad_equity(self):
        rows = [
            {"timestamp": "2026-10-20T11:00:00Z", "equity": "100", "position_value": "0"},
            {"timestamp": "2026-10-20T10:00:00Z", "equity": "90", "position_value": "0"},
            {"timestamp": "2026-10-20T12:00:00Z", "equity": "0", "position_value": "0"},
        ]
        result = analyse(rows)
        self.assertEqual(result["valid_snapshots"], 1)
        self.assertEqual(len(result["invalid_rows"]), 2)


if __name__ == "__main__":
    unittest.main()
