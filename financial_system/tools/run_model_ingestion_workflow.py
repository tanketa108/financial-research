#!/usr/bin/env python3
"""Single runner: model inventory -> valuation signals -> apply to valuation state -> render.

Usage:
  run_model_ingestion_workflow.py UBER /path/to/model.xlsx
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace')
FS = ROOT / 'financial_system'
SKILLS = ROOT / 'skills' / 'analyst-model-ingestion' / 'tools'
EXTRACTED = FS / 'valuations' / 'extracted'


def run(cmd: list[str]):
    subprocess.run(cmd, check=True)


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print('Usage: run_model_ingestion_workflow.py <TICKER> <MODEL.xlsx>', file=sys.stderr)
        return 1

    ticker = argv[1].upper()
    model_path = Path(argv[2])
    inventory_outdir = EXTRACTED
    signals_out = EXTRACTED / f'{ticker}-model-signals.json'

    run(['python3', str(SKILLS / 'extract_xlsx_inventory.py'), str(model_path), str(inventory_outdir)])
    run(['python3', str(SKILLS / 'extract_valuation_signals.py'), str(model_path), str(signals_out)])
    run(['python3', str(FS / 'tools' / 'apply_model_signals_to_valuation.py'), ticker])
    run(['python3', str(FS / 'tools' / 'render_valuation_state.py'), ticker])

    print(signals_out)
    print(FS / 'valuations' / f'{ticker}-valuation-display-v1.md')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
