# Data Delta Detector v1

## Objetivo
Comparar snapshots de `extracted_financials_registry` para detectar cambios en métricas estructuradas entre dos estados del sistema.

La pregunta que responde esta pieza es:

> ¿Qué ha cambiado en los datos financieros extraídos desde la última vez?

---

## Alcance v1
Detectar cambios mecánicos en:
- revenue
- operating_income
- net_income
- diluted_eps
- cash_and_equivalents
- total_debt

No interpreta aún tesis ni materialidad final. Solo detecta y estructura diferencias.

---

## Inputs
- `registry/extracted_financials_registry.previous.json`
- `registry/extracted_financials_registry.json`

---

## Outputs
- `registry/data_deltas.json`
- opcionalmente `outputs/data_deltas.md`

---

## Qué detecta
Para cada ticker:
- cambio de valor en una métrica
- aparición o desaparición de una métrica
- cambio de status (`ok`, `not_found`, etc.)
- nueva compañía con extracted data
- compañía sin cambios

---

## Output conceptual
```json
{
  "MSFT": {
    "changed": true,
    "metric_changes": [
      {
        "metric": "revenue",
        "old_value": 65000000000,
        "new_value": 70000000000,
        "delta": 5000000000,
        "delta_pct": 0.0769,
        "old_status": "ok",
        "new_status": "ok"
      }
    ],
    "status": "ok",
    "checked_at": "2026-05-01T15:00:00Z"
  }
}
```

---

## Reglas v1
### 1. Cambio de valor
Si `old_value != new_value` y ambos existen:
- registrar `delta`
- registrar `delta_pct` cuando `old_value != 0`

### 2. Cambio de status
Si cambia `status` de la métrica:
- registrar `status_changed`

### 3. Métrica nueva o perdida
- si antes era `null` y ahora tiene valor → `appeared`
- si antes tenía valor y ahora no → `disappeared`

### 4. Nueva compañía
Si aparece nueva en extracted registry → `new_company_added`

---

## Filosofía
Esto sigue siendo:
- barato
- determinista
- trazable

No usa LLM por defecto.

---

## Relación con la siguiente capa
El `data_delta_detector` prepara la base para:
- reglas de materialidad
- priorización
- input limpio al thesis monitor
