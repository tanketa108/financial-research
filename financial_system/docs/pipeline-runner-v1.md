# Pipeline Runner v1

## Objetivo
Pasar de un conjunto de módulos correctos a una máquina ejecutable de punta a punta.

El runner no reemplaza la lógica de cada módulo.
La orquesta.

---

## Responsabilidad
Ejecutar, en orden, las piezas del sistema financiero:

1. actualizar filing registry *(cuando exista update automático robusto)*
2. detectar filing deltas
3. extraer métricas por compañía cubierta
4. construir extracted financials registry
5. detectar data deltas
6. preparar thesis monitor input
7. ejecutar thesis monitor

---

## Principio
El runner debe ser:
- simple
- explícito
- auditable
- fácil de reanudar

Nada de magia escondida.

---

## Inputs mínimos
- `positions.json`
- `ticker_cik_map.json`
- `filing_registry.json`
- snapshots previos cuando existan

---

## Outputs principales
- `filing_deltas.json`
- `extracted_financials_registry.json`
- `data_deltas.json`
- `thesis_monitor_input.json`
- `thesis_monitor_output.json`
- outputs markdown equivalentes

---

## Fases del runner v1

### Phase 0 — snapshot management
Antes de regenerar artefactos comparables:
- copiar `filing_registry.json` a `filing_registry.previous.json` si procede
- copiar `extracted_financials_registry.json` a `extracted_financials_registry.previous.json` si procede

### Phase 1 — filing delta
- correr `detect_filing_deltas.py`
- renderizar `filing_deltas.md` *(opcional en v1, recomendable)*

### Phase 2 — extraction
Para cada ticker cubierto con CIK resuelto:
- correr `extract_financial_metrics.py <TICKER>`

### Phase 3 — extracted registry
- correr `build_extracted_financials_registry.py`

### Phase 4 — data delta
- correr `detect_data_deltas.py`
- renderizar `data_deltas.md`

### Phase 5 — thesis input
- correr `prepare_thesis_monitor_input.py`

### Phase 6 — thesis output
- correr `run_thesis_monitor.py`

---

## Qué no debe hacer todavía
- no enviar notificaciones externas
- no interpretar tesis complejas
- no reescribir posiciones
- no improvisar estrategias para foreign issuers

---

## Recomendación práctica
El runner v1 debería soportar dos modos:

### `baseline`
Construye o refresca estado sin asumir que hay novedades reales.

### `incremental`
Asume snapshots previos válidos y calcula cambios reales.

---

## Valor
Con este runner, el sistema pasa de ser:
- una colección de piezas buenas

a ser:
- un flujo operativo repetible
