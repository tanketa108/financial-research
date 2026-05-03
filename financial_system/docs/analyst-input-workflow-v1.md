# Analyst Input Workflow v1

## Objetivo
Dar una interfaz limpia para que el analista aporte juicio sin mezclarlo con trabajo mecánico ya automatizado.

---

## Principio
El sistema prepara contexto, datos base, huecos y guardrails.
El analista solo rellena:
- tesis
- postura
- qué importa
- supuestos estructurales
- escenarios
- qué invalidaría la idea

---

## Artefactos
Por ticker, v1 usa tres piezas:

1. `*-valuation-state-v1.json`
   - estado estructurado completo
   - vive el prefill del sistema

2. `*-analyst-input-v1.json`
   - capa corta y deliberada de juicio del analista
   - debe ser editable sin pelearse con JSON enorme

3. `*-valuation-display-v1.md`
   - vista legible combinada

---

## Flujo operativo

### Paso 1. System prefill
Charlie rellena automáticamente:
- base histórica
- update context
- debt / cash conversion base
- quality base
- normalization guardrails

### Paso 2. Analyst input
Ander rellena solo los campos de juicio.

### Paso 3. Merge
Un loader aplica `*-analyst-input-v1.json` sobre el `valuation-state`.

### Paso 4. Render
Se regeneran display y dashboard.

---

## Qué debe entrar en analyst input

### A. Thesis
- thesis_short
- current_stance
- what_would_change_my_mind

### B. Segment interpretation
- segmentos que importan de verdad
- lectura de crecimiento
- lectura de márgenes
- notas

### C. Core drivers / assumptions
- drivers clave
- margen consolidado o por segmento
- lectura de reinversión / operating leverage
- supuestos estructurales

### D. Scenarios
- escenario central
- escenarios alternativos
- implicaciones de negocio
- implicaciones de valoración

### E. Risks / catalysts
- riesgos clave
- catalysts / signposts

### F. Valuation assumptions
- discount rate / WACC base
- terminal growth
- exit multiple logic
- notas de weighting o central reference

---

## Qué NO debe entrar aquí
No meter en analyst input cosas que ya automatizamos razonablemente:
- latest filing metadata
- latest reported metrics
- debt / cash base
- series históricas
- flags de normalización

---

## Design rule
Si un campo cambia porque salió un nuevo filing, debe vivir en system prefill.
Si un campo cambia porque cambió tu forma de pensar, debe vivir en analyst input.

---

## v1 Recommendation
El analyst input debe ser:
- corto
- explícito
- fácil de revisar
- suficientemente estructurado para mergearse sin fricción

Nada de documentos gigantes si no hace falta.
