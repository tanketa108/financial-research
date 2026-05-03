#!/usr/bin/env python3
"""Aggregate per-ticker extracted financial outputs into a single registry."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
POSITIONS_PATH = ROOT / 'positions.json'
OUTPUTS_DIR = ROOT / 'outputs'
REGISTRY_PATH = ROOT / 'registry' / 'extracted_financials_registry.json'


def main() -> int:
    positions = json.loads(POSITIONS_PATH.read_text())
    registry = {}

    for position in positions:
        ticker = position['ticker']
        if not position.get('cik'):
            registry[ticker] = {
                'ticker': ticker,
                'status': 'pending_cik_resolution',
                'notes': [position.get('notes')],
            }
            continue

        path = OUTPUTS_DIR / f'{ticker.lower()}_extracted_financials.json'
        if not path.exists():
            registry[ticker] = {
                'ticker': ticker,
                'status': 'not_extracted_yet',
                'notes': [],
            }
            continue

        data = json.loads(path.read_text())
        registry[ticker] = {
            'ticker': ticker,
            'status': 'ok',
            'latest_period': data.get('latest_period'),
            'metrics': data.get('metrics'),
            'source': data.get('source'),
            'source_url': data.get('source_url'),
        }

    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n')
    print(str(REGISTRY_PATH))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
