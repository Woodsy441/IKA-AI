import unittest
from research.paper_experiment import experiment


def bars(count):
    for i in range(count):
        price = 100 + i % 3
        yield {
            "timestamp": f"2026-10-{1 + i // 24:02d}T{i % 24:02d}:00:00Z",
            "open": str(price), "high": str(price + 3),
            "low": str(price - 3), "close": str(price),
            "signal": "1" if i % 3 == 0 else "0",
        }


class ExperimentTests(unittest.TestCase):
    def test_grid_and_holdout(self):
        result = experiment(bars(48), minimum_train_trades=1)
        self.assertEqual(result["status"], "research_only")
        self.assertGreater(result["evaluated_candidates"], 0)
        self.assertEqual(result["training_bars"] + result["holdout_bars"], 48)
        self.assertIn("holdout_mean_net_return_pct", result)

    def test_insufficient_training_trades(self):
        result = experiment(bars(8), minimum_train_trades=100)
        self.assertEqual(result["status"], "insufficient_training_trades")

    def test_bad_split(self):
        with self.assertRaises(ValueError):
            experiment(bars(8), train_fraction=1)


if __name__ == "__main__":
    unittest.main()
