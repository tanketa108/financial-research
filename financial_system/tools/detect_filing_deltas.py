#!/usr/bin/env python3
"""Detect changes between filing_registry.previous.json and filing_registry.json."""

from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
REGISTRY_DIR = ROOT / 'registry'
CURRENT_PATH = REGISTRY_DIR / 'filing_registry.json'
PREVIOUS_PATH = REGISTRY_DIR / 'filing_registry.previous.json'
DELTAS_PATH = REGISTRY_DIR / 'filing_deltas.json'


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text())


def filing_accession(obj):
    if not obj:
        return None
    return obj.get('accession_number')


def accession_set(items):
    return {item.get('accession_number') for item in (items or []) if item.get('accession_number')}


def detect_company_delta(old: dict | None, new: dict, checked_at: str) -> dict:
    if old is None:
        return {
            'changed': False,
            'new_filing_types': [],
            'changes': [
                {
                    'kind': 'initial_snapshot'
                }
            ],
            'status_change': None,
            'checked_at': checked_at,
        }

    changes = []
    new_filing_types = []

    old_10q = filing_accession(old.get('latest_10q'))
    new_10q = filing_accession(new.get('latest_10q'))
    if old_10q != new_10q:
        changes.append({
            'kind': 'latest_10q_updated',
            'old_accession': old_10q,
            'new_accession': new_10q,
        })
        new_filing_types.append('10-Q')

    old_10k = filing_accession(old.get('latest_10k'))
    new_10k = filing_accession(new.get('latest_10k'))
    if old_10k != new_10k:
        changes.append({
            'kind': 'latest_10k_updated',
            'old_accession': old_10k,
            'new_accession': new_10k,
        })
        new_filing_types.append('10-K')

    old_8k = accession_set(old.get('recent_8k'))
    new_8k = accession_set(new.get('recent_8k'))
    added_8k = sorted(new_8k - old_8k)
    if added_8k:
        changes.append({
            'kind': 'new_8k_detected',
            'new_accessions': added_8k,
        })
        new_filing_types.append('8-K')

    old_status = old.get('status')
    new_status = new.get('status')
    status_change = None
    if old_status != new_status:
        status_change = {
            'old_status': old_status,
            'new_status': new_status,
        }
        changes.append({
            'kind': 'status_change',
            'old_status': old_status,
            'new_status': new_status,
        })

    return {
        'changed': bool(changes),
        'new_filing_types': list(dict.fromkeys(new_filing_types)),
        'changes': changes,
        'status_change': status_change,
        'checked_at': checked_at,
    }


def main() -> int:
    current = load_json(CURRENT_PATH) or {}
    previous = load_json(PREVIOUS_PATH) or {}
    checked_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

    deltas = {}
    for ticker, new_item in current.items():
        old_item = previous.get(ticker)
        deltas[ticker] = detect_company_delta(old_item, new_item, checked_at)

    DELTAS_PATH.write_text(json.dumps(deltas, ensure_ascii=False, indent=2) + '\n')
    print(str(DELTAS_PATH))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
