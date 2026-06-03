#!/usr/bin/env python3
"""Fetch latest Treasury General Account / operating cash balance state.

Uses Treasury FiscalData public API; no API key required.
Writes a compact state file for Macro Monitor v0.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "financial_system" / "macro" / "data" / "tga-state.json"
ENDPOINT = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance"
USER_AGENT = "financial-research-macro-v0/0.1"


def fetch_json(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def to_number(value: Any) -> float | None:
    if value in (None, "", "null"):
        return None
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return None


def latest_records(page_size: int = 480) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"page[size]": page_size, "sort": "-record_date"})
    payload = fetch_json(f"{ENDPOINT}?{params}")
    return payload.get("data", [])


def record_dates(records: list[dict[str, Any]]) -> list[str]:
    dates = sorted({r.get("record_date") for r in records if r.get("record_date")}, reverse=True)
    return dates


def build_state(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        raise ValueError("Treasury FiscalData returned no operating cash balance records")

    latest_date = records[0]["record_date"]
    latest = [r for r in records if r.get("record_date") == latest_date]

    history: list[dict[str, Any]] = []
    for record_date in record_dates(records)[:60]:
        rows = [r for r in records if r.get("record_date") == record_date]
        by_account_for_date = {r.get("account_type"): r for r in rows}
        tga_for_date = by_account_for_date.get("Treasury General Account (TGA) Opening Balance")
        if not tga_for_date:
            continue
        history.append({
            "recordDate": record_date,
            "tgaOpeningBalanceUsdMn": to_number(tga_for_date.get("open_today_bal")),
            "openMonthBalanceUsdMn": to_number(tga_for_date.get("open_month_bal")),
            "openFiscalYearBalanceUsdMn": to_number(tga_for_date.get("open_fiscal_year_bal")),
        })

    latest_balance = history[0].get("tgaOpeningBalanceUsdMn") if history else None
    prior_balance = history[1].get("tgaOpeningBalanceUsdMn") if len(history) > 1 else None
    oldest_balance = history[-1].get("tgaOpeningBalanceUsdMn") if len(history) > 1 else None

    one_day_change = None
    if latest_balance is not None and prior_balance is not None:
        one_day_change = latest_balance - prior_balance

    trend_change = None
    if latest_balance is not None and oldest_balance is not None:
        trend_change = latest_balance - oldest_balance

    by_account = {r.get("account_type"): r for r in latest}
    tga = by_account.get("Treasury General Account (TGA) Opening Balance")
    deposits = by_account.get("Total TGA Deposits (Table II)")
    withdrawals = by_account.get("Total TGA Withdrawals (Table II) (-)")

    def extract(row: dict[str, Any] | None) -> dict[str, Any] | None:
        if not row:
            return None
        return {
            "accountType": row.get("account_type"),
            "openTodayBalanceUsdMn": to_number(row.get("open_today_bal")),
            "openMonthBalanceUsdMn": to_number(row.get("open_month_bal")),
            "openFiscalYearBalanceUsdMn": to_number(row.get("open_fiscal_year_bal")),
            "closeTodayBalanceUsdMn": to_number(row.get("close_today_bal")),
            "raw": row,
        }

    return {
        "version": "0.1",
        "source": "treasury_fiscaldata",
        "sourceUrl": ENDPOINT,
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "recordDate": latest_date,
        "units": "USD millions",
        "tgaOpeningBalance": extract(tga),
        "totalTgaDeposits": extract(deposits),
        "totalTgaWithdrawals": extract(withdrawals),
        "tgaTrend": {
            "historyWindowRecords": len(history),
            "historyLatestFirst": history,
            "oneDayChangeUsdMn": one_day_change,
            "windowChangeUsdMn": trend_change,
            "windowStartDate": history[-1]["recordDate"] if history else None,
            "windowEndDate": history[0]["recordDate"] if history else None,
        },
        "recordCountForDate": len(latest),
        "caveats": [
            "Daily Treasury Statement fields are reported by Treasury FiscalData; use source field definitions for exact accounting treatment.",
            "Do not overinterpret one-day TGA moves without broader liquidity context."
        ],
    }


def main() -> int:
    state = build_state(latest_records())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
