#!/usr/bin/env python3
"""Render a human-readable data delta summary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
DELTAS_PATH = ROOT / 'registry' / 'data_deltas.json'
OUTPUT_PATH = ROOT / 'outputs' / 'data_deltas.md'


def main() -> int:
    deltas = json.loads(DELTAS_PATH.read_text())

    changed = []
    unchanged = []
    initial = []

    for ticker, item in deltas.items():
        kinds = [c.get('kind') for c in item.get('changes', []) or []]
        if kinds == ['initial_snapshot']:
            initial.append((ticker, item))
        elif item.get('changed'):
            changed.append((ticker, item))
        else:
            unchanged.append((ticker, item))

    lines = ['# Data Deltas', '']
    sample_ts = next((item.get('checked_at') for item in deltas.values() if item.get('checked_at')), None)
    if sample_ts:
        lines.append(f'_Checked at: {sample_ts}_')
        lines.append('')

    if changed:
        lines.append('## Changed')
        lines.append('')
        for ticker, item in changed:
            lines.append(f'### {ticker}')
            for change in item.get('metric_changes', []):
                metric = change.get('metric')
                old_value = change.get('old_value')
                new_value = change.get('new_value')
                delta_pct = change.get('delta_pct')
                unit = change.get('unit') or ''
                if delta_pct is None:
                    lines.append(f'- {metric}: `{old_value}` → `{new_value}` {unit}'.rstrip())
                else:
                    lines.append(f'- {metric}: `{old_value}` → `{new_value}` {unit} ({delta_pct:+.1%})'.rstrip())
            lines.append('')

    if unchanged:
        lines.append('## No Changes')
        lines.append('')
        for ticker, item in unchanged:
            status = item.get('status')
            if status == 'ok':
                lines.append(f'- {ticker}')
        lines.append('')

    pending = [ticker for ticker, item in unchanged if item.get('status') != 'ok']
    if pending:
        lines.append('## Pending Coverage / Resolution')
        lines.append('')
        for ticker in pending:
            lines.append(f'- {ticker}')
        lines.append('')

    if initial:
        lines.append('## Initial Snapshot')
        lines.append('')
        for ticker, _ in initial:
            lines.append(f'- {ticker}')
        lines.append('')

    if not changed and not unchanged and not initial:
        lines.append('No data delta available.')

    OUTPUT_PATH.write_text('\n'.join(lines).rstrip() + '\n')
    print(str(OUTPUT_PATH))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
