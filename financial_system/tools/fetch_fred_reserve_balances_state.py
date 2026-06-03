#!/usr/bin/env python3
"""Fetch Fed reserve balances state from FRED public CSV.

Uses the FRED graph CSV endpoint, which is publicly reachable without an API key.
Series: WRESBAL — Reserve Balances with Federal Reserve Banks.
Writes a compact state file for Macro Monitor v0.
"""

from __future__ import annotations

import csv
import io
import json
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "financial_system" / "macro" / "data" / "fed-reserve-balances-state.json"
SERIES_ID = "WRESBAL"
# Limit the public CSV to recent observations; full-history downloads can be slow
# from the FRED graph endpoint and are unnecessary for the v0 trend window.
ENDPOINT = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}&cosd=2026-01-01"
USER_AGENT = "Mozilla/5.0 financial-research-macro-v0/0.1"
HISTORY_WINDOW = 10


def fetch_csv(url: str, attempts: int = 3) -> list[dict[str, str]]:
    # Prefer curl in this environment: the FRED endpoint is reliably fast via
    # curl while Python urllib can intermittently hang on TLS reads.
    try:
        text = subprocess.check_output(
            ["curl", "-L", "--fail", "--silent", "--show-error", "--max-time", "20", url],
            text=True,
        )
        return list(csv.DictReader(io.StringIO(text)))
    except Exception:
        pass

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                text = resp.read().decode("utf-8-sig")
            return list(csv.DictReader(io.StringIO(text)))
        except Exception as exc:  # noqa: BLE001 - CLI fetcher should surface final network error clearly.
            last_error = exc
            if attempt < attempts:
                time.sleep(attempt * 2)
    raise RuntimeError(f"failed to fetch FRED public CSV after {attempts} attempts: {last_error}")


def to_number(value: Any) -> float | None:
    if value in (None, "", ".", "null"):
        return None
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return None


def normalize_row(row: dict[str, str]) -> dict[str, Any] | None:
    value = to_number(row.get(SERIES_ID))
    if value is None:
        return None
    return {
        "observationDate": row.get("observation_date"),
        "reserveBalancesUsdMn": value,
    }


def build_state(rows: list[dict[str, str]]) -> dict[str, Any]:
    history_all = [point for row in rows if (point := normalize_row(row))]
    if not history_all:
        raise ValueError("FRED public CSV returned no reserve balance observations")

    history_all.sort(key=lambda x: x["observationDate"], reverse=True)
    history = history_all[:HISTORY_WINDOW]
    latest = history[0]
    prior = history[1] if len(history) > 1 else None
    oldest = history[-1] if len(history) > 1 else None

    one_period_change = None
    if prior:
        one_period_change = latest["reserveBalancesUsdMn"] - prior["reserveBalancesUsdMn"]

    window_change = None
    if oldest:
        window_change = latest["reserveBalancesUsdMn"] - oldest["reserveBalancesUsdMn"]

    return {
        "version": "0.1",
        "source": "fred_public_csv",
        "seriesId": SERIES_ID,
        "seriesName": "Reserve Balances with Federal Reserve Banks",
        "sourceUrl": ENDPOINT,
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "frequency": "weekly",
        "units": "USD millions",
        "latest": latest,
        "trend": {
            "historyWindowRecords": len(history),
            "historyLatestFirst": history,
            "onePeriodChangeUsdMn": one_period_change,
            "windowChangeUsdMn": window_change,
            "windowStartDate": oldest.get("observationDate") if oldest else None,
            "windowEndDate": latest.get("observationDate"),
        },
        "caveats": [
            "FRED public CSV is keyless and suitable for monitoring, but official release notes/metadata should be checked before publication-grade claims.",
            "Reserve balances are a key liquidity indicator, but should be read alongside TGA, RRP and funding-market indicators.",
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
