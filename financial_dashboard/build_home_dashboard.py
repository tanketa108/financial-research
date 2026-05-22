#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
PORTFOLIO = WORKSPACE / 'portfolio' if (WORKSPACE / 'portfolio').exists() else ROOT / 'financial_system/portfolio'
DOCS = ROOT / 'docs'
OUT = DOCS / 'index.html'
REPORTS_SRC = ROOT / 'financial_system/portfolio/reports'
REPORTS_DOCS = DOCS / 'portfolio_reports'
STATIC_OUT = DOCS / 'static'
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


def page(title: str, body: str) -> str:
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="static/styles.css">
</head>
<body>
  <div class="wrap">{body}</div>
</body>
</html>
'''


def copy_reports():
    REPORTS_DOCS.mkdir(parents=True, exist_ok=True)
    copied = []
    for src in sorted(REPORTS_SRC.glob('*.md')) if REPORTS_SRC.exists() else []:
        dst = REPORTS_DOCS / src.name
        shutil.copy2(src, dst)
        copied.append(dst)
    return copied


def md_digest_preview(path: Path, max_bullets=5):
    if not path.exists():
        return '<li>[missing digest]</li>'
    bullets = []
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith('- '):
            bullets.append(stripped[2:])
        if len(bullets) >= max_bullets:
            break
    return ''.join(f'<li>{esc(x)}</li>' for x in bullets) or '<li>[no digest bullets]</li>'


def main():
    registry = read_json(PORTFOLIO / 'company-registry.json', {'companies': []})
    tasks = read_json(PORTFOLIO / 'task-pipeline.json', {'tasks': []}).get('tasks', [])
    outputs = read_json(PORTFOLIO / 'output-registry.json', {'outputs': []}).get('outputs', [])
    states = {}
    for p in sorted((PORTFOLIO / 'companies').glob('*.json')):
        j = read_json(p, {})
        if j.get('ticker'):
            states[j['ticker']] = j

    if STATIC_SRC.exists():
        STATIC_OUT.mkdir(parents=True, exist_ok=True)
        shutil.copy2(STATIC_SRC, STATIC_OUT / 'styles.css')
    copy_reports()

    companies = registry.get('companies', [])
    portfolio = [c for c in companies if c.get('type') == 'portfolio']
    watchlist = [c for c in companies if c.get('type') in ('watchlist', 'idea')]
    open_tasks = [t for t in tasks if t.get('status') in ('open', 'in_progress', 'waiting')]
    readiness = Counter((states.get(c.get('ticker'), {}).get('coverage') or {}).get('reportingReadiness', 'unknown') for c in companies)
    high_actions = [c for c in companies if (states.get(c.get('ticker'), {}).get('nextReviewAction') or {}).get('priority') == 'high']
    total_gaps = sum(len(states.get(c.get('ticker'), {}).get('coverageGaps') or []) for c in companies)

    def sort_action(c):
        n = states.get(c.get('ticker'), {}).get('nextReviewAction') or {}
        pr = {'high': 0, 'medium': 1, 'low': 2}.get(n.get('priority'), 3)
        typ = 0 if c.get('type') == 'portfolio' else 1
        return (pr, typ, c.get('ticker') or '')

    action_cards = ''.join(
        f'''<div class="portfolio-queue-item">{pill((states.get(c.get('ticker'), {}).get('nextReviewAction') or {}).get('priority'))}<strong>{esc(c.get('ticker'))} · {esc(c.get('name'))}</strong><span>{esc((states.get(c.get('ticker'), {}).get('nextReviewAction') or {}).get('action'))}</span><span class="small muted">Owner: {esc((states.get(c.get('ticker'), {}).get('nextReviewAction') or {}).get('owner'))} · Type: {esc(c.get('type'))}</span></div>'''
        for c in sorted(companies, key=sort_action)[:6]
    )

    readiness_html = ''.join(f'<li>{pill(k)} {v}</li>' for k, v in sorted(readiness.items()))

    latest_outputs = sorted(outputs, key=lambda o: (o.get('updatedAt') or o.get('createdAt') or '', o.get('id') or ''))[-6:]
    outputs_html = ''.join(
        f'''<div class="portfolio-queue-item">{pill(o.get('type'))}{pill(o.get('status'))}<strong>{esc(o.get('title'))}</strong><span>{esc(o.get('path'))}</span></div>'''
        for o in latest_outputs
    )

    digest_path = REPORTS_DOCS / '2026-05-22-portfolio-review-digest-v0.2.md'
    report_path = REPORTS_DOCS / '2026-05-22-portfolio-review-v0.2.md'

    universe_items = ''.join(
        f'<li><strong>{esc(c.get("ticker"))}</strong> — {pill(c.get("type"))} {pill(c.get("priority"))} <span class="muted small">{esc((states.get(c.get("ticker"), {}).get("coverage") or {}).get("reportingReadiness"))}</span></li>'
        for c in companies
    )

    body = f'''
<div class="topbar"><div><div class="muted small">Clawbot Financial Project · GitHub Dashboard</div><h1>Portfolio Research & Monitoring OS</h1><div class="muted">Portada operativa: visión PM del workflow, cobertura, next actions, reporting y dashboard.</div><div class="small muted mono">Build dashboard-home-v0.2 · 2026-05-22</div></div><div class="muted small"><a href="portfolio.html">Open Operations Dashboard →</a></div></div>
<div class="card section cockpit-hero">
  <div class="muted small">Operating principle</div>
  <h2>El sistema informa, estructura, prioriza y prepara. El Portfolio Manager decide.</h2>
  <p class="small">Esta portada es el punto de entrada del proyecto: cartera, watchlist, reporting, tareas abiertas y flujo de trabajo. Daily Radar detecta eventos; Portfolio Review organiza la visión PM.</p>
  <div class="download-chip-row"><a class="download-chip" href="portfolio.html">Operations Dashboard</a><a class="download-chip" href="portfolio_reports/{esc(report_path.name)}">Portfolio Review v0.2</a><a class="download-chip" href="portfolio_reports/{esc(digest_path.name)}">Digest v0.2</a></div>
</div>
<div class="grid section cockpit-kpi-grid">
  <div class="card"><div class="muted small">Portfolio companies</div><div class="kpi">{len(portfolio)}</div></div>
  <div class="card"><div class="muted small">Watchlist / ideas</div><div class="kpi">{len(watchlist)}</div></div>
  <div class="card"><div class="muted small">Open tasks</div><div class="kpi">{len(open_tasks)}</div></div>
  <div class="card"><div class="muted small">High next actions</div><div class="kpi">{len(high_actions)}</div></div>
  <div class="card"><div class="muted small">Coverage gaps</div><div class="kpi">{total_gaps}</div></div>
  <div class="card"><div class="muted small">Registered outputs</div><div class="kpi">{len(outputs)}</div></div>
</div>
<div class="snapshot-grid section">
  <section class="card snapshot-panel snapshot-panel-wide"><h2>Portfolio Review Digest</h2><ul class="list small">{md_digest_preview(digest_path)}</ul></section>
  <section class="card snapshot-panel"><h2>Readiness mix</h2><ul class="list small">{readiness_html}</ul></section>
</div>
<div class="snapshot-grid section">
  <section class="card snapshot-panel snapshot-panel-wide"><h2>PM review queue</h2><div class="portfolio-queue-list">{action_cards}</div></section>
  <section class="card snapshot-panel"><h2>Workflow map</h2><ol class="list small"><li>Research / Deep Dive / Model</li><li>Company State v0.2</li><li>Portfolio Review + Digest</li><li>Dashboard</li><li>PM next action</li></ol></section>
</div>
<div class="snapshot-grid section">
  <section class="card snapshot-panel"><h2>Universe</h2><ul class="list small">{universe_items}</ul></section>
  <section class="card snapshot-panel snapshot-panel-wide"><h2>Latest outputs</h2><div class="portfolio-queue-list">{outputs_html}</div></section>
</div>
<div class="card section"><h2>How to use this dashboard</h2><ul class="list small"><li><strong>Start here:</strong> read the digest and PM review queue.</li><li><strong>For workflow state:</strong> open Operations Dashboard.</li><li><strong>For company detail:</strong> open the company pages from the operations dashboard.</li><li><strong>For weekly/monthly review:</strong> use Portfolio Review v0.2.</li><li><strong>For event monitoring:</strong> Daily Radar remains separate and should only escalate material items.</li></ul></div>
'''
    OUT.write_text(page('Portfolio Research & Monitoring OS', body))
    print(OUT)


if __name__ == '__main__':
    main()
