#!/usr/bin/env python3
"""Build dashboard_state.json from analytical outputs and valuation states."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
EXTRACTED = ROOT / 'registry' / 'extracted_financials_registry.json'
FILING_DELTAS = ROOT / 'registry' / 'filing_deltas.json'
DATA_DELTAS = ROOT / 'registry' / 'data_deltas.json'
THESIS_OUTPUT = ROOT / 'registry' / 'thesis_monitor_output.json'
VALUATIONS = ROOT / 'valuations'
OUTPUT = ROOT / 'registry' / 'dashboard_state.json'


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def load_valuation_state(ticker: str) -> dict:
    path = VALUATIONS / f'{ticker}-valuation-state-v1.json'
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def main() -> int:
    extracted = load(EXTRACTED)
    filing_deltas = load(FILING_DELTAS)
    data_deltas = load(DATA_DELTAS)
    thesis_output = load(THESIS_OUTPUT)

    dashboard = {}
    tickers = sorted(set(thesis_output) | set(extracted))
    for ticker in tickers:
        extracted_item = extracted.get(ticker, {})
        metrics = extracted_item.get('metrics', {})
        thesis_item = thesis_output.get(ticker, {})
        filing_item = filing_deltas.get(ticker, {})
        data_item = data_deltas.get(ticker, {})
        valuation = load_valuation_state(ticker)
        aggregate = (valuation.get('valuation_methods') or {}).get('aggregate', {})
        thesis = valuation.get('thesis') or {}
        scenarios = valuation.get('scenarios') or []
        quality = valuation.get('quality') or {}
        cash_conv = valuation.get('cash_conversion') or {}
        cap_alloc = valuation.get('capital_allocation') or {}
        normalization = valuation.get('normalization') or {}

        hist = valuation.get('historical_base') or {}
        dashboard[ticker] = {
            'ticker': ticker,
            'coverage_status': thesis_item.get('coverage_status'),
            'update_status': {
                'latest_filing_date': (extracted_item.get('latest_period') or {}).get('filing_date'),
                'latest_report_date': (extracted_item.get('latest_period') or {}).get('report_date'),
                'filing_delta_changed': filing_item.get('changed', False),
                'data_delta_changed': data_item.get('changed', False),
                'thesis_monitor_decision': thesis_item.get('decision'),
            },
            'valuation_status': {
                'status': valuation.get('status'),
                'methods_filled': sum(1 for m in ['dcf', 'gordon', 'terminal_multiple'] if ((valuation.get('valuation_methods') or {}).get(m) or {}).get('output') is not None),
                'central_reference': aggregate.get('central_reference'),
                'range': aggregate.get('range'),
                'history_points': {
                    'revenue': len(hist.get('revenue_history') or []),
                    'operating_income': len(hist.get('operating_income_history') or []),
                    'net_income': len(hist.get('net_income_history') or []),
                    'diluted_eps': len(hist.get('diluted_eps_history') or []),
                    'cash': len(hist.get('cash_history') or []),
                    'debt': len(hist.get('debt_history') or []),
                },
                'normalization_status': quality.get('reported_vs_normalized_status'),
                'normalization_flags': normalization.get('flags') or [],
            },
            'thesis_status': {
                'thesis_short': thesis.get('thesis_short'),
                'current_stance': thesis.get('current_stance'),
                'scenario_central': next((s.get('name') for s in scenarios if 'central' in (s.get('name') or '').lower()), None),
            },
            'key_metrics': {
                'revenue': (metrics.get('revenue') or {}).get('value'),
                'operating_income': (metrics.get('operating_income') or {}).get('value'),
                'net_income': (metrics.get('net_income') or {}).get('value'),
                'diluted_eps': (metrics.get('diluted_eps') or {}).get('value'),
                'cash': (metrics.get('cash_and_equivalents') or {}).get('value'),
                'debt': (metrics.get('total_debt') or {}).get('value'),
                'operating_margin': quality.get('operating_margin'),
                'net_margin': quality.get('net_margin'),
                'ccc': ((cash_conv.get('ccc') or {}).get('ccc')),
                'share_count': hist.get('latest_share_count'),
                'sbc': ((cap_alloc.get('sbc') or {}).get('value')),
            },
            'key_risks': valuation.get('risks') or [],
            'key_catalysts': valuation.get('catalysts') or [],
        }

    OUTPUT.write_text(json.dumps(dashboard, ensure_ascii=False, indent=2) + '\n')
    print(str(OUTPUT))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
