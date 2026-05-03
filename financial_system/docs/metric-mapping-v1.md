# Metric Mapping v1

## Objetivo
Crear una capa reutilizable entre:
- tags SEC/XBRL específicos
- métricas canónicas del sistema

La idea es que el extractor no dependa de un único tag duro por métrica.

---

## Principio
Cada métrica canónica puede tener:
- un nombre interno estable
- varios tags candidatos
- una unidad esperada
- reglas mínimas de selección

Eso permite:
- soportar diferencias entre emisores
- soportar ausencia de tags concretos
- mantener comparabilidad sin rigidez absurda

---

## Métricas canónicas v1

### revenue
- **canonical_name:** `revenue`
- **expected_unit:** `USD`
- **candidate_tags:**
  - `RevenueFromContractWithCustomerExcludingAssessedTax`
  - `SalesRevenueNet`
  - `Revenues`

### operating_income
- **canonical_name:** `operating_income`
- **expected_unit:** `USD`
- **candidate_tags:**
  - `OperatingIncomeLoss`

### net_income
- **canonical_name:** `net_income`
- **expected_unit:** `USD`
- **candidate_tags:**
  - `NetIncomeLoss`
  - `ProfitLoss`

### diluted_eps
- **canonical_name:** `diluted_eps`
- **expected_unit:** `USD/share`
- **candidate_tags:**
  - `EarningsPerShareDiluted`

### cash_and_equivalents
- **canonical_name:** `cash_and_equivalents`
- **expected_unit:** `USD`
- **candidate_tags:**
  - `CashAndCashEquivalentsAtCarryingValue`

### total_debt
- **canonical_name:** `total_debt`
- **expected_unit:** `USD`
- **candidate_tags:**
  - `LongTermDebtAndFinanceLeaseObligations`
  - `LongTermDebtNoncurrent`
  - `LongTermDebt`
  - `DebtInstrumentFaceAmount`
  - `LongTermDebtFairValue`
- **note:** likely needs issuer-specific fallback logic later

---

## Selection rules v1
For each canonical metric:

1. Iterate candidate tags in order
2. Skip tags not present
3. Prefer records with:
   - desired form (`10-Q` or `10-K`)
   - latest `filed` date
   - matching target reporting period when possible
4. Return first robust candidate
5. If none found, emit explicit gap

---

## Output shape recommendation
For each canonical metric, extractor should return:

```json
{
  "value": 123,
  "unit": "USD",
  "tag": "NetIncomeLoss",
  "filed": "2026-04-29",
  "end": "2026-03-31",
  "frame": "CY2026Q1I",
  "status": "ok"
}
```

If not found:

```json
{
  "value": null,
  "unit": "USD",
  "tag": null,
  "filed": null,
  "end": null,
  "frame": null,
  "status": "not_found"
}
```

---

## Why this matters
Without this layer, extractor logic becomes:
- brittle
- issuer-specific too early
- hard to scale

With this layer, we keep:
- canonical internal names
- flexible XBRL resolution
- explicit gaps instead of fake precision

---

## Next step
Turn this mapping into a machine-readable file, e.g.:
- `financial_system/config/metric_mapping_v1.json`

Then build:
- `extract_financial_metrics.py`

That would be the first reusable implementation of the structured extractor.
