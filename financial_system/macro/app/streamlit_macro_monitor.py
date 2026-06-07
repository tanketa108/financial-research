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

try:
    import altair as alt
except ModuleNotFoundError:
    alt = None

ROOT = Path(__file__).resolve().parents[3]
MACRO = ROOT / "financial_system" / "macro"
DATA = MACRO / "data"
REPORTS = MACRO / "reports"
CHARTS = MACRO / "charts"
EVENTS = MACRO / "macro-release-events.json"
REGISTRY = MACRO / "macro-release-calendar-registry.json"
APP_VERSION = "Macro Terminal v0.4 · Fincept shell · 2026-06-07"

STATE_FILES = {
    "Rates / curve": DATA / "fred-rates-curve-state.json",
    "Inflation + labor": DATA / "fred-inflation-labor-state.json",
    "Growth / activity": DATA / "fred-growth-activity-state.json",
    "TGA": DATA / "tga-state.json",
    "RRP": DATA / "nyfed-rrp-state.json",
    "Reserve balances": DATA / "fed-reserve-balances-state.json",
    "Liquidity / markets": DATA / "fred-liquidity-markets-state.json",
}

BLOCKS = {
    "Dashboard": [],
    "Rates": ["FEDFUNDS", "DGS3MO", "DGS2", "DGS10", "DGS30", "MORTGAGE30US", "T10Y2Y", "T10Y3M"],
    "Inflation": ["CPIAUCSL", "CPILFESL", "PCEPI", "PCEPILFE"],
    "Labor": ["PAYEMS", "UNRATE", "CIVPART", "CES0500000003", "ICSA", "JTSJOL"],
    "Growth": ["GDPC1", "GDP", "PCECC96", "RSXFS", "RRSFS", "INDPRO", "HOUST", "PERMIT", "DGORDER", "NEWORDER", "BOPGSTB"],
    "Liquidity": [],
    "Markets": ["M2SL", "PSAVERT", "SP500", "VIXCLS"],
    "Calendar": [],
    "Report": [],
    "Raw state": [],
}

SIDEBAR_BLOCKS = ["Rates", "Inflation", "Labor", "Growth", "Liquidity", "Markets"]

SERIES_PRESETS = {
    "Rates curve": [("Rates", "DGS3MO"), ("Rates", "DGS2"), ("Rates", "DGS10"), ("Rates", "DGS30"), ("Rates", "T10Y2Y"), ("Rates", "T10Y3M")],
    "Inflation pulse": [("Inflation", "CPIAUCSL"), ("Inflation", "CPILFESL"), ("Inflation", "PCEPI"), ("Inflation", "PCEPILFE")],
    "Labor cooling": [("Labor", "PAYEMS"), ("Labor", "UNRATE"), ("Labor", "CIVPART"), ("Labor", "ICSA"), ("Labor", "JTSJOL")],
    "Growth activity": [("Growth", "GDPC1"), ("Growth", "PCECC96"), ("Growth", "RSXFS"), ("Growth", "INDPRO"), ("Growth", "HOUST"), ("Growth", "PERMIT")],
    "Liquidity drain": [("Markets", "M2SL"), ("Markets", "SP500"), ("Markets", "VIXCLS")],
}

SERIES_FAMILIES = {
    "Rates": {
        "Policy / front-end": ["FEDFUNDS", "DGS3MO", "DGS2"],
        "Long end": ["DGS10", "DGS30", "MORTGAGE30US"],
        "Curve spreads": ["T10Y2Y", "T10Y3M"],
        "All": BLOCKS["Rates"],
    },
    "Inflation": {"CPI": ["CPIAUCSL", "CPILFESL"], "PCE": ["PCEPI", "PCEPILFE"], "All": BLOCKS["Inflation"]},
    "Labor": {"Employment": ["PAYEMS", "CES0500000003"], "Slack": ["UNRATE", "CIVPART"], "Forward / claims": ["ICSA", "JTSJOL"], "All": BLOCKS["Labor"]},
    "Growth": {"GDP / consumption": ["GDPC1", "GDP", "PCECC96"], "Retail / industrial": ["RSXFS", "RRSFS", "INDPRO"], "Housing / orders / trade": ["HOUST", "PERMIT", "DGORDER", "NEWORDER", "BOPGSTB"], "All": BLOCKS["Growth"]},
    "Markets": {"Money / savings": ["M2SL", "PSAVERT"], "Risk assets": ["SP500", "VIXCLS"], "All": BLOCKS["Markets"]},
}

SERIES_CHART_DEFAULTS = {
    # Rates and spreads read best in original percentage / percentage-point units.
    "FEDFUNDS": {"years": 3, "scale": "Level"},
    "DGS3MO": {"years": 3, "scale": "Level"},
    "DGS2": {"years": 3, "scale": "Level"},
    "DGS10": {"years": 3, "scale": "Level"},
    "DGS30": {"years": 3, "scale": "Level"},
    "MORTGAGE30US": {"years": 3, "scale": "Level"},
    "T10Y2Y": {"years": 3, "scale": "Level"},
    "T10Y3M": {"years": 3, "scale": "Level"},
    # Index/level macro aggregates compare better when normalized by default.
    "CPIAUCSL": {"years": 5, "scale": "Indexed = 100"},
    "CPILFESL": {"years": 5, "scale": "Indexed = 100"},
    "PCEPI": {"years": 5, "scale": "Indexed = 100"},
    "PCEPILFE": {"years": 5, "scale": "Indexed = 100"},
    "PAYEMS": {"years": 5, "scale": "Indexed = 100"},
    "CES0500000003": {"years": 5, "scale": "Indexed = 100"},
    "GDPC1": {"years": 10, "scale": "Indexed = 100"},
    "GDP": {"years": 10, "scale": "Indexed = 100"},
    "PCECC96": {"years": 10, "scale": "Indexed = 100"},
    "RSXFS": {"years": 5, "scale": "Indexed = 100"},
    "RRSFS": {"years": 5, "scale": "Indexed = 100"},
    "INDPRO": {"years": 5, "scale": "Indexed = 100"},
    "DGORDER": {"years": 5, "scale": "Indexed = 100"},
    "NEWORDER": {"years": 5, "scale": "Indexed = 100"},
    "BOPGSTB": {"years": 5, "scale": "Level"},
    # Rates/point-in-time labor/housing indicators are more interpretable in levels.
    "UNRATE": {"years": 5, "scale": "Level"},
    "CIVPART": {"years": 5, "scale": "Level"},
    "ICSA": {"years": 3, "scale": "Level"},
    "JTSJOL": {"years": 5, "scale": "Level"},
    "HOUST": {"years": 5, "scale": "Level"},
    "PERMIT": {"years": 5, "scale": "Level"},
    # Liquidity charts: show levels, but keep recent windows to avoid visual compression.
    "TGA opening balance": {"years": 1, "scale": "Level"},
    "RRP accepted amount": {"years": 1, "scale": "Level"},
    "Reserve balances": {"years": 3, "scale": "Level"},
    "M2SL": {"years": 5, "scale": "Indexed = 100"},
    "PSAVERT": {"years": 5, "scale": "Level"},
    "SP500": {"years": 3, "scale": "Indexed = 100"},
    "VIXCLS": {"years": 3, "scale": "Level"},
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
    if block == "Markets":
        return (load_json(STATE_FILES["Liquidity / markets"]).get("series") or {}).get(sid, {})
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


def series_df(block: str, sid: str):
    return to_df(series_points(series_item(block, sid)))


def display_name(block: str, sid: str) -> str:
    if block == "Liquidity":
        return sid
    item = series_item(block, sid)
    name = item.get("seriesName") or sid
    return f"{sid} — {name}"


def filter_window(df, years: int | None):
    """Return a recent window so long historical series do not flatten charts."""
    if pd is None or df is None or df.empty or years is None:
        return df
    cutoff = df.index.max() - pd.DateOffset(years=years)
    return df[df.index >= cutoff]


def indexed_df(df):
    """Index a series to 100 at the first visible observation."""
    if pd is None or df is None or df.empty:
        return df
    first = df["value"].dropna().iloc[0]
    if first == 0:
        return df
    out = df.copy()
    out["value"] = out["value"] / first * 100
    return out


def pct_change_df(df):
    if pd is None or df is None or df.empty:
        return df
    out = df.copy()
    first = out["value"].dropna().iloc[0]
    if first == 0:
        return out
    out["value"] = (out["value"] / first - 1) * 100
    return out


def apply_scale(df, scale: str):
    if scale == "Indexed = 100":
        return indexed_df(df)
    if scale == "% change from start":
        return pct_change_df(df)
    return df


def long_compare_df(items: list[tuple[str, str]], years: int | None, scale: str):
    if pd is None:
        return None
    frames = []
    for block, sid in items:
        df = series_df(block, sid)
        if df is None or df.empty:
            continue
        shown = apply_scale(filter_window(df, years), scale)
        shown = shown.reset_index()
        shown["series"] = display_name(block, sid)
        frames.append(shown[["date", "series", "value"]])
    if not frames:
        return None
    return pd.concat(frames, ignore_index=True)


def chart_controls_key(name: str) -> str:
    return name.lower().replace(" ", "-").replace("/", "-")


def chart_df(df, *, key: str, default_years: int | None = 5, default_scale: str = "Level"):
    """Apply per-chart scale/window controls and return display dataframe."""
    if pd is None or df is None or df.empty:
        return df, "level"
    col1, col2 = st.columns([0.45, 0.55])
    with col1:
        window_label = st.selectbox(
            "Window",
            ["1Y", "3Y", "5Y", "10Y", "Max"],
            index={1: 0, 3: 1, 5: 2, 10: 3, None: 4}.get(default_years, 2),
            key=f"window-{key}",
        )
    with col2:
        view = st.radio(
            "Scale",
            ["Level", "Indexed = 100", "% change from start"],
            index=0 if default_scale == "Level" else 1,
            horizontal=True,
            key=f"scale-{key}",
        )
    years = None if window_label == "Max" else int(window_label.rstrip("Y"))
    shown = filter_window(df, years)
    shown = apply_scale(shown, view)
    mode = view
    return shown, mode


def render_line_chart(
    df,
    *,
    key: str,
    height: int = 360,
    default_years: int | None = 5,
    default_scale: str = "Level",
) -> None:
    shown, mode = chart_df(df, key=key, default_years=default_years, default_scale=default_scale)
    if shown is None or shown.empty:
        st.info("No chart data")
        return
    st.line_chart(shown, height=height, use_container_width=True)
    if mode == "Indexed = 100":
        st.caption("Indexed view: first visible observation = 100. Use Level for source units.")
    elif mode == "% change from start":
        st.caption("% change view: change since first visible observation. Use Level for source units.")


def render_altair_compare(data, *, title: str, height: int, independent_y: bool = False) -> None:
    if data is None or data.empty:
        st.info("No chart data")
        return
    if alt is None:
        pivot = data.pivot(index="date", columns="series", values="value")
        st.line_chart(pivot, height=height, use_container_width=True)
        return
    base = alt.Chart(data).mark_line().encode(
        x=alt.X("date:T", title=None),
        y=alt.Y("value:Q", title=None),
        color=alt.Color("series:N", legend=alt.Legend(orient="bottom", title=None)),
        tooltip=[alt.Tooltip("date:T"), alt.Tooltip("series:N"), alt.Tooltip("value:Q", format=",.2f")],
    ).properties(height=height, title=title)
    if independent_y:
        chart = base.facet(row=alt.Row("series:N", title=None, header=alt.Header(labelLimit=380))).resolve_scale(y="independent")
        st.altair_chart(chart, use_container_width=True)
    else:
        st.altair_chart(base.interactive(), use_container_width=True)


def inject_style() -> None:
    st.markdown(
        """
        <style>
        :root {--terminal-bg:#07111f; --terminal-panel:#0f1b2d; --terminal-line:#24364f; --terminal-cyan:#38bdf8; --terminal-text:#dbeafe;}
        .stApp {background: linear-gradient(180deg, #f8fafc 0%, #eef3f8 100%);}
        .main .block-container {padding-top: 1.1rem; max-width: 1480px;}
        h1 {font-size: 2.35rem !important; line-height: 1.05; margin-bottom: 0.2rem;}
        h2, h3 {letter-spacing: -0.02em;}
        [data-testid="stSidebar"] {background: #07111f; border-right: 1px solid #1f3350;}
        [data-testid="stSidebar"] * {color: #dbeafe !important;}
        [data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] .stRadio {background: transparent;}
        [data-testid="stSidebar"] div[data-baseweb="select"] > div {background: #0f1b2d; border-color: #2b4263; color: #e0f2fe;}
        [data-testid="stSidebar"] hr {border-color: #24364f;}
        div[data-testid="stMetric"] {background: #ffffff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 14px 16px; box-shadow: 0 1px 2px rgba(15,23,42,0.04);}
        .fincept-topbar {background: linear-gradient(90deg, #07111f 0%, #0f1b2d 55%, #13294b 100%); border: 1px solid #24364f; border-radius: 18px; padding: 14px 18px; margin-bottom: 14px; box-shadow: 0 14px 34px rgba(15,23,42,0.16);}
        .fincept-row {display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap;}
        .fincept-brand {color:#ffffff; font-weight:900; letter-spacing:.04em; font-size:1.02rem; text-transform:uppercase;}
        .fincept-sub {color:#93c5fd; font-size:.82rem; margin-top:2px;}
        .fincept-pills {display:flex; gap:8px; flex-wrap:wrap;}
        .fincept-pill {border:1px solid #31547b; border-radius:999px; padding:6px 10px; color:#c7d2fe; background:rgba(15,27,45,.75); font-size:.76rem; font-weight:750; text-transform:uppercase; letter-spacing:.035em;}
        .fincept-pill.hot {color:#07111f; background:#38bdf8; border-color:#7dd3fc;}
        .fincept-shell-note {background:#0f1b2d; color:#dbeafe; border:1px solid #24364f; border-radius:14px; padding:10px 12px; font-size:.82rem; margin-bottom:14px;}
        .macro-card {background: #ffffff; border: 1px solid #d7e0ea; border-radius: 16px; padding: 16px; margin: 8px 0 18px 0; box-shadow: 0 1px 3px rgba(15,23,42,0.05);}
        .snapshot-version {display: inline-flex; align-items: center; gap: 6px; background: #0f172a; color: #e0f2fe; border: 1px solid #38bdf8; border-radius: 999px; padding: 5px 10px; font-size: 0.78rem; font-weight: 800; letter-spacing: 0.03em; text-transform: uppercase; margin: 0.1rem 0 0.55rem 0;}
        .snapshot-grid {display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin: 0.6rem 0 1rem 0;}
        .snapshot-card {background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 58%, #0369a1 100%); border: 1px solid #38bdf8; border-radius: 14px; padding: 13px 14px; box-shadow: 0 10px 24px rgba(15,23,42,0.18);}
        .snapshot-label {color: #bae6fd; font-size: 0.78rem; font-weight: 800; letter-spacing: 0.055em; text-transform: uppercase; margin-bottom: 0.3rem;}
        .snapshot-value {color: #ffffff; font-size: 1.45rem; font-weight: 900; line-height: 1.05; text-shadow: 0 1px 2px rgba(0,0,0,0.28);}
        .snapshot-note {color: #dbeafe; font-size: 0.80rem; font-weight: 650; margin-top: 0.35rem;}
        .small-muted {color: #64748b; font-size: 0.88rem;}
        @media (max-width: 1100px) {.snapshot-grid {grid-template-columns: repeat(2, minmax(0, 1fr));}}
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


def render_terminal_header(active_page: str) -> None:
    st.markdown(
        f"""
        <div class="fincept-topbar">
          <div class="fincept-row">
            <div>
              <div class="fincept-brand">FINCEPT-STYLE MACRO TERMINAL · v0.4</div>
              <div class="fincept-sub">US macro monitor · official-source JSON states · report-ready workspace</div>
            </div>
            <div class="fincept-pills">
              <span class="fincept-pill hot">{active_page}</span>
              <span class="fincept-pill">Snapshot locked</span>
              <span class="fincept-pill">FRED</span>
              <span class="fincept-pill">Treasury</span>
              <span class="fincept-pill">NY Fed</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_snapshot() -> None:
    rates = load_json(STATE_FILES["Rates / curve"]).get("summary", {})
    infl = load_json(STATE_FILES["Inflation + labor"]).get("summary", {})
    growth = load_json(STATE_FILES["Growth / activity"]).get("summary", {})
    tga = load_json(STATE_FILES["TGA"])
    rrp = load_json(STATE_FILES["RRP"])
    reserves = load_json(STATE_FILES["Reserve balances"])
    liquidity_markets = load_json(STATE_FILES["Liquidity / markets"]).get("summary", {})

    latest_reserves = (reserves.get("latest") or {}).get("reserveBalancesUsdMn")
    snapshot = [
        ("10Y Treasury", pct(rates.get("latest10yPct")), "rates"),
        ("10Y–2Y curve", pct(rates.get("latest10y2ySpreadPctPts")), "spread"),
        ("Core PCE YoY", pct(infl.get("corePceYoyPct")), "inflation"),
        ("Unemployment", pct(infl.get("unemploymentRatePct")), "labor"),
        ("Real GDP QoQ", pct(growth.get("realGdpQoQPct")), "growth"),
        ("Payroll Δ", f"{fmt(infl.get('payrollsOneMonthChangeK'), 'k', 0)}", "latest month"),
        ("TGA", fmt(((tga.get("tgaOpeningBalance") or {}).get("openTodayBalanceUsdMn")), "mn", 0), "Treasury cash"),
        ("RRP", fmt(((rrp.get("latest") or {}).get("totalAcceptedUsdBn")), "bn", 3), "NY Fed"),
        ("Reserve balances", fmt(latest_reserves, "mn", 0), "Fed H.4.1"),
        ("M2 YoY", pct(liquidity_markets.get("m2YoyPct")), "money stock"),
        ("VIX", fmt(liquidity_markets.get("vixLatest"), "", 1), "risk context"),
    ]

    st.subheader("Macro regime snapshot")
    st.markdown("<div class='snapshot-version'>Snapshot UX v2 · high contrast</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='snapshot-grid'>"
        + "".join(
            f"<div class='snapshot-card'><div class='snapshot-label'>{label}</div><div class='snapshot-value'>{value}</div><div class='snapshot-note'>{note}</div></div>"
            for label, value, note in snapshot
        )
        + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='macro-card'><b>Read:</b> growth still expanding, labor resilient, inflation still above target context, rates falling with a positive but flattening curve, and liquidity mixed. <b>Actionability:</b> monitor-only.</div>",
        unsafe_allow_html=True,
    )


def render_series_explorer(block: str, global_window: str | None = None, global_scale: str | None = None, global_rows: int | None = None, global_mode: str | None = None) -> None:
    st.subheader(block)
    family_map = SERIES_FAMILIES.get(block, {"All": BLOCKS[block]})
    family_names = list(family_map.keys())
    family = st.segmented_control("Family", family_names, default=family_names[0], key=f"family-{block}")
    ids = family_map[family]
    view = global_mode or st.segmented_control(
        "Display mode",
        ["Single series", "Compare normalized", "Small multiples"],
        default="Single series",
        key=f"display-{block}",
    )

    if view in {"Compare normalized", "Small multiples"}:
        default_pick = ids[: min(4, len(ids))]
        selected_ids = st.multiselect(
            "Series",
            ids,
            default=default_pick,
            format_func=lambda sid: display_name(block, sid),
            key=f"compare-series-{block}",
        )
        c1, c2 = st.columns([0.28, 0.72])
        with c1:
            window_label = global_window or st.selectbox("Window", ["1Y", "3Y", "5Y", "10Y", "Max"], index=2, key=f"compare-window-{block}")
        with c2:
            default_scale = "Indexed = 100" if view == "Compare normalized" else "Level"
            scale = global_scale or st.radio(
                "Scale",
                ["Level", "Indexed = 100", "% change from start"],
                index=["Level", "Indexed = 100", "% change from start"].index(default_scale),
                horizontal=True,
                key=f"compare-scale-{block}",
            )
        years = None if window_label == "Max" else int(window_label.rstrip("Y"))
        items = [(block, sid) for sid in selected_ids]
        data = long_compare_df(items, years, scale)
        if view == "Small multiples":
            render_altair_compare(data, title=f"{block} — separated y-axes", height=150, independent_y=True)
            st.caption("Small multiples use independent y-axes, so low-amplitude series no longer disappear next to large-level series.")
        else:
            render_altair_compare(data, title=f"{block} — normalized comparison", height=430, independent_y=False)
            st.caption("Normalized comparison is best for shape/cycle comparison. Use Single series for source-unit inspection.")
        return

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
            defaults = SERIES_CHART_DEFAULTS.get(selected, {"years": 5, "scale": "Level"})
            render_line_chart(
                df,
                key=chart_controls_key(f"{block}-{selected}"),
                height=360,
                default_years=defaults["years"],
                default_scale=defaults["scale"],
            )
            st.dataframe(df.sort_index(ascending=False).head(global_rows or 250), use_container_width=True, height=260)
        else:
            st.dataframe(points, use_container_width=True)
        with st.expander("Metadata / raw latest + trend"):
            st.json({"latest": item.get("latest"), "trend": item.get("trend"), "sourceUrl": item.get("sourceUrl")}, expanded=False)


def render_dashboard(global_window: str = "5Y", global_scale: str = "Indexed = 100", global_mode: str | None = None) -> None:
    render_snapshot()
    st.subheader("Portfolio-style macro workspace")
    quick_default = [
        ("Rates", "DGS10"),
        ("Rates", "T10Y2Y"),
        ("Rates", "MORTGAGE30US"),
        ("Inflation", "PCEPILFE"),
        ("Labor", "UNRATE"),
        ("Labor", "ICSA"),
        ("Growth", "GDPC1"),
        ("Growth", "INDPRO"),
        ("Markets", "M2SL"),
        ("Markets", "VIXCLS"),
    ]
    series_universe = [(block, sid) for block in ["Rates", "Inflation", "Labor", "Growth", "Markets"] for sid in BLOCKS[block]]
    with st.expander("Dashboard display controls", expanded=True):
        preset_name = st.selectbox("Preset", ["Custom"] + list(SERIES_PRESETS.keys()), index=0, key="dashboard-preset")
        preset_default = quick_default if preset_name == "Custom" else SERIES_PRESETS[preset_name]
        selected_quick = st.multiselect(
            "Series shown on dashboard",
            series_universe,
            default=[pair for pair in preset_default if pair in series_universe],
            format_func=lambda pair: display_name(pair[0], pair[1]),
            key="dashboard-key-series",
        )
        layout = global_mode or st.segmented_control(
            "Layout",
            ["Grid", "Normalized overlay", "Small multiples"],
            default="Grid",
            key="dashboard-layout",
        )
    if layout in {"Normalized overlay", "Small multiples"}:
        years = None if global_window == "Max" else int(global_window.rstrip("Y"))
        data = long_compare_df(selected_quick, years=years, scale=global_scale)
        render_altair_compare(
            data,
            title=f"Dashboard key series — {global_scale}",
            height=150 if layout == "Small multiples" else 460,
            independent_y=layout == "Small multiples",
        )
        return
    cols = st.columns(2)
    for i, (block, sid) in enumerate(selected_quick):
        item = series_item(block, sid)
        with cols[i % 2]:
            st.markdown(f"**{sid} — {item.get('seriesName', sid)}**")
            df = to_df(series_points(item))
            if df is not None:
                defaults = SERIES_CHART_DEFAULTS.get(sid, {"years": 5, "scale": "Level"})
                shown = filter_window(df, defaults["years"])
                if defaults["scale"] == "Indexed = 100":
                    shown = indexed_df(shown)
                st.line_chart(shown, height=180, use_container_width=True)
                if defaults["scale"] == "Indexed = 100":
                    st.caption("Indexed = 100")
            else:
                st.info("No data")


def render_multi_window_workspace(window_label: str, scale: str, rows: int, mode: str) -> None:
    render_snapshot()
    st.subheader("Macro data windows")
    st.caption("Main project-style structure: module windows, dense series coverage, sidebar display controls, tables limited by selected row count.")
    tabs = st.tabs(["Rates", "Inflation", "Labor", "Growth", "Liquidity", "Markets"])
    for tab, block in zip(tabs, ["Rates", "Inflation", "Labor", "Growth", "Liquidity", "Markets"]):
        with tab:
            if block == "Liquidity":
                render_liquidity()
            else:
                local_mode = "Small multiples" if mode == "Separated windows" else "Compare normalized"
                render_series_explorer(block, global_window=window_label, global_scale=scale, global_rows=rows, global_mode=local_mode)


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
                defaults = SERIES_CHART_DEFAULTS.get(title, {"years": 3, "scale": "Level"})
                render_line_chart(
                    df,
                    key=chart_controls_key(title),
                    height=360,
                    default_years=defaults["years"],
                    default_scale=defaults["scale"],
                )
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
        st.markdown("### FINCEPT")
        st.caption("Macro terminal shell")
        st.code(APP_VERSION)
        page = st.selectbox("Choose", ["Portfolio", "Dashboard", "Rates", "Inflation", "Labor", "Growth", "Liquidity", "Markets", "Calendar", "Report", "Raw state"], index=0)
        window_label = st.selectbox("Data window", ["1Y", "3Y", "5Y", "10Y", "Max"], index=2)
        scale = st.selectbox("Display scale", ["Level", "Indexed = 100", "% change from start"], index=1)
        rows = st.slider("Rows shown in tables", min_value=25, max_value=500, value=150, step=25)
        chart_mode = st.selectbox("Chart layout", ["Separated windows", "Overlay"], index=0)
        st.divider()
        st.markdown("**Workspace presets**")
        for name in SERIES_PRESETS:
            st.caption(f"▸ {name}")
        st.divider()
        st.markdown("**Series map**")
        for block, ids in BLOCKS.items():
            if ids:
                st.caption(f"{block.upper()} · {len(ids)} series")
        st.divider()
        st.markdown("**Scope**")
        st.caption("US macro spine: FRED + Treasury + NY Fed. Market series are context, not thesis signals.")
        st.divider()
        st.caption("Last data refresh")
        st.code(state_timestamp())
        st.caption("Source of truth: JSON states + Markdown report")

    render_terminal_header(page)

    missing = [name for name, path in STATE_FILES.items() if not path.exists()]
    if missing:
        st.warning(f"Missing state files: {', '.join(missing)}")

    if page == "Portfolio":
        render_multi_window_workspace(window_label, scale, rows, chart_mode)
    elif page == "Dashboard":
        layout = "Small multiples" if chart_mode == "Separated windows" else "Normalized overlay"
        render_dashboard(global_window=window_label, global_scale=scale, global_mode=layout)
    elif page in {"Rates", "Inflation", "Labor", "Growth", "Markets"}:
        mode = "Small multiples" if chart_mode == "Separated windows" else "Compare normalized"
        render_series_explorer(page, global_window=window_label, global_scale=scale, global_rows=rows, global_mode=mode)
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
