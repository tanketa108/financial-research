# Valuation State Contract v1

## Objetivo
Definir un formato estructurado para almacenar el estado de valoración de una compañía.

El markdown sirve para pensar y leer.
El estado estructurado sirve para:
- prefill automático
- comparación futura
- dashboard
- integración con otras capas

---

## Principios
- separar datos estructurados de notas narrativas
- permitir campos vacíos explícitos
- distinguir inputs de sistema vs juicio del analista
- hacer posible completar una valoración por etapas

---

## Top-level fields

```json
{
  "ticker": "UBER",
  "name": "Uber Technologies, Inc.",
  "status": "draft",
  "latest_period": {},
  "historical_base": {},
  "thesis": {},
  "segments": [],
  "drivers": [],
  "quality": {},
  "debt": {},
  "cash_conversion": {},
  "capital_allocation": {},
  "comparables": {},
  "valuation_methods": {},
  "sensitivities": {},
  "scenarios": [],
  "catalysts": [],
  "risks": [],
  "qualitative_notes": {}
}
```

---

## Status values
- `draft`
- `prefilled`
- `analyst_review_needed`
- `active`
- `stale`

---

## Design intent by section

### `latest_period`
Latest extracted period metadata.

### `historical_base`
Structured financial history or placeholders for it.

### `thesis`
Analyst-owned fields.

### `segments`
Reported lines + forward interpretation.

### `drivers`
Compact list of key variables that matter most.

### `quality`
DuPont, ROIC, WACC, EVA spread.

### `debt`
Debt structure and service capacity.

### `cash_conversion`
WC / CCC / FCF conversion mechanics.

### `capital_allocation`
Buybacks, dilution, SBC, reinvestment, M&A.

### `valuation_methods`
Method-specific assumptions and outputs.

### `sensitivities`
One-way and two-way sensitivity containers.

### `scenarios`
Discrete business-model scenarios.

### `catalysts`
Near-to-medium-term signposts.

### `risks`
Risk register.

### `qualitative_notes`
Narrative layer linked to knowledge / thesis maintenance.

---

## Intended workflow
1. System pre-fills what it can.
2. Charlie exposes gaps clearly.
3. Ander fills thesis/judgment sections.
4. Valuation state becomes the source for future dashboard/rendering.
