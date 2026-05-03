#!/usr/bin/env python3
"""Render a human-readable filing delta summary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
DELTAS_PATH = ROOT / 'registry' / 'filing_deltas.json'
OUTPUT_PATH = ROOT / 'outputs' / 'filing_deltas.md'


def main() -> int:
    deltas = json.loads(DELTAS_PATH.read_text())

    changed = []
    unchanged = []
    initial = []

    for ticker, item in deltas.items():
        changes = item.get('changes', []) or []
        kinds = [c.get('kind') for c in changes]
        if kinds == ['initial_snapshot']:
            initial.append((ticker, item))
        elif item.get('changed'):
            changed.append((ticker, item))
        else:
            unchanged.append((ticker, item))

    lines = ['# Filing Deltas', '']

    sample_ts = None
    for _, item in deltas.items():
        sample_ts = item.get('checked_at')
        if sample_ts:
            break
    if sample_ts:
        lines.append(f'_Checked at: {sample_ts}_')
        lines.append('')

    if changed:
        lines.append('## Changed')
        lines.append('')
        for ticker, item in changed:
            nft = item.get('new_filing_types') or []
            lines.append(f'### {ticker}')
            lines.append(f"- **New filing types:** {', '.join(nft) if nft else 'unspecified'}")
            for change in item.get('changes', []):
                kind = change.get('kind')
                if kind == 'latest_10q_updated':
                    lines.append(f"- 10-Q updated: `{change.get('old_accession')}` → `{change.get('new_accession')}`")
                elif kind == 'latest_10k_updated':
                    lines.append(f"- 10-K updated: `{change.get('old_accession')}` → `{change.get('new_accession')}`")
                elif kind == 'new_8k_detected':
                    lines.append(f"- New 8-K accessions: {', '.join(change.get('new_accessions', []))}")
                elif kind == 'status_change':
                    lines.append(f"- Status: `{change.get('old_status')}` → `{change.get('new_status')}`")
                elif kind == 'new_company_added':
                    lines.append('- New company added to coverage')
            lines.append('')

    if unchanged:
        lines.append('## No Changes')
        lines.append('')
        for ticker, _ in unchanged:
            lines.append(f'- {ticker}')
        lines.append('')

    if initial:
        lines.append('## Initial Snapshot')
        lines.append('')
        lines.append('These names have no prior comparison baseline yet:')
        lines.append('')
        for ticker, _ in initial:
            lines.append(f'- {ticker}')
        lines.append('')

    if not changed and not unchanged and not initial:
        lines.append('No delta data available.')

    OUTPUT_PATH.write_text('\n'.join(lines).rstrip() + '\n')
    print(str(OUTPUT_PATH))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
