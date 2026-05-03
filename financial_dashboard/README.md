# Financial Dashboard v1

Primer dashboard local en HTML para el Financial System.

## Objetivo
Dar una superficie usable para:
- priorizar revisión
- abrir una compañía
- inspeccionar base financiera, cash conversion y valoración
- detectar huecos estructurales antes de Fase 3

## Build
```bash
python3 /data/.openclaw/workspace/financial_dashboard/build_dashboard_html.py
```

## Output
- `output/index.html`
- `output/companies/<TICKER>.html`

## Fuentes
- `financial_system/registry/dashboard_state.json`
- `financial_system/registry/thesis_monitor_output.json`
- `financial_system/valuations/*-valuation-state-v1.json`
