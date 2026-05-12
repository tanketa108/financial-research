#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / 'financial_system' / 'dashboard_inputs' / 'UBER-dashboard-input-v0.json'
DEFAULT_OUTPUT = ROOT / 'docs' / 'preview' / 'UBER-dashboard-v2.html'
CSS_REL = '../static/styles.css'


def esc(value):
    if value is None:
        return '[missing]'
    return html.escape(str(value))


def money(value):
    if value is None:
        return '[missing]'
    try:
        v = float(value)
    except Exception:
        return esc(value)
    abs_v = abs(v)
    if abs_v >= 1_000_000_000:
        return f'${v/1_000_000_000:.1f}B'
    if abs_v >= 1_000_000:
        return f'${v/1_000_000:.1f}M'
    return f'${v:,.0f}'


def pct(value):
    if value is None:
        return '[missing]'
    try:
        return f'{float(value) * 100:.1f}%'
    except Exception:
        return esc(value)


def pill(value, kind=None):
    text = 'missing' if value is None else str(value)
    cls = (kind or text).lower().replace(' ', '_').replace('/', '_')
    return f'<span class="pill pill-{esc(cls)}">{esc(text)}</span>'


def card_list(title, items, field='title', sub='summary', empty='[none]'):
    rows = []
    for item in items or []:
        if isinstance(item, dict):
            main = item.get(field) or item.get('question') or item.get('statement') or item.get('summary') or item.get('id')
            detail = item.get(sub) if sub else None
            rows.append(f'<li><strong>{esc(main)}</strong>{f": {esc(detail)}" if detail and detail != main else ""}</li>')
        else:
            rows.append(f'<li>{esc(item)}</li>')
    return f'<div class="card cockpit-card"><h2>{esc(title)}</h2><ul class="list small">{"".join(rows) or f"<li>{esc(empty)}</li>"}</ul></div>'


def render(data: dict, css_rel: str = CSS_REL) -> str:
    ticker = data.get('ticker')
    name = data.get('company_name')
    thesis = data.get('thesis') or {}
    maintenance = data.get('maintenance') or {}
    qualitative = data.get('qualitative') or {}
    valuation = data.get('valuation') or {}
    metrics = data.get('key_metrics') or {}
    guardrails = data.get('guardrails') or {}

    drivers = qualitative.get('drivers') or []
    risks = qualitative.get('risks') or []
    catalysts = qualitative.get('catalysts') or []
    assumptions = qualitative.get('assumptions') or []
    questions = qualitative.get('open_questions') or []
    updates = maintenance.get('latest_updates') or []
    sources = maintenance.get('sources') or []

    body = f'''
<div class="topbar workspace-header cockpit-topbar">
  <div>
    <div class="muted small">Company Thesis Cockpit v0 · generic template preview</div>
    <h1>{esc(ticker)} <span class="muted">{esc(name)}</span></h1>
    <div class="small muted">This preview is generated from dashboard input state, not hand-coded for one company.</div>
  </div>
  <div><a href="../index.html">← Portfolio</a></div>
</div>

<div class="status-rail section cockpit-status-rail">
  <div class="status-card"><div class="muted small">Thesis status</div><div>{pill(thesis.get('stance'))}</div></div>
  <div class="status-card"><div class="muted small">Maintenance</div><div>{pill(maintenance.get('status'))}</div></div>
  <div class="status-card"><div class="muted small">Valuation</div><div>{pill(valuation.get('status'))}</div></div>
  <div class="status-card"><div class="muted small">Last updated</div><div class="small mono">{esc(data.get('last_updated'))}</div></div>
  <div class="status-card"><div class="muted small">Template</div><div>{pill('generic')}</div></div>
</div>

<div class="card section cockpit-hero">
  <div class="muted small">Thesis snapshot</div>
  <h2>{esc(thesis.get('one_line'))}</h2>
  <p>{esc(thesis.get('current_thesis'))}</p>
  <div class="cockpit-committee-view"><strong>Committee view:</strong> {esc(thesis.get('committee_view'))}</div>
</div>

<div class="grid section cockpit-kpi-grid">
  <div class="card"><div class="muted small">Revenue</div><div class="kpi">{money(metrics.get('revenue'))}</div></div>
  <div class="card"><div class="muted small">Operating income</div><div class="kpi">{money(metrics.get('operating_income'))}</div></div>
  <div class="card"><div class="muted small">Operating margin</div><div class="kpi">{pct(metrics.get('operating_margin'))}</div></div>
  <div class="card"><div class="muted small">Central valuation</div><div class="kpi">{esc(valuation.get('central_reference'))}</div><div class="small muted">Range: {esc(valuation.get('range'))}</div></div>
</div>

<div class="workspace-grid section cockpit-main-grid">
  <div class="card panel panel-overview cockpit-panel-large">
    <h2>Maintenance / what changed</h2>
    <p class="small"><strong>Next action:</strong> {esc(maintenance.get('next_action'))}</p>
    <ul class="list small">{''.join(f'<li><strong>{esc(x.get("date") if isinstance(x, dict) else "")}</strong> {esc(x.get("summary") if isinstance(x, dict) else x)}</li>' for x in updates) or '<li>[none]</li>'}</ul>
  </div>
  <div class="card panel panel-actions cockpit-panel-side">
    <h2>Model / valuation source</h2>
    <ul class="list small">
      <li>Status: {esc(valuation.get('status'))}</li>
      <li>Excel/model: {esc(valuation.get('user_excel_model'))}</li>
      <li>{esc(valuation.get('note'))}</li>
    </ul>
  </div>
</div>

<div class="grid section cockpit-card-grid">
  {card_list('Key drivers', drivers)}
  {card_list('Risks', risks)}
  {card_list('Catalysts', catalysts)}
  {card_list('Assumptions to validate', assumptions, field='statement', sub='status')}
  {card_list('Open questions', questions, field='question', sub='status')}
  {card_list('Sources', sources, field='title', sub='notes')}
</div>

<div class="card section cockpit-guardrails">
  <h2>Guardrails</h2>
  <ul class="list small">{''.join(f'<li><strong>{esc(k)}</strong>: {esc(v)}</li>' for k, v in guardrails.items()) or '<li>[none]</li>'}</ul>
</div>
'''
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(ticker)} Company Thesis Cockpit v0</title>
  <link rel="stylesheet" href="{css_rel}">
</head>
<body>
  <div class="wrap">
{body}
  </div>
</body>
</html>
'''


def main():
    parser = argparse.ArgumentParser(description='Build a generic company dashboard preview from dashboard input JSON.')
    parser.add_argument('--input', type=Path, default=DEFAULT_INPUT)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(data), encoding='utf-8')
    print(args.output)


if __name__ == '__main__':
    main()
