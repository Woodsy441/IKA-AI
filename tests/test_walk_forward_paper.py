import unittest
from research.walk_forward_paper import evaluate


def row(key, time, variant, ret, delay):
    return dict(opportunity_id=key, signal_time=time, variant=variant,
                net_return_pct=str(ret), entry_delay_seconds=str(delay))


class WalkForwardTests(unittest.TestCase):
    def test_chronological_split(self):
        rows = []
        for i in range(4):
            stamp = f"2026-10-{i+1:02d}T10:00:00Z"
            rows += [row(str(i), stamp, "baseline", 0, 60),
                     row(str(i), stamp, "candidate", i + 1, 30)]
        report = evaluate(rows, 0.5)
        self.assertEqual(report["train"]["opportunities"], 2)
        self.assertEqual(report["out_of_sample"]["opportunities"], 2)
        self.assertEqual(report["out_of_sample"]["mean_candidate_minus_baseline_net_return_pct"], 3.5)

    def test_same_timestamp_stays_in_one_partition(self):
        rows = []
        for key, stamp in [("a", "2026-10-01T10:00:00Z"),
                           ("b", "2026-10-01T10:00:00Z"),
                           ("c", "2026-10-02T10:00:00Z")]:
            rows.extend([row(key, stamp, "baseline", 0, 5),
                         row(key, stamp, "candidate", 1, 4)])
        report = evaluate(rows, 0.5)
        self.assertEqual(report["train"]["opportunities"], 2)
        self.assertEqual(report["out_of_sample"]["opportunities"], 1)

    def test_insufficient_data(self):
        report = evaluate([row("a", "2026-10-01T10:00:00Z", "baseline", 0, 5)])
        self.assertIn("error", report)


if __name__ == "__main__":
    unittest.main()
