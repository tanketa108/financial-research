#!/usr/bin/env python3
"""Render a compact end-to-end pipeline status report."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
FILING_REGISTRY = ROOT / 'registry' / 'filing_registry.json'
FILING_DELTAS = ROOT / 'registry' / 'filing_deltas.json'
DATA_DELTAS = ROOT / 'registry' / 'data_deltas.json'
THESIS_OUTPUT = ROOT / 'registry' / 'thesis_monitor_output.json'
OUTPUT_PATH = ROOT / 'outputs' / 'pipeline_report.md'


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def main() -> int:
    filing_registry = load(FILING_REGISTRY)
    filing_deltas = load(FILING_DELTAS)
    data_deltas = load(DATA_DELTAS)
    thesis_output = load(THESIS_OUTPUT)

    checked_at = next((v.get('last_checked_at') for v in filing_registry.values() if v.get('last_checked_at')), None)
    total = len(thesis_output)
    decisions = {'high_priority': [], 'investigate': [], 'review': [], 'ignore': []}
    for ticker, item in thesis_output.items():
        decisions.setdefault(item.get('decision', 'ignore'), []).append(ticker)

    lines = ['# Pipeline Report', '']
    if checked_at:
        lines.append(f'_Last pipeline state: {checked_at}_')
        lines.append('')
    lines.append(f'- **Tracked names:** {total}')
    lines.append(f'- **Covered names:** {sum(1 for v in thesis_output.values() if v.get("coverage_status") == "covered")}')
    lines.append(f'- **Filing changes detected:** {sum(1 for v in filing_deltas.values() if v.get("changed"))}')
    lines.append(f'- **Data changes detected:** {sum(1 for v in data_deltas.values() if v.get("changed"))}')
    lines.append('')

    for level in ['high_priority', 'investigate', 'review', 'ignore']:
        tickers = decisions.get(level, [])
        if not tickers:
            continue
        lines.append(f'## {level}')
        lines.append('')
        for ticker in sorted(tickers):
            lines.append(f'- {ticker}')
        lines.append('')

    OUTPUT_PATH.write_text('\n'.join(lines).rstrip() + '\n')
    print(str(OUTPUT_PATH))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
