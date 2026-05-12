#!/usr/bin/env python3
from __future__ import annotations

import html, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUTS=ROOT/'financial_system/dashboard_inputs'
OUT=ROOT/'docs/portfolio.html'

def esc(x): return html.escape('[missing]' if x is None else str(x))
def pill(x):
    txt='missing' if x is None else str(x); cls=txt.lower().replace(' ','_').replace('/','_')
    return f'<span class="pill pill-{esc(cls)}">{esc(txt)}</span>'
def money(v):
    if v is None: return '[missing]'
    try: v=float(v)
    except: return esc(v)
    return f'${v/1e9:.1f}B' if abs(v)>=1e9 else f'${v/1e6:.1f}M'
def pct(v):
    if v is None: return '[missing]'
    try: return f'{float(v)*100:.1f}%'
    except: return esc(v)

def load():
    rows=[]
    for p in sorted(INPUTS.glob('*-dashboard-input-v0.json')):
        d=json.loads(p.read_text())
        rows.append(d)
    return rows

def main():
    data=load()
    need=sum(1 for d in data if (d.get('maintenance') or {}).get('status') in ('baseline_needed','watch','needs_periodic_review'))
    high=sum(1 for d in data for q in d.get('maintenance_queue',[]) if q.get('priority')=='high')
    watch=sum(1 for d in data for w in (d.get('health') or {}).get('watch_items',[]))
    cards=''.join(f'''
<a class="portfolio-company-card" href="companies/{esc(d['ticker'])}.html">
  <div class="portfolio-card-top"><strong>{esc(d['ticker'])}</strong>{pill((d.get('health') or {}).get('overall_status'))}</div>
  <div class="muted small">{esc(d.get('company_name'))}</div>
  <p>{esc((d.get('thesis') or {}).get('one_line'))}</p>
  <div class="portfolio-metrics"><span>Revenue <b>{money((d.get('key_metrics') or {}).get('revenue'))}</b></span><span>Op margin <b>{pct((d.get('key_metrics') or {}).get('operating_margin'))}</b></span></div>
  <div class="small muted">Next: {esc((d.get('maintenance') or {}).get('next_action'))}</div>
</a>''' for d in data)
    queue=[]
    for d in data:
        for q in d.get('maintenance_queue',[])[:2]:
            queue.append((q.get('priority'),d['ticker'],q.get('task'),q.get('output')))
    qhtml=''.join(f'<div class="portfolio-queue-item">{pill(pr)}<strong>{esc(t)} · {esc(task)}</strong><span>{esc(out)}</span></div>' for pr,t,task,out in queue[:12])
    news=[]
    for d in data:
        for n in d.get('stocktitan_news_snapshot',[])[:2]:
            news.append((n.get('thesis_relevance'),d['ticker'],n.get('headline'),n.get('category')))
    nhtml=''.join(f'<div class="portfolio-news-item">{pill(rel)}<strong>{esc(t)} · {esc(head)}</strong><span>{esc(cat)}</span></div>' for rel,t,head,cat in news[:12])
    body=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Portfolio Maintenance Dashboard</title><link rel="stylesheet" href="static/styles.css"></head><body><div class="wrap">
<div class="topbar"><div><div class="muted small">Portfolio Maintenance Cockpit v0</div><h1>Portfolio Dashboard</h1><div class="muted">Cuadro de mando para mantenimiento de tesis, señales y prioridades.</div></div><div><a href="index.html">← Home</a></div></div>
<div class="grid section cockpit-kpi-grid"><div class="card"><div class="muted small">Companies</div><div class="kpi">{len(data)}</div></div><div class="card"><div class="muted small">Need baseline/watch</div><div class="kpi">{need}</div></div><div class="card"><div class="muted small">High priority tasks</div><div class="kpi">{high}</div></div><div class="card"><div class="muted small">Watch items</div><div class="kpi">{watch}</div></div></div>
<div class="portfolio-card-grid section">{cards}</div>
<div class="snapshot-grid section"><section class="card snapshot-panel snapshot-panel-wide"><h2>Maintenance queue</h2><div class="portfolio-queue-list">{qhtml}</div></section><section class="card snapshot-panel"><h2>Methodology</h2><ul class="list small"><li>Dashboard = snapshot ejecutivo.</li><li>Tesis escrita = detalle cualitativo.</li><li>Excel/modelo = detalle cuantitativo.</li><li>StockTitan = radar externo secundario.</li><li>Material changes require primary-source verification.</li></ul></section></div>
<div class="card section"><h2>External radar / StockTitan news</h2><div class="portfolio-news-grid">{nhtml}</div></div>
</div></body></html>'''
    OUT.write_text(body)
    print(OUT)
if __name__=='__main__': main()
