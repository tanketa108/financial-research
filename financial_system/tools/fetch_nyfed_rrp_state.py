#!/usr/bin/env python3
"""Fetch latest NY Fed reverse repo operation state.

Uses the Federal Reserve Bank of New York Markets API; no API key required.
Writes a compact state file for Macro Monitor v0.
"""

from __future__ import annotations

import csv
import io
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "financial_system" / "macro" / "data" / "nyfed-rrp-state.json"
ENDPOINT = "https://markets.newyorkfed.org/api/rp/reverserepo/all/results/last/90.csv"
USER_AGENT = "financial-research-macro-v0/0.1"


def fetch_csv(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def to_number(value: Any) -> float | None:
    if value in (None, "", "null"):
        return None
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return None


def parse_operation_date(value: str) -> str:
    return datetime.strptime(value, "%m/%d/%Y").date().isoformat()


def normalize_row(row: dict[str, str]) -> dict[str, Any]:
    accepted_bn = to_number(row.get("Total Amt Accepted ($Billions)"))
    submitted_bn = to_number(row.get("Total Amt Submitted ($Billions)"))
    return {
        "operationId": row.get("Operation Id"),
        "operationDate": parse_operation_date(row["Operation Date"]),
        "settlementDate": parse_operation_date(row["Settlement Date"]),
        "maturityDate": parse_operation_date(row["Maturity Date"]),
        "operationType": row.get("Operation Type"),
        "operationMethod": row.get("Operation Method"),
        "term": row.get("Term"),
        "participatingCounterparties": to_number(row.get("Participating Counterparties")),
        "acceptedCounterparties": to_number(row.get("Accepted Counterparties")),
        "totalSubmittedUsdBn": submitted_bn,
        "totalAcceptedUsdBn": accepted_bn,
        "treasuryAcceptedUsdBn": to_number(row.get("Tsy Amt Accepted ($Billions)")),
        "treasuryOfferingRatePct": to_number(row.get("Tsy Offering Rate(%)")),
        "treasuryAwardRatePct": to_number(row.get("Tsy Award Rate (%)")),
        "lastUpdated": row.get("Last Updated"),
        "raw": row,
    }


def build_state(rows: list[dict[str, str]]) -> dict[str, Any]:
    if not rows:
        raise ValueError("NY Fed Markets API returned no reverse repo rows")

    history = [normalize_row(row) for row in rows]
    history.sort(key=lambda x: x["operationDate"], reverse=True)
    latest = history[0]
    prior = history[1] if len(history) > 1 else None
    oldest = history[-1] if len(history) > 1 else None

    one_day_change = None
    if prior and latest.get("totalAcceptedUsdBn") is not None and prior.get("totalAcceptedUsdBn") is not None:
        one_day_change = latest["totalAcceptedUsdBn"] - prior["totalAcceptedUsdBn"]

    window_change = None
    if oldest and latest.get("totalAcceptedUsdBn") is not None and oldest.get("totalAcceptedUsdBn") is not None:
        window_change = latest["totalAcceptedUsdBn"] - oldest["totalAcceptedUsdBn"]

    return {
        "version": "0.1",
        "source": "nyfed_markets_api",
        "sourceUrl": ENDPOINT,
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "units": "USD billions",
        "latest": latest,
        "trend": {
            "historyWindowRecords": len(history),
            "historyLatestFirst": history,
            "oneDayChangeUsdBn": one_day_change,
            "windowChangeUsdBn": window_change,
            "windowStartDate": oldest.get("operationDate") if oldest else None,
            "windowEndDate": latest.get("operationDate"),
        },
        "caveats": [
            "NY Fed reverse repo operation results measure take-up at the operation, not a complete standalone liquidity signal.",
            "Use alongside TGA, reserves and broader funding-market indicators before drawing conclusions.",
        ],
    }


def main() -> int:
    state = build_state(fetch_csv(ENDPOINT))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
