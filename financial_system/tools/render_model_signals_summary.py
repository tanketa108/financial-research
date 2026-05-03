#!/usr/bin/env python3
"""Render a compact executive markdown summary from <TICKER>-model-signals.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
EXTRACTED = ROOT / 'valuations' / 'extracted'


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('Usage: render_model_signals_summary.py <TICKER>', file=sys.stderr)
        return 1

    ticker = argv[1].upper()
    src = EXTRACTED / f'{ticker}-model-signals.json'
    out = EXTRACTED / f'{ticker}-model-signals-summary.md'
    if not src.exists():
        print(f'missing {src}', file=sys.stderr)
        return 1

    data = load_json(src)
    lines = [f'# {ticker} — Model Signals Summary', '']
    lines.append(f"- Source file: `{data.get('source_file')}`")
    outputs = data.get('output_signals') or []
    summary = data.get('summary') or {}
    lines.append(f"- Output signals detected: {len(outputs)}")
    lines.append('')

    if outputs:
        lines.append('## Output Signals')
        lines.append('')
        for item in outputs:
            lines.append(f"- {item.get('name')}: value={item.get('value')} | method={item.get('method')} | confidence={item.get('confidence')} | validated={item.get('validated')}")
        lines.append('')

    lines.append('## Forecast Snapshot')
    lines.append('')
    lines.append(f"- Revenue 2025E-2029E: {summary.get('revenue_2025e_2029e') or '[missing]'}")
    lines.append(f"- EBITDA 2025E-2029E: {summary.get('ebitda_2025e_2029e') or '[missing]'}")
    lines.append(f"- FCF 2025E-2029E: {summary.get('fcf_2025e_2029e') or '[missing]'}")
    lines.append('')

    out.write_text('\n'.join(lines).rstrip() + '\n')
    print(out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
