import tempfile
import unittest
from pathlib import Path

from research.v12_dashboard import render
from research.v12_research_runner import run


class DashboardTests(unittest.TestCase):
    def test_dashboard_escapes_untrusted_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "research.sqlite"
            run(db, [{"proposal_id": "<script>alert(1)</script>"}])
            page = render(db)
            self.assertIn("&lt;script&gt;", page)
            self.assertNotIn("<script>", page)
            self.assertIn("EXECUTION DISABLED", page)
            self.assertIn("Stocks", page)
            self.assertIn("Crypto", page)
            self.assertIn("Forex", page)

    def test_does_not_create_database_on_missing_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "missing.sqlite"
            with self.assertRaises(FileNotFoundError):
                render(db)
            self.assertFalse(db.exists())


if __name__ == "__main__":
    unittest.main()
