# Structured Extractor v1

## Objetivo
Pasar de detectar que existe un filing nuevo a extraer de ese filing un conjunto pequeño, consistente y útil de datos estructurados.

La pregunta que responde esta pieza es:

> ¿Qué información concreta ha salido y cómo la guardamos de forma comparable?

---

## Principio
Esta capa no intenta resumir todo el filing.

Hace una cosa más útil y robusta:
- extraer un set limitado de campos
- guardarlos con un contrato estable
- dejar preparado el terreno para comparar periodos y evaluar tesis

---

## Prioridad de fuentes
Orden recomendado:

1. **submissions / endpoints estructurados SEC**
2. **companyfacts / XBRL facts**
3. **filing HTML bruto**, solo si hace falta
4. **LLM**, solo como capa de apoyo en casos ambiguos

---

## Alcance v1
Empezaría solo con compañías domésticas US y con un set muy pequeño de métricas.

### Campos iniciales recomendados
#### Income statement / growth
- revenue
- operating_income
- net_income
- diluted_eps

#### Cash / balance sheet
- free_cash_flow *(si está fácil; si no, más tarde)*
- cash_and_equivalents
- total_debt

#### Shareholder / capital allocation
- share_count_diluted *(si está disponible de forma limpia)*
- buybacks *(si es extraíble con bajo riesgo)*

#### Metadata
- ticker
- cik
- form_type
- accession_number
- filing_date
- report_date
- fiscal_period
- fiscal_year
- source_url

---

## Qué no metería en v1
- segment reporting complejo
- guidance cualitativa libre
- KPIs muy company-specific
- management commentary larga
- extracción semántica abierta con LLM por defecto

Eso vendrá después.

---

## Output esperado
### `extracted_financials.json`
Ejemplo conceptual:

```json
{
  "MSFT": {
    "latest_10q": {
      "accession_number": "0001193125-26-191507",
      "filing_date": "2026-04-29",
      "report_date": "2026-03-31",
      "fiscal_period": "Q3",
      "fiscal_year": 2026,
      "metrics": {
        "revenue": {
          "value": 61800000000,
          "unit": "USD"
        },
        "operating_income": {
          "value": 27500000000,
          "unit": "USD"
        },
        "net_income": {
          "value": 21900000000,
          "unit": "USD"
        },
        "diluted_eps": {
          "value": 2.95,
          "unit": "USD/share"
        }
      }
    }
  }
}
```

---

## Estrategia de implementación

### Paso 1
Construir un mapeo simple:
- ticker
- form principal a extraer (`latest_10q` o `latest_10k`)
- url / accession

### Paso 2
Tirar primero de `companyfacts` para métricas comparables.

### Paso 3
Normalizar salida a un contrato estable.

### Paso 4
Marcar gaps explícitamente cuando un campo no se puede resolver de forma fiable.

---

## Filosofía de calidad
Prefiero:
- 6 métricas bien extraídas

antes que:
- 40 métricas medio rotas

La prioridad es:
- comparabilidad
- robustez
- trazabilidad
- bajo coste

---

## Relación con thesis_monitor
Secuencia correcta:
1. filing detection
2. filing delta
3. structured extractor
4. data delta
5. thesis monitor

El thesis monitor no debería leer filings crudos si puede evitarlo.
Debería leer datos ya estructurados y, solo cuando haga falta, volver al filing original.

---

## Recomendación práctica
Empezar con un solo caso de control:
- **MSFT** o **UBER**

Y demostrar que podemos sacar 4-6 métricas limpias con contrato estable.

Una vez funcione con un nombre, escalar a los demás.
