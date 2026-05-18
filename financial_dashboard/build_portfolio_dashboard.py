#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
# Canonical source of truth lives at workspace-root portfolio/*. The
# financial-research copy is a generated mirror for publishing compatibility.
PORTFOLIO = WORKSPACE / 'portfolio' if (WORKSPACE / 'portfolio').exists() else ROOT / 'financial_system/portfolio'
OUT = ROOT / 'docs/portfolio.html'
COMPANY_OUT = ROOT / 'docs/portfolio_companies'
STATIC_OUT = ROOT / 'docs/static'
STATIC_SRC = ROOT / 'financial_dashboard/static/styles.css'


def esc(x):
    return html.escape('[missing]' if x is None else str(x))


def pill(x):
    txt = 'missing' if x is None else str(x)
    cls = txt.lower().replace(' ', '_').replace('/', '_')
    return f'<span class="pill pill-{esc(cls)}">{esc(txt)}</span>'


def read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def list_html(items):
    return ''.join(f'<li>{esc(x)}</li>' for x in (items or [])) or '<li>[missing]</li>'


def page(title: str, body: str, css_path: str = 'static/styles.css') -> str:
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
</html>
'''


def load_portfolio_os():
    registry = read_json(PORTFOLIO / 'company-registry.json', {'companies': []})
    pipeline = read_json(PORTFOLIO / 'task-pipeline.json', {'tasks': []})
    outputs = read_json(PORTFOLIO / 'output-registry.json', {'outputs': []})
    system_health = read_json(WORKSPACE / 'runtime/state/system-health.json', {'overallStatus': 'missing', 'checks': {}, 'knownWarnings': []})
    states = {}
    for path in sorted((PORTFOLIO / 'companies').glob('*.json')):
        state = read_json(path, {})
        if state.get('ticker'):
            states[state['ticker']] = state
    radars = sorted((PORTFOLIO / 'daily-radar').glob('*.md')) if (PORTFOLIO / 'daily-radar').exists() else []
    return registry, pipeline, states, radars, outputs, system_health


def task_rows(tasks):
    rows = []
    for task in tasks:
        rows.append(f'''<tr>
<td class="mono small">{esc(task.get('id'))}</td>
<td>{esc(task.get('company'))}</td>
<td>{pill(task.get('type'))}</td>
<td>{pill(task.get('priority'))}</td>
<td>{pill(task.get('status'))}</td>
<td class="small">{esc(task.get('reason'))}</td>
<td class="small">{esc(task.get('nextAction') or task.get('closeCriteria'))}</td>
</tr>''')
    return ''.join(rows) or '<tr><td colspan="7" class="muted small">No open tasks.</td></tr>'


def render_company_state_page(state, tasks_by_id):
    ticker = state.get('ticker') or 'UNKNOWN'
    thesis = state.get('thesisState') or {}
    business = state.get('businessSnapshot') or {}
    links = state.get('tasks') or {}
    open_ids = links.get('open') or []
    linked_tasks = [tasks_by_id[t] for t in open_ids if t in tasks_by_id]
    recent = state.get('recentEvents') or []
    outputs = state.get('researchOutputs') or []
    recent_html = ''.join(
        f'<div class="portfolio-queue-item">{pill(e.get("materiality"))}<strong>{esc(e.get("date"))} · {esc(e.get("type"))}</strong><span>{esc(e.get("summary"))}</span></div>'
        for e in recent
    ) or '<div class="muted small">No recent events recorded.</div>'
    outputs_html = ''.join(
        f'<div class="portfolio-queue-item">{pill(o.get("type"))}<strong>{esc(o.get("date"))} · {esc(o.get("title"))}</strong><span>{esc(o.get("path"))}</span></div>'
        for o in outputs
    ) or '<div class="muted small">No research outputs recorded.</div>'
    linked_task_html = ''.join(
        f'<div class="portfolio-queue-item">{pill(t.get("priority"))}<strong>{esc(t.get("id"))} · {esc(t.get("type"))}</strong><span>{esc(t.get("reason"))}</span></div>'
        for t in linked_tasks
    ) or '<div class="muted small">No linked open tasks.</div>'

    body = f'''
<div class="topbar"><div><div class="muted small">Company State v0</div><h1>{esc(ticker)} · {esc(state.get('name'))}</h1><div class="muted">Estado vivo para mantenimiento de tesis. No sustituye la decisión del Portfolio Manager.</div></div><div><a href="../portfolio.html">← Portfolio OS</a></div></div>
<div class="grid section cockpit-kpi-grid"><div class="card"><div class="muted small">Status</div><div>{pill(state.get('status'))}</div></div><div class="card"><div class="muted small">Priority</div><div>{pill(state.get('priority'))}</div></div><div class="card"><div class="muted small">Thesis</div><div>{pill(thesis.get('status'))}</div></div><div class="card"><div class="muted small">Conviction</div><div>{pill(thesis.get('conviction'))}</div></div></div>
<div class="snapshot-grid section"><section class="card snapshot-panel snapshot-panel-wide"><h2>Thesis State</h2><p>{esc(thesis.get('summary'))}</p><ul class="list small"><li>Owner: {esc(thesis.get('owner'))}</li><li>Last reviewed: {esc(thesis.get('lastReviewedAt'))}</li><li>Portfolio Manager decision: {esc(thesis.get('portfolioManagerDecision'))}</li></ul><h3>What would change our mind</h3><ul class="list small">{list_html(thesis.get('whatWouldChangeOurMind'))}</ul></section><section class="card snapshot-panel"><h2>Business Snapshot</h2><p>{esc(business.get('description'))}</p><ul class="list small"><li>Segments: {esc(', '.join(business.get('segments') or []))}</li><li>Competitors: {esc(', '.join(business.get('competitors') or []))}</li><li>Cycle exposure: {esc(business.get('cycleExposure'))}</li></ul></section></div>
<div class="snapshot-grid section"><section class="card snapshot-panel"><h2>Key Drivers</h2><ul class="list small">{list_html(state.get('keyDrivers'))}</ul></section><section class="card snapshot-panel"><h2>Key Risks</h2><ul class="list small">{list_html(state.get('keyRisks'))}</ul></section><section class="card snapshot-panel"><h2>Watch Metrics</h2><ul class="list small">{list_html(state.get('watchMetrics'))}</ul></section><section class="card snapshot-panel"><h2>Open Questions</h2><ul class="list small">{list_html(state.get('openQuestions'))}</ul></section></div>
<div class="snapshot-grid section"><section class="card snapshot-panel snapshot-panel-wide"><h2>Linked Open Tasks</h2><div class="portfolio-queue-list">{linked_task_html}</div></section><section class="card snapshot-panel snapshot-panel-wide"><h2>Recent Events</h2><div class="portfolio-queue-list">{recent_html}</div></section></div>
<div class="card section"><h2>Research Outputs</h2><div class="portfolio-queue-list">{outputs_html}</div></div>
'''
    COMPANY_OUT.mkdir(parents=True, exist_ok=True)
    (COMPANY_OUT / f'{ticker}.html').write_text(page(f'{ticker} Company State', body, '../static/styles.css'))


def output_items(outputs):
    items = outputs.get('outputs') or []
    recent = sorted(items, key=lambda x: (x.get('updatedAt') or x.get('createdAt') or '', x.get('id') or ''))[-8:]
    return ''.join(
        f'<div class="portfolio-queue-item">{pill(o.get("type"))}{pill(o.get("status"))}<strong>{esc(o.get("id"))} · {esc(o.get("title"))}</strong><span>{esc(o.get("entity"))} · {esc(o.get("path"))}</span><span class="small muted">{esc(o.get("summary"))}</span></div>'
        for o in recent
    ) or '<div class="muted small">No outputs registered.</div>'


def health_items(system_health):
    checks = system_health.get('checks') or {}
    check_html = ''.join(
        f'<li><strong>{esc(name)}:</strong> {pill(check.get("status"))} <span class="muted small">{esc(check.get("checkedAt"))}</span></li>'
        for name, check in checks.items()
    ) or '<li>[missing checks]</li>'
    warnings = system_health.get('knownWarnings') or []
    warning_html = ''.join(f'<li>{esc(w)}</li>' for w in warnings[:8]) or '<li>No active warnings.</li>'
    return check_html, warning_html


def main():
    registry, pipeline, company_states, radars, outputs, system_health = load_portfolio_os()
    companies = registry.get('companies', [])
    tasks = pipeline.get('tasks', [])
    tasks_by_id = {t.get('id'): t for t in tasks if t.get('id')}
    open_tasks = [t for t in tasks if t.get('status') in ('open', 'in_progress', 'waiting')]
    terminal_tasks = [t for t in tasks if t.get('status') in ('done', 'dismissed', 'superseded', 'failed', 'cancelled')]
    high_tasks = [t for t in open_tasks if t.get('priority') == 'high']
    review_companies = [c for c in companies if c.get('status') == 'thesis_review_needed']
    stale_states = [c for c in companies if not c.get('lastUpdate')]
    missing_threads = [c for c in companies if c.get('type') != 'archived' and not c.get('discordThreadId')]
    structural_health = []
    structural_health.append(('Canonical source', str(PORTFOLIO.relative_to(WORKSPACE)) if PORTFOLIO.is_relative_to(WORKSPACE) else str(PORTFOLIO)))
    structural_health.append(('Open tasks', len(open_tasks)))
    structural_health.append(('Stale states', len(stale_states)))
    structural_health.append(('Missing company threads', len(missing_threads)))
    structural_health.append(('System health', system_health.get('overallStatus', 'missing')))
    structural_health.append(('Output registry entries', len(outputs.get('outputs') or [])))
    structural_health.append(('Last health event', system_health.get('lastEventId', '[missing]')))
    by_status = Counter(c.get('status') for c in companies)
    by_priority = Counter(c.get('priority') for c in companies)
    tasks_by_company = defaultdict(list)
    for task in open_tasks:
        tasks_by_company[task.get('company')].append(task)

    STATIC_OUT.mkdir(parents=True, exist_ok=True)
    if STATIC_SRC.exists():
        (STATIC_OUT / 'styles.css').write_text(STATIC_SRC.read_text())

    for state in company_states.values():
        render_company_state_page(state, tasks_by_id)

    company_cards = ''.join(
        f'''
<a class="portfolio-company-card" href="portfolio_companies/{esc(c.get('ticker'))}.html">
  <div class="portfolio-card-top"><strong>{esc(c.get('ticker'))}</strong>{pill(c.get('status'))}</div>
  <div class="muted small">{esc(c.get('name'))}</div>
  <p>{esc(c.get('notes'))}</p>
  <div class="portfolio-metrics"><span>Type <b>{esc(c.get('type'))}</b></span><span>Priority <b>{esc(c.get('priority'))}</b></span><span>Tasks <b>{len(tasks_by_company.get(c.get('ticker'), []))}</b></span></div>
  <div class="small muted">Last update: {esc(c.get('lastUpdate'))} · Next: {esc(c.get('nextKnownEvent'))}</div>
</a>'''
        for c in companies
    )

    recent_radar_html = ''.join(
        f'<li><span class="mono">{esc(p.name)}</span></li>' for p in radars[-5:]
    ) or '<li>[none]</li>'

    status_html = ''.join(f'<li>{pill(k)} {v}</li>' for k, v in sorted(by_status.items()))
    priority_html = ''.join(f'<li>{pill(k)} {v}</li>' for k, v in sorted(by_priority.items()))

    health_html = ''.join(f'<li><strong>{esc(k)}:</strong> {pill(v) if k == "System health" else esc(v)}</li>' for k, v in structural_health)
    check_html, warning_html = health_items(system_health)
    recent_outputs_html = output_items(outputs)

    body = f'''
<div class="topbar"><div><div class="muted small">Portfolio OS · Structural Dashboard</div><h1>Research Operations Queue</h1><div class="muted">Vista operativa: inbox implícito, tasks abiertas, estados obsoletos, outputs recientes y salud estructural.</div></div><div><a href="index.html">← Home</a></div></div>
<div class="card section cockpit-hero">
  <div class="muted small">Operating rule</div>
  <h2>El sistema informa, estructura, prioriza y prepara. El Portfolio Manager decide.</h2>
  <p class="small">Daily Radar no duplica tareas: si una task abierta ya cubre el evento, se enriquece con fuentes/contexto y solo se escala si cambia la materialidad.</p>
</div>
<div class="grid section cockpit-kpi-grid">
  <div class="card"><div class="muted small">Companies</div><div class="kpi">{len(companies)}</div></div>
  <div class="card"><div class="muted small">Open tasks</div><div class="kpi">{len(open_tasks)}</div></div>
  <div class="card"><div class="muted small">High priority tasks</div><div class="kpi">{len(high_tasks)}</div></div>
  <div class="card"><div class="muted small">Thesis review needed</div><div class="kpi">{len(review_companies)}</div></div>
  <div class="card"><div class="muted small">System health</div><div class="kpi">{esc(str(system_health.get('overallStatus', 'missing')).upper())}</div></div>
  <div class="card"><div class="muted small">Registered outputs</div><div class="kpi">{len(outputs.get('outputs') or [])}</div></div>
</div>
<div class="snapshot-grid section">
  <section class="card snapshot-panel"><h2>Structural Health</h2><ul class="list small">{health_html}</ul></section>
  <section class="card snapshot-panel"><h2>Company status</h2><ul class="list small">{status_html}</ul></section>
  <section class="card snapshot-panel"><h2>Priority mix</h2><ul class="list small">{priority_html}</ul></section>
  <section class="card snapshot-panel"><h2>Daily Radar runs</h2><ul class="list small">{recent_radar_html}</ul></section>
</div>
<div class="snapshot-grid section">
  <section class="card snapshot-panel snapshot-panel-wide"><h2>Runtime Checks</h2><ul class="list small">{check_html}</ul></section>
  <section class="card snapshot-panel snapshot-panel-wide"><h2>Active Warnings</h2><ul class="list small">{warning_html}</ul></section>
</div>
<div class="portfolio-card-grid section">{company_cards}</div>
<div class="section card">
  <h2>Open Task Pipeline</h2>
  <table>
    <thead><tr><th>ID</th><th>Company</th><th>Type</th><th>Priority</th><th>Status</th><th>Reason</th><th>Next action</th></tr></thead>
    <tbody>{task_rows(open_tasks)}</tbody>
  </table>
</div>
<div class="card section"><h2>Output Registry</h2><div class="portfolio-queue-list">{recent_outputs_html}</div></div>
<div class="snapshot-grid section">
  <section class="card snapshot-panel snapshot-panel-wide"><h2>Workflow</h2><ol class="list small"><li>Evento detectado</li><li>Evaluación de materialidad</li><li>Crear o enriquecer task existente</li><li>Trabajar en thread de compañía</li><li>Actualizar Company State / Dashboard</li><li>Cerrar task con output trazable</li></ol></section>
  <section class="card snapshot-panel"><h2>Products</h2><ul class="list small"><li>Informe preliminar</li><li>Deep Dive pre-valoración</li><li>Daily Radar</li><li>Company State</li><li>Task Pipeline</li></ul></section>
</div>
'''
    OUT.write_text(page('Research & Monitoring Dashboard', body))
    print(OUT)


if __name__ == '__main__':
    main()
