#!/usr/bin/env python3
"""Enrich valuation-state history fields from SEC companyfacts."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
POSITIONS = ROOT / 'positions.json'
VALUATIONS = ROOT / 'valuations'
EXTRACTED_REGISTRY = ROOT / 'registry' / 'extracted_financials_registry.json'
USER_AGENT = 'Ander personal research / OpenClaw helper'

HISTORY_TAGS = {
    'revenue_history': ['RevenueFromContractWithCustomerExcludingAssessedTax', 'SalesRevenueNet', 'Revenues'],
    'operating_income_history': ['OperatingIncomeLoss'],
    'net_income_history': ['NetIncomeLoss', 'ProfitLoss'],
    'diluted_eps_history': ['EarningsPerShareDiluted'],
    'cash_history': ['CashAndCashEquivalentsAtCarryingValue'],
    'debt_history': ['LongTermDebtNoncurrent', 'LongTermDebt', 'DebtInstrumentFaceAmount'],
}


def load_json(path: Path):
    return json.loads(path.read_text())


def fetch_companyfacts(cik: str) -> dict:
    url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def pick_series(us_gaap: dict, tags: list[str], period_type: str) -> list[dict]:
    for tag in tags:
        obj = us_gaap.get(tag)
        if not obj:
            continue
        rows = obj.get('units', {}).get('USD', []) if 'EarningsPerShareDiluted' not in tags else []
        if 'EarningsPerShareDiluted' in tags:
            for unit_name, unit_rows in obj.get('units', {}).items():
                if 'USD' in unit_name and ('shares' in unit_name or '/share' in unit_name.lower() or 'shar' in unit_name.lower()):
                    rows.extend(unit_rows)
        filtered = []
        for row in rows:
            form = row.get('form')
            fp = row.get('fp')
            end = row.get('end')
            val = row.get('val')
            if form not in ('10-Q', '10-K') or end is None or val is None:
                continue
            if period_type == 'flow' and fp not in ('Q1', 'Q2', 'Q3', 'FY'):
                continue
            filtered.append({
                'tag': tag,
                'fy': row.get('fy'),
                'fp': fp,
                'form': form,
                'filed': row.get('filed'),
                'end': end,
                'value': val,
                'frame': row.get('frame'),
            })
        filtered.sort(key=lambda r: (r.get('end', ''), r.get('filed', '')))
        # dedupe by end taking latest filed
        dedup = {}
        for row in filtered:
            dedup[row['end']] = row
        series = list(dedup.values())[-8:]
        if series:
            return series
    return []


def main() -> int:
    positions = load_json(POSITIONS)
    extracted_registry = load_json(EXTRACTED_REGISTRY) if EXTRACTED_REGISTRY.exists() else {}
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
        hist = state.setdefault('historical_base', {})
        hist['revenue_history'] = pick_series(us_gaap, HISTORY_TAGS['revenue_history'], 'flow')
        hist['operating_income_history'] = pick_series(us_gaap, HISTORY_TAGS['operating_income_history'], 'flow')
        hist['net_income_history'] = pick_series(us_gaap, HISTORY_TAGS['net_income_history'], 'flow')
        hist['diluted_eps_history'] = pick_series(us_gaap, HISTORY_TAGS['diluted_eps_history'], 'flow')
        hist['cash_history'] = pick_series(us_gaap, HISTORY_TAGS['cash_history'], 'stock')
        hist['debt_history'] = pick_series(us_gaap, HISTORY_TAGS['debt_history'], 'stock')

        extracted_item = extracted_registry.get(ticker, {})
        metrics = extracted_item.get('metrics') or {}

        hist['latest_revenue'] = ((metrics.get('revenue') or {}).get('value')
            if (metrics.get('revenue') or {}).get('value') is not None
            else (hist['revenue_history'][-1]['value'] if hist['revenue_history'] else None))
        hist['latest_operating_income'] = ((metrics.get('operating_income') or {}).get('value')
            if (metrics.get('operating_income') or {}).get('value') is not None
            else (hist['operating_income_history'][-1]['value'] if hist['operating_income_history'] else None))
        hist['latest_net_income'] = ((metrics.get('net_income') or {}).get('value')
            if (metrics.get('net_income') or {}).get('value') is not None
            else (hist['net_income_history'][-1]['value'] if hist['net_income_history'] else None))
        hist['latest_diluted_eps'] = ((metrics.get('diluted_eps') or {}).get('value')
            if (metrics.get('diluted_eps') or {}).get('value') is not None
            else (hist['diluted_eps_history'][-1]['value'] if hist['diluted_eps_history'] else None))
        hist['latest_cash_and_equivalents'] = ((metrics.get('cash_and_equivalents') or {}).get('value')
            if (metrics.get('cash_and_equivalents') or {}).get('value') is not None
            else (hist['cash_history'][-1]['value'] if hist['cash_history'] else None))
        hist['latest_total_debt'] = ((metrics.get('total_debt') or {}).get('value')
            if (metrics.get('total_debt') or {}).get('value') is not None
            else (hist['debt_history'][-1]['value'] if hist['debt_history'] else None))

        if extracted_item.get('latest_period'):
            state['latest_period'] = extracted_item['latest_period']

        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
        print(state_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
