#!/usr/bin/env python3
"""Detect metric-level deltas between extracted financial registries."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
REGISTRY_DIR = ROOT / 'registry'
CURRENT_PATH = REGISTRY_DIR / 'extracted_financials_registry.json'
PREVIOUS_PATH = REGISTRY_DIR / 'extracted_financials_registry.previous.json'
DELTAS_PATH = REGISTRY_DIR / 'data_deltas.json'

METRICS = [
    'revenue',
    'operating_income',
    'net_income',
    'diluted_eps',
    'cash_and_equivalents',
    'total_debt',
]


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def metric_change(metric: str, old: dict | None, new: dict | None) -> dict | None:
    old = old or {}
    new = new or {}
    old_value = old.get('value')
    new_value = new.get('value')
    old_status = old.get('status')
    new_status = new.get('status')

    changed = False
    kind = []
    if old_status != new_status:
        changed = True
        kind.append('status_changed')
    if old_value is None and new_value is not None:
        changed = True
        kind.append('appeared')
    elif old_value is not None and new_value is None:
        changed = True
        kind.append('disappeared')
    elif old_value != new_value:
        changed = True
        kind.append('value_changed')

    if not changed:
        return None

    delta = None
    delta_pct = None
    if isinstance(old_value, (int, float)) and isinstance(new_value, (int, float)):
        delta = new_value - old_value
        if old_value != 0:
            delta_pct = delta / old_value

    return {
        'metric': metric,
        'kinds': kind,
        'old_value': old_value,
        'new_value': new_value,
        'delta': delta,
        'delta_pct': delta_pct,
        'old_status': old_status,
        'new_status': new_status,
        'unit': new.get('unit') or old.get('unit'),
    }


def detect_company_delta(old: dict | None, new: dict, checked_at: str) -> dict:
    if old is None:
        return {
            'changed': False,
            'status': new.get('status'),
            'metric_changes': [],
            'changes': [{'kind': 'initial_snapshot'}],
            'checked_at': checked_at,
        }

    changes = []
    metric_changes = []

    if old.get('status') != new.get('status'):
        changes.append({
            'kind': 'company_status_changed',
            'old_status': old.get('status'),
            'new_status': new.get('status'),
        })

    old_metrics = old.get('metrics', {})
    new_metrics = new.get('metrics', {})
    for metric in METRICS:
        change = metric_change(metric, old_metrics.get(metric), new_metrics.get(metric))
        if change:
            metric_changes.append(change)

    return {
        'changed': bool(changes or metric_changes),
        'status': new.get('status'),
        'metric_changes': metric_changes,
        'changes': changes,
        'checked_at': checked_at,
    }


def main() -> int:
    current = load_json(CURRENT_PATH)
    previous = load_json(PREVIOUS_PATH)
    checked_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

    deltas = {}
    for ticker, new_item in current.items():
        deltas[ticker] = detect_company_delta(previous.get(ticker), new_item, checked_at)

    DELTAS_PATH.write_text(json.dumps(deltas, ensure_ascii=False, indent=2) + '\n')
    print(str(DELTAS_PATH))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
