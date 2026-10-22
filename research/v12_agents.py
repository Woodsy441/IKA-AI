"""V12 offline multi-agent research pipeline with explicit agent handoffs.

Agents are separate deterministic Python components, not LLM services.
No network, credentials, order placement or automatic strategy promotion.
"""
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from research.v12_agent_coordinator import MARKETS, STRATEGIES, review


@dataclass
class Context:
    market: str
    symbol: str
    strategy: str
    evidence: dict
    findings: list


class Agent:
    name = "agent"

    def evaluate(self, context):
        raise NotImplementedError

    def emit(self, finding):
        return {"agent": self.name, "finding": finding}


class MarketScanner(Agent):
    name = "market_scanner"

    def evaluate(self, context):
        valid = context.market in MARKETS and context.symbol in MARKETS.get(context.market, ())
        return self.emit("universe_confirmed" if valid else "unsupported_universe")


class StrategyDiscovery(Agent):
    name = "strategy_discovery"

    def evaluate(self, context):
        return self.emit("hypothesis_registered" if context.strategy in STRATEGIES
                         else "unsupported_strategy")


class EntryAgent(Agent):
    name = "entry"

    def evaluate(self, context):
        return self.emit("next_bar_entry_research_only")


class ExitAgent(Agent):
    name = "exit"

    def evaluate(self, context):
        return self.emit("conservative_stop_target_time_research_only")


class MarketIntelligence(Agent):
    name = "market_intelligence"

    def evaluate(self, context):
        return self.emit("no_external_news_or_macro_feed_connected")


class BacktestingAgent(Agent):
    name = "backtesting"

    def evaluate(self, context):
        return self.emit("external_evidence_supplied_unverified" if context.evidence
                         else "no_evidence")


class RiskAgent(Agent):
    name = "risk"

    def evaluate(self, context):
        proposal = {"proposal_id": f"{context.market}:{context.symbol}:{context.strategy}"}
        return self.emit(review(proposal, context.evidence)["decision"])


class PerformanceAgent(Agent):
    name = "performance"

    def evaluate(self, context):
        return self.emit("requires_independent_out_of_sample_validation")


class SelectionAgent(Agent):
    name = "strategy_selection"

    def evaluate(self, context):
        return self.emit("human_shadow_review_only_no_promotion")


class ChiefResearchAgent(Agent):
    name = "chief_research"

    def evaluate(self, context):
        return self.emit("research_completed_no_execution")


AGENTS = (
    MarketScanner(), StrategyDiscovery(), EntryAgent(), ExitAgent(),
    MarketIntelligence(), BacktestingAgent(), RiskAgent(),
    PerformanceAgent(), SelectionAgent(), ChiefResearchAgent(),
)


def evaluate(market, symbol, strategy, evidence=None):
    context = Context(market, symbol, strategy, evidence or {}, [])
    for agent in AGENTS:
        result = agent.evaluate(context)
        context.findings.append(result)
        if result["finding"] in ("unsupported_universe", "unsupported_strategy"):
            break
    return {
        "proposal_id": f"{market}:{symbol}:{strategy}",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "agent_findings": context.findings,
        "execution_enabled": False,
        "auto_promotion": False,
        "mode": "RESEARCH_ONLY",
    }
