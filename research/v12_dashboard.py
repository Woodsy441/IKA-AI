"""Read-only static V12 dashboard from a local SQLite research ledger.

No HTTP server, credentials, network requests, trading, or external assets.
Escapes all data before rendering. Open generated HTML locally on a computer.
"""
import argparse
import html
import sqlite3
from collections import Counter
from pathlib import Path

from research.v12_agent_coordinator import AGENTS, MARKETS


def render(db_path):
    path = Path(db_path)
    if not path.is_file():
        raise FileNotFoundError("research database does not exist")
    with sqlite3.connect(f"file:{path.resolve()}?mode=ro", uri=True) as conn:
        reviews = conn.execute(
            "SELECT proposal_id, decision, created_utc FROM experiments "
            "ORDER BY created_utc DESC, proposal_id LIMIT 250"
        ).fetchall()
        events = conn.execute(
            "SELECT agent, finding, created_utc FROM agent_events "
            "ORDER BY event_id DESC LIMIT 100"
        ).fetchall()
    counts = Counter(decision for _, decision, _ in reviews)
    esc = lambda x: html.escape(str(x), quote=True)
    review_rows = "".join(
        f"<tr><td>{esc(p)}</td><td>{esc(d)}</td><td>{esc(t)}</td></tr>"
        for p, d, t in reviews
    ) or "<tr><td colspan='3'>No evidence reviewed yet</td></tr>"
    event_rows = "".join(
        f"<tr><td>{esc(a)}</td><td>{esc(f)}</td><td>{esc(t)}</td></tr>"
        for a, f, t in events
    ) or "<tr><td colspan='3'>No agent handoffs yet</td></tr>"
    market_cards = "".join(
        f"<article><h3>{esc(market.title())}</h3><p>{esc(', '.join(symbols))}</p>"
        "<small>Research universe only — no feed connected</small></article>"
        for market, symbols in MARKETS.items()
    )
    statuses = "".join(
        f"<li>{esc(key)}: {count}</li>" for key, count in sorted(counts.items())
    ) or "<li>No reviewed evidence</li>"
    agents = ", ".join(AGENTS)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<title>IKA V12 | Offline Research Dashboard</title>
<style>
:root{{font-family:system-ui,sans-serif;color-scheme:dark;background:#0b1220;color:#e5eaf5}}
body{{max-width:1120px;margin:auto;padding:20px}}
header{{padding:22px;border-radius:16px;background:#17233c}}
.badge{{display:inline-block;background:#553026;color:#ffe3b0;padding:7px 12px;border-radius:9px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:18px 0}}
article{{padding:18px;background:#182741;border-radius:14px}}
table{{border-collapse:collapse;width:100%;margin:14px 0}}
td,th{{border-bottom:1px solid #33445f;padding:11px;text-align:left;overflow-wrap:anywhere}}
section{{overflow-x:auto;margin-top:22px}}
small{{color:#aebbd3}}
</style></head><body>
<header><h1>IKA AI V12 — Research Intelligence</h1>
<span class="badge">OFFLINE RESEARCH · EXECUTION DISABLED</span>
<p>Static report. No market feeds, autonomous agents, or live trading.</p></header>
<div class="cards">{market_cards}</div>
<article><h2>Evidence decisions</h2><ul>{statuses}</ul>
<p><small>Agent roles defined: {esc(agents)}</small></p></article>
<section><h2>Research reviews</h2><table><thead><tr><th>Proposal</th><th>Decision</th><th>Recorded UTC</th></tr></thead>
<tbody>{review_rows}</tbody></table></section>
<section><h2>Agent audit trail</h2><table><thead><tr><th>Stage</th><th>Finding</th><th>Recorded UTC</th></tr></thead>
<tbody>{event_rows}</tbody></table></section>
</body></html>"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(render(args.database), encoding="utf-8")
    print(f"Generated offline dashboard: {args.output}")


if __name__ == "__main__":
    main()
