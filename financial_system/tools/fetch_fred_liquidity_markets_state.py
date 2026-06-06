#!/usr/bin/env python3
"""Fetch US liquidity and market context state from FRED public CSV endpoints."""

from __future__ import annotations

import csv
import io
import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "financial_system" / "macro" / "data" / "fred-liquidity-markets-state.json"
COSD = "2025-01-01"
USER_AGENT = "Mozilla/5.0 financial-research-macro-v0/0.1"
HISTORY_WINDOW = 180

SERIES = {
    "M2SL": {"block": "liquidity", "name": "M2 Money Stock", "units": "USD billions", "calc": "mom_yoy"},
    "PSAVERT": {"block": "liquidity", "name": "Personal Saving Rate", "units": "percent", "calc": "level_change"},
    "SP500": {"block": "markets", "name": "S&P 500", "units": "index", "calc": "level_change"},
    "VIXCLS": {"block": "markets", "name": "CBOE Volatility Index: VIX", "units": "index", "calc": "level_change"},
}


def endpoint(series_id: str) -> str:
    return f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={COSD}"


def fetch_text(url: str) -> str:
    try:
        return subprocess.check_output(["curl", "-L", "--fail", "--silent", "--show-error", "--max-time", "60", url], text=True)
    except Exception:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8-sig")


def to_number(value: Any) -> float | None:
    if value in (None, "", ".", "null"):
        return None
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return None


def pct_change(new: float | None, old: float | None) -> float | None:
    if new is None or old in (None, 0):
        return None
    return (new / old - 1.0) * 100.0


def direction(value: Any, deadband: float = 0.05) -> str:
    if not isinstance(value, (int, float)):
        return "unknown"
    if value > deadband:
        return "rising"
    if value < -deadband:
        return "falling"
    return "flat"


def fetch_series(series_id: str) -> dict[str, Any]:
    rows = list(csv.DictReader(io.StringIO(fetch_text(endpoint(series_id)))))
    points: list[dict[str, Any]] = []
    for row in rows:
        value = to_number(row.get(series_id))
        if value is None:
            continue
        points.append({"observationDate": row.get("observation_date"), "value": value})
    if not points:
        raise ValueError(f"FRED returned no observations for {series_id}")
    points.sort(key=lambda x: x["observationDate"])
    latest = points[-1]
    prior = points[-2] if len(points) >= 2 else None
    year_ago = points[-13] if len(points) >= 13 else None
    latest_first = list(reversed(points))[:HISTORY_WINDOW]
    oldest = latest_first[-1] if len(latest_first) > 1 else None
    meta = SERIES[series_id]
    one_period_change = latest["value"] - prior["value"] if prior else None
    window_change = latest["value"] - oldest["value"] if oldest else None
    return {
        "seriesId": series_id,
        "seriesName": meta["name"],
        "block": meta["block"],
        "sourceUrl": endpoint(series_id),
        "units": meta["units"],
        "calc": meta["calc"],
        "latest": latest,
        "trend": {
            "historyWindowRecords": len(latest_first),
            "historyLatestFirst": latest_first,
            "onePeriodChange": one_period_change,
            "onePeriodPct": pct_change(latest["value"], prior["value"]) if prior else None,
            "yoyPct": pct_change(latest["value"], year_ago["value"]) if year_ago and meta["calc"] == "mom_yoy" else None,
            "windowChange": window_change,
            "windowDirection": direction(window_change),
            "yearAgoDate": year_ago.get("observationDate") if year_ago else None,
            "windowStartDate": oldest.get("observationDate") if oldest else None,
            "windowEndDate": latest.get("observationDate"),
        },
    }


def build_state() -> dict[str, Any]:
    series = {sid: fetch_series(sid) for sid in SERIES}
    return {
        "version": "0.1",
        "source": "fred_public_csv",
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "series": series,
        "summary": {
            "m2YoyPct": series["M2SL"]["trend"]["yoyPct"],
            "personalSavingRatePct": series["PSAVERT"]["latest"]["value"],
            "sp500Latest": series["SP500"]["latest"]["value"],
            "vixLatest": series["VIXCLS"]["latest"]["value"],
        },
        "caveats": [
            "Liquidity/markets are supporting context, not macro-release truth or portfolio instructions.",
            "FRED public CSV provides revised/latest-vintage data only; publication-grade use should verify source metadata.",
        ],
    }


def main() -> int:
    state = build_state()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
