#!/usr/bin/env python3
"""Run the financial system pipeline v1 in sequence."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
REGISTRY = ROOT / 'registry'
TOOLS = ROOT / 'tools'
POSITIONS = ROOT / 'positions.json'

FILING_REGISTRY = REGISTRY / 'filing_registry.json'
FILING_PREV = REGISTRY / 'filing_registry.previous.json'
EXTRACTED_REGISTRY = REGISTRY / 'extracted_financials_registry.json'
EXTRACTED_PREV = REGISTRY / 'extracted_financials_registry.previous.json'


def load_positions():
    return json.loads(POSITIONS.read_text())


def snapshot(src: Path, dst: Path) -> None:
    if src.exists():
        shutil.copy2(src, dst)


def run_step(args: list[str]) -> None:
    subprocess.run(args, check=True)


def main(argv: list[str]) -> int:
    mode = argv[1] if len(argv) > 1 else 'baseline'
    if mode not in {'baseline', 'incremental'}:
        print('Usage: run_pipeline_v1.py [baseline|incremental]', file=sys.stderr)
        return 1

    if mode == 'incremental':
        snapshot(FILING_REGISTRY, FILING_PREV)
        snapshot(EXTRACTED_REGISTRY, EXTRACTED_PREV)

    run_step(['python3', str(TOOLS / 'update_filing_registry.py')])
    run_step(['python3', str(TOOLS / 'render_filing_summary.py')])
    run_step(['python3', str(TOOLS / 'detect_filing_deltas.py')])
    run_step(['python3', str(TOOLS / 'render_filing_deltas.py')])

    positions = load_positions()
    for position in positions:
        ticker = position['ticker']
        if not position.get('cik'):
            continue
        run_step(['python3', str(TOOLS / 'extract_financial_metrics.py'), ticker])

    run_step(['python3', str(TOOLS / 'build_extracted_financials_registry.py')])
    run_step(['python3', str(TOOLS / 'detect_data_deltas.py')])
    run_step(['python3', str(TOOLS / 'render_data_deltas.py')])
    run_step(['python3', str(TOOLS / 'prepare_thesis_monitor_input.py')])
    run_step(['python3', str(TOOLS / 'run_thesis_monitor.py')])
    run_step(['python3', str(TOOLS / 'render_pipeline_report.py')])

    print('pipeline_v1_complete')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
