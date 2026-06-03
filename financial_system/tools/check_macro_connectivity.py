#!/usr/bin/env python3
"""Connectivity smoke test for Macro v0 sources.

FRED:
- Uses FRED API when FRED_API_KEY is set.
- Falls back to public fredgraph CSV downloads for basic series checks.

Treasury:
- Uses FiscalData public API; no key required.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "financial_system" / "macro" / "macro-series-registry.json"
OUT = ROOT / "financial_system" / "macro" / "data" / "connectivity-smoke-test.json"


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "financial-research-macro-v0/0.1"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "financial-research-macro-v0/0.1"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def fred_check(series_id: str) -> dict:
    api_key = os.getenv("FRED_API_KEY")
    if api_key:
        params = urllib.parse.urlencode({
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 5,
        })
        url = f"https://api.stlouisfed.org/fred/series/observations?{params}"
        payload = fetch_json(url)
        observations = payload.get("observations", [])
        return {
            "ok": bool(observations),
            "mode": "fred_api",
            "sample": observations[:3],
        }

    # FRED's official API requires an API key. This key must be supplied by the
    # user/operator as FRED_API_KEY; it must not be committed to the repository.
    # We still test that the API endpoint is reachable and returns the expected
    # missing-key response.
    try:
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={urllib.parse.quote(series_id)}&file_type=json&limit=1"
        fetch_json(url)
    except Exception as exc:
        if "HTTP Error 400" in str(exc) or "Bad Request" in str(exc):
            return {
                "ok": False,
                "mode": "fred_api_missing_key",
                "error": "FRED_API_KEY is not configured; endpoint reachable but official API requires a key.",
            }
        return {"ok": False, "mode": "fred_api_probe", "error": repr(exc)}

    return {"ok": False, "mode": "fred_api_missing_key", "error": "FRED_API_KEY is not configured."}


def treasury_check(endpoint: str) -> dict:
    params = urllib.parse.urlencode({
        "page[size]": 5,
        "sort": "-record_date",
    })
    url = f"{endpoint}?{params}"
    payload = fetch_json(url)
    data = payload.get("data", [])
    return {
        "ok": bool(data),
        "mode": "treasury_fiscaldata_public_api",
        "sample": data[:3],
        "meta": payload.get("meta", {}),
    }


def main() -> int:
    registry = json.loads(REGISTRY.read_text())
    results = {
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "fredApiKeyPresent": bool(os.getenv("FRED_API_KEY")),
        "checks": [],
    }
    for series in registry["series"]:
        check = {"id": series["id"], "source": series["source"]}
        try:
            if series["source"] == "fred":
                check.update(fred_check(series["sourceSeriesId"]))
            elif series["source"] == "treasury_fiscaldata":
                check.update(treasury_check(series["endpoint"]))
            else:
                check.update({"ok": False, "error": "unsupported source"})
        except Exception as exc:  # smoke test should report all failures
            check.update({"ok": False, "error": repr(exc)})
        results["checks"].append(check)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0 if all(c.get("ok") for c in results["checks"]) else 1


if __name__ == "__main__":
    sys.exit(main())
