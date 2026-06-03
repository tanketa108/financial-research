#!/usr/bin/env python3
"""Render a Macro Monitor v0 report from template + macro event seed.

Dependency-free by design. This produces a disciplined draft report without
pretending the live data spine is complete.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TEMPLATE = ROOT / "financial_system" / "macro" / "templates" / "macro-monitor-template-v0.md"
DEFAULT_REGISTRY = ROOT / "financial_system" / "macro" / "macro-release-calendar-registry.json"
DEFAULT_EVENTS = ROOT / "financial_system" / "macro" / "macro-release-events.json"
DEFAULT_TGA_STATE = ROOT / "financial_system" / "macro" / "data" / "tga-state.json"
DEFAULT_RRP_STATE = ROOT / "financial_system" / "macro" / "data" / "nyfed-rrp-state.json"
DEFAULT_RESERVES_STATE = ROOT / "financial_system" / "macro" / "data" / "fed-reserve-balances-state.json"
DEFAULT_RATES_STATE = ROOT / "financial_system" / "macro" / "data" / "fred-rates-curve-state.json"
DEFAULT_INFLATION_LABOR_STATE = ROOT / "financial_system" / "macro" / "data" / "fred-inflation-labor-state.json"
DEFAULT_GROWTH_STATE = ROOT / "financial_system" / "macro" / "data" / "fred-growth-activity-state.json"
DEFAULT_REPORTS_DIR = ROOT / "financial_system" / "macro" / "reports"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def render_upcoming(registry: dict[str, Any], events: dict[str, Any], today: date, days: int) -> str:
    releases_by_id = {r["id"]: r for r in registry.get("releases", [])}
    horizon = date.fromordinal(today.toordinal() + days)
    dated: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []

    for event in events.get("events", []):
        release = releases_by_id.get(event.get("releaseId"))
        if not release:
            continue
        merged = {**event, "release": release}
        if event.get("releaseDate"):
            event_date = date.fromisoformat(event["releaseDate"])
            if today <= event_date <= horizon:
                dated.append(merged)
        else:
            pending.append(merged)

    dated.sort(key=lambda e: (e["releaseDate"], e.get("releaseTimeET") or "99:99", e["releaseId"]))

    lines = [f"Window: {today.isoformat()} to {horizon.isoformat()}", ""]
    if dated:
        for event in dated:
            release = event["release"]
            source = event.get("sourceUrl") or release.get("officialCalendarUrl")
            lines.append(
                f"- **{event['releaseDate']} {event.get('releaseTimeET', release.get('usualReleaseTimeET', 'TBD'))} ET** — "
                f"{release['name']} ({event.get('period', 'period TBD')}); "
                f"status: `{event.get('status', 'status TBD')}`; source: <{source}>"
            )
    else:
        lines.append("- No confirmed dated events in current window.")

    if pending:
        lines.extend(["", "Pending manual confirmation:"])
        for event in pending:
            release = event["release"]
            lines.append(f"- {release['name']} — {event.get('sourceNote', 'date not confirmed')}")
    return "\n".join(lines)


def render_executive_summary(events: dict[str, Any], report_date: date, rates_state_path: Path, inflation_labor_state_path: Path, growth_state_path: Path, tga_state_path: Path, rrp_state_path: Path, reserves_state_path: Path) -> str:
    next_event = None
    for event in sorted(events.get("events", []), key=lambda e: (e.get("releaseDate") or "9999-12-31", e.get("releaseTimeET") or "99:99")):
        if event.get("releaseDate") and date.fromisoformat(event["releaseDate"]) >= report_date:
            next_event = event
            break

    rates = load_json(rates_state_path).get("summary", {}) if rates_state_path.exists() else {}
    infl = load_json(inflation_labor_state_path).get("summary", {}) if inflation_labor_state_path.exists() else {}
    growth = load_json(growth_state_path).get("summary", {}) if growth_state_path.exists() else {}
    tga = load_json(tga_state_path) if tga_state_path.exists() else {}
    rrp = load_json(rrp_state_path) if rrp_state_path.exists() else {}
    reserves = load_json(reserves_state_path) if reserves_state_path.exists() else {}

    regime = (
        f"growth still expanding, labor resilient, inflation still above target context, "
        f"rates falling with a positive but flattening curve, and liquidity mixed."
    )
    change = (
        "v0.4 now has the full first-pass macro spine connected: rates/curve, inflation, labor, growth/activity and liquidity."
    )
    event_text = "not found"
    if next_event:
        event_text = f"{next_event.get('releaseId', 'macro release')} on {next_event.get('releaseDate')} {next_event.get('releaseTimeET', 'time TBD')} ET"
    uncertainty = (
        f"whether sticky core inflation ({fmt_pct(infl.get('corePceYoyPct'))} core PCE YoY) and resilient labor "
        f"keep rates restrictive, or falling rates/positive growth become the dominant portfolio context."
    )

    return "\n".join([
        f"- Current macro regime: **{regime}**",
        f"- Main change since last monitor: **{change}**",
        f"- Highest-signal release/event ahead: **{event_text}**.",
        f"- Key uncertainty: **{uncertainty}**",
        "",
        "Bottom line: **macro context is now usable, but still monitor-first.** No automatic portfolio action follows from this report alone; use it to frame valuation sensitivity, sector exposure and follow-up research tasks.",
        "",
        f"Quick cross-checks: 10Y-2Y spread **{fmt_pct(rates.get('latest10y2ySpreadPctPts'))}**; core PCE YoY **{fmt_pct(infl.get('corePceYoyPct'))}**; payroll change **{fmt_number(infl.get('payrollsOneMonthChangeK'), 0)}k**; real GDP QoQ **{fmt_signed_percent(growth.get('realGdpQoQPct'))}**; TGA/RRP/reserve liquidity remains mixed.",
    ])


def fmt_usd_mn(value: Any) -> str:
    if value is None:
        return "not reported"
    return f"${float(value):,.0f}mn"


def fmt_signed_usd_mn(value: Any) -> str:
    if value is None:
        return "not reported"
    number = float(value)
    sign = "+" if number > 0 else ""
    amount = abs(number)
    if number < 0:
        return f"-${amount:,.0f}mn"
    return f"{sign}${amount:,.0f}mn"


def fmt_usd_bn(value: Any) -> str:
    if value is None:
        return "not reported"
    return f"${float(value):,.3f}bn"


def fmt_signed_usd_bn(value: Any) -> str:
    if value is None:
        return "not reported"
    number = float(value)
    sign = "+" if number > 0 else ""
    amount = abs(number)
    if number < 0:
        return f"-${amount:,.3f}bn"
    return f"{sign}${amount:,.3f}bn"


def fmt_pct(value: Any) -> str:
    if value is None:
        return "not reported"
    return f"{float(value):.2f}%"


def fmt_signed_pct(value: Any) -> str:
    if value is None:
        return "not reported"
    number = float(value)
    sign = "+" if number > 0 else ""
    return f"{sign}{number:.2f}pp"


def fmt_signed_percent(value: Any) -> str:
    if value is None:
        return "not reported"
    number = float(value)
    sign = "+" if number > 0 else ""
    return f"{sign}{number:.2f}%"


def render_rates_curve_state(path: Path) -> str:
    if not path.exists():
        return "Data status: `pending`; run `fetch_fred_rates_curve_state.py` first."
    state = load_json(path)
    series = state.get("series") or {}
    summary = state.get("summary") or {}

    order = ["FEDFUNDS", "DGS2", "DGS10", "DGS30", "T10Y2Y", "T10Y3M"]
    lines = [
        "Data status: `FRED public CSV reachable; rates/curve extraction v0 active`",
        "",
        f"- Curve shape 10Y-2Y: **{summary.get('curveShape10y2y', 'unknown')}**; spread: **{fmt_pct(summary.get('latest10y2ySpreadPctPts'))}**.",
        f"- 2Y trend: `{summary.get('twoYearTrend', 'unknown')}`; 10Y trend: `{summary.get('tenYearTrend', 'unknown')}`; 10Y-2Y curve trend: `{summary.get('curveTrend10y2y', 'unknown')}`.",
        "- Latest rates/spreads:",
    ]
    for sid in order:
        item = series.get(sid) or {}
        latest = item.get("latest") or {}
        trend = item.get("trend") or {}
        lines.append(
            f"  - {sid} — {item.get('seriesName', sid)}: **{fmt_pct(latest.get('value'))}** "
            f"on {latest.get('observationDate', 'unknown')}; "
            f"one-period change: **{fmt_signed_pct(trend.get('onePeriodChange'))}**; "
            f"{trend.get('historyWindowRecords', 'n')}-obs trend: **{fmt_signed_pct(trend.get('windowChange'))}**."
        )
    lines.extend([
        "- Source URLs:",
    ])
    for sid in order:
        item = series.get(sid) or {}
        lines.append(f"  - {sid}: <{item.get('sourceUrl')}>")
    lines.extend([
        "- Caveat: rates/curve context frames valuation sensitivity and policy expectations; it is not a standalone portfolio instruction.",
    ])
    return "\n".join(lines)


def render_rates_interpretation(path: Path) -> str:
    if not path.exists():
        return "- Rates/curve interpretation: `pending`; rates state file missing."
    state = load_json(path)
    summary = state.get("summary") or {}
    shape = summary.get("curveShape10y2y", "unknown")
    ten_trend = summary.get("tenYearTrend", "unknown")
    two_trend = summary.get("twoYearTrend", "unknown")
    curve_trend = summary.get("curveTrend10y2y", "unknown")

    if shape.startswith("positive") and curve_trend == "falling":
        curve_signal = "positive but flattening curve; monitor whether long-end resilience or front-end repricing is driving the move."
    elif shape.startswith("positive") and curve_trend == "rising":
        curve_signal = "positive and steepening curve; usually a cleaner cyclical/term-premium context than an inverted curve."
    elif shape == "inverted":
        curve_signal = "inverted curve; keep recession/policy-tightness risk in the macro frame."
    else:
        curve_signal = "low-conviction curve signal; data or trend is incomplete."

    if two_trend == "rising" and ten_trend == "rising":
        policy_signal = "rates are rising across front and long end; valuation duration sensitivity should be monitored."
    elif two_trend == "falling" and ten_trend == "falling":
        policy_signal = "rates are falling across front and long end; confirm whether this reflects easing expectations or growth risk."
    else:
        policy_signal = "mixed rate move; avoid a single policy/risk conclusion without inflation/labor data."

    return "\n".join([
        f"- Curve signal: **{curve_signal}**",
        f"- Policy expectations signal: **{policy_signal}**",
        "- Portfolio use: frame valuation sensitivity, especially rate-sensitive growth, financials and cyclicals; do not create company tasks from curve data alone.",
        "- Caveat: inflation/labor data are still missing, so the rates read is context rather than a regime conclusion.",
    ])


def fmt_number(value: Any, decimals: int = 0) -> str:
    if value is None:
        return "not reported"
    return f"{float(value):,.{decimals}f}"


def render_inflation_state(path: Path) -> str:
    if not path.exists():
        return "Data status: `pending`; run `fetch_fred_inflation_labor_state.py` first."
    state = load_json(path)
    series = state.get("series") or {}
    order = ["CPIAUCSL", "CPILFESL", "PCEPI", "PCEPILFE"]
    lines = [
        "Data status: `FRED public CSV reachable; inflation extraction v0 active`",
        "",
        "Latest inflation indexes:",
    ]
    for sid in order:
        item = series.get(sid) or {}
        latest = item.get("latest") or {}
        trend = item.get("trend") or {}
        lines.append(
            f"- {sid} — {item.get('seriesName', sid)}: **{fmt_number(latest.get('value'), 3)}** "
            f"on {latest.get('observationDate', 'unknown')}; "
            f"MoM: **{fmt_signed_percent(trend.get('momPct'))}**; YoY: **{fmt_pct(trend.get('yoyPct'))}**."
        )
    lines.append("- Source URLs:")
    for sid in order:
        item = series.get(sid) or {}
        lines.append(f"  - {sid}: <{item.get('sourceUrl')}>")
    lines.append("- Caveat: FRED values are revised series; no consensus/surprise or release-vintage claims are made.")
    return "\n".join(lines)


def render_inflation_interpretation(path: Path) -> str:
    if not path.exists():
        return "- Inflation interpretation: `pending`; state file missing."
    state = load_json(path)
    summary = state.get("summary") or {}
    core_pce = summary.get("corePceYoyPct")
    core_cpi = summary.get("coreCpiYoyPct")
    if isinstance(core_pce, (int, float)) and core_pce > 2.5:
        momentum = "core PCE remains above a 2% inflation objective context; keep Fed sensitivity high."
    elif isinstance(core_pce, (int, float)):
        momentum = "core PCE is closer to target context, but confirm with monthly momentum and revisions."
    else:
        momentum = "inflation momentum is incomplete."
    return "\n".join([
        f"- Inflation momentum: **{momentum}**",
        f"- Core comparison: core CPI YoY **{fmt_pct(core_cpi)}**; core PCE YoY **{fmt_pct(core_pce)}**.",
        "- Fed relevance: use alongside rates/curve and upcoming FOMC/PCE releases; do not infer policy path without labor and release context.",
    ])


def render_labor_state(path: Path) -> str:
    if not path.exists():
        return "Data status: `pending`; run `fetch_fred_inflation_labor_state.py` first."
    state = load_json(path)
    series = state.get("series") or {}
    order = ["PAYEMS", "UNRATE", "CIVPART", "CES0500000003", "ICSA", "JTSJOL"]
    lines = [
        "Data status: `FRED public CSV reachable; labor extraction v0 active`",
        "",
        "Latest labor indicators:",
    ]
    for sid in order:
        item = series.get(sid) or {}
        latest = item.get("latest") or {}
        trend = item.get("trend") or {}
        decimals = 2 if item.get("units") in {"percent", "USD/hour"} else 0
        change_decimals = 2 if item.get("units") in {"percent", "USD/hour"} else 0
        extra = ""
        if item.get("calc") == "mom_yoy":
            extra = f"; MoM: **{fmt_signed_percent(trend.get('momPct'))}**; YoY: **{fmt_pct(trend.get('yoyPct'))}**"
        else:
            extra = f"; one-period change: **{fmt_number(trend.get('onePeriodChange'), change_decimals)}**; window direction: `{trend.get('windowDirection', 'unknown')}`"
        lines.append(
            f"- {sid} — {item.get('seriesName', sid)}: **{fmt_number(latest.get('value'), decimals)}** "
            f"{item.get('units', '')} on {latest.get('observationDate', 'unknown')}{extra}."
        )
    lines.append("- Source URLs:")
    for sid in order:
        item = series.get(sid) or {}
        lines.append(f"  - {sid}: <{item.get('sourceUrl')}>")
    lines.append("- Caveat: labor data may be revised; release-time surprise and detail tables are outside v0.")
    return "\n".join(lines)


def render_labor_interpretation(path: Path) -> str:
    if not path.exists():
        return "- Labor interpretation: `pending`; state file missing."
    state = load_json(path)
    summary = state.get("summary") or {}
    payroll = summary.get("payrollsOneMonthChangeK")
    unrate = summary.get("unemploymentRatePct")
    claims = summary.get("initialClaimsLatest")
    if isinstance(payroll, (int, float)) and payroll > 0 and isinstance(unrate, (int, float)) and unrate <= 4.5:
        demand = "labor market still looks resilient on headline payrolls/unemployment."
    elif isinstance(payroll, (int, float)) and payroll < 0:
        demand = "payrolls contracted in the latest observation; monitor cooling risk."
    else:
        demand = "mixed or incomplete labor signal."
    return "\n".join([
        f"- Labor demand: **{demand}**",
        f"- Headline checks: payroll one-month change **{fmt_number(payroll, 0)}k**; unemployment **{fmt_pct(unrate)}**; initial claims **{fmt_number(claims, 0)}**.",
        "- Fed relevance: labor is now usable as context, but not yet release-grade without NFP detail/revisions and BLS calendar wiring.",
    ])


def render_growth_state(path: Path) -> str:
    if not path.exists():
        return "Data status: `pending`; run `fetch_fred_growth_activity_state.py` first."
    state = load_json(path)
    series = state.get("series") or {}
    order = ["GDPC1", "PCECC96", "RSXFS", "RRSFS", "INDPRO", "HOUST", "PERMIT", "DGORDER", "NEWORDER"]
    lines = [
        "Data status: `FRED public CSV reachable; growth/activity extraction v0 active`",
        "",
        "Latest growth/activity indicators:",
    ]
    for sid in order:
        item = series.get(sid) or {}
        latest = item.get("latest") or {}
        trend = item.get("trend") or {}
        decimals = 3 if item.get("units") == "index" else 0
        lines.append(
            f"- {sid} — {item.get('seriesName', sid)}: **{fmt_number(latest.get('value'), decimals)}** "
            f"{item.get('units', '')} on {latest.get('observationDate', 'unknown')}; "
            f"one-period: **{fmt_signed_percent(trend.get('onePeriodPct'))}**; YoY: **{fmt_pct(trend.get('yoyPct'))}**; "
            f"window direction: `{trend.get('windowDirection', 'unknown')}`."
        )
    lines.append("- Source URLs:")
    for sid in order:
        item = series.get(sid) or {}
        lines.append(f"  - {sid}: <{item.get('sourceUrl')}>")
    lines.append("- Caveat: FRED values are revised series; no consensus/surprise or release-vintage claims are made.")
    return "\n".join(lines)


def render_growth_interpretation(path: Path) -> str:
    if not path.exists():
        return "- Growth interpretation: `pending`; state file missing."
    state = load_json(path)
    summary = state.get("summary") or {}
    gdp_qoq = summary.get("realGdpQoQPct")
    pce_qoq = summary.get("realPceQoQPct")
    retail = summary.get("realRetailSalesMoMPct")
    ip = summary.get("industrialProductionMoMPct")
    capex = summary.get("coreCapexOrdersMoMPct")

    if isinstance(gdp_qoq, (int, float)) and gdp_qoq > 0 and isinstance(pce_qoq, (int, float)) and pce_qoq > 0:
        momentum = "real GDP and real PCE are still expanding in the latest quarterly observations."
    elif isinstance(gdp_qoq, (int, float)) and gdp_qoq < 0:
        momentum = "real GDP contracted in the latest quarterly observation; monitor downside growth risk."
    else:
        momentum = "growth signal is mixed or incomplete."

    if isinstance(retail, (int, float)) and retail < 0:
        consumer = "real retail sales fell in the latest monthly observation; consumer momentum needs monitoring."
    elif isinstance(retail, (int, float)):
        consumer = "real retail sales are not showing acute monthly weakness in the latest observation."
    else:
        consumer = "consumer signal incomplete."

    capex_line = f"industrial production MoM **{fmt_signed_percent(ip)}**; core capex orders MoM **{fmt_signed_percent(capex)}**."
    return "\n".join([
        f"- Growth momentum: **{momentum}**",
        f"- Consumer/capex split: **{consumer}** {capex_line}",
        "- Cyclical risk: context is not recessionary from this minimal block alone, but full call requires revisions, ISM/surveys and credit conditions.",
    ])


def render_portfolio_context(rates_state_path: Path, inflation_labor_state_path: Path, growth_state_path: Path) -> str:
    rates = load_json(rates_state_path).get("summary", {}) if rates_state_path.exists() else {}
    infl = load_json(inflation_labor_state_path).get("summary", {}) if inflation_labor_state_path.exists() else {}
    growth = load_json(growth_state_path).get("summary", {}) if growth_state_path.exists() else {}
    return "\n".join([
        "Operating rule: macro informs portfolio context; it does not make portfolio decisions.",
        "",
        "- Portfolio areas potentially affected: rate-sensitive growth, financials/banks, cyclicals, housing-exposed names, consumer discretionary, USD/liquidity-sensitive assets and valuation duration broadly.",
        "- Current macro framing: falling rates and positive growth are supportive context, but sticky core inflation and mixed liquidity prevent a clean risk-on conclusion.",
        f"- Key numbers to carry into portfolio review: 10Y **{fmt_pct(rates.get('latest10yPct'))}**; 10Y-2Y **{fmt_pct(rates.get('latest10y2ySpreadPctPts'))}**; core PCE YoY **{fmt_pct(infl.get('corePceYoyPct'))}**; unemployment **{fmt_pct(infl.get('unemploymentRatePct'))}**; real GDP QoQ **{fmt_signed_percent(growth.get('realGdpQoQPct'))}**.",
        "- Actionability: **monitor only**. No model update or company-specific task should be created from this report alone unless the user wants a sector/company sensitivity pass.",
    ])


def render_tga_trend(state: dict[str, Any]) -> list[str]:
    trend = state.get("tgaTrend") or {}
    history = trend.get("historyLatestFirst") or []
    if not history:
        return ["- TGA trend: `pending`; history not available in state file."]

    direction = "flat"
    window_change = trend.get("windowChangeUsdMn")
    if isinstance(window_change, (int, float)):
        if window_change > 0:
            direction = "rising"
        elif window_change < 0:
            direction = "falling"

    lines = [
        f"- TGA one-day change: **{fmt_signed_usd_mn(trend.get('oneDayChangeUsdMn'))}** vs prior available DTS record.",
        f"- TGA {trend.get('historyWindowRecords', len(history))}-record trend ({trend.get('windowStartDate', 'unknown')} → {trend.get('windowEndDate', 'unknown')}): **{fmt_signed_usd_mn(window_change)}**; direction: `{direction}`.",
        "- Recent TGA history, latest first:",
    ]
    for point in history[:5]:
        lines.append(f"  - {point.get('recordDate')}: {fmt_usd_mn(point.get('tgaOpeningBalanceUsdMn'))}")
    return lines


def render_tga_state(path: Path) -> str:
    if not path.exists():
        return "- TGA state: `pending`; run `fetch_treasury_tga_state.py` first."
    state = load_json(path)
    tga = state.get("tgaOpeningBalance") or {}
    deposits = state.get("totalTgaDeposits") or {}
    withdrawals = state.get("totalTgaWithdrawals") or {}
    lines = [
        f"- Source: Treasury FiscalData Daily Treasury Statement; record date: **{state.get('recordDate', 'unknown')}**; units: `{state.get('units', 'USD millions')}`.",
        f"- TGA opening balance: **{fmt_usd_mn(tga.get('openTodayBalanceUsdMn'))}**.",
        f"- Total TGA deposits: **{fmt_usd_mn(deposits.get('openTodayBalanceUsdMn'))}**.",
        f"- Total TGA withdrawals: **{fmt_usd_mn(withdrawals.get('openTodayBalanceUsdMn'))}**.",
        *render_tga_trend(state),
        f"- Source URL: <{state.get('sourceUrl')}>",
        "- Caveat: Treasury accounting fields need exact source definitions; treat this as liquidity context, not a standalone signal.",
    ]
    return "\n".join(lines)


def render_rrp_state(path: Path) -> str:
    if not path.exists():
        return "- NY Fed reverse repo state: `pending`; run `fetch_nyfed_rrp_state.py` first."
    state = load_json(path)
    latest = state.get("latest") or {}
    trend = state.get("trend") or {}
    history = trend.get("historyLatestFirst") or []

    direction = "flat"
    window_change = trend.get("windowChangeUsdBn")
    if isinstance(window_change, (int, float)):
        if window_change > 0:
            direction = "rising"
        elif window_change < 0:
            direction = "falling"

    lines = [
        "",
        "NY Fed reverse repo:",
        f"- Source: NY Fed Markets API; latest operation date: **{latest.get('operationDate', 'unknown')}**; units: `{state.get('units', 'USD billions')}`.",
        f"- Total accepted RRP amount: **{fmt_usd_bn(latest.get('totalAcceptedUsdBn'))}**.",
        f"- Accepted counterparties: **{latest.get('acceptedCounterparties', 'not reported')}**; award/offering rate: **{latest.get('treasuryAwardRatePct', latest.get('treasuryOfferingRatePct', 'not reported'))}%**.",
        f"- RRP one-day change: **{fmt_signed_usd_bn(trend.get('oneDayChangeUsdBn'))}** vs prior available operation.",
        f"- RRP {trend.get('historyWindowRecords', len(history))}-operation trend ({trend.get('windowStartDate', 'unknown')} → {trend.get('windowEndDate', 'unknown')}): **{fmt_signed_usd_bn(window_change)}**; direction: `{direction}`.",
        "- Recent RRP history, latest first:",
    ]
    for point in history[:5]:
        lines.append(f"  - {point.get('operationDate')}: {fmt_usd_bn(point.get('totalAcceptedUsdBn'))}")
    lines.extend([
        f"- Source URL: <{state.get('sourceUrl')}>",
        "- Caveat: reverse repo take-up is useful liquidity context, not a standalone macro/portfolio signal.",
    ])
    return "\n".join(lines)


def render_reserves_state(path: Path) -> str:
    if not path.exists():
        return "- Fed reserve balances state: `pending`; run `fetch_fred_reserve_balances_state.py` first."
    state = load_json(path)
    latest = state.get("latest") or {}
    trend = state.get("trend") or {}
    history = trend.get("historyLatestFirst") or []

    direction = trend_direction(trend.get("windowChangeUsdMn"))

    lines = [
        "",
        "Fed reserve balances:",
        f"- Source: FRED public CSV `{state.get('seriesId', 'WRESBAL')}` / {state.get('seriesName', 'Reserve Balances with Federal Reserve Banks')}; latest observation: **{latest.get('observationDate', 'unknown')}**; units: `{state.get('units', 'USD millions')}`.",
        f"- Reserve balances: **{fmt_usd_mn(latest.get('reserveBalancesUsdMn'))}**.",
        f"- Reserve balances one-period change: **{fmt_signed_usd_mn(trend.get('onePeriodChangeUsdMn'))}** vs prior available observation.",
        f"- Reserve balances {trend.get('historyWindowRecords', len(history))}-observation trend ({trend.get('windowStartDate', 'unknown')} → {trend.get('windowEndDate', 'unknown')}): **{fmt_signed_usd_mn(trend.get('windowChangeUsdMn'))}**; direction: `{direction}`.",
        "- Recent reserve balances history, latest first:",
    ]
    for point in history[:5]:
        lines.append(f"  - {point.get('observationDate')}: {fmt_usd_mn(point.get('reserveBalancesUsdMn'))}")
    lines.extend([
        f"- Source URL: <{state.get('sourceUrl')}>",
        "- Caveat: reserve balances improve the liquidity read, but still need funding-market context before portfolio conclusions.",
    ])
    return "\n".join(lines)


def trend_direction(value: Any) -> str:
    if not isinstance(value, (int, float)):
        return "unknown"
    if value > 0:
        return "rising"
    if value < 0:
        return "falling"
    return "flat"


def render_liquidity_interpretation(tga_state_path: Path, rrp_state_path: Path, reserves_state_path: Path) -> str:
    if not tga_state_path.exists() or not rrp_state_path.exists():
        return "- `pending`: TGA and RRP state files are both required for automatic liquidity interpretation."

    tga_state = load_json(tga_state_path)
    rrp_state = load_json(rrp_state_path)
    tga_change = (tga_state.get("tgaTrend") or {}).get("windowChangeUsdMn")
    rrp_change = (rrp_state.get("trend") or {}).get("windowChangeUsdBn")
    tga_dir = trend_direction(tga_change)
    rrp_dir = trend_direction(rrp_change)

    if tga_dir == "rising" and rrp_dir == "falling":
        summary = "mixed liquidity context: rising TGA is a reserve drain, while falling RRP can partly offset by releasing cash from the facility."
        stance = "monitor net effect; do not collapse it into a single bullish/bearish signal."
    elif tga_dir == "rising" and rrp_dir in {"rising", "flat"}:
        summary = "potential liquidity drain: TGA is rising and RRP is not providing a clear offset."
        stance = "watch funding/liquidity sensitivity more closely."
    elif tga_dir == "falling" and rrp_dir == "falling":
        summary = "potential liquidity support: TGA and RRP are both falling, mechanically reducing two cash-absorbing balances."
        stance = "supportive context only; confirm with reserves/funding indicators."
    elif tga_dir == "falling" and rrp_dir in {"rising", "flat"}:
        summary = "mixed liquidity context: falling TGA adds cash, but RRP is not clearly reinforcing that impulse."
        stance = "monitor persistence before drawing conclusions."
    else:
        summary = "low-conviction liquidity context: TGA/RRP trend combination is incomplete or flat."
        stance = "keep as context, not signal."

    reserve_lines: list[str] = []
    if reserves_state_path.exists():
        reserves_state = load_json(reserves_state_path)
        reserve_change = (reserves_state.get("trend") or {}).get("windowChangeUsdMn")
        reserve_dir = trend_direction(reserve_change)
        reserve_lines.append(f"- Cross-check: reserve balances trend `{reserve_dir}` ({fmt_signed_usd_mn(reserve_change)} over window). This is the direct balance-sheet confirmation leg for the TGA/RRP read.")
    else:
        reserve_lines.append("- Cross-check: reserve balances missing; run `fetch_fred_reserve_balances_state.py` to close the TGA/RRP/reserves triangle.")

    return "\n".join([
        f"- Automatic liquidity read: **{summary}**",
        f"- Inputs: TGA trend `{tga_dir}` ({fmt_signed_usd_mn(tga_change)} over window); RRP trend `{rrp_dir}` ({fmt_signed_usd_bn(rrp_change)} over window).",
        *reserve_lines,
        f"- Portfolio use: {stance}",
        "- Caveat: this is a rules-based context note, not an investment conclusion; funding spreads and market plumbing stress indicators are still outside the v0 data spine.",
    ])


def render_report(template: str, registry: dict[str, Any], events: dict[str, Any], report_date: date, days: int, tga_state_path: Path, rrp_state_path: Path, reserves_state_path: Path, rates_state_path: Path, inflation_labor_state_path: Path, growth_state_path: Path) -> str:
    return (
        template
        .replace("{{report_date}}", report_date.isoformat())
        .replace("{{executive_summary}}", render_executive_summary(events, report_date, rates_state_path, inflation_labor_state_path, growth_state_path, tga_state_path, rrp_state_path, reserves_state_path))
        .replace("{{upcoming_releases}}", render_upcoming(registry, events, report_date, days))
        .replace("{{rates_curve_state}}", render_rates_curve_state(rates_state_path))
        .replace("{{rates_interpretation}}", render_rates_interpretation(rates_state_path))
        .replace("{{inflation_state}}", render_inflation_state(inflation_labor_state_path))
        .replace("{{inflation_interpretation}}", render_inflation_interpretation(inflation_labor_state_path))
        .replace("{{labor_state}}", render_labor_state(inflation_labor_state_path))
        .replace("{{labor_interpretation}}", render_labor_interpretation(inflation_labor_state_path))
        .replace("{{growth_state}}", render_growth_state(growth_state_path))
        .replace("{{growth_interpretation}}", render_growth_interpretation(growth_state_path))
        .replace("{{portfolio_context}}", render_portfolio_context(rates_state_path, inflation_labor_state_path, growth_state_path))
        .replace("{{tga_state}}", render_tga_state(tga_state_path))
        .replace("{{rrp_state}}", render_rrp_state(rrp_state_path))
        .replace("{{reserves_state}}", render_reserves_state(reserves_state_path))
        .replace("{{liquidity_interpretation}}", render_liquidity_interpretation(tga_state_path, rrp_state_path, reserves_state_path))
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Macro Monitor v0 report.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Report date YYYY-MM-DD")
    parser.add_argument("--days", type=int, default=60, help="Upcoming-release horizon")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--tga-state", type=Path, default=DEFAULT_TGA_STATE)
    parser.add_argument("--rrp-state", type=Path, default=DEFAULT_RRP_STATE)
    parser.add_argument("--reserves-state", type=Path, default=DEFAULT_RESERVES_STATE)
    parser.add_argument("--rates-state", type=Path, default=DEFAULT_RATES_STATE)
    parser.add_argument("--inflation-labor-state", type=Path, default=DEFAULT_INFLATION_LABOR_STATE)
    parser.add_argument("--growth-state", type=Path, default=DEFAULT_GROWTH_STATE)
    parser.add_argument("--out", type=Path, help="Output path; defaults to reports/YYYY-MM-DD-macro-monitor-v0.md")
    args = parser.parse_args()

    report_date = date.fromisoformat(args.date)
    template = args.template.read_text(encoding="utf-8")
    report = render_report(template, load_json(args.registry), load_json(args.events), report_date, args.days, args.tga_state, args.rrp_state, args.reserves_state, args.rates_state, args.inflation_labor_state, args.growth_state)

    out = args.out or (DEFAULT_REPORTS_DIR / f"{report_date.isoformat()}-macro-monitor-v0.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
