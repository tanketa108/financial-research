# Quality / Coverage Status v1

## Objetivo
Tener una vista explícita de:
- qué nombres están cubiertos
- qué nombres siguen pendientes
- qué calidad tiene la extracción actual

Esto evita falsa sensación de completitud.

---

## Estados de cobertura

### `covered`
La compañía tiene:
- CIK resuelto
- filing registry operativo
- extracted financials disponibles
- data delta disponible

### `partial`
La compañía tiene parte del pipeline, pero no todo.
Ejemplos:
- CIK resuelto pero sin extracted data
- filings disponibles pero extractor no validado

### `pending_identity_resolution`
No hay CIK/path resuelto todavía.

### `pending_issuer_strategy`
Sabemos que el nombre es relevante, pero necesita estrategia distinta por tipo de emisor.
Ejemplo:
- foreign issuer
- ADR

---

## Estados de calidad de extracción

### `validated`
La extracción ya fue probada y el periodo está alineado correctamente con el filing objetivo.

### `usable_with_caution`
La extracción funciona, pero hay algún matiz no completamente generalizado todavía.

### `not_validated`
Existe output, pero aún no se ha revisado de forma suficiente.

### `blocked`
No se puede considerar usable todavía.

---

## Estado actual del sample

### UBER
- coverage: `covered`
- extraction_quality: `validated`
- notes:
  - revenue required fallback to alternate tag (`Revenues`)
  - period alignment logic was tested on this case

### MSFT
- coverage: `covered`
- extraction_quality: `validated`
- notes:
  - strong fit for domestic issuer structured extraction

### NFLX
- coverage: `covered`
- extraction_quality: `validated`
- notes:
  - clean extraction on first pass after generalized selector improvements

### RACE
- coverage: `pending_identity_resolution`
- extraction_quality: `blocked`
- notes:
  - SEC path / CIK still unresolved in current pipeline

### NVO
- coverage: `pending_issuer_strategy`
- extraction_quality: `blocked`
- notes:
  - foreign issuer / ADR path likely needs distinct treatment

---

## Recomendación práctica
Toda salida futura debería incluir una mini-sección de cobertura/calidad.

Eso ayuda a distinguir entre:
- ausencia de cambio
- ausencia de cobertura
- dato incompleto
