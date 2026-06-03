#!/usr/bin/env python3
"""Fetch US inflation and labor state from FRED public CSV endpoints.

Keyless v0 source block for Macro Monitor. It captures latest values and
simple MoM/YoY or level changes without consensus/surprise claims.
"""

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
OUT = ROOT / "financial_system" / "macro" / "data" / "fred-inflation-labor-state.json"
COSD = "2025-01-01"
USER_AGENT = "Mozilla/5.0 financial-research-macro-v0/0.1"
HISTORY_WINDOW = 36

SERIES = {
    "CPIAUCSL": {"block": "inflation", "name": "Consumer Price Index for All Urban Consumers: All Items", "units": "index", "calc": "mom_yoy"},
    "CPILFESL": {"block": "inflation", "name": "Consumer Price Index for All Urban Consumers: All Items Less Food and Energy", "units": "index", "calc": "mom_yoy"},
    "PCEPI": {"block": "inflation", "name": "Personal Consumption Expenditures: Chain-type Price Index", "units": "index", "calc": "mom_yoy"},
    "PCEPILFE": {"block": "inflation", "name": "Personal Consumption Expenditures Excluding Food and Energy", "units": "index", "calc": "mom_yoy"},
    "PAYEMS": {"block": "labor", "name": "All Employees, Total Nonfarm", "units": "thousands", "calc": "level_change"},
    "UNRATE": {"block": "labor", "name": "Unemployment Rate", "units": "percent", "calc": "level_change"},
    "CIVPART": {"block": "labor", "name": "Labor Force Participation Rate", "units": "percent", "calc": "level_change"},
    "CES0500000003": {"block": "labor", "name": "Average Hourly Earnings of All Employees, Total Private", "units": "USD/hour", "calc": "mom_yoy"},
    "ICSA": {"block": "labor", "name": "Initial Claims", "units": "persons", "calc": "level_change"},
    "JTSJOL": {"block": "labor", "name": "Job Openings: Total Nonfarm", "units": "thousands", "calc": "level_change"},
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


def direction(value: Any, deadband: float = 0.01) -> str:
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

    # Keep chronological list for 12m lookback, then latest-first history for report.
    points.sort(key=lambda x: x["observationDate"])
    latest = points[-1]
    prior = points[-2] if len(points) >= 2 else None
    year_ago = points[-13] if len(points) >= 13 else None
    latest_first = list(reversed(points))[:HISTORY_WINDOW]
    oldest_window = latest_first[-1] if len(latest_first) > 1 else None

    meta = SERIES[series_id]
    calc = meta["calc"]
    one_period_change = latest["value"] - prior["value"] if prior else None
    window_change = latest["value"] - oldest_window["value"] if oldest_window else None
    mom_pct = pct_change(latest["value"], prior["value"]) if calc == "mom_yoy" else None
    yoy_pct = pct_change(latest["value"], year_ago["value"]) if calc == "mom_yoy" and year_ago else None

    return {
        "seriesId": series_id,
        "seriesName": meta["name"],
        "block": meta["block"],
        "sourceUrl": endpoint(series_id),
        "units": meta["units"],
        "calc": calc,
        "latest": latest,
        "trend": {
            "historyWindowRecords": len(latest_first),
            "historyLatestFirst": latest_first,
            "onePeriodChange": one_period_change,
            "windowChange": window_change,
            "windowDirection": direction(window_change),
            "momPct": mom_pct,
            "yoyPct": yoy_pct,
            "yearAgoDate": year_ago.get("observationDate") if year_ago else None,
            "windowStartDate": oldest_window.get("observationDate") if oldest_window else None,
            "windowEndDate": latest.get("observationDate"),
        },
    }


def build_state() -> dict[str, Any]:
    series = {sid: fetch_series(sid) for sid in SERIES}
    infl = series
    labor = series
    summary = {
        "headlineCpiYoyPct": infl["CPIAUCSL"]["trend"]["yoyPct"],
        "coreCpiYoyPct": infl["CPILFESL"]["trend"]["yoyPct"],
        "headlinePceYoyPct": infl["PCEPI"]["trend"]["yoyPct"],
        "corePceYoyPct": infl["PCEPILFE"]["trend"]["yoyPct"],
        "payrollsOneMonthChangeK": labor["PAYEMS"]["trend"]["onePeriodChange"],
        "unemploymentRatePct": labor["UNRATE"]["latest"]["value"],
        "participationRatePct": labor["CIVPART"]["latest"]["value"],
        "initialClaimsLatest": labor["ICSA"]["latest"]["value"],
        "joltsOpeningsLatestK": labor["JTSJOL"]["latest"]["value"],
    }
    return {
        "version": "0.1",
        "source": "fred_public_csv",
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "series": series,
        "summary": summary,
        "caveats": [
            "FRED public CSV provides revised historical series; it does not provide consensus, surprise, or release-time vintage analysis.",
            "Inflation/labor reads are context only until release calendars, revisions and source release notes are fully wired.",
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
