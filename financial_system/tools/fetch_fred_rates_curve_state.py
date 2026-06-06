#!/usr/bin/env python3
"""Fetch US rates/curve state from FRED public CSV endpoints.

Uses keyless FRED graph CSV endpoints. Writes a compact state file for
Macro Monitor v0.
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
OUT = ROOT / "financial_system" / "macro" / "data" / "fred-rates-curve-state.json"
USER_AGENT = "Mozilla/5.0 financial-research-macro-v0/0.1"
COSD = "2025-01-01"
HISTORY_WINDOW = 120

SERIES = {
    "FEDFUNDS": {
        "name": "Effective Federal Funds Rate",
        "units": "percent",
        "frequency": "monthly",
    },
    "DGS3MO": {
        "name": "Market Yield on U.S. Treasury Securities at 3-Month Constant Maturity",
        "units": "percent",
        "frequency": "daily",
    },
    "DGS2": {
        "name": "Market Yield on U.S. Treasury Securities at 2-Year Constant Maturity",
        "units": "percent",
        "frequency": "daily",
    },
    "DGS10": {
        "name": "Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity",
        "units": "percent",
        "frequency": "daily",
    },
    "DGS30": {
        "name": "Market Yield on U.S. Treasury Securities at 30-Year Constant Maturity",
        "units": "percent",
        "frequency": "daily",
    },
    "MORTGAGE30US": {
        "name": "30-Year Fixed Rate Mortgage Average in the United States",
        "units": "percent",
        "frequency": "weekly",
    },
    "T10Y2Y": {
        "name": "10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity",
        "units": "percentage points",
        "frequency": "daily",
    },
    "T10Y3M": {
        "name": "10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity",
        "units": "percentage points",
        "frequency": "daily",
    },
}


def endpoint(series_id: str) -> str:
    return f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={COSD}"


def fetch_text(url: str) -> str:
    try:
        return subprocess.check_output(
            ["curl", "-L", "--fail", "--silent", "--show-error", "--max-time", "60", url],
            text=True,
        )
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


def fetch_series(series_id: str) -> dict[str, Any]:
    rows = list(csv.DictReader(io.StringIO(fetch_text(endpoint(series_id)))))
    points = []
    for row in rows:
        value = to_number(row.get(series_id))
        if value is None:
            continue
        points.append({"observationDate": row.get("observation_date"), "value": value})
    if not points:
        raise ValueError(f"FRED public CSV returned no observations for {series_id}")
    points.sort(key=lambda x: x["observationDate"], reverse=True)
    history = points[:HISTORY_WINDOW]
    latest = history[0]
    prior = history[1] if len(history) > 1 else None
    oldest = history[-1] if len(history) > 1 else None
    one_period_change = latest["value"] - prior["value"] if prior else None
    window_change = latest["value"] - oldest["value"] if oldest else None
    return {
        "seriesId": series_id,
        "seriesName": SERIES[series_id]["name"],
        "sourceUrl": endpoint(series_id),
        "units": SERIES[series_id]["units"],
        "frequency": SERIES[series_id]["frequency"],
        "latest": latest,
        "trend": {
            "historyWindowRecords": len(history),
            "historyLatestFirst": history,
            "onePeriodChange": one_period_change,
            "windowChange": window_change,
            "windowStartDate": oldest.get("observationDate") if oldest else None,
            "windowEndDate": latest.get("observationDate"),
        },
    }


def direction(value: Any, deadband: float = 0.01) -> str:
    if not isinstance(value, (int, float)):
        return "unknown"
    if value > deadband:
        return "rising"
    if value < -deadband:
        return "falling"
    return "flat"


def build_state() -> dict[str, Any]:
    series = {sid: fetch_series(sid) for sid in SERIES}
    dgs2 = series["DGS2"]["latest"]["value"]
    dgs10 = series["DGS10"]["latest"]["value"]
    t10y2y = series["T10Y2Y"]["latest"]["value"]
    curve_shape = "inverted" if t10y2y < 0 else "positive/upward sloping"
    ten_year_trend = direction(series["DGS10"]["trend"]["windowChange"])
    two_year_trend = direction(series["DGS2"]["trend"]["windowChange"])
    curve_trend = direction(series["T10Y2Y"]["trend"]["windowChange"])

    return {
        "version": "0.1",
        "source": "fred_public_csv",
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "series": series,
        "summary": {
            "latest3mPct": series["DGS3MO"]["latest"]["value"],
            "latest2yPct": dgs2,
            "latest10yPct": dgs10,
            "latest30yPct": series["DGS30"]["latest"]["value"],
            "latestMortgage30yPct": series["MORTGAGE30US"]["latest"]["value"],
            "latest10y2ySpreadPctPts": t10y2y,
            "latest10y3mSpreadPctPts": series["T10Y3M"]["latest"]["value"],
            "curveShape10y2y": curve_shape,
            "twoYearTrend": two_year_trend,
            "tenYearTrend": ten_year_trend,
            "curveTrend10y2y": curve_trend,
        },
        "caveats": [
            "FRED graph CSV is keyless and suitable for monitoring; publication-grade reports should verify metadata/revisions when needed.",
            "Rates/curve context is not a portfolio instruction; use it to frame valuation sensitivity and macro regime questions.",
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
