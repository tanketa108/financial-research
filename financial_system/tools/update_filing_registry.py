#!/usr/bin/env python3
"""Refresh filing_registry.json from SEC submissions endpoints."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
POSITIONS_PATH = ROOT / 'positions.json'
OUTPUT_PATH = ROOT / 'registry' / 'filing_registry.json'
USER_AGENT = 'Ander personal research / OpenClaw helper'
NOW = '2026-05-01T21:22:00Z'


def load_positions():
    return json.loads(POSITIONS_PATH.read_text())


def fetch_submissions(cik: str) -> dict:
    url = f'https://data.sec.gov/submissions/CIK{cik}.json'
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def build_filing(cik: str, recent: dict, idx: int) -> dict:
    acc = recent['accessionNumber'][idx]
    doc = recent['primaryDocument'][idx]
    return {
        'accession_number': acc,
        'filing_date': recent['filingDate'][idx],
        'report_date': recent['reportDate'][idx],
        'primary_document': doc,
        'url': f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}",
    }


def main() -> int:
    positions = load_positions()
    registry = {}

    for position in positions:
        ticker = position['ticker']
        cik = position.get('cik')
        if not cik:
            continue
        try:
            data = fetch_submissions(cik)
            recent = data['filings']['recent']
            latest_10q = None
            latest_10k = None
            recent_8k = []
            for i, form in enumerate(recent['form']):
                if form == '10-Q' and latest_10q is None:
                    latest_10q = build_filing(cik, recent, i)
                elif form == '10-K' and latest_10k is None:
                    latest_10k = build_filing(cik, recent, i)
                elif form == '8-K' and len(recent_8k) < 5:
                    recent_8k.append(build_filing(cik, recent, i))
                if latest_10q and latest_10k and len(recent_8k) >= 5:
                    break

            registry[ticker] = {
                'ticker': ticker,
                'cik': cik,
                'latest_10q': latest_10q,
                'latest_10k': latest_10k,
                'recent_8k': recent_8k,
                'has_new_filing': False,
                'new_filing_types': [],
                'status': 'ok',
                'last_checked_at': NOW,
                'notes': [],
            }
        except Exception as exc:
            registry[ticker] = {
                'ticker': ticker,
                'cik': cik,
                'latest_10q': None,
                'latest_10k': None,
                'recent_8k': [],
                'has_new_filing': False,
                'new_filing_types': [],
                'status': 'error',
                'last_checked_at': NOW,
                'notes': [f'update error: {exc}'],
            }

    OUTPUT_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n')
    print(str(OUTPUT_PATH))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
