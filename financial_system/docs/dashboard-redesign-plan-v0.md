# Dashboard Redesign Plan v0

## Context

The current dashboard contains valuable work, especially the company-level investment terminal pages, but the visible layer is too fragile and has become cluttered. The next phase should redesign the dashboard deliberately, not by incremental accidental mutations.

This plan is for branch `dashboard-redesign-v0`. Do not merge to `main` until reviewed.

## Non-negotiables

1. Do not overwrite the existing dashboard on `main` without explicit approval.
2. Keep company content and prior work recoverable.
3. Separate data contracts from presentation.
4. Preview before publishing.
5. Make small, reviewable commits.

## Product objective

The dashboard should be the executive reflection of the investment thesis system.

It should answer quickly:

- What do I own / track?
- What is the current thesis?
- What changed recently?
- What needs attention?
- What are the key drivers, risks and catalysts?
- What does the quantitative model say?
- What source supports each material claim?

## Recommended information architecture

### Portfolio homepage

Purpose: control tower.

Recommended blocks:

1. Portfolio summary
   - companies covered
   - review needed
   - stale theses
   - high priority updates

2. Attention queue
   - companies requiring action
   - reason for review
   - next action

3. Portfolio table
   - ticker
   - thesis status
   - valuation status
   - last update
   - priority
   - next action

4. Recent thesis changes
   - accepted changes only
   - date/source

### Company page

Purpose: single-company thesis cockpit.

Recommended block order:

1. Header / status rail
   - ticker
   - company name
   - thesis status
   - last updated
   - review priority
   - valuation status

2. Thesis snapshot
   - one-line thesis
   - current stance
   - conviction / underwriting status
   - what would change the thesis

3. Update / maintenance panel
   - latest source reviewed
   - what changed
   - open review items
   - next action

4. Qualitative thesis
   - key drivers
   - risks
   - catalysts
   - assumptions
   - open questions

5. Quantitative / valuation panel
   - fair value / range
   - market price
   - upside/downside
   - model source
   - sensitivity highlights
   - caveats

6. Financials / operating data
   - keep existing valuable charts/tables, but reduce noise and improve hierarchy

7. Sources / provenance
   - source register
   - data freshness
   - confidence / missing evidence

## Data contract direction

The dashboard should eventually consume:

```text
financial_system/dashboard_inputs/<TICKER>-dashboard-input-v0.json
```

This file should be generated from:

- `financial_system/companies/<TICKER>/company-thesis-state-v0.json`
- valuation state
- thesis monitor output
- source register
- dashboard aggregate state

But the first redesign can still be static/HTML if that is faster. The key is to define the destination contract now.

## First implementation target: UBER

Start with UBER only.

Why:

- strongest thesis baseline,
- user has the most context,
- existing dashboard already has useful valuation/financial blocks,
- best case to define the canonical company-page pattern.

## Proposed safe workflow

1. Build a preview page only:

```text
docs/preview/UBER-dashboard-v2.html
```

2. Do not alter:

```text
docs/companies/UBER.html
```

until preview is approved.

3. Iterate visually and structurally on the preview.
4. Once approved, replace the live company page.
5. Then generalize to other companies.

## Immediate next steps

1. Create `financial_system/dashboard_inputs/UBER-dashboard-input-v0.json`.
2. Create a preview HTML page `docs/preview/UBER-dashboard-v2.html`.
3. Preserve the strongest existing sections:
   - Quant Workspace
   - financial health
   - valuation workspace
   - normalization layer
4. Reorganize them under a cleaner thesis-first layout.
5. Ask user to review preview before changing live dashboard.
