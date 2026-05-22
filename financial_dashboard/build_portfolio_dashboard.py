#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
PORTFOLIO = WORKSPACE / 'portfolio' if (WORKSPACE / 'portfolio').exists() else ROOT / 'financial_system/portfolio'
OUT = ROOT / 'docs/portfolio.html'
COMPANY_OUT = ROOT / 'docs/portfolio_companies'
STATIC_OUT = ROOT / 'docs/static'
STATIC_SRC = ROOT / 'financial_dashboard/static/styles.css'
REPORTS = ROOT / 'financial_system/portfolio/reports'


def esc(x):
    return html.escape('[missing]' if x is None else str(x))


def pill(x):
    txt = 'missing' if x is None else str(x)
    cls = txt.lower().replace(' ', '_').replace('/', '_').replace('|', '_')
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
    reports = sorted(REPORTS.glob('*portfolio-review*.md')) if REPORTS.exists() else []
    return registry, pipeline, states, radars, reports, outputs, system_health


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


def linked_task_ids(raw):
    if isinstance(raw, dict):
        out = []
        for key in ('open', 'active', 'ids'):
            val = raw.get(key) or []
            if isinstance(val, str):
                out.append(val)
            elif isinstance(val, list):
                out.extend(val)
        return out
    if isinstance(raw, list):
        return raw
    return []


def coverage_summary(coverage):
    coverage = coverage or {}
    return {
        'readiness': coverage.get('reportingReadiness', 'unknown'),
        'deepDive': (coverage.get('deepDive') or {}).get('status', 'unknown'),
        'model': (coverage.get('model') or {}).get('status', 'unknown'),
        'thesis': (coverage.get('thesis') or {}).get('status', 'unknown'),
    }


def report_link(path: str, label: str):
    p = Path(path)
    rel = None
    if p.exists():
        try:
            rel = p.relative_to(ROOT / 'docs')
        except ValueError:
            rel = None
    return f'<a class="download-chip" href="{esc(rel or path)}">{esc(label)}</a>'


def render_company_state_page(state, tasks_by_id):
    ticker = state.get('ticker') or 'UNKNOWN'
    thesis = state.get('thesisState') or {}
    business = state.get('businessSnapshot') or {}
    linked_tasks = [tasks_by_id[t] for t in linked_task_ids(state.get('tasks')) if t in tasks_by_id]
    recent = state.get('recentEvents') or []
    outputs = state.get('researchOutputs') or []
    coverage = coverage_summary(state.get('coverage'))
    gaps = state.get('coverageGaps') or []
    next_action = state.get('nextReviewAction') or {}
    position = state.get('portfolioPosition') or {}
    reporting = state.get('reporting') or {}

    recent_html = ''.join(
        f'<div class="portfolio-queue-item">{pill(e.get("materiality"))}<strong>{esc(e.get("date"))} · {esc(e.get("type"))}</strong><span>{esc(e.get("summary"))}</span></div>'
        for e in recent
    ) or '<div class="muted small">No recent events recorded.</div>'
    outputs_html = ''.join(
        f'<div class="portfolio-queue-item">{pill(o.get("type"))}<strong>{esc(o.get("date"))} · {esc(o.get("title") or o.get("version"))}</strong><span>{esc(o.get("path"))}</span></div>'
        for o in outputs
    ) or '<div class="muted small">No research outputs recorded.</div>'
    linked_task_html = ''.join(
        f'<div class="portfolio-queue-item">{pill(t.get("priority"))}<strong>{esc(t.get("id"))} · {esc(t.get("type"))}</strong><span>{esc(t.get("reason"))}</span></div>'
        for t in linked_tasks
    ) or '<div class="muted small">No linked open tasks.</div>'
    gaps_html = ''.join(
        f'<div class="portfolio-queue-item">{pill(g.get("severity"))}{pill(g.get("type"))}<strong>{esc(g.get("summary"))}</strong><span>{esc(g.get("recommendedAction"))}</span></div>'
        for g in gaps
    ) or '<div class="muted small">No material coverage gaps for current reporting.</div>'

    body = f'''
<div class="topbar"><div><div class="muted small">Company State v0.2</div><h1>{esc(ticker)} · {esc(state.get('name'))}</h1><div class="muted">Estado vivo para reporting PM. No sustituye la decisión del Portfolio Manager.</div></div><div><a href="../portfolio.html">← Portfolio OS</a></div></div>
<div class="grid section cockpit-kpi-grid"><div class="card"><div class="muted small">Type</div><div>{pill(state.get('type'))}</div></div><div class="card"><div class="muted small">Status</div><div>{pill(state.get('status'))}</div></div><div class="card"><div class="muted small">Priority</div><div>{pill(state.get('priority'))}</div></div><div class="card"><div class="muted small">Readiness</div><div>{pill(coverage['readiness'])}</div></div></div>
<div class="snapshot-grid section"><section class="card snapshot-panel snapshot-panel-wide"><h2>Next Review Action</h2><p>{esc(next_action.get('action'))}</p><ul class="list small"><li>Priority: {pill(next_action.get('priority'))}</li><li>Owner: {esc(next_action.get('owner'))}</li><li>Trigger: {esc(next_action.get('trigger'))}</li><li>Status: {pill(next_action.get('status'))}</li></ul></section><section class="card snapshot-panel"><h2>Portfolio Position</h2><ul class="list small"><li>Status: {pill(position.get('status'))}</li><li>Weight: {esc(position.get('weight'))}</li><li>Price: {esc(position.get('currentPrice'))}</li><li>Source: {esc(position.get('source'))}</li></ul></section></div>
<div class="snapshot-grid section"><section class="card snapshot-panel"><h2>Coverage</h2><ul class="list small"><li>Deep Dive: {pill(coverage['deepDive'])}</li><li>Model: {pill(coverage['model'])}</li><li>Thesis: {pill(coverage['thesis'])}</li><li>Reporting: {esc(reporting.get('notes'))}</li></ul></section><section class="card snapshot-panel snapshot-panel-wide"><h2>Coverage Gaps</h2><div class="portfolio-queue-list">{gaps_html}</div></section></div>
<div class="snapshot-grid section"><section class="card snapshot-panel snapshot-panel-wide"><h2>Thesis State</h2><p>{esc(thesis.get('summary'))}</p><ul class="list small"><li>Owner: {esc(thesis.get('owner'))}</li><li>Last reviewed: {esc(thesis.get('lastReviewedAt'))}</li><li>PM decision: {esc(thesis.get('portfolioManagerDecision'))}</li></ul><h3>What would change our mind</h3><ul class="list small">{list_html(thesis.get('whatWouldChangeOurMind'))}</ul></section><section class="card snapshot-panel"><h2>Business Snapshot</h2><p>{esc(business.get('description'))}</p><ul class="list small"><li>Segments: {esc(', '.join(business.get('segments') or []))}</li><li>Competitors: {esc(', '.join(business.get('competitors') or []))}</li><li>Cycle exposure: {esc(business.get('cycleExposure'))}</li></ul></section></div>
<div class="snapshot-grid section"><section class="card snapshot-panel"><h2>Key Drivers</h2><ul class="list small">{list_html(state.get('keyDrivers'))}</ul></section><section class="card snapshot-panel"><h2>Key Risks</h2><ul class="list small">{list_html(state.get('keyRisks'))}</ul></section><section class="card snapshot-panel"><h2>Watch Metrics</h2><ul class="list small">{list_html(state.get('watchMetrics'))}</ul></section><section class="card snapshot-panel"><h2>Open Questions</h2><ul class="list small">{list_html(state.get('openQuestions'))}</ul></section></div>
<div class="snapshot-grid section"><section class="card snapshot-panel snapshot-panel-wide"><h2>Linked Open Tasks</h2><div class="portfolio-queue-list">{linked_task_html}</div></section><section class="card snapshot-panel snapshot-panel-wide"><h2>Recent Events</h2><div class="portfolio-queue-list">{recent_html}</div></section></div>
<div class="card section"><h2>Research Outputs</h2><div class="portfolio-queue-list">{outputs_html}</div></div>
'''
    COMPANY_OUT.mkdir(parents=True, exist_ok=True)
    (COMPANY_OUT / f'{ticker}.html').write_text(page(f'{ticker} Company State', body, '../static/styles.css'))


def output_items(outputs):
    items = outputs.get('outputs') or []
    recent = sorted(items, key=lambda x: (x.get('updatedAt') or x.get('createdAt') or '', x.get('id') or ''))[-10:]
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


def md_preview(path: Path, max_lines=12):
    if not path.exists():
        return '[missing]'
    lines = []
    for line in path.read_text().splitlines():
        if line.strip():
            lines.append(line.strip())
        if len(lines) >= max_lines:
            break
    return '\n'.join(lines)


def main():
    registry, pipeline, company_states, radars, reports, outputs, system_health = load_portfolio_os()
    companies = registry.get('companies', [])
    tasks = pipeline.get('tasks', [])
    tasks_by_id = {t.get('id'): t for t in tasks if t.get('id')}
    open_tasks = [t for t in tasks if t.get('status') in ('open', 'in_progress', 'waiting')]
    high_tasks = [t for t in open_tasks if t.get('priority') == 'high']
    tasks_by_company = defaultdict(list)
    for task in open_tasks:
        tasks_by_company[task.get('company')].append(task)

    STATIC_OUT.mkdir(parents=True, exist_ok=True)
    if STATIC_SRC.exists():
        shutil.copy2(STATIC_SRC, STATIC_OUT / 'styles.css')

    for state in company_states.values():
        render_company_state_page(state, tasks_by_id)

    states_for_registry = {c.get('ticker'): company_states.get(c.get('ticker'), {}) for c in companies}
    portfolio_companies = [c for c in companies if c.get('type') == 'portfolio']
    watchlist_companies = [c for c in companies if c.get('type') in ('watchlist', 'idea')]
    readiness = Counter((states_for_registry[c.get('ticker')].get('coverage') or {}).get('reportingReadiness', 'unknown') for c in companies)
    by_status = Counter(c.get('status') for c in companies)
    by_priority = Counter(c.get('priority') for c in companies)
    total_gaps = sum(len((states_for_registry[c.get('ticker')].get('coverageGaps') or [])) for c in companies)
    high_next = [c for c in companies if (states_for_registry[c.get('ticker')].get('nextReviewAction') or {}).get('priority') == 'high']

    report_full = REPORTS / '2026-05-22-portfolio-review-v0.2.md'
    report_digest = REPORTS / '2026-05-22-portfolio-review-digest-v0.2.md'
    latest_report_links = ''.join([
        report_link(str(report_full), 'Portfolio Review v0.2'),
        report_link(str(report_digest), 'Digest v0.2'),
    ])
    digest_preview = '<br>'.join(esc(x) for x in md_preview(report_digest, 9).splitlines())

    def company_sort(c):
        n = states_for_registry[c.get('ticker')].get('nextReviewAction') or {}
        pr = {'high': 0, 'medium': 1, 'low': 2}.get(n.get('priority'), 3)
        typ = 0 if c.get('type') == 'portfolio' else 1
        return (typ, pr, c.get('ticker') or '')

    company_cards = ''.join(
        f'''
<a class="portfolio-company-card" href="portfolio_companies/{esc(c.get('ticker'))}.html">
  <div class="portfolio-card-top"><strong>{esc(c.get('ticker'))}</strong>{pill(c.get('status'))}</div>
  <div class="muted small">{esc(c.get('name'))}</div>
  <p>{esc(c.get('notes'))}</p>
  <div class="portfolio-metrics"><span>Type <b>{esc(c.get('type'))}</b></span><span>Priority <b>{esc(c.get('priority'))}</b></span><span>Readiness <b>{esc((states_for_registry[c.get('ticker')].get('coverage') or {}).get('reportingReadiness'))}</b></span><span>Gaps <b>{len(states_for_registry[c.get('ticker')].get('coverageGaps') or [])}</b></span></div>
  <div class="small muted">Next: {esc((states_for_registry[c.get('ticker')].get('nextReviewAction') or {}).get('action'))}</div>
</a>'''
        for c in sorted(companies, key=company_sort)
    )

    next_rows = ''.join(
        f'''<tr><td><strong>{esc(c.get('ticker'))}</strong><div class="muted small">{esc(c.get('type'))}</div></td><td>{pill((states_for_registry[c.get('ticker')].get('nextReviewAction') or {}).get('priority'))}</td><td class="small">{esc((states_for_registry[c.get('ticker')].get('nextReviewAction') or {}).get('action'))}</td><td>{esc((states_for_registry[c.get('ticker')].get('nextReviewAction') or {}).get('owner'))}</td></tr>'''
        for c in sorted(companies, key=company_sort)
        if (states_for_registry[c.get('ticker')].get('nextReviewAction') or {}).get('status') in ('open', 'waiting')
    )

    gaps_html = ''.join(
        f'<div class="portfolio-queue-item">{pill(g.get("severity"))}{pill(g.get("type"))}<strong>{esc(c.get("ticker"))}: {esc(g.get("summary"))}</strong><span>{esc(g.get("recommendedAction"))}</span></div>'
        for c in sorted(companies, key=company_sort)
        for g in (states_for_registry[c.get('ticker')].get('coverageGaps') or [])
    ) or '<div class="muted small">No coverage gaps recorded.</div>'

    recent_radar_html = ''.join(f'<li><span class="mono">{esc(p.name)}</span></li>' for p in radars[-5:]) or '<li>[none]</li>'
    status_html = ''.join(f'<li>{pill(k)} {v}</li>' for k, v in sorted(by_status.items()))
    priority_html = ''.join(f'<li>{pill(k)} {v}</li>' for k, v in sorted(by_priority.items()))
    readiness_html = ''.join(f'<li>{pill(k)} {v}</li>' for k, v in sorted(readiness.items()))
    check_html, warning_html = health_items(system_health)
    recent_outputs_html = output_items(outputs)

    body = f'''
<div class="topbar"><div><div class="muted small">Portfolio OS · Dashboard v0.2</div><h1>Research & Monitoring Dashboard</h1><div class="muted">Conectado a Portfolio State Contract v0.2: readiness, coverage gaps, next review actions y Portfolio Review.</div></div><div><a href="index.html">← Home</a></div></div>
<div class="card section cockpit-hero">
  <div class="muted small">Operating rule</div>
  <h2>El sistema informa, estructura, prioriza y prepara. El Portfolio Manager decide.</h2>
  <p class="small">La clasificación portfolio/watchlist y la prioridad PM salen de estado explícito, no de inferencia por artefactos.</p>
</div>
<div class="grid section cockpit-kpi-grid">
  <div class="card"><div class="muted small">Portfolio companies</div><div class="kpi">{len(portfolio_companies)}</div></div>
  <div class="card"><div class="muted small">Watchlist / ideas</div><div class="kpi">{len(watchlist_companies)}</div></div>
  <div class="card"><div class="muted small">Open tasks</div><div class="kpi">{len(open_tasks)}</div></div>
  <div class="card"><div class="muted small">High next actions</div><div class="kpi">{len(high_next)}</div></div>
  <div class="card"><div class="muted small">Coverage gaps</div><div class="kpi">{total_gaps}</div></div>
  <div class="card"><div class="muted small">System health</div><div class="kpi">{esc(str(system_health.get('overallStatus', 'missing')).upper())}</div></div>
</div>
<div class="card section"><h2>Latest Portfolio Review</h2><div class="download-chip-row">{latest_report_links}</div><p class="small muted">{digest_preview}</p></div>
<div class="snapshot-grid section">
  <section class="card snapshot-panel"><h2>Readiness mix</h2><ul class="list small">{readiness_html}</ul></section>
  <section class="card snapshot-panel"><h2>Company status</h2><ul class="list small">{status_html}</ul></section>
  <section class="card snapshot-panel"><h2>Priority mix</h2><ul class="list small">{priority_html}</ul></section>
  <section class="card snapshot-panel"><h2>Daily Radar runs</h2><ul class="list small">{recent_radar_html}</ul></section>
</div>
<div class="section card"><h2>Next Review Actions</h2><table><thead><tr><th>Company</th><th>Priority</th><th>Action</th><th>Owner</th></tr></thead><tbody>{next_rows}</tbody></table></div>
<div class="card section"><h2>Coverage Gaps</h2><div class="portfolio-queue-list">{gaps_html}</div></div>
<div class="portfolio-card-grid section">{company_cards}</div>
<div class="section card"><h2>Open Task Pipeline</h2><table><thead><tr><th>ID</th><th>Company</th><th>Type</th><th>Priority</th><th>Status</th><th>Reason</th><th>Next action</th></tr></thead><tbody>{task_rows(open_tasks)}</tbody></table></div>
<div class="snapshot-grid section"><section class="card snapshot-panel snapshot-panel-wide"><h2>Runtime Checks</h2><ul class="list small">{check_html}</ul></section><section class="card snapshot-panel snapshot-panel-wide"><h2>Active Warnings</h2><ul class="list small">{warning_html}</ul></section></div>
<div class="card section"><h2>Output Registry</h2><div class="portfolio-queue-list">{recent_outputs_html}</div></div>
<div class="snapshot-grid section"><section class="card snapshot-panel snapshot-panel-wide"><h2>Workflow</h2><ol class="list small"><li>Load registry + Company State v0.2</li><li>Split portfolio vs watchlist/idea</li><li>Read coverage gaps and nextReviewAction</li><li>Generate Portfolio Review + digest</li><li>Register output and validate ledgers</li></ol></section><section class="card snapshot-panel"><h2>Products</h2><ul class="list small"><li>Portfolio Review</li><li>Digest</li><li>Daily Radar</li><li>Company State</li><li>Task Pipeline</li></ul></section></div>
'''
    OUT.write_text(page('Research & Monitoring Dashboard', body))
    print(OUT)


if __name__ == '__main__':
    main()
