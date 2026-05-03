# MSFT Pilot Findings

## Result
The pilot looks promising.

Using SEC `companyfacts`, we were able to retrieve a clean first-pass set of structured metrics for Microsoft.

## Metrics that appear cleanly extractable
- revenue
- operating_income
- net_income
- diluted_eps
- cash_and_equivalents

## Metric that needs extra mapping work
- total_debt

The first candidate tag (`LongTermDebtAndFinanceLeaseObligations`) was not present in the first pass.
This suggests we need:
- alternate tag mapping
- or fallback logic for debt-related fields

## Practical takeaway
The structured extractor approach looks valid for domestic issuers if we:
- keep the metric set initially small
- support tag aliasing
- explicitly allow gaps when a field is not robustly found

## Recommended next move
Build a generic metric-mapping layer with:
- canonical metric name
- preferred tags list
- unit expectations
- selection rules for latest valid period

That would turn this pilot into the first reusable extractor.
