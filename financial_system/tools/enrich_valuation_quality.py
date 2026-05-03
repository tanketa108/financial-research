#!/usr/bin/env python3
"""Enrich valuation states with basic quality metrics (margins, simple ROIC-like pieces)."""

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


def latest_value(series: list[dict]) -> float | None:
    if not series:
        return None
    return series[-1].get('value')


def main() -> int:
    for path in sorted(VALUATIONS.glob('*-valuation-state-v1.json')):
        state = load_json(path)
        hist = state.get('historical_base', {})
        quality = state.setdefault('quality', {})
        dupont = quality.setdefault('dupont', {})
        roic = quality.setdefault('roic', {})
        cash_conv = state.setdefault('cash_conversion', {})
        ccc = cash_conv.setdefault('ccc', {})

        latest_revenue = hist.get('latest_revenue')
        latest_operating_income = hist.get('latest_operating_income')
        latest_net_income = hist.get('latest_net_income')
        latest_cash = hist.get('latest_cash_and_equivalents')
        latest_debt = hist.get('latest_total_debt')
        latest_receivables = ((cash_conv.get('working_capital') or {}).get('receivables') or {}).get('value')
        latest_payables = ((cash_conv.get('working_capital') or {}).get('payables') or {}).get('value')
        latest_inventory = ((cash_conv.get('working_capital') or {}).get('inventories') or {}).get('value')

        operating_margin = safe_div(latest_operating_income, latest_revenue)
        net_margin = safe_div(latest_net_income, latest_revenue)
        dupont['net_margin'] = net_margin
        dupont['asset_turnover'] = None
        dupont['financial_leverage'] = None

        # Simple placeholder quality pieces, explicit about limits.
        quality['operating_margin'] = operating_margin
        quality['net_margin'] = net_margin
        roic['historical'] = None
        roic['expected'] = None
        roic['incremental'] = None
        quality['wacc'] = None
        quality['eva_spread'] = None
        quality['notes'] = [
            'Basic margin metrics prefilled mechanically',
            'ROIC/WACC still require deeper balance-sheet and analyst normalization work',
        ]

        # Very lightweight CCC component estimates where possible.
        if latest_revenue and latest_receivables is not None:
            ccc['dso'] = (latest_receivables / latest_revenue) * 365
        if latest_revenue and latest_payables is not None:
            ccc['dpo'] = (latest_payables / latest_revenue) * 365
        if latest_revenue and latest_inventory is not None:
            ccc['dio'] = (latest_inventory / latest_revenue) * 365
        dso = ccc.get('dso')
        dpo = ccc.get('dpo')
        dio = ccc.get('dio')
        if dso is not None or dpo is not None or dio is not None:
            ccc['ccc'] = (dio or 0) + (dso or 0) - (dpo or 0)

        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
        print(path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
