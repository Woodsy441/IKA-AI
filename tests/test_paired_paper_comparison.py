import unittest
from research.paired_paper_comparison import compare


class PairedPaperComparisonTests(unittest.TestCase):
    def test_paired_comparison(self):
        rows = [
            {"opportunity_id": "1", "variant": "baseline", "net_return_pct": "1.0", "entry_delay_seconds": "120"},
            {"opportunity_id": "1", "variant": "candidate", "net_return_pct": "1.5", "entry_delay_seconds": "60"},
            {"opportunity_id": "2", "variant": "baseline", "net_return_pct": "-2", "entry_delay_seconds": "30"},
        ]
        report = compare(rows)
        self.assertEqual(report["paired_opportunities"], 1)
        self.assertEqual(report["unmatched_opportunities"], 1)
        self.assertAlmostEqual(report["candidate_minus_baseline_mean_net_return_pct"], 0.5)

    def test_invalid_inputs(self):
        rows = [
            {"opportunity_id": "1", "variant": "candidate", "net_return_pct": "nan", "entry_delay_seconds": "1"},
            {"opportunity_id": "2", "variant": "baseline", "net_return_pct": "1", "entry_delay_seconds": "-1"},
        ]
        report = compare(rows)
        self.assertEqual(len(report["invalid_rows"]), 2)
        self.assertEqual(report["paired_opportunities"], 0)

    def test_duplicate_is_not_counted_twice(self):
        row = {"opportunity_id": "1", "variant": "candidate", "net_return_pct": "1", "entry_delay_seconds": "2"}
        report = compare([row, row])
        self.assertEqual(len(report["invalid_rows"]), 1)


if __name__ == "__main__":
    unittest.main()
