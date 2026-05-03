# Thesis Monitor Input v1

## Objetivo
Definir la interfaz limpia entre:
- maintenance layer / data layer
- y la futura capa de thesis monitoring

La capa de thesis monitor no debería leer directamente todos los artefactos brutos salvo necesidad.
Debe recibir un input ya condensado.

---

## Principio
El thesis monitor recibe:
- contexto de cobertura
- filing delta
- data delta
- prioridad preliminar por reglas

Y decide:
- ignorar
- revisar
- investigar más
- escalar

---

## Output esperado del preparador
### `thesis_monitor_input.json`
Ejemplo conceptual:

```json
{
  "ticker": "MSFT",
  "coverage_status": "covered",
  "extraction_quality": "validated",
  "latest_period": {
    "form_type": "10-Q",
    "filing_date": "2026-04-29",
    "report_date": "2026-03-31"
  },
  "filing_delta": {
    "changed": true,
    "new_filing_types": ["10-Q"],
    "changes": ["latest_10q_updated"]
  },
  "data_delta": {
    "changed": true,
    "metric_changes": [
      {
        "metric": "revenue",
        "delta_pct": 0.08,
        "priority": "investigate"
      }
    ]
  },
  "preliminary_priority": "investigate",
  "notes": []
}
```

---

## Campos mínimos recomendados
- `ticker`
- `coverage_status`
- `extraction_quality`
- `latest_period`
- `filing_delta`
- `data_delta`
- `preliminary_priority`
- `notes`

---

## Reglas de preparación
### `coverage_status`
Viene de la capa de quality/coverage.

### `filing_delta`
Resume si hubo cambios relevantes en filings.

### `data_delta`
Resume si hubo cambios en métricas y cuáles.

### `preliminary_priority`
Se calcula por reglas de materialidad v1:
- tomar la prioridad máxima observada
- si no hay cambios → `ignore`

---

## Qué gana la arquitectura con esto
Separamos claramente:
- recolección
- extracción
- comparación
- priorización
- interpretación de tesis

Eso reduce coste y evita que el modelo tenga que re-hacer trabajo mecánico.

---

## Siguiente paso lógico
Después de este contrato, la siguiente pieza sería:
- `prepare_thesis_monitor_input.py`

o bien:
- una primera versión del `thesis_monitor` que consuma este contrato

Pero conceptualmente, esta interfaz ya deja bien desacopladas las capas.
