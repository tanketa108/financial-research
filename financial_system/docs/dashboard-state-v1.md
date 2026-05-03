# Dashboard State v1

## Objetivo
Definir el estado agregado que un dashboard de capa 2 debería leer sin tener que interpretar todos los artefactos brutos.

Este estado debe servir como vista operativa de:
- actualización
- cobertura
- prioridad
- valoración
- tesis

---

## Principio
El dashboard no debe nacer como una UI bonita sin backend.
Debe leer un contrato claro y suficientemente estable.

---

## Campos sugeridos por compañía

```json
{
  "ticker": "UBER",
  "coverage_status": "covered",
  "update_status": {
    "latest_filing_date": "2025-11-04",
    "latest_report_date": "2025-09-30",
    "filing_delta_changed": true,
    "data_delta_changed": false,
    "thesis_monitor_decision": "review"
  },
  "valuation_status": {
    "status": "draft",
    "methods_filled": 0,
    "central_reference": null,
    "range": null
  },
  "thesis_status": {
    "thesis_short": null,
    "current_stance": null,
    "scenario_central": null
  },
  "key_metrics": {
    "revenue": 13467000000,
    "operating_income": 1113000000,
    "net_income": 6626000000,
    "diluted_eps": 3.11,
    "cash": 8432000000,
    "debt": 10615000000
  },
  "key_risks": [],
  "key_catalysts": []
}
```

---

## Inputs to build this state
- extracted financials registry
- filing deltas
- data deltas
- thesis monitor output
- valuation state per company

---

## Why this matters
This is the bridge between:
- back-end analytical pipeline
- future Discord / dashboard / UI surfaces

Without this state, every UI layer will need to re-interpret too much raw information.
