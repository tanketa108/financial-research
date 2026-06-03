#!/usr/bin/env python3
"""Fetch US growth/activity state from FRED public CSV endpoints."""

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
OUT = ROOT / "financial_system" / "macro" / "data" / "fred-growth-activity-state.json"
COSD = "2024-01-01"
USER_AGENT = "Mozilla/5.0 financial-research-macro-v0/0.1"
HISTORY_WINDOW = 8

SERIES = {
    "GDPC1": {"name": "Real Gross Domestic Product", "units": "bn chained 2017 USD", "calc": "qoq_yoy"},
    "PCECC96": {"name": "Real Personal Consumption Expenditures", "units": "bn chained 2017 USD", "calc": "qoq_yoy"},
    "RSXFS": {"name": "Advance Retail Sales", "units": "USD millions", "calc": "mom_yoy"},
    "RRSFS": {"name": "Advance Real Retail and Food Services Sales", "units": "USD millions", "calc": "mom_yoy"},
    "INDPRO": {"name": "Industrial Production: Total Index", "units": "index", "calc": "mom_yoy"},
    "HOUST": {"name": "Housing Starts", "units": "thousands SAAR", "calc": "mom_yoy"},
    "PERMIT": {"name": "New Privately-Owned Housing Units Authorized by Building Permits", "units": "thousands SAAR", "calc": "mom_yoy"},
    "DGORDER": {"name": "Manufacturers' New Orders: Durable Goods", "units": "USD millions", "calc": "mom_yoy"},
    "NEWORDER": {"name": "Manufacturers' New Orders: Nondefense Capital Goods Excluding Aircraft", "units": "USD millions", "calc": "mom_yoy"},
}


def endpoint(series_id: str) -> str:
    return f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={COSD}"


def fetch_text(url: str) -> str:
    try:
        return subprocess.check_output(["curl", "-L", "--fail", "--silent", "--show-error", "--max-time", "20", url], text=True)
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
    points=[]
    for row in rows:
        value=to_number(row.get(series_id))
        if value is None:
            continue
        points.append({"observationDate": row.get("observation_date"), "value": value})
    if not points:
        raise ValueError(f"FRED returned no observations for {series_id}")
    points.sort(key=lambda x:x["observationDate"])
    latest=points[-1]
    prior=points[-2] if len(points)>=2 else None
    year_ago=points[-5] if SERIES[series_id]["calc"]=="qoq_yoy" and len(points)>=5 else (points[-13] if len(points)>=13 else None)
    latest_first=list(reversed(points))[:HISTORY_WINDOW]
    oldest=latest_first[-1] if len(latest_first)>1 else None
    one_period_pct=pct_change(latest["value"], prior["value"]) if prior else None
    yoy_pct=pct_change(latest["value"], year_ago["value"]) if year_ago else None
    window_pct=pct_change(latest["value"], oldest["value"]) if oldest else None
    return {
        "seriesId": series_id,
        "seriesName": SERIES[series_id]["name"],
        "sourceUrl": endpoint(series_id),
        "units": SERIES[series_id]["units"],
        "calc": SERIES[series_id]["calc"],
        "latest": latest,
        "trend": {
            "historyWindowRecords": len(latest_first),
            "historyLatestFirst": latest_first,
            "onePeriodChange": latest["value"] - prior["value"] if prior else None,
            "onePeriodPct": one_period_pct,
            "yoyPct": yoy_pct,
            "windowPct": window_pct,
            "windowDirection": direction(window_pct),
            "yearAgoDate": year_ago.get("observationDate") if year_ago else None,
            "windowStartDate": oldest.get("observationDate") if oldest else None,
            "windowEndDate": latest.get("observationDate"),
        },
    }


def build_state() -> dict[str, Any]:
    series={sid:fetch_series(sid) for sid in SERIES}
    summary={
        "realGdpQoQPct": series["GDPC1"]["trend"]["onePeriodPct"],
        "realGdpYoYPct": series["GDPC1"]["trend"]["yoyPct"],
        "realPceQoQPct": series["PCECC96"]["trend"]["onePeriodPct"],
        "retailSalesMoMPct": series["RSXFS"]["trend"]["onePeriodPct"],
        "realRetailSalesMoMPct": series["RRSFS"]["trend"]["onePeriodPct"],
        "industrialProductionMoMPct": series["INDPRO"]["trend"]["onePeriodPct"],
        "housingStartsMoMPct": series["HOUST"]["trend"]["onePeriodPct"],
        "permitsMoMPct": series["PERMIT"]["trend"]["onePeriodPct"],
        "durableGoodsMoMPct": series["DGORDER"]["trend"]["onePeriodPct"],
        "coreCapexOrdersMoMPct": series["NEWORDER"]["trend"]["onePeriodPct"],
    }
    return {
        "version":"0.1",
        "source":"fred_public_csv",
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "series": series,
        "summary": summary,
        "caveats":[
            "FRED public CSV provides revised series; no release-vintage, consensus, surprise or component-table claims are made.",
            "Growth/activity readings are context and should be validated against official release notes before publication-grade use.",
        ],
    }


def main() -> int:
    state=build_state()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
