#!/usr/bin/env python3
"""Add a lightweight normalization layer to valuation states.

This does not try to infer true economic earnings. It only flags and separates
reported metrics from safer operating-reference metrics for later analyst review.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
VALUATIONS = ROOT / 'valuations'


def load_json(path: Path):
    return json.loads(path.read_text())


def safe_div(a, b):
    if a is None or b in (None, 0):
        return None
    try:
        return a / b
    except Exception:
        return None


def main() -> int:
    for path in sorted(VALUATIONS.glob('*-valuation-state-v1.json')):
        state = load_json(path)
        hist = state.get('historical_base', {})
        quality = state.setdefault('quality', {})
        normalization = state.setdefault('normalization', {})

        revenue = hist.get('latest_revenue')
        operating_income = hist.get('latest_operating_income')
        net_income = hist.get('latest_net_income')
        debt = hist.get('latest_total_debt')
        cash = hist.get('latest_cash_and_equivalents')
        net_debt = None
        if isinstance(debt, (int, float)) and isinstance(cash, (int, float)):
            net_debt = debt - cash

        reported_operating_margin = safe_div(operating_income, revenue)
        reported_net_margin = safe_div(net_income, revenue)

        flags = []
        if reported_net_margin is not None and reported_operating_margin is not None:
            if abs(reported_net_margin - reported_operating_margin) > 0.20:
                flags.append('reported_net_margin_far_from_operating_margin')
            if reported_net_margin > reported_operating_margin * 2:
                flags.append('reported_net_income_likely_contains_non_operating_noise')
        if net_debt is not None and revenue is not None and revenue != 0:
            if abs(net_debt) < revenue * 0.05:
                flags.append('net_debt_relatively_small_vs_latest_period_revenue')

        normalization['reported'] = {
            'revenue': revenue,
            'operating_income': operating_income,
            'net_income': net_income,
            'operating_margin': reported_operating_margin,
            'net_margin': reported_net_margin,
        }
        normalization['operating_reference'] = {
            'revenue': revenue,
            'operating_income': operating_income,
            'operating_margin': reported_operating_margin,
            'net_debt': net_debt,
            'analyst_normalized_earnings': None,
            'analyst_normalized_margin': None,
        }
        normalization['flags'] = flags
        normalization['notes'] = [
            'Reported metrics are kept separate from operating-reference metrics.',
            'Net income and net margin may be noisy for valuation unless analyst-normalized.',
            'This layer is only a guardrail, not a substitute for analyst judgment.',
        ]

        quality['reported_vs_normalized_status'] = 'guardrail_added'

        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
        print(path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
