#!/usr/bin/env python3
"""Streamlit Macro Monitor UI v0.

Reads generated macro JSON state files and Markdown reports. The source of truth
remains the fetcher-produced JSON state files plus the rendered Markdown report;
this app is a visualization layer only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import streamlit as st
except ModuleNotFoundError as exc:  # pragma: no cover - helpful CLI error.
    raise SystemExit(
        "Streamlit is not installed. Install with:\n"
        "  python3 -m pip install -r financial-research/financial_system/macro/app/requirements.txt\n"
        "Then run:\n"
        "  streamlit run financial-research/financial_system/macro/app/streamlit_macro_monitor.py"
    ) from exc

try:
    import pandas as pd
except ModuleNotFoundError:  # Streamlit can run without pandas, but charts are better with it.
    pd = None

ROOT = Path(__file__).resolve().parents[3]
MACRO = ROOT / "financial_system" / "macro"
DATA = MACRO / "data"
REPORTS = MACRO / "reports"
CHARTS = MACRO / "charts"

STATE_FILES = {
    "Rates / curve": DATA / "fred-rates-curve-state.json",
    "Inflation + labor": DATA / "fred-inflation-labor-state.json",
    "Growth / activity": DATA / "fred-growth-activity-state.json",
    "TGA": DATA / "tga-state.json",
    "RRP": DATA / "nyfed-rrp-state.json",
    "Reserve balances": DATA / "fed-reserve-balances-state.json",
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def fmt(value: Any, suffix: str = "", decimals: int = 2) -> str:
    if value is None:
        return "n/a"
    try:
        return f"{float(value):,.{decimals}f}{suffix}"
    except (TypeError, ValueError):
        return str(value)


def latest_report() -> Path | None:
    reports = sorted(REPORTS.glob("*-macro-monitor-v*.md"))
    return reports[-1] if reports else None


def series_points(item: dict[str, Any]) -> list[dict[str, Any]]:
    history = (item.get("trend") or {}).get("historyLatestFirst") or []
    points = []
    for row in reversed(history):
        date = row.get("observationDate") or row.get("operationDate") or row.get("recordDate")
        value = row.get("value")
        if value is None:
            value = row.get("reserveBalancesUsdMn")
        if value is None:
            value = row.get("totalAcceptedUsdBn")
        if value is None:
            value = row.get("tgaOpeningBalanceUsdMn")
        if date is not None and value is not None:
            points.append({"date": date, "value": float(value)})
    return points


def render_line_chart(title: str, points: list[dict[str, Any]], unit: str = "") -> None:
    st.markdown(f"**{title}**")
    if not points:
        st.info("No history available for this series yet.")
        return
    if pd is not None:
        df = pd.DataFrame(points).set_index("date")
        st.line_chart(df, height=220)
    else:
        # Dependency-light fallback: show compact table if pandas is not available.
        st.caption("Install pandas for line charts. Showing table fallback.")
        st.dataframe(points, use_container_width=True)
    latest = points[-1]
    st.caption(f"Latest: {latest['date']} — {fmt(latest['value'], unit)}")


def render_series_block(block_name: str, state: dict[str, Any], series_ids: list[str]) -> None:
    series = state.get("series") or {}
    if not series:
        st.warning(f"Missing state for {block_name}.")
        return
    st.subheader(block_name)
    selected = st.multiselect(
        f"Series to visualize — {block_name}",
        options=series_ids,
        default=series_ids[: min(3, len(series_ids))],
        key=f"select-{block_name}",
    )
    for sid in selected:
        item = series.get(sid) or {}
        title = f"{sid} — {item.get('seriesName', sid)}"
        render_line_chart(title, series_points(item), unit="")
        with st.expander(f"Source / metadata — {sid}"):
            st.write(f"Source: {item.get('sourceUrl', 'n/a')}")
            st.write(f"Units: {item.get('units', 'n/a')}")
            st.json({"latest": item.get("latest"), "trend": item.get("trend")}, expanded=False)


def render_cards() -> None:
    rates = load_json(STATE_FILES["Rates / curve"]).get("summary", {})
    infl = load_json(STATE_FILES["Inflation + labor"]).get("summary", {})
    growth = load_json(STATE_FILES["Growth / activity"]).get("summary", {})
    reserves = load_json(STATE_FILES["Reserve balances"])
    tga = load_json(STATE_FILES["TGA"])
    rrp = load_json(STATE_FILES["RRP"])

    cols = st.columns(4)
    cols[0].metric("10Y", fmt(rates.get("latest10yPct"), "%"))
    cols[1].metric("10Y-2Y", fmt(rates.get("latest10y2ySpreadPctPts"), "%"))
    cols[2].metric("Core PCE YoY", fmt(infl.get("corePceYoyPct"), "%"))
    cols[3].metric("Unemployment", fmt(infl.get("unemploymentRatePct"), "%"))

    cols = st.columns(4)
    cols[0].metric("Real GDP QoQ", fmt(growth.get("realGdpQoQPct"), "%"))
    cols[1].metric("Payroll Δ", f"{fmt(infl.get('payrollsOneMonthChangeK'), 'k', 0)}")
    cols[2].metric("TGA", fmt(((tga.get("tgaOpeningBalance") or {}).get("openTodayBalanceUsdMn")), "mn", 0))
    cols[3].metric("RRP", fmt(((rrp.get("latest") or {}).get("totalAcceptedUsdBn")), "bn", 3))

    latest_reserves = (reserves.get("latest") or {}).get("reserveBalancesUsdMn")
    st.metric("Reserve balances", fmt(latest_reserves, "mn", 0))


def render_liquidity() -> None:
    st.subheader("Liquidity triangle")
    svg = CHARTS / "2026-06-03-liquidity-triangle-v0.svg"
    if svg.exists():
        st.image(str(svg), use_container_width=True)
    else:
        st.info("Liquidity SVG not generated yet. Run render_macro_liquidity_svg.py.")

    tga = load_json(STATE_FILES["TGA"])
    rrp = load_json(STATE_FILES["RRP"])
    reserves = load_json(STATE_FILES["Reserve balances"])
    cols = st.columns(3)
    with cols[0]:
        render_line_chart("TGA opening balance", series_points({"trend": tga.get("tgaTrend") or {}}), unit="mn")
    with cols[1]:
        render_line_chart("RRP accepted amount", series_points(rrp), unit="bn")
    with cols[2]:
        render_line_chart("Reserve balances", series_points(reserves), unit="mn")


def render_report_tab() -> None:
    report = latest_report()
    if not report:
        st.warning("No Macro Monitor report found.")
        return
    st.caption(f"Showing: {report.relative_to(ROOT)}")
    st.markdown(report.read_text(encoding="utf-8"))


def main() -> None:
    st.set_page_config(page_title="Macro Monitor", layout="wide")
    st.title("Macro Monitor")
    st.caption("Visualization layer over generated macro JSON states + Markdown report. Source of truth remains the data files.")

    missing = [name for name, path in STATE_FILES.items() if not path.exists()]
    if missing:
        st.warning(f"Missing state files: {', '.join(missing)}")

    render_cards()

    tabs = st.tabs(["Report", "Rates", "Inflation", "Labor", "Growth", "Liquidity", "Raw state"])
    with tabs[0]:
        render_report_tab()
    with tabs[1]:
        render_series_block("Rates / curve", load_json(STATE_FILES["Rates / curve"]), ["FEDFUNDS", "DGS2", "DGS10", "DGS30", "T10Y2Y", "T10Y3M"])
    with tabs[2]:
        render_series_block("Inflation", load_json(STATE_FILES["Inflation + labor"]), ["CPIAUCSL", "CPILFESL", "PCEPI", "PCEPILFE"])
    with tabs[3]:
        render_series_block("Labor", load_json(STATE_FILES["Inflation + labor"]), ["PAYEMS", "UNRATE", "CIVPART", "CES0500000003", "ICSA", "JTSJOL"])
    with tabs[4]:
        render_series_block("Growth / activity", load_json(STATE_FILES["Growth / activity"]), ["GDPC1", "PCECC96", "RSXFS", "RRSFS", "INDPRO", "HOUST", "PERMIT", "DGORDER", "NEWORDER"])
    with tabs[5]:
        render_liquidity()
    with tabs[6]:
        for name, path in STATE_FILES.items():
            with st.expander(name):
                st.caption(str(path.relative_to(ROOT)))
                st.json(load_json(path), expanded=False)


if __name__ == "__main__":
    main()
