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
    if abs(v) >= 1_000_000_000:
        return f'${v/1_000_000_000:.1f}B'
    if abs(v) >= 1_000_000:
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


def first(items, n=3):
    return (items or [])[:n]


def item_title(item, fallback='[missing]'):
    if isinstance(item, dict):
        return item.get('title') or item.get('question') or item.get('statement') or item.get('summary') or item.get('id') or fallback
    return item or fallback


def bullets(items, n=3, field=None):
    rows = []
    for item in first(items, n):
        text = item.get(field) if field and isinstance(item, dict) else item_title(item)
        rows.append(f'<li>{esc(text)}</li>')
    return ''.join(rows) or '<li>[none]</li>'


def format_value(value, fmt):
    if fmt == 'money':
        return money(value)
    if fmt == 'percent':
        return pct(value)
    if value is None:
        return '[missing]'
    if isinstance(value, float):
        return f'{value:.1f}'
    return esc(value)


def status_dot(status):
    return f'<span class="status-dot status-{esc(status or "neutral")}"></span>'


def horizontal_bar(label, value, max_value, display, tone='blue'):
    try:
        width = max(3, min(100, abs(float(value)) / max_value * 100)) if max_value else 0
    except Exception:
        width = 0
    return f'''
<div class="snapshot-bar-row">
  <div class="snapshot-bar-label">{esc(label)}</div>
  <div class="snapshot-bar-track"><div class="snapshot-bar-fill tone-{esc(tone)}" style="width:{width:.1f}%"></div></div>
  <div class="snapshot-bar-value">{esc(display)}</div>
</div>'''


def mini_chart(title, series, tone='blue', percent=False):
    points = (series or {}).get('points') or []
    vals = [float(p.get('value') or 0) for p in points]
    max_v = max([abs(v) for v in vals] + [1])
    rows = []
    for p, v in zip(points, vals):
        width = max(3, min(100, abs(v) / max_v * 100))
        label = str(p.get('label') or p.get('date') or '').replace('CY', '')
        display = pct(v) if percent else money(v)
        rows.append(f'''
<div class="mini-bar-row">
  <div class="mini-bar-label small mono">{esc(label)}</div>
  <div class="mini-bar-track"><div class="mini-bar-fill tone-{esc(tone)}" style="width:{width:.1f}%"></div></div>
  <div class="mini-bar-value small">{esc(display)}</div>
</div>''')
    return f'''
<div class="mini-chart-card snapshot-chart-card tone-border-{esc(tone)}">
  <h3>{esc(title)}</h3>
  <div class="mini-chart">{''.join(rows) or '<div class="small muted">[missing]</div>'}</div>
</div>'''


def render_document_card(doc):
    primary_href = doc.get('primary_href')
    primary_link = ''
    if primary_href:
        primary_link = f'<a class="document-secondary-link" href="{esc(primary_href)}" target="_blank" rel="noopener">Open report document</a>'
    accession = doc.get('accession')
    accession_line = f'<small class="mono">{esc(accession)}</small>' if accession else ''
    period = f' · period {esc(doc.get("period"))}' if doc.get('period') else ''
    return f'''
<div class="document-card document-card-with-actions">
  <a class="document-main-link" href="{esc(doc.get('href'))}" target="_blank" rel="noopener">
    <div class="muted small">{esc(doc.get('type'))}{period}</div>
    <strong>{esc(doc.get('label'))}</strong>
    <span>{esc(doc.get('date'))}</span>
    <small>{esc(doc.get('note'))}</small>
    {accession_line}
  </a>
  {primary_link}
</div>'''


def render(data: dict, css_rel: str = CSS_REL) -> str:
    ticker = data.get('ticker')
    name = data.get('company_name')
    thesis = data.get('thesis') or {}
    maintenance = data.get('maintenance') or {}
    qualitative = data.get('qualitative') or {}
    valuation = data.get('valuation') or {}
    metrics = data.get('key_metrics') or {}
    charts = data.get('charts') or {}
    health = data.get('health') or {}
    signal_cards = data.get('signal_cards') or []
    quality_flags = data.get('quality_flags') or []
    thesis_change_monitor = data.get('thesis_change_monitor') or {}
    maintenance_queue = data.get('maintenance_queue') or []
    source_freshness = data.get('source_freshness') or {}
    key_documents = data.get('key_documents') or []
    stocktitan_news = data.get('stocktitan_news_snapshot') or []

    drivers = qualitative.get('drivers') or []
    risks = qualitative.get('risks') or []
    catalysts = qualitative.get('catalysts') or []
    assumptions = qualitative.get('assumptions') or []
    questions = qualitative.get('open_questions') or []
    updates = maintenance.get('latest_updates') or []

    revenue = metrics.get('revenue')
    op_income = metrics.get('operating_income')
    net_income = metrics.get('net_income')
    cash = metrics.get('cash')
    debt = metrics.get('debt')
    op_margin = metrics.get('operating_margin')
    net_margin = metrics.get('net_margin')
    fcf = metrics.get('free_cash_flow')
    max_fin = max([abs(float(x or 0)) for x in [revenue, op_income, net_income, cash, debt, fcf]] + [1])

    body = f'''
<div class="topbar workspace-header snapshot-topbar">
  <div>
    <div class="muted small">Company Snapshot · generic dashboard template v0</div>
    <h1>{esc(ticker)} <span class="muted">{esc(name)}</span></h1>
  </div>
  <div><a href="../index.html">← Portfolio</a></div>
</div>

<div class="snapshot-layout section">
  <section class="card snapshot-hero">
    <div class="snapshot-label">Investment snapshot</div>
    <h2>{esc(thesis.get('one_line'))}</h2>
    <div class="snapshot-status-row">
      {pill(thesis.get('stance'))}
      {pill(health.get('overall_status'))}
      {pill(maintenance.get('status'))}
      {pill(valuation.get('status'))}
    </div>
    <div class="snapshot-mini-note">Last update: {esc(data.get('last_updated'))}</div>
  </section>

  <section class="snapshot-score-grid">
    <div class="card snapshot-score"><div class="muted small">Revenue</div><div class="kpi">{money(revenue)}</div></div>
    <div class="card snapshot-score"><div class="muted small">Op. margin</div><div class="kpi">{pct(op_margin)}</div></div>
    <div class="card snapshot-score"><div class="muted small">Fair value</div><div class="kpi">{esc(valuation.get('central_reference'))}</div></div>
    <div class="card snapshot-score"><div class="muted small">Open questions</div><div class="kpi">{len(questions)}</div></div>
  </section>
</div>

<div class="card section health-summary-card">
  <div>
    <div class="muted small">Financial / thesis health</div>
    <h2>{status_dot(health.get('overall_status'))}{esc(health.get('overall_status') or 'unknown').upper()}</h2>
    <p>{esc(health.get('summary'))}</p>
  </div>
  <div class="health-score-grid">
    {''.join(f'<div class="health-score-item">{status_dot(x.get("status"))}<span>{esc(x.get("label"))}</span><strong>{esc(x.get("value"))}</strong><small>{esc(x.get("note"))}</small></div>' for x in health.get('scorecards', []))}
  </div>
</div>

<div class="signal-card-grid section">
  {''.join(f'<div class="card signal-card signal-{esc(x.get("direction"))}"><div class="muted small">{esc(x.get("label"))}</div><div class="kpi">{format_value(x.get("value"), x.get("format"))}</div><div class="small muted">{esc(x.get("note"))}</div></div>' for x in signal_cards)}
</div>

<div class="document-access-grid section">
  {''.join(render_document_card(x) for x in key_documents)}
</div>

<div class="snapshot-grid section">
  <section class="card snapshot-panel snapshot-panel-wide">
    <h2>Financial snapshot</h2>
    <div class="snapshot-bars">
      {horizontal_bar('Revenue', revenue, max_fin, money(revenue), 'blue')}
      {horizontal_bar('Operating income', op_income, max_fin, money(op_income), 'green')}
      {horizontal_bar('Net income', net_income, max_fin, money(net_income), 'green')}
      {horizontal_bar('Cash', cash, max_fin, money(cash), 'amber')}
      {horizontal_bar('Debt', debt, max_fin, money(debt), 'red')}
    </div>
  </section>

  <section class="card snapshot-panel">
    <h2>Thesis health</h2>
    <div class="snapshot-health-list">
      <div><span>Drivers</span><strong>{len(drivers)}</strong></div>
      <div><span>Risks</span><strong>{len(risks)}</strong></div>
      <div><span>Catalysts</span><strong>{len(catalysts)}</strong></div>
      <div><span>Assumptions</span><strong>{len(assumptions)}</strong></div>
    </div>
  </section>
</div>

<div class="snapshot-chart-grid section">
  {mini_chart('Revenue trend', (charts.get('financial_trends') or [{}])[0], 'blue')}
  {mini_chart('Operating income', (charts.get('financial_trends') or [{}, {}])[1] if len(charts.get('financial_trends') or []) > 1 else {}, 'green')}
  {mini_chart('Net income', (charts.get('financial_trends') or [{}, {}, {}])[2] if len(charts.get('financial_trends') or []) > 2 else {}, 'green')}
  {mini_chart('Cash', (charts.get('balance_sheet') or [{}])[0], 'amber')}
  {mini_chart('Debt', (charts.get('balance_sheet') or [{}, {}])[1] if len(charts.get('balance_sheet') or []) > 1 else {}, 'red')}
  {mini_chart('Operating margin', (charts.get('margins') or [{}])[0], 'blue', percent=True)}
</div>

<div class="card section stocktitan-news-card">
  <div class="muted small">External input · StockTitan</div>
  <h2>Recent news monitor</h2>
  <div class="stocktitan-news-grid">
    {''.join(f'<div class="news-item"><strong>{esc(x.get("headline"))}</strong><span>{esc(x.get("category"))} · relevance {esc(x.get("thesis_relevance"))}</span></div>' for x in stocktitan_news[:6])}
  </div>
</div>

<div class="snapshot-grid section">
  <section class="card snapshot-panel">
    <h2>Top drivers</h2>
    <ul class="list small">{bullets(drivers, 3)}</ul>
  </section>
  <section class="card snapshot-panel">
    <h2>Main risks</h2>
    <ul class="list small">{bullets(risks, 3)}</ul>
  </section>
  <section class="card snapshot-panel">
    <h2>Catalysts</h2>
    <ul class="list small">{bullets(catalysts, 3)}</ul>
  </section>
</div>

<div class="snapshot-grid section">
  <section class="card snapshot-panel snapshot-panel-wide thesis-monitor-card">
    <h2>Thesis Change Monitor</h2>
    <div class="monitor-head">
      {pill(thesis_change_monitor.get('status'))}
      {pill(thesis_change_monitor.get('materiality'))}
      <span class="small muted">{esc(thesis_change_monitor.get('last_event'))}</span>
    </div>
    <p class="small">{esc(thesis_change_monitor.get('changed_view'))}</p>
    <div class="impact-grid">
      {''.join(f'<div>{status_dot(x.get("impact"))}<strong>{esc(x.get("area"))}</strong><span>{esc(x.get("impact"))}</span><small>{esc(x.get("note"))}</small></div>' for x in thesis_change_monitor.get('impact_by_area', []))}
    </div>
  </section>
  <section class="card snapshot-panel">
    <h2>Watch items</h2>
    <ul class="list small">{''.join(f'<li><strong>{esc(x.get("item"))}</strong> · {esc(x.get("severity"))}<br><span class="muted">{esc(x.get("why"))}</span></li>' for x in health.get('watch_items', [])) or '<li>[none]</li>'}</ul>
  </section>
</div>

<div class="snapshot-grid section">
  <section class="card snapshot-panel snapshot-panel-wide">
    <h2>Maintenance queue</h2>
    <div class="queue-list">
      {''.join(f'<div class="queue-item"><div>{pill(x.get("priority"))}</div><strong>{esc(x.get("task"))}</strong><span>{esc(x.get("trigger"))}</span><small>{esc(x.get("output"))}</small></div>' for x in maintenance_queue)}
    </div>
  </section>
  <section class="card snapshot-panel">
    <h2>Source freshness</h2>
    <ul class="list small">
      <li>Thesis memo: {esc(source_freshness.get('latest_thesis_memo'))}</li>
      <li>Excel model: {esc(source_freshness.get('latest_excel_model'))}</li>
      <li>Latest review: {esc(source_freshness.get('latest_filing_or_results_reviewed'))}</li>
      <li>Status: {esc(source_freshness.get('freshness_status'))}</li>
      <li>Next trigger: {esc(source_freshness.get('next_refresh_trigger'))}</li>
    </ul>
  </section>
</div>

<div class="snapshot-grid section">
  <section class="card snapshot-panel snapshot-panel-wide">
    <h2>Quality flags</h2>
    <div class="quality-flag-grid">
      {''.join(f'<div class="quality-flag quality-{esc(x.get("severity"))}"><strong>{esc(x.get("flag"))}</strong><small>{esc(x.get("explanation"))}</small></div>' for x in quality_flags)}
    </div>
  </section>
  <section class="card snapshot-panel">
    <h2>Open questions</h2>
    <ul class="list small">{bullets(questions, 3)}</ul>
  </section>
</div>

<div class="card section snapshot-footer-note">
  <strong>Design rule:</strong> this page is a company snapshot, not the full thesis. Detailed argumentation belongs in the written thesis; detailed valuation belongs in Excel/model files. The dashboard only shows status, signals, changes, and action priorities.
</div>
'''
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(ticker)} Company Snapshot</title>
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
    parser = argparse.ArgumentParser(description='Build a generic company dashboard snapshot from dashboard input JSON.')
    parser.add_argument('--input', type=Path, default=DEFAULT_INPUT)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(data), encoding='utf-8')
    print(args.output)


if __name__ == '__main__':
    main()
