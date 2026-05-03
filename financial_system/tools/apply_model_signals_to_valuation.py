#!/usr/bin/env python3
"""Apply extracted workbook valuation signals to a valuation-state file.

Current v1 policy:
- Keep workbook-derived outputs explicit and auditable.
- Avoid pretending ambiguous workbook outputs are more certain than they are.
- Populate valuation_methods and model_context conservatively.
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
VALUATIONS = ROOT / 'valuations'
EXTRACTED = VALUATIONS / 'extracted'


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def build_generic_state(ticker: str) -> dict:
    return {
        'ticker': ticker,
        'name': ticker,
        'status': 'bootstrapped_from_model',
        'latest_period': {},
        'historical_base': {
            'latest_revenue': None,
            'latest_operating_income': None,
            'latest_net_income': None,
            'latest_diluted_eps': None,
            'latest_cash_and_equivalents': None,
            'latest_total_debt': None,
            'revenue_history': [],
            'operating_income_history': [],
            'net_income_history': [],
            'diluted_eps_history': [],
            'cash_history': [],
            'debt_history': [],
            'share_count_history': [],
            'fcf_history': [],
            'capex_history': [],
        },
        'thesis': {'thesis_short': None, 'current_stance': None, 'what_would_change_my_mind': None},
        'segments': [],
        'drivers': [],
        'quality': {'dupont': {'net_margin': None, 'asset_turnover': None, 'financial_leverage': None}, 'roic': {'historical': None, 'expected': None, 'incremental': None}, 'wacc': None, 'eva_spread': None},
        'debt': {'total_debt': None, 'cash': None, 'net_debt': None, 'interest_burden': None, 'maturities': [], 'refinancing_risk': None},
        'cash_conversion': {'working_capital': {'receivables': None, 'payables': None, 'inventories': None}, 'ccc': {'dso': None, 'dpo': None, 'dio': None, 'ccc': None}, 'profit_to_cash_bridge': {'ebit_or_ebitda': None, 'cash_taxes': None, 'capex': None, 'working_capital_impact': None, 'fcf_conversion': None}},
        'capital_allocation': {'buybacks': None, 'dividends': None, 'sbc': None, 'diluted_share_count_evolution': None, 'm_and_a': None, 'notes': None},
        'comparables': {'peer_set': [], 'notes': None},
        'valuation_methods': {
            'dcf': {'status': 'not_filled', 'assumptions': {}, 'output': None, 'range': None},
            'gordon': {'status': 'not_filled', 'assumptions': {}, 'output': None, 'range': None},
            'terminal_multiple': {'status': 'not_filled', 'assumptions': {}, 'output': None, 'range': None},
            'aggregate': {'central_reference': None, 'range': None, 'dispersion': None},
        },
        'sensitivities': {'one_way': [], 'two_way_tables': []},
        'scenarios': [],
        'catalysts': [],
        'risks': [],
        'qualitative_notes': {'moat': None, 'fragilities': None, 'management_quality': None, 'industry_structure': None, 'knowledge_links': []},
        'system_context': {'coverage_status': 'external_model_bootstrap'},
    }


def series_values(signals: dict, key: str):
    row = (signals.get('extracted_rows') or {}).get(key) or {}
    return [item.get('value') for item in row.get('series') or [] if isinstance(item.get('value'), (int, float))]


def first_numeric(signals: dict, key: str):
    vals = series_values(signals, key)
    return vals[0] if vals else None


def last_numeric(signals: dict, key: str):
    vals = series_values(signals, key)
    return vals[-1] if vals else None


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('Usage: apply_model_signals_to_valuation.py <TICKER>', file=sys.stderr)
        return 1

    ticker = argv[1].upper()
    state_path = VALUATIONS / f'{ticker}-valuation-state-v1.json'
    signals_path = EXTRACTED / f'{ticker}-model-signals.json'
    if not signals_path.exists():
        print(f'missing {signals_path}', file=sys.stderr)
        return 1

    if not state_path.exists():
        state = build_generic_state(ticker)
    else:
        state = load_json(state_path)

    if not signals_path.exists():
        print(f'missing {signals_path}', file=sys.stderr)
        return 1

    signals = load_json(signals_path)

    valuation_methods = state.setdefault('valuation_methods', {})
    dcf = valuation_methods.setdefault('dcf', {})
    gordon = valuation_methods.setdefault('gordon', {})
    terminal_multiple = valuation_methods.setdefault('terminal_multiple', {})
    aggregate = valuation_methods.setdefault('aggregate', {})

    gordon_price = first_numeric(signals, 'implied_stock_price_gordon')
    exit_price = first_numeric(signals, 'implied_stock_price_gordon_exit')
    output_signals = signals.get('output_signals') or []

    # Heuristic: hybrid formula row often sits in summary_like_rows under terminal value row.
    hybrid_output = None
    wacc = None
    terminal_growth = None
    for row in signals.get('summary_like_rows') or []:
        if row.get('label') == 'terminal value':
            for cell in row.get('row') or []:
                if cell.get('ref') == 'O54':
                    try:
                        hybrid_output = float(cell.get('value'))
                    except Exception:
                        pass
                if cell.get('ref') == 'L54':
                    try:
                        wacc = float(cell.get('value'))
                    except Exception:
                        pass
        if row.get('label') == 'present value of terminal value':
            for cell in row.get('row') or []:
                if cell.get('ref') == 'L55':
                    try:
                        terminal_growth = float(cell.get('value'))
                    except Exception:
                        pass
        if row.get('label') == 'wacc' and wacc is None:
            for cell in row.get('row') or []:
                if cell.get('ref') == 'Q14':
                    try:
                        wacc = float(cell.get('value'))
                    except Exception:
                        pass

    revenue_forecast = [v for v in series_values(signals, 'revenue') if isinstance(v, (int, float))][-5:]
    growth_forecast = [v for v in series_values(signals, 'growth') if isinstance(v, (int, float))][-5:]
    ebitda_forecast = [v for v in series_values(signals, 'ebitda') if isinstance(v, (int, float))][-5:]
    fcf_forecast = [v for v in series_values(signals, 'fcf') if isinstance(v, (int, float))][-5:]
    pv_fcf_forecast = [v for v in series_values(signals, 'pv_fcf') if isinstance(v, (int, float))][-5:]

    dcf['status'] = 'model_extracted'
    dcf['assumptions'] = {
        'notes': 'Workbook-derived DCF-style outputs extracted heuristically; validate conceptually before treating as final.',
        'wacc': wacc,
        'terminal_growth': terminal_growth,
        'fcf_series_2025e_2029e': fcf_forecast,
        'pv_fcf_series_2025e_2029e': pv_fcf_forecast,
    }
    dcf['output'] = gordon_price
    dcf['range'] = [gordon_price, hybrid_output] if gordon_price is not None and hybrid_output is not None else None
    dcf['confidence'] = 0.65
    dcf['source_status'] = 'extracted_not_validated'

    gordon['status'] = 'model_extracted'
    gordon['assumptions'] = {
        'notes': 'Explicit Gordon output read from workbook.',
        'wacc': wacc,
        'terminal_growth': terminal_growth,
    }
    gordon['output'] = gordon_price
    gordon['range'] = [gordon_price, gordon_price] if gordon_price is not None else None
    gordon['confidence'] = 0.9
    gordon['source_status'] = 'extracted_not_validated'

    terminal_multiple['status'] = 'model_extracted'
    terminal_multiple['assumptions'] = {
        'notes': 'Terminal/exit multiple style output read from workbook; map still heuristic.',
        'wacc': wacc,
        'hybrid_formula_output': hybrid_output,
    }
    terminal_multiple['output'] = exit_price
    terminal_multiple['range'] = [hybrid_output, exit_price] if hybrid_output is not None and exit_price is not None else None
    terminal_multiple['confidence'] = 0.75
    terminal_multiple['source_status'] = 'extracted_not_validated'

    weighted_outputs = [(x.get('value'), x.get('confidence', 0)) for x in output_signals if isinstance(x.get('value'), (int, float))]
    plain_outputs = [x[0] for x in weighted_outputs]
    weighted_sum = sum(v * w for v, w in weighted_outputs)
    weight_total = sum(w for _, w in weighted_outputs)
    weighted_central = (weighted_sum / weight_total) if weight_total else None
    aggregate['central_reference'] = weighted_central
    aggregate['range'] = [min(plain_outputs), max(plain_outputs)] if plain_outputs else None
    aggregate['dispersion'] = (max(plain_outputs) - min(plain_outputs)) if len(plain_outputs) >= 2 else 0
    aggregate['notes'] = 'Central reference is confidence-weighted across workbook-derived outputs pending analyst refinement.'
    aggregate['source_status'] = 'extracted_not_validated'
    aggregate['confidence'] = round(weight_total / len(weighted_outputs), 3) if weighted_outputs else None

    state['model_context'] = {
        'source_file': signals.get('source_file'),
        'signals_file': str(signals_path),
        'years_map': signals.get('years_map'),
        'extracted_model_highlights': {
            'revenue_2025e_2029e': revenue_forecast,
            'growth_2025e_2029e': growth_forecast,
            'ebitda_2025e_2029e': ebitda_forecast,
            'fcf_2025e_2029e': fcf_forecast,
            'wacc': wacc,
            'terminal_growth': terminal_growth,
            'implied_stock_price_gordon': gordon_price,
            'implied_stock_price_terminal_multiple': exit_price,
            'hybrid_formula_output': hybrid_output,
        },
        'output_signals': output_signals,
        'summary': signals.get('summary'),
        'validation': {
            'status': 'extracted_not_validated',
            'validated_by_analyst': False,
        },
        'notes': [
            'Outputs were extracted by the analyst-model-ingestion skill.',
            'Workbook semantics are partially inferred; keep analyst review in the loop.',
        ],
    }

    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    print(state_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
