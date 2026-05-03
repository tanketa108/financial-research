#!/usr/bin/env python3
"""Prepare thesis monitor input from coverage, filing deltas and data deltas."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
EXTRACTED_REGISTRY = ROOT / 'registry' / 'extracted_financials_registry.json'
FILING_DELTAS = ROOT / 'registry' / 'filing_deltas.json'
DATA_DELTAS = ROOT / 'registry' / 'data_deltas.json'
OUTPUT_PATH = ROOT / 'registry' / 'thesis_monitor_input.json'

QUALITY = {
    'UBER': {'coverage_status': 'covered', 'extraction_quality': 'validated'},
    'MSFT': {'coverage_status': 'covered', 'extraction_quality': 'validated'},
    'NFLX': {'coverage_status': 'covered', 'extraction_quality': 'validated'},
    'DVN': {'coverage_status': 'covered', 'extraction_quality': 'validated'},
    'RACE': {'coverage_status': 'pending_identity_resolution', 'extraction_quality': 'blocked'},
    'NVO': {'coverage_status': 'pending_issuer_strategy', 'extraction_quality': 'blocked'},
}

PRIORITY_ORDER = ['ignore', 'review', 'investigate', 'high_priority']

RULES = {
    'revenue': [(0.03, 'ignore'), (0.07, 'review'), (0.12, 'investigate'), (float('inf'), 'high_priority')],
    'operating_income': [(0.05, 'ignore'), (0.10, 'review'), (0.20, 'investigate'), (float('inf'), 'high_priority')],
    'net_income': [(0.05, 'ignore'), (0.15, 'review'), (0.25, 'investigate'), (float('inf'), 'high_priority')],
    'diluted_eps': [(0.05, 'ignore'), (0.15, 'review'), (0.25, 'investigate'), (float('inf'), 'high_priority')],
    'cash_and_equivalents': [(0.10, 'ignore'), (0.20, 'review'), (0.35, 'investigate'), (float('inf'), 'high_priority')],
    'total_debt': [(0.08, 'ignore'), (0.15, 'review'), (0.25, 'investigate'), (float('inf'), 'high_priority')],
}


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def priority_for_metric(metric: str, change: dict) -> str:
    kinds = set(change.get('kinds', []))
    if 'status_changed' in kinds or 'appeared' in kinds or 'disappeared' in kinds:
        return 'review'
    delta_pct = change.get('delta_pct')
    if delta_pct is None:
        return 'ignore'
    abs_delta = abs(delta_pct)
    for threshold, priority in RULES.get(metric, [(float('inf'), 'ignore')]):
        if abs_delta < threshold:
            return priority
    return 'ignore'


def max_priority(priorities: list[str]) -> str:
    if not priorities:
        return 'ignore'
    return max(priorities, key=lambda p: PRIORITY_ORDER.index(p))


def main() -> int:
    extracted = load(EXTRACTED_REGISTRY)
    filing_deltas = load(FILING_DELTAS)
    data_deltas = load(DATA_DELTAS)

    out = {}
    tickers = sorted(set(extracted) | set(filing_deltas) | set(data_deltas) | set(QUALITY))
    for ticker in tickers:
        info = QUALITY.get(ticker, {'coverage_status': 'unknown', 'extraction_quality': 'not_validated'})
        extracted_item = extracted.get(ticker, {})
        filing_item = filing_deltas.get(ticker, {})
        data_item = data_deltas.get(ticker, {})

        metric_changes = []
        priorities = []
        for change in data_item.get('metric_changes', []) or []:
            metric = change.get('metric')
            priority = priority_for_metric(metric, change)
            row = dict(change)
            row['priority'] = priority
            metric_changes.append(row)
            priorities.append(priority)

        if filing_item.get('changed') and not priorities:
            priorities.append('review')

        preliminary_priority = max_priority(priorities)

        out[ticker] = {
            'ticker': ticker,
            'coverage_status': info['coverage_status'],
            'extraction_quality': info['extraction_quality'],
            'latest_period': extracted_item.get('latest_period'),
            'filing_delta': {
                'changed': filing_item.get('changed', False),
                'new_filing_types': filing_item.get('new_filing_types', []),
                'changes': filing_item.get('changes', []),
            },
            'data_delta': {
                'changed': data_item.get('changed', False),
                'metric_changes': metric_changes,
            },
            'preliminary_priority': preliminary_priority,
            'notes': extracted_item.get('notes', []),
        }

    OUTPUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(str(OUTPUT_PATH))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
