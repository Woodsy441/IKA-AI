import unittest
from research.entry_latency_audit import audit


class AuditTests(unittest.TestCase):
    def row(self, **overrides):
        base = dict(symbol="AAPL", signal_time="2026-10-19T14:00:00+00:00",
                    entry_time="2026-10-19T14:01:00+00:00", status="entered",
                    reason="", opportunity_id="one")
        base.update(overrides)
        return base

    def test_delay_and_rejection(self):
        report = audit([
            self.row(),
            self.row(opportunity_id="two", status="rejected", entry_time="",
                     reason="spread"),
        ])
        self.assertEqual(report["entry_delay_seconds"]["median"], 60)
        self.assertEqual(report["rejection_and_missed_reasons"], {"spread": 1})
        self.assertEqual(report["valid_opportunities"], 2)

    def test_duplicate_and_invalid_timestamps(self):
        report = audit([
            self.row(),
            self.row(),
            self.row(opportunity_id="three", signal_time="2026-10-19T14:00:00"),
        ])
        self.assertEqual(report["valid_opportunities"], 1)
        self.assertEqual(len(report["invalid_rows"]), 2)

    def test_negative_delay_and_nonentered_entry(self):
        report = audit([
            self.row(entry_time="2026-10-19T13:59:00+00:00"),
            self.row(opportunity_id="two", status="missed"),
        ])
        self.assertEqual(report["valid_opportunities"], 0)
        self.assertEqual(len(report["invalid_rows"]), 2)


if __name__ == "__main__":
    unittest.main()
