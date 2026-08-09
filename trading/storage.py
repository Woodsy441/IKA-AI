import json
from pathlib import Path


# ============================================================
# IKA AI - Portfolio Storage
# ============================================================

# This file is:
#
# IKA_AI/trading/storage.py
#
# parents[0] = trading
# parents[1] = IKA_AI
#
# Therefore this always finds the main project folder,
# regardless of whether we run v2 or v3.
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PORTFOLIO_FILE = PROJECT_ROOT / "history" / "portfolio.json"


def save_portfolio(portfolio):
    """
    Save the current portfolio to the main IKA AI
    history folder.
    """

    PORTFOLIO_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        PORTFOLIO_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            portfolio,
            f,
            indent=4,
            default=str
        )


def load_portfolio():
    """
    Load the portfolio from the main IKA AI
    history folder.

    Returns an empty list if the file does not exist.
    """

    if not PORTFOLIO_FILE.exists():
        return []

    with open(
        PORTFOLIO_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

        