#!/usr/bin/env python3
"""Render a human-readable filing summary from filing_registry.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
POSITIONS_PATH = ROOT / 'positions.json'
TICKER_CIK_PATH = ROOT / 'registry' / 'ticker_cik_map.json'
REGISTRY_PATH = ROOT / 'registry' / 'filing_registry.json'
OUTPUT_PATH = ROOT / 'outputs' / 'filing_summary.md'


def main() -> int:
    positions = json.loads(POSITIONS_PATH.read_text())
    ticker_map = json.loads(TICKER_CIK_PATH.read_text())
    registry = json.loads(REGISTRY_PATH.read_text())

    lines = ["# Filing Summary", ""]
    last_updated = None
    if registry:
        last_updated = max((v.get('last_checked_at') for v in registry.values() if v.get('last_checked_at')), default=None)
    if last_updated:
        lines.append(f"_Last updated: {last_updated}_")
        lines.append("")

    for ticker, item in registry.items():
        lines.append(f"## {ticker}")
        lines.append(f"- **CIK:** {item.get('cik')}")
        for label, key in (("Latest 10-Q", "latest_10q"), ("Latest 10-K", "latest_10k")):
            filing = item.get(key)
            if filing:
                lines.append(f"- **{label}:** filed {filing.get('filing_date')} | report date {filing.get('report_date')}")
                lines.append(f"  - Document: `{filing.get('primary_document')}`")
                if filing.get('url'):
                    lines.append(f"  - Link: <{filing.get('url')}>")
            else:
                lines.append(f"- **{label}:** not found")
        lines.append(f"- **Recent 8-Ks:** {len(item.get('recent_8k', []))} tracked")
        new_types = item.get('new_filing_types') or []
        lines.append(f"- **New filings since last check:** {', '.join(new_types) if new_types else 'none'}")
        lines.append(f"- **Status:** {item.get('status')}")
        lines.append("")

    pending = []
    for p in positions:
        ticker = p['ticker']
        info = ticker_map.get(ticker)
        if info and info.get('status') != 'resolved':
            pending.append((ticker, info))

    if pending:
        lines.append("## Pending Review / Coverage Gaps")
        lines.append("")
        for ticker, info in pending:
            lines.append(f"### {ticker}")
            lines.append(f"- **Status:** {info.get('status')}")
            notes = info.get('notes') or []
            if notes:
                lines.append(f"- **Issue:** {notes[0]}")
            lines.append("")

    OUTPUT_PATH.write_text("\n".join(lines).rstrip() + "\n")
    print(str(OUTPUT_PATH))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
