# Delta Detector v1

## Objetivo
Convertir el filing registry de una foto estática en un sistema de mantenimiento real.

La pregunta que responde esta pieza es:

> ¿Qué ha cambiado desde la última vez que miramos?

---

## Responsabilidad
El `delta_detector` compara dos estados del `filing_registry`:
- estado anterior
- estado actual

Y produce una salida estructurada que resume diferencias relevantes a nivel de filings.

En v1, todavía no interpreta tesis. Solo detecta cambios de mantenimiento.

---

## Qué detecta
Como mínimo:
- nuevo 10-Q
- nuevo 10-K
- nuevos 8-K
- cambio de estado (`ok`, `needs_review`, `error`)
- cambios en cobertura (por ejemplo una compañía pasa de unresolved a resolved)

---

## Qué no detecta aún
- impacto en la tesis
- cambios en métricas financieras
- cambios cualitativos del negocio
- materialidad económica

Eso pertenece a capas posteriores.

---

## Input esperado

### `old_filing_registry.json`
Snapshot anterior.

### `new_filing_registry.json`
Snapshot recién actualizado.

---

## Output esperado
### `filing_deltas.json`
Ejemplo conceptual:

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
    "status_change": null
  },
  "MSFT": {
    "changed": false,
    "new_filing_types": [],
    "changes": [],
    "status_change": null
  }
}
```

### `filing_deltas.md`
Salida legible para Ander:
- qué compañías tienen cambios
- qué tipo de filing cambió
- qué nombres merecen mirar más de cerca

---

## Reglas de detección

### 1. Nuevo 10-Q
Si `latest_10q.accession_number` cambia, marcar:
- `latest_10q_updated`
- `new_filing_types += ["10-Q"]`

### 2. Nuevo 10-K
Si `latest_10k.accession_number` cambia, marcar:
- `latest_10k_updated`
- `new_filing_types += ["10-K"]`

### 3. Nuevos 8-K
Si aparecen accession numbers nuevos en `recent_8k`, marcar:
- `new_8k_detected`
- `new_filing_types += ["8-K"]`

### 4. Cambio de status
Si cambia `status`, marcar:
- `status_change`

### 5. Compañía nueva en cobertura
Si aparece una compañía nueva en el registry actual y no en el anterior, marcar:
- `new_company_added`

---

## Diseño orientado a coste
Esto debe seguir siendo prácticamente determinista y muy barato.

No debería gastar LLM por defecto.

Su trabajo es:
- comparar estructuras
- resumir diferencias mecánicas
- preparar la siguiente capa

---

## Por qué esta pieza es importante
Sin delta detector, el sistema siempre enseña el estado actual, pero no sabe decir:
- qué cambió
- quién requiere atención
- qué merece pasar a la capa de análisis

Con delta detector, ya podemos priorizar.

---

## Relación con thesis_monitor
Secuencia correcta:
1. `positions.json`
2. `ticker_to_cik_resolution`
3. `filing_registry`
4. `delta_detector`
5. `structured_extractor` / actualización de datos
6. `thesis_monitor`

O, según el diseño final:
- filing delta primero
- data delta después
- thesis impact al final

---

## Recomendación práctica
El delta detector debe ser la última pieza de la fase 1.

Con él ya tendríamos:
- cobertura de posiciones
- detección de filings
- estado legible
- detección de cambios

Eso ya convierte el sistema en una capa real de mantenimiento.
