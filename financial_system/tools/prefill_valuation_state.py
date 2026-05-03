#!/usr/bin/env python3
"""Prefill valuation-state JSON from extracted financial registries and monitor outputs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
EXTRACTED = ROOT / 'registry' / 'extracted_financials_registry.json'
THESIS_OUTPUT = ROOT / 'registry' / 'thesis_monitor_output.json'
VALUATIONS = ROOT / 'valuations'

DRIVER_DEFAULTS = {
    'UBER': [
        'Mobility growth',
        'Delivery profitability',
        'Segment mix shift',
        'Operating leverage',
        'Advertising / ancillary monetization',
        'AV ecosystem structure',
    ],
    'MSFT': [
        'Azure / cloud growth',
        'Operating margin durability',
        'Capital allocation quality',
        'AI monetization path',
        'Productivity / enterprise mix',
    ],
    'NFLX': [
        'Subscriber / revenue growth',
        'Operating leverage',
        'Content efficiency',
        'Advertising monetization',
        'Pricing power',
    ],
}

SEGMENT_DEFAULTS = {
    'UBER': ['Mobility', 'Delivery', 'Freight / Other'],
    'MSFT': ['Productivity & Business Processes', 'Intelligent Cloud', 'More Personal Computing'],
    'NFLX': ['Streaming'],
}

SCENARIO_DEFAULTS = {
    'UBER': [
        ('Network wins / AV integrated into existing network', 'Uber remains the control point of demand/network while AV supply plugs into the platform.', 'Asset-light economics preserved; strong operating leverage.'),
        ('AV ecosystem owns the customer relationship', 'Value shifts toward OEM/AV stack and Uber loses structural control over the network relationship.', 'Lower structural value capture by Uber.'),
        ('Vertical integration / asset-heavy Uber', 'Uber owns or effectively controls fleets and becomes more capital intensive.', 'Lower quality economics, more capex, lower structural margins.'),
        ('Hybrid asset-light central case', 'Uber integrates AV into its network while preserving a mostly asset-light model.', 'Best combination of network value and operating leverage if it works.'),
    ],
    'MSFT': [
        ('AI productivity upside', 'AI monetization deepens enterprise lock-in and pricing power.', 'Higher quality growth and sustained margin strength.'),
        ('Base durable compounder', 'Core franchises continue compounding with strong enterprise economics.', 'High-quality but more normalized valuation path.'),
    ],
    'NFLX': [
        ('Advertising + margin expansion', 'Advertising and scale deepen operating leverage.', 'Higher structural earnings power.'),
        ('Mature streaming normalization', 'Growth moderates and valuation depends on durable cash generation.', 'More mature but still high-quality media platform economics.'),
    ],
}


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def build_state(ticker: str, extracted_item: dict, thesis_item: dict) -> dict:
    latest = extracted_item.get('latest_period') or {}
    metrics = extracted_item.get('metrics') or {}
    debt = metrics.get('total_debt') or {}
    cash = metrics.get('cash_and_equivalents') or {}
    debt_value = debt.get('value')
    cash_value = cash.get('value')
    net_debt = None
    if isinstance(debt_value, (int, float)) and isinstance(cash_value, (int, float)):
        net_debt = debt_value - cash_value

    return {
        'ticker': ticker,
        'name': ticker,
        'status': 'prefilled',
        'latest_period': latest,
        'historical_base': {
            'latest_revenue': (metrics.get('revenue') or {}).get('value'),
            'latest_operating_income': (metrics.get('operating_income') or {}).get('value'),
            'latest_net_income': (metrics.get('net_income') or {}).get('value'),
            'latest_diluted_eps': (metrics.get('diluted_eps') or {}).get('value'),
            'latest_cash_and_equivalents': cash_value,
            'latest_total_debt': debt_value,
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
        'thesis': {
            'thesis_short': None,
            'current_stance': None,
            'what_would_change_my_mind': None,
            'input_owner': 'analyst',
        },
        'segments': [
            {
                'name': name,
                'importance': None,
                'growth_view': None,
                'margin_view': None,
                'notes': None,
                'input_owner': 'hybrid',
            }
            for name in SEGMENT_DEFAULTS.get(ticker, [])
        ],
        'drivers': DRIVER_DEFAULTS.get(ticker, []),
        'quality': {
            'dupont': {'net_margin': None, 'asset_turnover': None, 'financial_leverage': None},
            'roic': {'historical': None, 'expected': None, 'incremental': None},
            'wacc': None,
            'eva_spread': None,
            'input_owner': 'hybrid',
        },
        'debt': {
            'total_debt': debt_value,
            'cash': cash_value,
            'net_debt': net_debt,
            'interest_burden': None,
            'maturities': [],
            'refinancing_risk': None,
            'input_owner': 'hybrid',
        },
        'cash_conversion': {
            'working_capital': {'receivables': None, 'payables': None, 'inventories': None},
            'ccc': {'dso': None, 'dpo': None, 'dio': None, 'ccc': None},
            'profit_to_cash_bridge': {'ebit_or_ebitda': None, 'cash_taxes': None, 'capex': None, 'working_capital_impact': None, 'fcf_conversion': None},
            'input_owner': 'hybrid',
        },
        'capital_allocation': {
            'buybacks': None,
            'dividends': None,
            'sbc': None,
            'diluted_share_count_evolution': None,
            'm_and_a': None,
            'notes': None,
            'input_owner': 'hybrid',
        },
        'comparables': {
            'peer_set': [],
            'notes': None,
            'input_owner': 'analyst',
        },
        'valuation_methods': {
            'dcf': {'status': 'not_filled', 'assumptions': {}, 'output': None, 'range': None, 'input_owner': 'hybrid'},
            'gordon': {'status': 'not_filled', 'assumptions': {}, 'output': None, 'range': None, 'input_owner': 'hybrid'},
            'terminal_multiple': {'status': 'not_filled', 'assumptions': {}, 'output': None, 'range': None, 'input_owner': 'hybrid'},
            'aggregate': {'central_reference': None, 'range': None, 'dispersion': None},
        },
        'sensitivities': {'one_way': [], 'two_way_tables': [], 'input_owner': 'hybrid'},
        'scenarios': [
            {
                'name': name,
                'description': desc,
                'business_model_implication': implication,
                'key_assumptions': [],
                'valuation_implication': None,
                'input_owner': 'analyst',
            }
            for name, desc, implication in SCENARIO_DEFAULTS.get(ticker, [])
        ],
        'catalysts': [],
        'risks': [],
        'qualitative_notes': {
            'moat': None,
            'fragilities': None,
            'management_quality': None,
            'industry_structure': None,
            'knowledge_links': [],
            'input_owner': 'analyst',
        },
        'system_context': {
            'thesis_monitor_decision': thesis_item.get('decision'),
            'coverage_status': thesis_item.get('coverage_status'),
            'extraction_quality': thesis_item.get('extraction_quality'),
        },
    }


def main(argv: list[str]) -> int:
    extracted = load(EXTRACTED)
    thesis_output = load(THESIS_OUTPUT)

    tickers = []
    if len(argv) > 1:
        tickers = [argv[1].upper()]
    else:
        tickers = [ticker for ticker, item in extracted.items() if item.get('status') == 'ok']

    VALUATIONS.mkdir(parents=True, exist_ok=True)
    written = []
    for ticker in tickers:
        extracted_item = extracted.get(ticker)
        if not extracted_item or extracted_item.get('status') != 'ok':
            continue
        state = build_state(ticker, extracted_item, thesis_output.get(ticker, {}))
        out = VALUATIONS / f'{ticker}-valuation-state-v1.json'
        out.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
        written.append(str(out))

    print('\n'.join(written))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
