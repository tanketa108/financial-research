#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import html
from pathlib import Path


def resolve_paths(repo_root: Path, output_dir: Path | None = None):
    root = repo_root.resolve()
    dashboard_root = root / 'financial_dashboard'
    output = (output_dir or (dashboard_root / 'output')).resolve()
    return {
        'root': root,
        'dashboard_root': dashboard_root,
        'output': output,
        'companies': output / 'companies',
        'static': dashboard_root / 'static',
        'financial_system': root / 'financial_system',
    }


DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[1]
PATHS = resolve_paths(DEFAULT_REPO_ROOT)
DASHBOARD_ROOT = PATHS['dashboard_root']
OUTPUT = PATHS['output']
COMPANIES = PATHS['companies']
STATIC = PATHS['static']
FS = PATHS['financial_system']

DASHBOARD_STATE = FS / 'registry' / 'dashboard_state.json'
THESIS_OUTPUT = FS / 'registry' / 'thesis_monitor_output.json'
VALUATIONS = FS / 'valuations'
COMPANY_STATES = FS / 'companies'


def load_json(path: Path):
    return json.loads(path.read_text())


def esc(x):
    return html.escape(str(x))


def fmt_num(v, digits=2):
    if v is None:
        return '[missing]'
    if isinstance(v, float):
        return f'{v:.{digits}f}'
    return f'{v}'


def fmt_money(v):
    if v is None:
        return '[missing]'
    try:
        return f'{v:,.0f}'
    except Exception:
        return str(v)


def pill(value: str | None, kind: str | None = None):
    txt = 'null' if value is None else str(value)
    cls = kind or txt.lower().replace(' ', '_')
    return f'<span class="pill pill-{esc(cls)}">{esc(txt)}</span>'


def base_page(title: str, body: str, css_path: str) -> str:
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="{css_path}">
</head>
<body>
  <div class="wrap">{body}</div>
</body>
</html>'''


def collect_company_warnings(summary: dict, thesis_item: dict, valuation: dict) -> list[str]:
    warnings = []
    if summary.get('coverage_status') != 'covered':
        warnings.append(f"coverage_status={summary.get('coverage_status')}")
    if thesis_item.get('extraction_quality') not in (None, 'validated'):
        warnings.append(f"extraction_quality={thesis_item.get('extraction_quality')}")
    if not (valuation.get('thesis') or {}).get('thesis_short'):
        warnings.append('missing thesis_short')
    if not (valuation.get('risks') or []):
        warnings.append('missing risks')
    if not (valuation.get('catalysts') or []):
        warnings.append('missing catalysts')
    if not ((valuation.get('valuation_methods') or {}).get('aggregate') or {}).get('central_reference'):
        warnings.append('missing central valuation reference')
    return warnings


def load_company_states() -> dict[str, dict]:
    states: dict[str, dict] = {}
    if not COMPANY_STATES.exists():
        return states
    for path in COMPANY_STATES.glob('*/company-thesis-state-v0.json'):
        try:
            item = load_json(path)
        except Exception:
            continue
        ticker = item.get('ticker') or path.parent.name
        states[ticker] = item
    return states


def compact_items(items: list, key: str = 'title') -> list[str]:
    out = []
    for item in items or []:
        if isinstance(item, dict):
            title = item.get(key) or item.get('summary') or item.get('question') or item.get('statement')
            summary = item.get('summary')
            if title and summary and title != summary:
                out.append(f'{title}: {summary}')
            elif title:
                out.append(str(title))
        else:
            out.append(str(item))
    return out


def render_company_page(ticker: str, summary: dict, thesis_item: dict, valuation: dict, company_state: dict | None = None):
    latest = valuation.get('latest_period') or thesis_item.get('latest_period') or {}
    hist = valuation.get('historical_base') or {}
    q = valuation.get('quality') or {}
    debt = valuation.get('debt') or {}
    cash_conv = valuation.get('cash_conversion') or {}
    ccc = cash_conv.get('ccc') or {}
    bridge = cash_conv.get('profit_to_cash_bridge') or {}
    company_state = company_state or {}
    thesis = valuation.get('thesis') or {}
    thesis_snapshot = company_state.get('thesis_snapshot') or {}
    dashboard_fields = company_state.get('dashboard_fields') or {}
    agg = (valuation.get('valuation_methods') or {}).get('aggregate') or {}
    warnings = collect_company_warnings(summary, thesis_item, valuation)
    reasons = thesis_item.get('reasons') or []
    risks = compact_items(company_state.get('risks')) or valuation.get('risks') or summary.get('key_risks') or []
    catalysts = compact_items(company_state.get('catalysts')) or valuation.get('catalysts') or summary.get('key_catalysts') or []
    drivers = compact_items(company_state.get('qualitative_drivers'))
    assumptions = compact_items(company_state.get('assumptions'), key='statement')
    questions = compact_items(company_state.get('open_questions'), key='question')
    latest_updates = compact_items(company_state.get('latest_updates'), key='summary')

    body = f'''
<div class="topbar"><div><h1>{esc(ticker)}</h1><div class="muted">Company dashboard v1</div></div><div><a href="../index.html">← Portfolio</a></div></div>
<div class="grid">
  <div class="card"><div class="muted small">Coverage</div><div>{pill(summary.get('coverage_status'))}</div></div>
  <div class="card"><div class="muted small">Decision</div><div>{pill(thesis_item.get('decision'))}</div></div>
  <div class="card"><div class="muted small">Valuation status</div><div>{pill((summary.get('valuation_status') or {}).get('status'))}</div></div>
  <div class="card"><div class="muted small">Latest period</div><div class="small mono">{esc(latest.get('form_type'))} | {esc(latest.get('report_date'))}</div></div>
</div>
<div class="split section">
  <div class="card">
    <h2>Overview</h2>
    <ul class="list small">
      <li>Latest filing date: {esc((summary.get('update_status') or {}).get('latest_filing_date'))}</li>
      <li>Filing delta changed: {esc((summary.get('update_status') or {}).get('filing_delta_changed'))}</li>
      <li>Data delta changed: {esc((summary.get('update_status') or {}).get('data_delta_changed'))}</li>
      <li>Preliminary priority: {esc(thesis_item.get('preliminary_priority'))}</li>
    </ul>
    <h2>Monitor reasons</h2>
    <ul class="list small">{''.join(f'<li>{esc(r)}</li>' for r in reasons) or '<li>[none]</li>'}</ul>
  </div>
  <div class="card">
    <h2>Warnings / Gaps</h2>
    <ul class="list small">{''.join(f'<li class="warning">{esc(w)}</li>' for w in warnings) or '<li class="good">No obvious structural warnings</li>'}</ul>
  </div>
</div>
<div class="section card">
  <h2>Financial Base</h2>
  <div class="grid">
    <div><div class="muted small">Revenue</div><div class="kpi">{fmt_money(hist.get('latest_revenue'))}</div></div>
    <div><div class="muted small">Operating income</div><div class="kpi">{fmt_money(hist.get('latest_operating_income'))}</div></div>
    <div><div class="muted small">Net income</div><div class="kpi">{fmt_money(hist.get('latest_net_income'))}</div></div>
    <div><div class="muted small">Diluted EPS</div><div class="kpi">{fmt_num(hist.get('latest_diluted_eps'))}</div></div>
    <div><div class="muted small">Cash</div><div class="kpi">{fmt_money(hist.get('latest_cash_and_equivalents'))}</div></div>
    <div><div class="muted small">Total debt</div><div class="kpi">{fmt_money(hist.get('latest_total_debt'))}</div></div>
  </div>
</div>
<div class="section card">
  <h2>Cash Flow / Conversion</h2>
  <div class="grid">
    <div><div class="muted small">DSO</div><div class="kpi">{fmt_num(ccc.get('dso'))}</div></div>
    <div><div class="muted small">DPO</div><div class="kpi">{fmt_num(ccc.get('dpo'))}</div></div>
    <div><div class="muted small">DIO</div><div class="kpi">{fmt_num(ccc.get('dio'))}</div></div>
    <div><div class="muted small">CCC</div><div class="kpi">{fmt_num(ccc.get('ccc'))}</div></div>
    <div><div class="muted small">Capex</div><div class="kpi">{fmt_money((bridge.get('capex') or {}).get('value'))}</div></div>
    <div><div class="muted small">Depreciation</div><div class="kpi">{fmt_money((bridge.get('depreciation') or {}).get('value'))}</div></div>
  </div>
</div>
<div class="section card">
  <h2>Debt / Balance Sheet</h2>
  <div class="grid">
    <div><div class="muted small">Debt</div><div class="kpi">{fmt_money(debt.get('total_debt'))}</div></div>
    <div><div class="muted small">Cash</div><div class="kpi">{fmt_money(debt.get('cash'))}</div></div>
    <div><div class="muted small">Net debt</div><div class="kpi">{fmt_money(debt.get('net_debt'))}</div></div>
    <div><div class="muted small">Interest burden</div><div class="kpi">{fmt_money((debt.get('interest_burden') or {}).get('value'))}</div></div>
  </div>
</div>
<div class="section card">
  <h2>Valuation</h2>
  <div class="grid">
    <div><div class="muted small">Central reference</div><div class="kpi">{fmt_num(agg.get('central_reference'))}</div></div>
    <div><div class="muted small">Range</div><div class="small mono">{esc(agg.get('range'))}</div></div>
    <div><div class="muted small">Confidence</div><div class="kpi">{fmt_num(agg.get('confidence'))}</div></div>
    <div><div class="muted small">Source status</div><div>{pill(agg.get('source_status'))}</div></div>
  </div>
</div>
<div class="section card">
  <h2>Thesis / Risks / Catalysts</h2>
  <p><strong>Thesis short:</strong> {esc(thesis_snapshot.get('one_sentence_summary') or thesis.get('thesis_short') or '[missing]')}</p>
  <p><strong>Current stance:</strong> {esc(thesis_snapshot.get('conviction_level') or thesis.get('current_stance') or '[missing]')}</p>
  <p><strong>Committee view:</strong> {esc(thesis_snapshot.get('committee_view') or thesis.get('what_would_change_my_mind') or '[missing]')}</p>
  <div class="split">
    <div><h2>Risks</h2><ul class="list small">{''.join(f'<li>{esc(x)}</li>' for x in risks) or '<li>[missing]</li>'}</ul></div>
    <div><h2>Catalysts</h2><ul class="list small">{''.join(f'<li>{esc(x)}</li>' for x in catalysts) or '<li>[missing]</li>'}</ul></div>
  </div>
</div>
<div class="section card">
  <h2>Qualitative Maintenance</h2>
  <p><strong>Status:</strong> {esc(dashboard_fields.get('qualitative_maintenance_status') or company_state.get('status') or '[missing]')}</p>
  <p><strong>Dashboard summary:</strong> {esc(dashboard_fields.get('dashboard_summary') or '[missing]')}</p>
  <p><strong>Next action:</strong> {esc(dashboard_fields.get('next_action') or '[missing]')}</p>
  <div class="split">
    <div><h2>Drivers</h2><ul class="list small">{''.join(f'<li>{esc(x)}</li>' for x in drivers) or '<li>[missing]</li>'}</ul></div>
    <div><h2>Assumptions</h2><ul class="list small">{''.join(f'<li>{esc(x)}</li>' for x in assumptions) or '<li>[missing]</li>'}</ul></div>
  </div>
  <div class="split">
    <div><h2>Open questions</h2><ul class="list small">{''.join(f'<li>{esc(x)}</li>' for x in questions) or '<li>[missing]</li>'}</ul></div>
    <div><h2>Latest updates</h2><ul class="list small">{''.join(f'<li>{esc(x)}</li>' for x in latest_updates) or '<li>[missing]</li>'}</ul></div>
  </div>
</div>
'''
    page = base_page(f'{ticker} Dashboard v1', body, '../static/styles.css')
    (COMPANIES / f'{ticker}.html').write_text(page)


def render_index(data: dict, thesis_output: dict, valuation_map: dict):
    rows = []
    for ticker in sorted(data):
        item = data[ticker]
        thesis_item = thesis_output.get(ticker, {})
        valuation = valuation_map.get(ticker, {})
        warns = collect_company_warnings(item, thesis_item, valuation)
        flags = []
        if (item.get('update_status') or {}).get('filing_delta_changed'):
            flags.append('filing_delta')
        if (item.get('update_status') or {}).get('data_delta_changed'):
            flags.append('data_delta')
        flags.extend((item.get('valuation_status') or {}).get('normalization_flags') or [])
        rows.append(f'''<tr>
<td><a href="companies/{ticker}.html">{esc(ticker)}</a></td>
<td>{pill(item.get('coverage_status'))}</td>
<td class="mono">{esc((thesis_item.get('latest_period') or {}).get('form_type'))} | {esc((thesis_item.get('latest_period') or {}).get('report_date'))}</td>
<td>{esc((item.get('update_status') or {}).get('latest_filing_date'))}</td>
<td>{esc((item.get('update_status') or {}).get('filing_delta_changed'))}</td>
<td>{esc((item.get('update_status') or {}).get('data_delta_changed'))}</td>
<td>{pill(thesis_item.get('decision'))}</td>
<td>{pill((item.get('valuation_status') or {}).get('status'))}</td>
<td class="small">{esc(', '.join(flags[:3]) if flags else '[none]')}</td>
<td class="small">{esc(', '.join(warns[:2]) if warns else '[none]')}</td>
</tr>''')
    body = f'''
<div class="topbar"><div><h1>Financial Dashboard v1</h1><div class="muted">Portfolio overview and company drill-down</div></div><div class="muted small">Local HTML build</div></div>
<div class="grid section">
  <div class="card"><div class="muted small">Companies</div><div class="kpi">{len(data)}</div></div>
  <div class="card"><div class="muted small">Covered</div><div class="kpi">{sum(1 for x in data.values() if x.get('coverage_status') == 'covered')}</div></div>
  <div class="card"><div class="muted small">Need review</div><div class="kpi">{sum(1 for x in thesis_output.values() if x.get('decision') in ('review', 'high_priority'))}</div></div>
  <div class="card"><div class="muted small">High priority</div><div class="kpi">{sum(1 for x in thesis_output.values() if x.get('decision') == 'high_priority')}</div></div>
</div>
<div class="section">
  <table>
    <thead>
      <tr><th>Ticker</th><th>Coverage</th><th>Latest period</th><th>Latest filing</th><th>Filing delta</th><th>Data delta</th><th>Decision</th><th>Valuation</th><th>Flags</th><th>Warnings</th></tr>
    </thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</div>
'''
    (OUTPUT / 'index.html').write_text(base_page('Financial Dashboard v1', body, 'static/styles.css'))


def main():
    parser = argparse.ArgumentParser(description='Build the static financial dashboard HTML.')
    parser.add_argument(
        '--repo-root',
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help='Repository root. Defaults to the parent of financial_dashboard/.',
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=None,
        help='Output directory. Defaults to <repo-root>/financial_dashboard/output.',
    )
    args = parser.parse_args()

    paths = resolve_paths(args.repo_root, args.output_dir)
    global DASHBOARD_ROOT, OUTPUT, COMPANIES, STATIC, FS, DASHBOARD_STATE, THESIS_OUTPUT, VALUATIONS, COMPANY_STATES
    DASHBOARD_ROOT = paths['dashboard_root']
    OUTPUT = paths['output']
    COMPANIES = paths['companies']
    STATIC = paths['static']
    FS = paths['financial_system']
    DASHBOARD_STATE = FS / 'registry' / 'dashboard_state.json'
    THESIS_OUTPUT = FS / 'registry' / 'thesis_monitor_output.json'
    VALUATIONS = FS / 'valuations'
    COMPANY_STATES = FS / 'companies'

    data = load_json(DASHBOARD_STATE)
    thesis_output = load_json(THESIS_OUTPUT)
    valuation_map = {}
    for path in VALUATIONS.glob('*-valuation-state-v1.json'):
        valuation_map[path.name.split('-')[0]] = load_json(path)
    company_states = load_company_states()

    OUTPUT.mkdir(parents=True, exist_ok=True)
    COMPANIES.mkdir(parents=True, exist_ok=True)
    (OUTPUT / 'static').mkdir(parents=True, exist_ok=True)
    (OUTPUT / 'static' / 'styles.css').write_text((STATIC / 'styles.css').read_text())

    render_index(data, thesis_output, valuation_map)
    for ticker, summary in data.items():
        render_company_page(ticker, summary, thesis_output.get(ticker, {}), valuation_map.get(ticker, {}), company_states.get(ticker))
    print(str(OUTPUT / 'index.html'))


if __name__ == '__main__':
    main()
