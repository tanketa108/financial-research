# External Source Methodology v0

## Purpose

Use selected free external sources as monitoring and display leverage for the dashboard and thesis maintenance workflow.

## StockTitan role

StockTitan is approved as a **secondary monitoring input** and external display link.

Useful for:

- quick financial health overview,
- financial metric summaries,
- news monitoring,
- preliminary alerts,
- display inspiration,
- identifying items for the maintenance queue.

Not sufficient for:

- final accepted financial figures,
- material thesis changes without verification,
- valuation assumptions,
- primary evidence for investment conclusions.

## Workflow

1. Link StockTitan Financials and News on the company dashboard.
2. Periodically fetch StockTitan news/financial page.
3. Classify items by thesis relevance: low / medium / high.
4. Add relevant items to `maintenance_queue`.
5. Verify material items against primary sources:
   - SEC filings,
   - company investor relations,
   - press releases,
   - earnings transcripts,
   - user-provided Excel/model/materials.
6. Only accepted/verified changes update thesis state or dashboard conclusions.

## Guardrail

StockTitan can trigger investigation. It should not directly rewrite the thesis.
