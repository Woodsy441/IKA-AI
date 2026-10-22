# IKA V12 research architecture (prototype)

**State:** Offline research scaffolding on an isolated development branch.
This is **not** the Windows V11.3 runtime, not a connected market scanner,
not an autonomous LLM team, and not evidence of trading profitability.

## Agent responsibilities

The coordinator lists ten roles: chief research, market scanner, entry,
exit, market intelligence, strategy discovery, backtesting, risk,
performance, and strategy selection. In this prototype these roles are
**declarative**. No independent agents run or exchange messages yet.

## Research universes

- Stocks: AAPL, MSFT, SPY
- Crypto spot research: BTC-USD, ETH-USD
- FX spot-reference research: GBP/USD, EUR/USD, USD/JPY

Symbols are examples only. No feeds, exchanges or broker connections exist.

## Research pipeline

1. Produce reproducible proposals by market, symbol and strategy.
2. Obtain timestamped market observations from an independently validated feed.
3. Run next-bar entry and conservative exit simulations.
4. Compare candidates with costs, drawdowns and chronological holdout testing.
5. Record rejected hypotheses and audit evidence.
6. Allow human review of candidates for **shadow paper research only**.

No step may automatically promote a strategy to execution.

## Run

```bash
python -m research.v12_agent_coordinator --output v12_report.json
python -m unittest discover -s tests -p 'test_v12_agent_coordinator.py' -v
```

Optional `--evidence evidence.csv` fields:
`proposal_id,train_trades,holdout_trades,holdout_mean_net_return_pct,max_drawdown_pct,data_quality_errors`.
The evidence gate is deliberately preliminary and does not independently
verify the evidence or establish statistical significance.

## Next integration gates

- Run all tests and inspect CI failures.
- Map V11.3's actual event schemas, logs and current safety controls.
- Integrate trustworthy stocks, crypto and FX historical data with
  timestamp, market-session, spread and fee validation.
- Add independent role execution, persistent experiment registry,
  scheduling, rolling out-of-sample evaluation, and auditable approvals.
- Build mobile read-only dashboards from verified reports.
- Keep live execution disabled and preserve all protected baseline files.
