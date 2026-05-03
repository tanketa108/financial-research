# Financial System — Data Contracts v1

## Objetivo
Definir los contratos de datos mínimos de la fase 1 del sistema financiero.

Esta fase se centra en:
- universo de posiciones
- resolución ticker -> CIK
- filing registry
- salida legible

Sin análisis de tesis todavía.

---

## 1. `positions.json`

### Propósito
Lista humana y operativa de posiciones activas que el sistema debe seguir.

### Schema conceptual
```json
[
  {
    "ticker": "UBER",
    "name": "Uber Technologies, Inc.",
    "cik": "0001543151",
    "active": true,
    "notes": "Control sample"
  }
]
```

### Campos
- `ticker` *(string, required)*
- `name` *(string, required)*
- `cik` *(string|null, optional at bootstrap)*
- `active` *(boolean, required)*
- `notes` *(string, optional)*

---

## 2. `registry/ticker_cik_map.json`

### Propósito
Persistir el mapping operativo entre ticker y CIK, con estado de resolución y notas de edge cases.

### Schema conceptual
```json
{
  "UBER": {
    "ticker": "UBER",
    "name": "Uber Technologies, Inc.",
    "cik": "0001543151",
    "status": "resolved",
    "issuer_type": "domestic",
    "sec_entity_name": "Uber Technologies, Inc",
    "last_verified_at": "2026-04-29T22:00:00Z",
    "notes": []
  },
  "NVO": {
    "ticker": "NVO",
    "name": "Novo Nordisk A/S",
    "cik": "0000000000",
    "status": "needs_review",
    "issuer_type": "foreign_issuer",
    "sec_entity_name": "...",
    "last_verified_at": "2026-04-29T22:00:00Z",
    "notes": [
      "ADR / foreign issuer path requires validation"
    ]
  }
}
```

### Campos
- `ticker` *(string, required)*
- `name` *(string, required)*
- `cik` *(string|null, required)*
- `status` *(enum, required)*
  - `resolved`
  - `needs_review`
  - `ambiguous`
  - `not_found`
- `issuer_type` *(enum, optional but recommended)*
  - `domestic`
  - `foreign_issuer`
  - `adr`
  - `unknown`
- `sec_entity_name` *(string|null)*
- `last_verified_at` *(ISO timestamp string)*
- `notes` *(array of strings)*

### Reglas
- Este archivo es el mapping persistente de referencia para SEC.
- Si un ticker está en `resolved`, el resto del sistema puede usar su CIK.
- Si está en `needs_review` o `ambiguous`, el filing registry no debería asumir éxito silencioso.

---

## 3. `registry/filing_registry.json`

### Propósito
Guardar el estado actual de filings relevantes por compañía para detectar novedades y alimentar las siguientes capas.

### Schema conceptual
```json
{
  "UBER": {
    "ticker": "UBER",
    "cik": "0001543151",
    "latest_10q": {
      "accession_number": "0001543151-25-000033",
      "filing_date": "2025-11-04",
      "report_date": "2025-09-30",
      "primary_document": "uber-20250930.htm",
      "url": "https://www.sec.gov/Archives/edgar/data/1543151/000154315125000033/uber-20250930.htm"
    },
    "latest_10k": {
      "accession_number": "...",
      "filing_date": "...",
      "report_date": "...",
      "primary_document": "...",
      "url": "..."
    },
    "recent_8k": [
      {
        "accession_number": "...",
        "filing_date": "...",
        "report_date": "...",
        "primary_document": "...",
        "url": "..."
      }
    ],
    "has_new_filing": true,
    "new_filing_types": ["10-Q"],
    "status": "ok",
    "last_checked_at": "2026-04-29T22:00:00Z",
    "notes": []
  }
}
```

### Campos de nivel compañía
- `ticker` *(string, required)*
- `cik` *(string, required)*
- `latest_10q` *(object|null)*
- `latest_10k` *(object|null)*
- `recent_8k` *(array)*
- `has_new_filing` *(boolean, required)*
- `new_filing_types` *(array of strings)*
- `status` *(enum, required)*
  - `ok`
  - `needs_review`
  - `error`
  - `missing_cik`
- `last_checked_at` *(ISO timestamp string, required)*
- `notes` *(array of strings)*

### Filing object schema
- `accession_number` *(string, required)*
- `filing_date` *(YYYY-MM-DD, required)*
- `report_date` *(YYYY-MM-DD|null)*
- `primary_document` *(string|null)*
- `url` *(string|null)*

### Reglas
- `latest_10q` y `latest_10k` deben representar solo el filing más reciente de ese tipo.
- `recent_8k` puede limitarse a una ventana corta (por ejemplo, últimos 5 o desde último check).
- `has_new_filing` depende de comparar contra el estado previo del registro.
- `new_filing_types` resume qué tipos cambiaron desde el último estado conocido.

---

## 4. `outputs/filing_summary.md`

### Propósito
Salida legible para Ander.

### Estructura conceptual
```md
# Filing Summary

## UBER
- Latest 10-Q: 2025-11-04 (report date 2025-09-30)
- Latest 10-K: ...
- New filings since last check: 10-Q
- Notes: none
```

### Regla
No debe intentar interpretar todavía el impacto en tesis.
Solo resumir el estado del mantenimiento.

---

## 5. `logs/update_history.jsonl`

### Propósito
Trazabilidad mínima de cada corrida.

### Ejemplo
```json
{"ts":"2026-04-29T22:10:00Z","kind":"filing_registry_update","positions_checked":5,"updated":["UBER"],"errors":[]}
```

### Campos
- `ts`
- `kind`
- `positions_checked`
- `updated`
- `errors`
- `notes` *(optional)*

---

## Principios de estos contratos
1. Simples
2. Auditables
3. Estables
4. Pensados para código, no para LLM
5. Suficientes para alimentar capas posteriores

---

## Siguiente paso recomendado
Implementar estos contratos con una primera corrida real sobre la muestra de control, empezando por:
1. `ticker_cik_map.json`
2. `filing_registry.json`
