#!/usr/bin/env python3
"""Enrich valuation states with additional mechanical balance/cash-conversion fields."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
POSITIONS = ROOT / 'positions.json'
VALUATIONS = ROOT / 'valuations'
USER_AGENT = 'Ander personal research / OpenClaw helper'

BALANCE_TAGS = {
    'receivables': ['AccountsReceivableNetCurrent', 'ReceivablesNetCurrent'],
    'payables': ['AccountsPayableCurrent'],
    'inventory': ['InventoryNet'],
    'shares': ['CommonStockSharesOutstanding', 'CommonStockSharesIssued'],
}

FLOW_TAGS = {
    'capex': ['PaymentsToAcquirePropertyPlantAndEquipment', 'CapitalExpendituresIncurredButNotYetPaid'],
    'depreciation': ['DepreciationDepletionAndAmortization'],
    'stock_comp': ['ShareBasedCompensation'],
    'interest_expense': ['InterestExpenseAndDebtExpense', 'InterestExpense'],
}


def load_json(path: Path):
    return json.loads(path.read_text())


def fetch_companyfacts(cik: str) -> dict:
    url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def latest_matching(us_gaap: dict, tags: list[str], stock: bool) -> dict | None:
    for tag in tags:
        obj = us_gaap.get(tag)
        if not obj:
            continue
        rows = []
        for unit_name, unit_rows in obj.get('units', {}).items():
            if stock:
                if unit_name in ('USD', 'shares', 'pure') or 'shares' in unit_name.lower():
                    rows.extend(unit_rows)
            else:
                if unit_name == 'USD':
                    rows.extend(unit_rows)
        filtered = [r for r in rows if r.get('form') in ('10-Q', '10-K') and r.get('end') and r.get('val') is not None]
        filtered.sort(key=lambda r: (r.get('end', ''), r.get('filed', '')))
        if filtered:
            row = filtered[-1]
            return {
                'tag': tag,
                'value': row.get('val'),
                'end': row.get('end'),
                'filed': row.get('filed'),
                'form': row.get('form'),
                'fy': row.get('fy'),
                'fp': row.get('fp'),
            }
    return None


def main() -> int:
    positions = load_json(POSITIONS)
    for position in positions:
        ticker = position['ticker']
        cik = position.get('cik')
        if not cik:
            continue
        state_path = VALUATIONS / f'{ticker}-valuation-state-v1.json'
        if not state_path.exists():
            continue
        state = load_json(state_path)
        companyfacts = fetch_companyfacts(cik)
        us_gaap = companyfacts.get('facts', {}).get('us-gaap', {})

        cash_conv = state.setdefault('cash_conversion', {})
        wc = cash_conv.setdefault('working_capital', {})
        bridge = cash_conv.setdefault('profit_to_cash_bridge', {})
        debt = state.setdefault('debt', {})
        cap_alloc = state.setdefault('capital_allocation', {})
        hist = state.setdefault('historical_base', {})

        rec = latest_matching(us_gaap, BALANCE_TAGS['receivables'], stock=True)
        pay = latest_matching(us_gaap, BALANCE_TAGS['payables'], stock=True)
        inv = latest_matching(us_gaap, BALANCE_TAGS['inventory'], stock=True)
        shares = latest_matching(us_gaap, BALANCE_TAGS['shares'], stock=True)
        capex = latest_matching(us_gaap, FLOW_TAGS['capex'], stock=False)
        dep = latest_matching(us_gaap, FLOW_TAGS['depreciation'], stock=False)
        sbc = latest_matching(us_gaap, FLOW_TAGS['stock_comp'], stock=False)
        interest = latest_matching(us_gaap, FLOW_TAGS['interest_expense'], stock=False)

        wc['receivables'] = rec
        wc['payables'] = pay
        wc['inventories'] = inv
        bridge['capex'] = capex
        bridge['depreciation'] = dep
        debt['interest_burden'] = interest
        cap_alloc['sbc'] = sbc
        cap_alloc['diluted_share_count_evolution'] = shares
        hist['latest_share_count'] = shares['value'] if shares else hist.get('latest_share_count')

        latest_debt = hist.get('latest_total_debt')
        latest_cash = hist.get('latest_cash_and_equivalents')
        debt['total_debt'] = latest_debt
        debt['cash'] = latest_cash
        if isinstance(latest_debt, (int, float)) and isinstance(latest_cash, (int, float)):
            debt['net_debt'] = latest_debt - latest_cash

        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
        print(state_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
