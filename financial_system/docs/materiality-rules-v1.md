# Materiality Rules v1

## Objetivo
Definir reglas simples y deterministas para decidir si un cambio en datos financieros merece atención.

Estas reglas no sustituyen juicio inversor.
Solo priorizan qué debería subir de nivel en el sistema.

---

## Filosofía
Primero reglas claras y baratas.
Después, si hace falta, análisis más profundo.

La lógica no es:
- "¿es importante en absoluto?"

La lógica es:
- "¿merece revisión humana o una capa superior del sistema?"

---

## Niveles sugeridos
- `ignore`
- `review`
- `investigate`
- `high_priority`

---

## Reglas v1 por métrica

### revenue
- abs(delta_pct) < 3% → `ignore`
- 3% <= abs(delta_pct) < 7% → `review`
- 7% <= abs(delta_pct) < 12% → `investigate`
- abs(delta_pct) >= 12% → `high_priority`

### operating_income
- abs(delta_pct) < 5% → `ignore`
- 5% <= abs(delta_pct) < 10% → `review`
- 10% <= abs(delta_pct) < 20% → `investigate`
- abs(delta_pct) >= 20% → `high_priority`

### net_income
- abs(delta_pct) < 5% → `ignore`
- 5% <= abs(delta_pct) < 15% → `review`
- 15% <= abs(delta_pct) < 25% → `investigate`
- abs(delta_pct) >= 25% → `high_priority`

### diluted_eps
- abs(delta_pct) < 5% → `ignore`
- 5% <= abs(delta_pct) < 15% → `review`
- 15% <= abs(delta_pct) < 25% → `investigate`
- abs(delta_pct) >= 25% → `high_priority`

### cash_and_equivalents
- abs(delta_pct) < 10% → `ignore`
- 10% <= abs(delta_pct) < 20% → `review`
- 20% <= abs(delta_pct) < 35% → `investigate`
- abs(delta_pct) >= 35% → `high_priority`

### total_debt
- abs(delta_pct) < 8% → `ignore`
- 8% <= abs(delta_pct) < 15% → `review`
- 15% <= abs(delta_pct) < 25% → `investigate`
- abs(delta_pct) >= 25% → `high_priority`

---

## Reglas cualitativas mínimas
Independientemente del porcentaje:

### Siempre al menos `review`
- status change en extracción
- métrica desaparece
- métrica aparece tras estar ausente
- cambio de cobertura

### Siempre `investigate`
- varias métricas core cambian fuerte en la misma actualización
- revenue y operating income divergen mucho en dirección
- cash cae fuerte mientras debt sube fuerte

---

## Limitaciones
Estas reglas son genéricas.
No están adaptadas todavía a:
- business model
- estacionalidad
- guidance framework
- calidad del negocio
- tesis concreta

Eso se resolverá en la capa de thesis monitor.

---

## Uso correcto
1. detectar data deltas
2. pasar cada cambio por estas reglas
3. asignar prioridad preliminar
4. solo después decidir si se necesita análisis más caro
