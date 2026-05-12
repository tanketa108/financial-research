# Dashboard Maintenance Inputs v0

## Objective

Make the dashboard the visible reflection of the investment thesis system.

The dashboard should not be a separate manual UI. It should be rendered from accepted, structured thesis state.

## Principle

Discord is the operating conversation layer. The repository is the structured memory layer. The dashboard is the executive snapshot.

Therefore, a dashboard update should only happen after the relevant input has been converted into accepted structured state.

## Inputs required per company

### 1. Company thesis state

Path:

```text
financial_system/companies/<TICKER>/company-thesis-state-v0.json
```

Purpose:

- qualitative thesis baseline,
- drivers,
- risks,
- catalysts,
- assumptions,
- open questions,
- latest accepted updates,
- next action,
- qualitative maintenance status.

This is the main input for qualitative dashboard maintenance.

### 2. Dashboard aggregate state

Path:

```text
financial_system/registry/dashboard_state.json
```

Purpose:

- portfolio-level status,
- filing/data delta flags,
- valuation summary,
- current thesis short,
- key risks/catalysts,
- key metrics.

This should remain compact and dashboard-oriented.

### 3. Valuation state

Path:

```text
financial_system/valuations/<TICKER>-valuation-state-v1.json
```

Purpose:

- numerical financial base,
- valuation range/reference,
- balance sheet,
- cash conversion,
- quantitative quality flags.

For the user's workflow, Excel remains the source of deep quantitative analysis. This file should receive only reviewed/selected outputs from the Excel model.

### 4. Thesis monitor state

Paths:

```text
financial_system/registry/thesis_monitor_input.json
financial_system/registry/thesis_monitor_output.json
```

Purpose:

- decide whether a company needs review,
- explain why,
- track priority after filings/data changes.

### 5. Source register and change log

Paths:

```text
financial_system/companies/<TICKER>/source-register.md
financial_system/companies/<TICKER>/change-log.md
```

Purpose:

- record source materials,
- record accepted thesis changes,
- preserve auditability.

## Dashboard maintenance workflow

For each new company update:

1. Register uploaded/source materials.
2. Extract facts with source/date.
3. Separate facts, inferences and opinion.
4. Propose thesis diff.
5. Review/accept changes.
6. Update company thesis state.
7. Update compact dashboard aggregate state.
8. Rebuild dashboard HTML.

## UBER pilot fields now required

For UBER, the dashboard should reflect:

- thesis framing: demand aggregation / local network coordination platform,
- core drivers: Mobility, Delivery, Uber One, ads/AV optionality,
- risks: regulation/labor, competition, Delivery economics, complexity, valuation, AV disintermediation,
- catalysts: Uber One evidence, Delivery margin, Mobility monetization, ads scale, AV partnerships,
- open questions: Mobility revenue weakness, Delivery structural quality, Uber One incrementality, Q1 2026 normalization, valuation scenarios,
- next action: turn user materials into accepted baseline dashboard state.

## Acceptance criteria

The dashboard is considered maintained when:

- company page shows the accepted qualitative thesis state,
- portfolio index reflects correct status and priority,
- risks/catalysts/open questions are current,
- latest source/update is recorded,
- dashboard build passes checks.
