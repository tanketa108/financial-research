# Portfolio Reporting v0.1

Date: 2026-05-22
Owner: Charlie
Status: active baseline

## 1. Objective

Create a recurring portfolio reporting layer that turns company research, valuation artifacts, monitoring events and open tasks into a concise Portfolio Manager review pack.

The report must not make portfolio decisions. It should answer:

1. What is currently covered?
2. What changed since the last review?
3. Which theses/models need attention?
4. Which companies have material open questions?
5. What should the Portfolio Manager review next?

Operating rule:

> The system informs, structures, prioritizes and prepares. The user decides.

## 2. Report cadence

### v0.1 default

- **Weekly Review**: default recurring format.
- **Monthly Review**: same structure, with more emphasis on thesis/model changes and coverage evolution.
- **Ad hoc Review**: triggered after earnings, major news, model upload, Deep Dive completion or thesis review.

Daily monitoring remains separate as Daily Radar. The Portfolio Report is not a news feed.

## 3. Source of truth

The report consumes:

- `portfolio/company-registry.json`
- `portfolio/companies/<TICKER>.json`
- `portfolio/task-pipeline.json`
- latest Daily Radar files when relevant
- Deep Dive / model / thesis artifacts referenced in Company State `coverage`

Do not manually duplicate company facts in the report if the Company State should hold them.

## 4. Output location

Reports are stored in:

```text
financial-research/financial_system/portfolio/reports/YYYY-MM-DD-portfolio-review-v0.1.md
```

Optional future render targets:

```text
financial-research/docs/portfolio_reports/YYYY-MM-DD-portfolio-review-v0.1.html
financial-research/docs/portfolio_reports/YYYY-MM-DD-portfolio-review-v0.1.pdf
```

## 5. Report structure

### 5.1 Header

- Date
- Report type: weekly/monthly/ad hoc
- Universe reviewed
- Coverage snapshot
- Important caveat: no investment recommendation

### 5.2 Executive summary

Short bullets only:

- coverage state,
- material changes,
- top PM attention items,
- open task count,
- companies requiring model/thesis review.

### 5.3 Portfolio coverage dashboard

For each company:

- ticker,
- type,
- status,
- priority,
- reporting readiness,
- Deep Dive status,
- model status,
- thesis status,
- last update,
- next action.

Purpose: expose coverage quality and avoid false precision.

### 5.4 Company review blocks

Each company block should be compact and comparable:

```markdown
## TICKER — Company Name

Status: active / monitoring / research_pending / thesis_review_needed
Priority: high / medium / low
Reporting readiness: high / medium_high / medium / medium_low / low

Current thesis state:
- Status:
- Conviction:
- PM decision:
- Summary:

Key drivers:
- ...

Key risks:
- ...

Watch metrics:
- ...

Recent material events:
- ...

Research / model artifacts:
- Deep Dive:
- Model:
- Thesis:

Open questions:
- ...

Next action:
- ...
```

### 5.5 Open tasks and workflow

Summarize task pipeline:

- open tasks,
- stale tasks,
- recently closed tasks,
- suggested next actions.

Rules:

- Do not create tasks unless a clear action exists.
- Enrich existing tasks before creating new ones.
- Separate case-specific model work from structural system work.

### 5.6 Coverage gaps

Explicit list of missing pieces:

- no Deep Dive,
- no model,
- no explicit thesis,
- no company thread,
- stale Company State,
- missing next event date.

This section is important. It prevents the report from looking more complete than it is.

### 5.7 PM review queue

Prioritized review list:

1. urgent thesis/model review,
2. high-priority open tasks,
3. incomplete high-priority coverage,
4. medium-priority cleanup.

The report can recommend attention order, but not investment decisions.

## 6. Materiality rules

### High

Event or gap likely affects thesis, valuation, risk, position sizing discussion, or priority.

Examples:

- earnings/guidance miss or raise,
- major model assumption change,
- Deep Dive reveals thesis-level risk,
- regulatory/competitive event changes expected economics.

### Medium

Requires follow-up but not immediate thesis change.

Examples:

- model input needs review,
- new data point relevant to existing open question,
- post-Deep Dive valuation setup needed.

### Low

Useful context, not actionable yet.

### None

Noise. Do not include unless needed to explain why ignored.

## 7. Readiness interpretation

- **high**: Deep Dive + model/valuation artifact + thesis sufficiently documented.
- **medium_high**: Deep Dive complete; valuation/model or explicit thesis needs next pass.
- **medium**: research exists but model/thesis work still material.
- **medium_low**: preliminary coverage only.
- **low**: placeholder monitoring state; insufficient for meaningful portfolio reporting.

## 8. v0.1 company next-action policy

Default next actions:

- high readiness: monitor; review only if event/model assumption changes.
- medium_high: move to valuation/model assumptions if user wants deeper work.
- medium: close the open valuation/model gap before treating as fully covered.
- medium_low: decide whether to Deep Dive or keep preliminary.
- low: create thread/research only if still relevant to portfolio.

## 9. Validation checklist

Before calling a report complete:

- [ ] Registry loaded.
- [ ] Company States loaded.
- [ ] Task pipeline loaded.
- [ ] Coverage/readiness shown explicitly.
- [ ] Open tasks summarized.
- [ ] PM review queue included.
- [ ] No investment recommendation phrased as system decision.
- [ ] Report saved under expected path.
- [ ] Task ledger validation passes if task files changed.
- [ ] Dashboard/report index update considered separately, not silently assumed.

## 10. Known v0.1 limitations

- No automatic market data/prices yet.
- No benchmark/portfolio weights unless user supplies them.
- No automatic earnings calendar integration yet.
- No position sizing or buy/sell recommendations.
- No full PDF/HTML renderer required for first report.

These are intentional. v0.1 is an operating report, not a terminal portfolio analytics system.
