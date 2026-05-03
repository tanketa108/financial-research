# Delta Detector — Implementation Plan

## Objetivo
Cerrar la fase 1 con una implementación real de detección de cambios entre estados del `filing_registry`.

---

## Principio
El `delta_detector` no compara contra memoria implícita. Compara contra un snapshot persistido.

Eso da:
- trazabilidad
- auditabilidad
- reproducibilidad
- simplicidad

---

## Estrategia recomendada

### Archivos de estado
```text
financial_system/registry/
  filing_registry.json
  filing_registry.previous.json
  filing_deltas.json
```

### Regla operativa
Antes de escribir un registry nuevo:
1. mover/copiar `filing_registry.json` a `filing_registry.previous.json`
2. escribir el nuevo `filing_registry.json`
3. ejecutar `detect_filing_deltas.py`
4. producir `filing_deltas.json`
5. opcionalmente renderizar `filing_deltas.md`

---

## Script principal
### `financial_system/tools/detect_filing_deltas.py`

### Inputs
- `registry/filing_registry.previous.json`
- `registry/filing_registry.json`

### Outputs
- `registry/filing_deltas.json`
- opcionalmente `outputs/filing_deltas.md`

---

## Lógica mínima

### Para cada ticker del registry actual
Comparar contra el estado previo:

#### 1. Latest 10-Q
Si cambia `latest_10q.accession_number`:
- `changed = true`
- añadir cambio `latest_10q_updated`
- añadir `10-Q` a `new_filing_types`

#### 2. Latest 10-K
Si cambia `latest_10k.accession_number`:
- `changed = true`
- añadir cambio `latest_10k_updated`
- añadir `10-K` a `new_filing_types`

#### 3. 8-K recientes
Comparar accession numbers del array.
Si hay alguno nuevo:
- `changed = true`
- añadir cambio `new_8k_detected`
- añadir `8-K` a `new_filing_types`
- registrar cuáles son nuevos

#### 4. Status
Si cambia `status`:
- registrar `status_change`

#### 5. Nueva compañía
Si el ticker no existía antes:
- `changed = true`
- añadir cambio `new_company_added`

---

## Output esperado
### `filing_deltas.json`

```json
{
  "UBER": {
    "changed": true,
    "new_filing_types": ["10-Q"],
    "changes": [
      {
        "kind": "latest_10q_updated",
        "old_accession": "0001543151-25-000020",
        "new_accession": "0001543151-25-000033"
      }
    ],
    "status_change": null,
    "checked_at": "2026-05-01T11:00:00Z"
  }
}
```

### Campos mínimos
- `changed` *(bool)*
- `new_filing_types` *(array)*
- `changes` *(array)*
- `status_change` *(object|null)*
- `checked_at` *(timestamp)*

---

## Render legible opcional
### `outputs/filing_deltas.md`

Ejemplo:

```md
# Filing Deltas

## Changed
- UBER: new 10-Q
- MSFT: new 8-K

## No Changes
- NFLX
```

Este output ya sería muy útil como capa de mantenimiento diaria/semanal.

---

## Edge cases

### 1. Primera corrida
Si no existe `filing_registry.previous.json`:
- no hay comparación real
- marcar como `initial_snapshot`
- no interpretar todo como novedad operativa

### 2. Tickers pendientes de revisión
Si una compañía está fuera del registry por no tener CIK resuelto:
- no genera delta de filings
- puede salir en una sección de coverage gaps

### 3. 8-K en exceso
No todos serán igual de relevantes.
En fase 1 basta con detectar novedad; la materialidad se tratará después.

---

## Valor de esta pieza
Con esto, la fase 1 deja de ser:
- foto estática

y pasa a ser:
- mantenimiento incremental
- atención dirigida
- priorización

---

## Siguiente paso tras esto
Una vez exista el delta detector real, el siguiente bloque natural será:
- `structured_extractor`
- o la capa de actualización de métricas financieras

Pero solo después de cerrar esta capa de cambios de filings.
