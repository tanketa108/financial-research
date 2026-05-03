#!/usr/bin/env python3
"""Extract canonical financial metrics from SEC companyfacts using metric mapping v1."""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
POSITIONS_PATH = ROOT / 'positions.json'
MAPPING_PATH = ROOT / 'config' / 'metric_mapping_v1.json'
FILING_REGISTRY_PATH = ROOT / 'registry' / 'filing_registry.json'
OUTPUT_DIR = ROOT / 'outputs'
USER_AGENT = 'Ander personal research / OpenClaw helper'


def load_positions():
    return json.loads(POSITIONS_PATH.read_text())


def load_mapping():
    return json.loads(MAPPING_PATH.read_text())


def load_filing_registry():
    return json.loads(FILING_REGISTRY_PATH.read_text())


def fetch_companyfacts(cik: str) -> dict:
    url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def pick_best_record(records: list[dict], target_form: str | None, target_end: str | None, target_filed: str | None, allow_loose_fallback: bool = False) -> dict | None:
    filtered = [r for r in records if r.get('form') and r.get('filed') and r.get('end')]
    if not filtered:
        return None

    exact = [
        r for r in filtered
        if (not target_form or r.get('form') == target_form)
        and (not target_end or r.get('end') == target_end)
        and (not target_filed or r.get('filed') == target_filed)
    ]
    if exact:
        exact.sort(key=lambda r: (r.get('filed', ''), r.get('end', ''), r.get('fy', 0), r.get('fp', '')))
        return exact[-1]

    same_filed = [
        r for r in filtered
        if (not target_form or r.get('form') == target_form)
        and (not target_filed or r.get('filed') == target_filed)
    ]
    if same_filed:
        same_filed.sort(key=lambda r: (r.get('end', ''), r.get('fy', 0), r.get('fp', '')))
        return same_filed[-1]

    same_end = [
        r for r in filtered
        if (not target_form or r.get('form') == target_form)
        and (not target_end or r.get('end') == target_end)
    ]
    if same_end:
        same_end.sort(key=lambda r: (r.get('filed', ''), r.get('fy', 0), r.get('fp', '')))
        return same_end[-1]

    if not allow_loose_fallback:
        return None

    filtered.sort(key=lambda r: (r.get('filed', ''), r.get('end', ''), r.get('fy', 0), r.get('fp', '')))
    return filtered[-1]


def extract_metric(us_gaap: dict, metric_name: str, metric_cfg: dict, target_form: str | None, target_end: str | None, target_filed: str | None) -> dict:
    expected_unit = metric_cfg.get('expected_unit')
    prepared = []
    for tag in metric_cfg.get('candidate_tags', []):
        tag_obj = us_gaap.get(tag)
        if not tag_obj:
            continue
        units = tag_obj.get('units', {})
        candidates = []
        for unit_name, rows in units.items():
            if expected_unit == 'USD/share':
                if 'USD' in unit_name and ('shares' in unit_name or '/share' in unit_name.lower() or 'shar' in unit_name.lower()):
                    candidates.extend(rows)
            elif expected_unit == 'USD':
                if unit_name == 'USD':
                    candidates.extend(rows)
            else:
                candidates.extend(rows)
        prepared.append((tag, candidates))

    for tag, candidates in prepared:
        best = pick_best_record(candidates, target_form=target_form, target_end=target_end, target_filed=target_filed, allow_loose_fallback=False)
        if best:
            unit = 'USD/share' if expected_unit == 'USD/share' else expected_unit
            return {
                'value': best.get('val'),
                'unit': unit,
                'tag': tag,
                'filed': best.get('filed'),
                'end': best.get('end'),
                'frame': best.get('frame'),
                'fy': best.get('fy'),
                'fp': best.get('fp'),
                'form': best.get('form'),
                'status': 'ok',
            }

    for tag, candidates in prepared:
        best = pick_best_record(candidates, target_form=target_form, target_end=target_end, target_filed=target_filed, allow_loose_fallback=True)
        if best:
            unit = 'USD/share' if expected_unit == 'USD/share' else expected_unit
            return {
                'value': best.get('val'),
                'unit': unit,
                'tag': tag,
                'filed': best.get('filed'),
                'end': best.get('end'),
                'frame': best.get('frame'),
                'fy': best.get('fy'),
                'fp': best.get('fp'),
                'form': best.get('form'),
                'status': 'fallback_ok',
            }
    return {
        'value': None,
        'unit': expected_unit,
        'tag': None,
        'filed': None,
        'end': None,
        'frame': None,
        'fy': None,
        'fp': None,
        'form': None,
        'status': 'not_found',
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('Usage: extract_financial_metrics.py <TICKER>', file=sys.stderr)
        return 1
    ticker = argv[1].upper()
    positions = load_positions()
    mapping = load_mapping()
    filing_registry = load_filing_registry()

    position = next((p for p in positions if p.get('ticker') == ticker), None)
    if not position:
        print(f'Unknown ticker: {ticker}', file=sys.stderr)
        return 1
    cik = position.get('cik')
    if not cik:
        print(f'Ticker has no resolved CIK: {ticker}', file=sys.stderr)
        return 1

    companyfacts = fetch_companyfacts(cik)
    us_gaap = companyfacts.get('facts', {}).get('us-gaap', {})

    filing_info = filing_registry.get(ticker, {})
    target_filing = filing_info.get('latest_10q') or filing_info.get('latest_10k') or {}
    target_form = '10-Q' if filing_info.get('latest_10q') else ('10-K' if filing_info.get('latest_10k') else None)
    target_end = target_filing.get('report_date')
    target_filed = target_filing.get('filing_date')

    metrics = {
        name: extract_metric(us_gaap, name, cfg, target_form=target_form, target_end=target_end, target_filed=target_filed)
        for name, cfg in mapping.items()
    }

    latest_metric = None
    for key in ['revenue', 'operating_income', 'net_income', 'diluted_eps']:
        if metrics.get(key, {}).get('status') == 'ok':
            latest_metric = metrics[key]
            break

    result = {
        'ticker': ticker,
        'cik': cik,
        'source': 'sec_companyfacts',
        'source_url': f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',
        'latest_period': {
            'form_type': target_form or (latest_metric.get('form') if latest_metric else None),
            'filing_date': target_filing.get('filing_date') or (latest_metric.get('filed') if latest_metric else None),
            'report_date': target_end or (latest_metric.get('end') if latest_metric else None),
            'fiscal_year': latest_metric.get('fy') if latest_metric else None,
            'fiscal_period': latest_metric.get('fp') if latest_metric else None,
        },
        'metrics': metrics,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f'{ticker.lower()}_extracted_financials.json'
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(str(output_path))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
