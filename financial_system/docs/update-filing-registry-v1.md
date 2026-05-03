# Update Filing Registry v1

## Objetivo
Refrescar automáticamente `filing_registry.json` a partir de SEC `submissions` para los tickers con CIK resuelto.

---

## Responsabilidad
Para cada compañía cubierta:
- consultar `https://data.sec.gov/submissions/CIK<CIK>.json`
- identificar:
  - latest 10-Q
  - latest 10-K
  - hasta 5 recent 8-K
- reconstruir la entrada del registry

---

## Principio
- determinista
- barato
- sin LLM
- sin depender de HTML raw

---

## Input
- `positions.json`
- `registry/ticker_cik_map.json`

---

## Output
- `registry/filing_registry.json`

---

## Reglas v1
- solo tickers con CIK resuelto
- si falla una compañía, marcar `status=error` y seguir con las demás
- `has_new_filing` y `new_filing_types` pueden quedarse en `false`/`[]` en esta capa; los deltas los calculará `detect_filing_deltas.py`

---

## Relación con pipeline runner
Una vez exista este script, el runner debería llamarlo antes de `detect_filing_deltas.py`.

Eso haría el flujo mucho más completo:
1. update filing registry
2. detect filing deltas
3. extract metrics
4. build extracted registry
5. detect data deltas
6. prepare thesis input
7. run thesis monitor
