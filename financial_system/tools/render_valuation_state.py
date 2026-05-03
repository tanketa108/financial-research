#!/usr/bin/env python3
"""Render a human-readable valuation view from valuation-state JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
VALUATIONS = ROOT / 'valuations'


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def fmt_money(value):
    if value is None:
        return '[missing]'
    try:
        return f"{value:,.0f}"
    except Exception:
        return str(value)


def fmt_num(value):
    if value is None:
        return '[missing]'
    return str(value)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('Usage: render_valuation_state.py <TICKER>', file=sys.stderr)
        return 1

    ticker = argv[1].upper()
    state_path = VALUATIONS / f'{ticker}-valuation-state-v1.json'
    if not state_path.exists():
        print(f'missing {state_path}', file=sys.stderr)
        return 1

    data = load_json(state_path)
    output_path = VALUATIONS / f'{ticker}-valuation-display-v1.md'

    lines = [f'# {ticker} — Valuation Display v1', '']
    lines.append(f"- **Status:** {data.get('status')}")
    lp = data.get('latest_period') or {}
    if lp:
        lines.append(f"- **Latest period:** {lp.get('form_type')} | report date {lp.get('report_date')}")
    lines.append('')

    thesis = data.get('thesis') or {}
    lines.append('## Thesis Snapshot')
    lines.append('')
    lines.append(f"- **Thesis short:** {thesis.get('thesis_short') or '[missing]'}")
    lines.append(f"- **Current stance:** {thesis.get('current_stance') or '[missing]'}")
    lines.append(f"- **What would change my mind:** {thesis.get('what_would_change_my_mind') or '[missing]'}")
    lines.append('')

    hist = data.get('historical_base') or {}
    lines.append('## Current Financial Base')
    lines.append('')
    lines.append(f"- Revenue: {fmt_money(hist.get('latest_revenue'))} USD")
    lines.append(f"- Operating income: {fmt_money(hist.get('latest_operating_income'))} USD")
    lines.append(f"- Net income: {fmt_money(hist.get('latest_net_income'))} USD")
    lines.append(f"- Diluted EPS: {fmt_num(hist.get('latest_diluted_eps'))} USD/share")
    lines.append(f"- Cash and equivalents: {fmt_money(hist.get('latest_cash_and_equivalents'))} USD")
    lines.append(f"- Total debt: {fmt_money(hist.get('latest_total_debt'))} USD")
    lines.append('')

    lines.append('## Key Drivers')
    lines.append('')
    for d in data.get('drivers') or []:
        lines.append(f'- {d}')
    lines.append('')

    lines.append('## Segments')
    lines.append('')
    for seg in data.get('segments') or []:
        lines.append(f"### {seg.get('name')}")
        lines.append(f"- Importance: {seg.get('importance') or '[missing]'}")
        lines.append(f"- Growth view: {seg.get('growth_view') or '[missing]'}")
        lines.append(f"- Margin view: {seg.get('margin_view') or '[missing]'}")
        lines.append(f"- Notes: {seg.get('notes') or '[missing]'}")
        lines.append('')

    quality = data.get('quality') or {}
    lines.append('## Quality of Business')
    lines.append('')
    lines.append(f"- Operating margin: {fmt_num(quality.get('operating_margin'))}")
    lines.append(f"- Net margin: {fmt_num(quality.get('net_margin'))}")
    lines.append(f"- ROIC (historical): {fmt_num((quality.get('roic') or {}).get('historical'))}")
    lines.append(f"- ROIC (expected): {fmt_num((quality.get('roic') or {}).get('expected'))}")
    lines.append(f"- WACC: {fmt_num(quality.get('wacc'))}")
    lines.append(f"- EVA spread: {fmt_num(quality.get('eva_spread'))}")
    notes = quality.get('notes') or []
    for note in notes:
        lines.append(f"- Note: {note}")
    lines.append('')

    debt = data.get('debt') or {}
    lines.append('## Debt')
    lines.append('')
    lines.append(f"- Total debt: {fmt_money(debt.get('total_debt'))} USD")
    lines.append(f"- Cash: {fmt_money(debt.get('cash'))} USD")
    lines.append(f"- Net debt: {fmt_money(debt.get('net_debt'))} USD")
    interest = debt.get('interest_burden') or {}
    lines.append(f"- Interest burden: {fmt_money(interest.get('value')) if interest else '[missing]'} USD")
    lines.append(f"- Refinancing risk: {debt.get('refinancing_risk') or '[missing]'}")
    lines.append('')

    cash_conv = data.get('cash_conversion') or {}
    lines.append('## Cash Conversion')
    lines.append('')
    ccc = cash_conv.get('ccc') or {}
    lines.append(f"- DSO: {fmt_num(ccc.get('dso'))}")
    lines.append(f"- DPO: {fmt_num(ccc.get('dpo'))}")
    lines.append(f"- DIO: {fmt_num(ccc.get('dio'))}")
    lines.append(f"- CCC: {fmt_num(ccc.get('ccc'))}")
    bridge = cash_conv.get('profit_to_cash_bridge') or {}
    capex = bridge.get('capex') or {}
    depreciation = bridge.get('depreciation') or {}
    lines.append(f"- Capex: {fmt_money(capex.get('value')) if capex else '[missing]'} USD")
    lines.append(f"- Depreciation: {fmt_money(depreciation.get('value')) if depreciation else '[missing]'} USD")
    lines.append('')

    normalization = data.get('normalization') or {}
    lines.append('## Normalization Guardrails')
    lines.append('')
    reported = normalization.get('reported') or {}
    operating_ref = normalization.get('operating_reference') or {}
    lines.append(f"- Reported operating margin: {fmt_num(reported.get('operating_margin'))}")
    lines.append(f"- Reported net margin: {fmt_num(reported.get('net_margin'))}")
    lines.append(f"- Operating-reference margin: {fmt_num(operating_ref.get('operating_margin'))}")
    lines.append(f"- Operating-reference net debt: {fmt_money(operating_ref.get('net_debt')) if operating_ref.get('net_debt') is not None else '[missing]'} USD")
    flags = normalization.get('flags') or []
    if flags:
        for flag in flags:
            lines.append(f"- Flag: {flag}")
    else:
        lines.append('- Flag: [none]')
    for note in normalization.get('notes') or []:
        lines.append(f"- Note: {note}")
    lines.append('')

    lines.append('## Valuation Methods')
    lines.append('')
    for method_name, method in (data.get('valuation_methods') or {}).items():
        if method_name == 'aggregate':
            continue
        lines.append(f"### {method_name}")
        lines.append(f"- Status: {method.get('status')}")
        if method.get('source_status') is not None:
            lines.append(f"- Source status: {method.get('source_status')}")
        if method.get('confidence') is not None:
            lines.append(f"- Confidence: {method.get('confidence')}")
        lines.append(f"- Output: {method.get('output') if method.get('output') is not None else '[missing]'}")
        lines.append(f"- Range: {method.get('range') if method.get('range') is not None else '[missing]'}")
        lines.append('')

    agg = (data.get('valuation_methods') or {}).get('aggregate') or {}
    lines.append('## Aggregate Valuation View')
    lines.append('')
    if agg.get('source_status') is not None:
        lines.append(f"- Source status: {agg.get('source_status')}")
    if agg.get('confidence') is not None:
        lines.append(f"- Confidence: {agg.get('confidence')}")
    lines.append(f"- Central reference: {agg.get('central_reference') if agg.get('central_reference') is not None else '[missing]'}")
    lines.append(f"- Range: {agg.get('range') if agg.get('range') is not None else '[missing]'}")
    lines.append(f"- Dispersion: {agg.get('dispersion') if agg.get('dispersion') is not None else '[missing]'}")
    lines.append(f"- Notes: {agg.get('notes') if agg.get('notes') is not None else '[missing]'}")
    lines.append('')

    model_context = data.get('model_context') or {}
    if model_context:
        lines.append('## Model Ingestion Context')
        lines.append('')
        lines.append(f"- Source file: {model_context.get('source_file') or '[missing]'}")
        validation = model_context.get('validation') or {}
        if validation:
            lines.append(f"- Validation status: {validation.get('status') or '[missing]'}")
            lines.append(f"- Validated by analyst: {validation.get('validated_by_analyst')}")
        summary = model_context.get('summary') or {}
        if summary:
            lines.append(f"- Extracted output signals: {', '.join(summary.get('output_signal_names') or []) or '[missing]'}")
            lines.append(f"- Revenue 2025E-2029E: {summary.get('revenue_2025e_2029e') or '[missing]'}")
            lines.append(f"- EBITDA 2025E-2029E: {summary.get('ebitda_2025e_2029e') or '[missing]'}")
            lines.append(f"- FCF 2025E-2029E: {summary.get('fcf_2025e_2029e') or '[missing]'}")
        for note in model_context.get('notes') or []:
            lines.append(f"- Note: {note}")
        lines.append('')

    lines.append('## Scenarios')
    lines.append('')
    for scenario in data.get('scenarios') or []:
        lines.append(f"### {scenario.get('name')}")
        lines.append(f"- Description: {scenario.get('description')}")
        lines.append(f"- Business model implication: {scenario.get('business_model_implication')}")
        lines.append(f"- Valuation implication: {scenario.get('valuation_implication') or '[missing]'}")
        lines.append('')

    lines.append('## Catalysts')
    lines.append('')
    catalysts = data.get('catalysts') or []
    if catalysts:
        for c in catalysts:
            lines.append(f'- {c}')
    else:
        lines.append('- [missing]')
    lines.append('')

    lines.append('## Risks')
    lines.append('')
    risks = data.get('risks') or []
    if risks:
        for r in risks:
            lines.append(f'- {r}')
    else:
        lines.append('- [missing]')
    lines.append('')

    output_path.write_text('\n'.join(lines).rstrip() + '\n')
    print(str(output_path))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
