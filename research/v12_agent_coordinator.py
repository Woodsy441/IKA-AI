"""IKA V12 offline research coordinator.

Deterministic agents produce auditable proposals, never broker instructions.
No API credentials, network calls, LLM keys, orders or automatic promotion.
"""
import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

MARKETS = {
    "stocks": ("AAPL", "MSFT", "SPY"),
    "crypto": ("BTC-USD", "ETH-USD"),
    "forex": ("GBP/USD", "EUR/USD", "USD/JPY"),
}
AGENTS = (
    "chief_research", "market_scanner", "entry", "exit",
    "market_intelligence", "strategy_discovery", "backtesting",
    "risk", "performance", "strategy_selection",
)
STRATEGIES = ("momentum", "mean_reversion", "breakout", "trend_following")


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    market: str
    symbol: str
    strategy: str
    entry_hypothesis: str
    exit_hypothesis: str
    status: str = "RESEARCH_ONLY"


def propose(markets=MARKETS, strategies=STRATEGIES):
    """Generate reproducible research hypotheses, not trade signals."""
    return [
        asdict(Proposal(
            proposal_id=f"{market}:{symbol}:{strategy}",
            market=market,
            symbol=symbol,
            strategy=strategy,
            entry_hypothesis=f"Test {strategy} signals using next-bar entries; compare delays and costs",
            exit_hypothesis="Compare conservative stop, target and time exits",
        ))
        for market, symbols in markets.items()
        for symbol in symbols
        for strategy in strategies
    ]


def review(proposal, evidence):
    """Fail closed: independent evidence needed before paper shadow review."""
    required = ("train_trades", "holdout_trades", "holdout_mean_net_return_pct",
                "max_drawdown_pct", "data_quality_errors")
    if not all(k in evidence for k in required):
        return {"proposal_id": proposal["proposal_id"], "decision": "INSUFFICIENT_EVIDENCE"}
    try:
        train = int(evidence["train_trades"])
        test = int(evidence["holdout_trades"])
        net = float(evidence["holdout_mean_net_return_pct"])
        dd = float(evidence["max_drawdown_pct"])
        errors = int(evidence["data_quality_errors"])
        from math import isfinite
        if not isfinite(net) or not isfinite(dd) or dd < 0 or dd > 100:
            raise ValueError("invalid numeric evidence")
    except (ValueError, TypeError):
        return {"proposal_id": proposal["proposal_id"], "decision": "INVALID_EVIDENCE"}
    if errors or train < 30 or test < 20 or net <= 0 or dd > 15:
        decision = "REJECT_OR_COLLECT_MORE_EVIDENCE"
    else:
        decision = "SHADOW_REVIEW_CANDIDATE"
    return {
        "proposal_id": proposal["proposal_id"],
        "decision": decision,
        "approval": "NONE",
        "execution_enabled": False,
        "warning": "Thresholds are illustrative research gates, not proof of profitability.",
    }


def report(evidence_rows=()):
    proposals = propose()
    index = {p["proposal_id"]: p for p in proposals}
    decisions = []
    for row in evidence_rows:
        key = row.get("proposal_id", "")
        if key not in index:
            decisions.append({"proposal_id": key, "decision": "UNKNOWN_PROPOSAL"})
        else:
            decisions.append(review(index[key], row))
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "PAPER_RESEARCH_ONLY",
        "monitor": "STOPPED",
        "trading_execution_enabled": False,
        "agent_roles": list(AGENTS),
        "markets": {k: list(v) for k, v in MARKETS.items()},
        "proposals": proposals,
        "reviews": decisions,
        "notes": [
            "Agent roles are deterministic research stages, not independently running LLMs.",
            "Crypto and forex are research universes only; no market feeds connected.",
            "No autonomous model training, strategy deployment or broker access.",
            "Evidence CSV is externally supplied and must be independently audited.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, help="Optional read-only research evidence CSV")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()
    rows = []
    if args.evidence:
        with args.evidence.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
    result = report(rows)
    serialized = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(serialized + "\n", encoding="utf-8")
    else:
        print(serialized)


if __name__ == "__main__":
    main()
