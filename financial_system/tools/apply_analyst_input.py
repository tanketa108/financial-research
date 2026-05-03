#!/usr/bin/env python3
"""Apply analyst-input JSON on top of valuation-state JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
VALUATIONS = ROOT / 'valuations'

MERGE_KEYS = [
    'thesis',
    'segments',
    'drivers',
    'scenarios',
    'catalysts',
    'risks',
    'qualitative_notes',
    'valuation_methods',
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('Usage: apply_analyst_input.py <TICKER>', file=sys.stderr)
        return 1

    ticker = argv[1].upper()
    state_path = VALUATIONS / f'{ticker}-valuation-state-v1.json'
    input_path = VALUATIONS / f'{ticker}-analyst-input-v1.json'

    if not state_path.exists():
        print(f'missing {state_path}', file=sys.stderr)
        return 1
    if not input_path.exists():
        print(f'missing {input_path}', file=sys.stderr)
        return 1

    state = load_json(state_path)
    analyst_input = load_json(input_path)

    for key in MERGE_KEYS:
        if key in analyst_input:
            state[key] = analyst_input[key]

    state.setdefault('input_meta', {})['analyst_input_applied'] = True
    state['input_meta']['analyst_input_source'] = str(input_path)

    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    print(str(state_path))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
