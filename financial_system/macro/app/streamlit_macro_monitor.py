#!/usr/bin/env python3
"""Streamlit Macro Monitor UI v0.2.

Visual layer over generated macro JSON states + Markdown reports. The app does
not fetch external APIs at runtime; fetchers produce JSON state files and this
UI reads them.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

try:
    import streamlit as st
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Streamlit is not installed. Install with:\n"
        "  python3 -m pip install -r requirements.txt\n"
        "Then run:\n"
        "  streamlit run streamlit_app.py"
    ) from exc

try:
    import pandas as pd
except ModuleNotFoundError:
    pd = None

ROOT = Path(__file__).resolve().parents[3]
MACRO = ROOT / "financial_system" / "macro"
DATA = MACRO / "data"
REPORTS = MACRO / "reports"
CHARTS = MACRO / "charts"
EVENTS = MACRO / "macro-release-events.json"
REGISTRY = MACRO / "macro-release-calendar-registry.json"

STATE_FILES = {
    "Rates / curve": DATA / "fred-rates-curve-state.json",
    "Inflation + labor": DATA / "fred-inflation-labor-state.json",
    "Growth / activity": DATA / "fred-growth-activity-state.json",
    "TGA": DATA / "tga-state.json",
    "RRP": DATA / "nyfed-rrp-state.json",
    "Reserve balances": DATA / "fed-reserve-balances-state.json",
}

BLOCKS = {
    "Dashboard": [],
    "Rates": ["FEDFUNDS", "DGS2", "DGS10", "DGS30", "T10Y2Y", "T10Y3M"],
    "Inflation": ["CPIAUCSL", "CPILFESL", "PCEPI", "PCEPILFE"],
    "Labor": ["PAYEMS", "UNRATE", "CIVPART", "CES0500000003", "ICSA", "JTSJOL"],
    "Growth": ["GDPC1", "PCECC96", "RSXFS", "RRSFS", "INDPRO", "HOUST", "PERMIT", "DGORDER", "NEWORDER"],
    "Liquidity": [],
    "Calendar": [],
    "Report": [],
    "Raw state": [],
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


def pct(value: Any) -> str:
    return fmt(value, "%", 2)


def latest_report() -> Path | None:
    reports = sorted(REPORTS.glob("*-macro-monitor-v*.md"))
    return reports[-1] if reports else None


def series_item(block: str, sid: str) -> dict[str, Any]:
    if block in {"Rates"}:
        return (load_json(STATE_FILES["Rates / curve"]).get("series") or {}).get(sid, {})
    if block in {"Inflation", "Labor"}:
        return (load_json(STATE_FILES["Inflation + labor"]).get("series") or {}).get(sid, {})
    if block == "Growth":
        return (load_json(STATE_FILES["Growth / activity"]).get("series") or {}).get(sid, {})
    return {}


def series_points(item: dict[str, Any]) -> list[dict[str, Any]]:
    history = (item.get("trend") or {}).get("historyLatestFirst") or []
    points: list[dict[str, Any]] = []
    for row in reversed(history):
        obs_date = row.get("observationDate") or row.get("operationDate") or row.get("recordDate")
        value = row.get("value")
        if value is None:
            value = row.get("reserveBalancesUsdMn")
        if value is None:
            value = row.get("totalAcceptedUsdBn")
        if value is None:
            value = row.get("tgaOpeningBalanceUsdMn")
        if obs_date and value is not None:
            points.append({"date": obs_date, "value": float(value)})
    return points


def to_df(points: list[dict[str, Any]]):
    if pd is None or not points:
        return None
    df = pd.DataFrame(points)
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")


def inject_style() -> None:
    st.markdown(
        """
        <style>
        .main .block-container {padding-top: 2.2rem; max-width: 1180px;}
        h1 {font-size: 3.1rem !important; line-height: 1.05; margin-bottom: 0.4rem;}
        h2, h3 {letter-spacing: -0.02em;}
        [data-testid="stSidebar"] {background: #f4f7fb;}
        div[data-testid="stMetric"] {background: #ffffff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 14px 16px; box-shadow: 0 1px 2px rgba(15,23,42,0.04);}
        .macro-card {background: #ffffff; border: 1px solid #e5e7eb; border-radius: 18px; padding: 18px; margin: 8px 0 18px 0;}
        .small-muted {color: #64748b; font-size: 0.88rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def state_timestamp() -> str:
    timestamps = []
    for path in STATE_FILES.values():
        state = load_json(path)
        if state.get("fetchedAt"):
            timestamps.append(state["fetchedAt"])
    return max(timestamps) if timestamps else "n/a"


def render_header(title: str = "Macro Monitor") -> None:
    st.title(title)
    st.caption("Market-style macro dashboard: report + long history series + event calendar. Data source: generated JSON state files.")


def render_snapshot() -> None:
    rates = load_json(STATE_FILES["Rates / curve"]).get("summary", {})
    infl = load_json(STATE_FILES["Inflation + labor"]).get("summary", {})
    growth = load_json(STATE_FILES["Growth / activity"]).get("summary", {})
    tga = load_json(STATE_FILES["TGA"])
    rrp = load_json(STATE_FILES["RRP"])
    reserves = load_json(STATE_FILES["Reserve balances"])

    st.subheader("Macro regime snapshot")
    cols = st.columns(4)
    cols[0].metric("10Y Treasury", pct(rates.get("latest10yPct")))
    cols[1].metric("10Y-2Y", pct(rates.get("latest10y2ySpreadPctPts")))
    cols[2].metric("Core PCE YoY", pct(infl.get("corePceYoyPct")))
    cols[3].metric("Unemployment", pct(infl.get("unemploymentRatePct")))

    cols = st.columns(4)
    cols[0].metric("Real GDP QoQ", pct(growth.get("realGdpQoQPct")))
    cols[1].metric("Payroll Δ", f"{fmt(infl.get('payrollsOneMonthChangeK'), 'k', 0)}")
    cols[2].metric("TGA", fmt(((tga.get("tgaOpeningBalance") or {}).get("openTodayBalanceUsdMn")), "mn", 0))
    cols[3].metric("RRP", fmt(((rrp.get("latest") or {}).get("totalAcceptedUsdBn")), "bn", 3))

    latest_reserves = (reserves.get("latest") or {}).get("reserveBalancesUsdMn")
    st.metric("Reserve balances", fmt(latest_reserves, "mn", 0))
    st.markdown(
        "<div class='macro-card'><b>Read:</b> growth still expanding, labor resilient, inflation still above target context, rates falling with a positive but flattening curve, and liquidity mixed. <b>Actionability:</b> monitor-only.</div>",
        unsafe_allow_html=True,
    )


def render_series_explorer(block: str) -> None:
    st.subheader(block)
    ids = BLOCKS[block]
    left, right = st.columns([0.28, 0.72])
    with left:
        selected = st.selectbox("Series", ids, index=0, key=f"series-{block}")
        item = series_item(block, selected)
        latest = item.get("latest") or {}
        trend = item.get("trend") or {}
        st.markdown("### Latest")
        st.metric(selected, fmt(latest.get("value"), "", 3 if item.get("units") == "index" else 2))
        st.write(f"Date: `{latest.get('observationDate', 'n/a')}`")
        st.write(f"Units: `{item.get('units', 'n/a')}`")
        if trend.get("onePeriodPct") is not None:
            st.write(f"One-period %: **{pct(trend.get('onePeriodPct'))}**")
        if trend.get("momPct") is not None:
            st.write(f"MoM: **{pct(trend.get('momPct'))}**")
        if trend.get("yoyPct") is not None:
            st.write(f"YoY: **{pct(trend.get('yoyPct'))}**")
        if trend.get("windowChange") is not None:
            st.write(f"Window change: **{fmt(trend.get('windowChange'), '', 2)}**")
        st.link_button("Open source", item.get("sourceUrl", "https://fred.stlouisfed.org/"))
    with right:
        item = series_item(block, selected)
        points = series_points(item)
        st.markdown(f"### {selected} — {item.get('seriesName', selected)}")
        df = to_df(points)
        if df is not None:
            st.line_chart(df, height=360)
            st.dataframe(df.sort_index(ascending=False), use_container_width=True, height=260)
        else:
            st.dataframe(points, use_container_width=True)
        with st.expander("Metadata / raw latest + trend"):
            st.json({"latest": item.get("latest"), "trend": item.get("trend"), "sourceUrl": item.get("sourceUrl")}, expanded=False)


def render_dashboard() -> None:
    render_snapshot()
    st.subheader("Key series")
    cols = st.columns(2)
    quick = [("Rates", "DGS10"), ("Rates", "T10Y2Y"), ("Inflation", "PCEPILFE"), ("Labor", "UNRATE"), ("Growth", "GDPC1"), ("Growth", "INDPRO")]
    for i, (block, sid) in enumerate(quick):
        item = series_item(block, sid)
        with cols[i % 2]:
            st.markdown(f"**{sid} — {item.get('seriesName', sid)}**")
            df = to_df(series_points(item))
            if df is not None:
                st.line_chart(df, height=180)
            else:
                st.info("No data")


def calendar_rows() -> list[dict[str, Any]]:
    events = load_json(EVENTS).get("events") or []
    registry = {r.get("id"): r for r in (load_json(REGISTRY).get("releases") or [])}
    rows = []
    for ev in events:
        rel = registry.get(ev.get("releaseId"), {})
        rows.append({
            "date": ev.get("releaseDate") or "pending",
            "time_et": ev.get("releaseTimeET") or rel.get("usualReleaseTimeET") or "TBD",
            "release": rel.get("name") or ev.get("releaseId"),
            "category": rel.get("category", "unknown"),
            "importance": rel.get("importance", "unknown"),
            "period": ev.get("period"),
            "status": ev.get("status"),
            "source": ev.get("sourceUrl") or rel.get("officialCalendarUrl"),
            "note": ev.get("sourceNote") or rel.get("interpretationHint"),
        })
    return rows


def render_calendar() -> None:
    st.subheader("Macro release calendar")
    rows = calendar_rows()
    if not rows:
        st.warning("No release events found.")
        return
    if pd is not None:
        df = pd.DataFrame(rows)
        dated = df[df["date"] != "pending"].copy()
        pending = df[df["date"] == "pending"].copy()
        st.markdown("### Upcoming confirmed events")
        if not dated.empty:
            dated["date_sort"] = pd.to_datetime(dated["date"])
            dated = dated.sort_values(["date_sort", "time_et"]).drop(columns=["date_sort"])
            st.dataframe(dated, use_container_width=True, height=280)
        st.markdown("### Pending confirmation")
        st.dataframe(pending, use_container_width=True, height=180)
    else:
        st.dataframe(rows, use_container_width=True)
    with st.expander("Calendar registry / event source discipline"):
        st.json({"events": load_json(EVENTS), "registry": load_json(REGISTRY)}, expanded=False)


def render_liquidity() -> None:
    st.subheader("Liquidity")
    svg = CHARTS / "2026-06-03-liquidity-triangle-v0.svg"
    if svg.exists():
        st.image(str(svg), use_container_width=True)
    tga = load_json(STATE_FILES["TGA"])
    rrp = load_json(STATE_FILES["RRP"])
    reserves = load_json(STATE_FILES["Reserve balances"])
    tabs = st.tabs(["TGA", "RRP", "Reserve balances"])
    liquidity_items = [
        (tabs[0], "TGA opening balance", {"trend": tga.get("tgaTrend") or {}}, "USD mn"),
        (tabs[1], "RRP accepted amount", rrp, "USD bn"),
        (tabs[2], "Reserve balances", reserves, "USD mn"),
    ]
    for tab, title, item, units in liquidity_items:
        with tab:
            st.markdown(f"### {title}")
            df = to_df(series_points(item))
            if df is not None:
                st.line_chart(df, height=360)
                st.dataframe(df.sort_index(ascending=False), use_container_width=True, height=260)
            st.caption(units)
            st.json({"latest": item.get("latest"), "trend": item.get("trend") or item.get("tgaTrend")}, expanded=False)


def render_report() -> None:
    report = latest_report()
    if not report:
        st.warning("No Macro Monitor report found.")
        return
    st.caption(f"Showing: {report.relative_to(ROOT)}")
    st.markdown(report.read_text(encoding="utf-8"))


def render_raw_state() -> None:
    for name, path in STATE_FILES.items():
        with st.expander(name):
            st.caption(str(path.relative_to(ROOT)))
            st.json(load_json(path), expanded=False)


def main() -> None:
    st.set_page_config(page_title="Macro Monitor", layout="wide")
    inject_style()
    with st.sidebar:
        st.markdown("### Choose")
        page = st.selectbox("", list(BLOCKS.keys()), label_visibility="collapsed")
        st.divider()
        st.caption("Last data refresh")
        st.code(state_timestamp())
        st.caption("Source of truth: JSON states + Markdown report")

    render_header("Market Information App")
    st.markdown("## Macro Monitor")

    missing = [name for name, path in STATE_FILES.items() if not path.exists()]
    if missing:
        st.warning(f"Missing state files: {', '.join(missing)}")

    if page == "Dashboard":
        render_dashboard()
    elif page in {"Rates", "Inflation", "Labor", "Growth"}:
        render_series_explorer(page)
    elif page == "Liquidity":
        render_liquidity()
    elif page == "Calendar":
        render_calendar()
    elif page == "Report":
        render_report()
    elif page == "Raw state":
        render_raw_state()


if __name__ == "__main__":
    main()
