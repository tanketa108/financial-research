#!/usr/bin/env python3
"""Run a simple thesis monitor over prepared monitor inputs."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
INPUT_PATH = ROOT / 'registry' / 'thesis_monitor_input.json'
OUTPUT_JSON = ROOT / 'registry' / 'thesis_monitor_output.json'
OUTPUT_MD = ROOT / 'outputs' / 'thesis_monitor_output.md'

PRIORITY_ORDER = ['ignore', 'review', 'investigate', 'high_priority']


def escalate(current: str, candidate: str) -> str:
    return candidate if PRIORITY_ORDER.index(candidate) > PRIORITY_ORDER.index(current) else current


def load() -> dict:
    if not INPUT_PATH.exists():
        return {}
    return json.loads(INPUT_PATH.read_text())


def main() -> int:
    data = load()
    output = {}

    for ticker, item in data.items():
        coverage = item.get('coverage_status')
        extraction_quality = item.get('extraction_quality')
        preliminary = item.get('preliminary_priority', 'ignore')
        filing_changed = item.get('filing_delta', {}).get('changed', False)
        data_changed = item.get('data_delta', {}).get('changed', False)

        decision = preliminary
        reasons = []

        if coverage != 'covered':
            decision = escalate(decision, 'review')
            reasons.append(f'coverage gap: coverage_status={coverage}')
        if extraction_quality not in ('validated', 'usable_with_caution'):
            decision = escalate(decision, 'review')
            reasons.append(f'extraction quality issue: extraction_quality={extraction_quality}')
        if filing_changed and not data_changed:
            decision = escalate(decision, 'review')
            reasons.append('filing changed without data delta yet')
        if data_changed:
            reasons.append('data delta detected')
        if preliminary != 'ignore':
            reasons.append(f'preliminary priority from materiality rules: {preliminary}')
        if not reasons:
            reasons.append('no relevant filing/data changes in current baseline')

        output[ticker] = {
            'ticker': ticker,
            'decision': decision,
            'coverage_status': coverage,
            'extraction_quality': extraction_quality,
            'latest_period': item.get('latest_period'),
            'reasons': reasons,
            'preliminary_priority': preliminary,
            'filing_delta': item.get('filing_delta'),
            'data_delta': item.get('data_delta'),
        }

    OUTPUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')

    groups = {k: [] for k in PRIORITY_ORDER}
    for ticker, item in output.items():
        groups[item['decision']].append((ticker, item))

    lines = ['# Thesis Monitor Output', '']
    for level in ['high_priority', 'investigate', 'review', 'ignore']:
        items = groups[level]
        if not items:
            continue
        lines.append(f'## {level}')
        lines.append('')
        for ticker, item in items:
            lines.append(f'### {ticker}')
            lp = item.get('latest_period') or {}
            if lp.get('report_date'):
                lines.append(f"- Latest period: {lp.get('form_type')} | report date {lp.get('report_date')}")
            lines.append(f"- Coverage: {item.get('coverage_status')}")
            lines.append(f"- Extraction quality: {item.get('extraction_quality')}")
            for reason in item.get('reasons', []):
                lines.append(f"- Reason: {reason}")
            lines.append('')

    OUTPUT_MD.write_text('\n'.join(lines).rstrip() + '\n')
    print(str(OUTPUT_JSON))
    print(str(OUTPUT_MD))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
