import unittest
from research.paper_entry_exit_simulator import simulate


def bar(hour, o, h, l, c, signal=0):
    return dict(timestamp=f"2026-10-20T{hour:02d}:00:00Z",
                open=str(o), high=str(h), low=str(l), close=str(c),
                signal=str(signal))


class PaperEntryExitTests(unittest.TestCase):
    def test_next_bar_entry_and_target(self):
        result = simulate([
            bar(10, 100, 101, 99, 100, 1),
            bar(11, 101, 106, 100, 104),
        ], fee_bps=0, slippage_bps=0)
        self.assertEqual(result["trade_count"], 1)
        self.assertEqual(result["closed_trades"][0]["entry_price"], 101)
        self.assertEqual(result["closed_trades"][0]["exit_reason"], "target")

    def test_both_stop_and_target_hit_assumes_stop(self):
        result = simulate([
            bar(10, 100, 100, 100, 100, 1),
            bar(11, 100, 105, 97, 100),
        ], fee_bps=0, slippage_bps=0)
        self.assertEqual(result["closed_trades"][0]["exit_reason"], "stop")
        self.assertLess(result["closed_trades"][0]["net_return_pct"], 0)

    def test_gap_beyond_stop(self):
        result = simulate([
            bar(10, 100, 100, 100, 100, 1),
            bar(11, 95, 96, 94, 95),
        ], fee_bps=0, slippage_bps=0)
        self.assertEqual(result["closed_trades"][0]["entry_price"], 95)

    def test_signal_on_last_bar_never_fills(self):
        result = simulate([bar(10, 100, 100, 100, 100, 1)])
        self.assertEqual(result["trade_count"], 0)

    def test_bad_bars_fail(self):
        with self.assertRaises(ValueError):
            simulate([bar(10, 100, 99, 101, 100)])


if __name__ == "__main__":
    unittest.main()
