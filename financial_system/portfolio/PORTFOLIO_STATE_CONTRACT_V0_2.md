# Portfolio State Contract v0.2

Date: 2026-05-22
Owner: Charlie/Core
Status: active baseline

## 1. Purpose

Define the canonical state fields required for Portfolio Reporting, monitoring and PM review workflows.

This contract exists because v0.1 exposed a real issue: repo artifacts alone were not enough to infer portfolio status or priority. UBER was incorrectly treated as weak/urgent because its linked artifacts were incomplete, while the user clarified that the thesis is actually comparatively mature. AMZN was incorrectly treated as portfolio when it is an idea/watchlist.

Rule:

> Portfolio classification and PM priority must come from explicit state, not inference from artifact completeness.

## 2. Canonical files

Primary source of truth:

- `portfolio/company-registry.json`
- `portfolio/companies/<TICKER>.json`
- `portfolio/task-pipeline.json`
- `portfolio/output-registry.json`

Mirror path:

- `financial-research/financial_system/portfolio/*`

The mirror is a generated/synced operating copy, not the conceptual source of truth.

## 3. Registry contract

Each company in `portfolio/company-registry.json` must define:

- `ticker`
- `name`
- `type`: `portfolio | watchlist | idea | archived`
- `status`: `active | monitoring | research_pending | thesis_review_needed | archived`
- `priority`: `high | medium | low`
- `cik` or `null`
- `discordThreadId` or `null`
- `lastDeepDive` or `null`
- `lastUpdate` or `null`
- `nextKnownEvent` or `null`
- `sources`
- `notes`

### 3.1 Type semantics

- `portfolio`: current portfolio company.
- `watchlist`: not current portfolio, but actively followed.
- `idea`: earlier-stage candidate; may be promoted to watchlist/portfolio later.
- `archived`: no active reporting unless explicitly requested.

### 3.2 Priority semantics

Priority is not the same as artifact completeness.

- `high`: should be reviewed soon or has material open work.
- `medium`: relevant, but not urgent.
- `low`: keep in system, but do not crowd out higher-friction names.

Example from current state:

- UBER is `portfolio` but `low` priority because the user clarified the thesis is comparatively well developed.
- AMZN is `watchlist`/idea, not portfolio.

## 4. Company State v0.2 fields

Each `portfolio/companies/<TICKER>.json` must keep all v0.1 required fields and should now include:

```json
{
  "coverage": {},
  "coverageGaps": [],
  "nextReviewAction": {},
  "portfolioPosition": {},
  "reporting": {}
}
```

### 4.1 `coverage`

Purpose: summarize linked research/model/thesis artifacts.

Required shape:

```json
{
  "deepDive": {
    "status": "yes | no | no_preliminary_only | pending_valuation_step | not_in_repo_or_not_linked",
    "path": "string|null",
    "date": "YYYY-MM-DD|null"
  },
  "model": {
    "status": "yes | yes_needs_review | no | open_task | pending_valuation_step | exists_outside_repo_or_not_linked",
    "path": "string|null",
    "date": "YYYY-MM-DD|null",
    "taskId": "string|null"
  },
  "thesis": {
    "status": "yes | implicit_in_deep_dive | implicit_in_preliminary_and_model | preliminary | developed_but_not_fully_linked | placeholder",
    "path": "string|null"
  },
  "reportingReadiness": "high | medium_high | medium | medium_low | low | unknown"
}
```

### 4.2 `coverageGaps`

Purpose: make missing reporting inputs machine-readable.

Each gap:

```json
{
  "type": "deep_dive | model | thesis | thread | event_date | state_quality | portfolio_classification | other",
  "severity": "high | medium | low",
  "summary": "string",
  "recommendedAction": "string"
}
```

Rules:

- Gaps describe missing/incomplete system state, not investment weaknesses.
- A company can have no gaps if current state is good enough for reporting.
- Do not create fake gaps just because a company lacks a perfect output.

### 4.3 `nextReviewAction`

Purpose: one canonical next action for reporting and dashboard.

Shape:

```json
{
  "action": "string",
  "priority": "high | medium | low",
  "owner": "Portfolio Manager | Charlie | Scout | Extractor | Writer",
  "trigger": "string|null",
  "due": "YYYY-MM-DD|null",
  "status": "open | waiting | done | not_required"
}
```

Rules:

- One primary next action only.
- If multiple actions exist, pick the one that best reduces PM friction.
- Do not turn every gap into a task.

### 4.4 `portfolioPosition`

Purpose: optional portfolio analytics input. Never infer.

Shape:

```json
{
  "status": "in_portfolio | watchlist | idea | exited | unknown",
  "weight": null,
  "costBasis": null,
  "currentPrice": null,
  "currency": null,
  "asOf": null,
  "source": "user | broker | manual | unknown"
}
```

Rules:

- `weight`, `costBasis` and `currentPrice` stay `null` unless the user supplies or authorizes a source.
- The system may know a company is in portfolio without knowing size or price.

### 4.5 `reporting`

Purpose: reporting-specific metadata.

Shape:

```json
{
  "includeInPortfolioReview": true,
  "includeInWatchlistReview": false,
  "lastReviewedInReport": "YYYY-MM-DD|null",
  "lastMaterialChange": "YYYY-MM-DD|null",
  "notes": "string"
}
```

Rules:

- Portfolio companies default to `includeInPortfolioReview: true`.
- Watchlist/ideas can be included as separate section, not mixed with portfolio holdings.

## 5. Portfolio Review consumption rules

Portfolio Review v0.2 must consume:

1. registry classification,
2. Company State `coverage`,
3. Company State `coverageGaps`,
4. Company State `nextReviewAction`,
5. task pipeline open tasks,
6. output registry recent artifacts.

It must not infer:

- portfolio membership from a thread name,
- priority from missing artifacts alone,
- valuation/model maturity from filename count,
- portfolio weights/prices unless supplied.

## 6. Validation checklist

Before reporting completion:

- [ ] All registry companies have Company State files.
- [ ] All Company States include `coverage`.
- [ ] All Company States include `coverageGaps`.
- [ ] All Company States include `nextReviewAction`.
- [ ] All Company States include `portfolioPosition`.
- [ ] All Company States include `reporting`.
- [ ] Registry type/priority reflects explicit user clarification when available.
- [ ] Mirror synced.
- [ ] Task ledger, event ledger and output registry validators pass.

## 7. Current baseline classification

As of 2026-05-22 after user correction:

Portfolio:

- MSFT
- UBER
- RACE
- NVO
- NFLX
- DVN
- LVMH
- EOG

Watchlist / idea:

- AMZN

Current priority interpretation:

- High: MSFT, NFLX, NVO, DVN
- Medium: RACE, LVMH, EOG, AMZN as idea/watchlist
- Low: UBER, because thesis is comparatively better worked and should not crowd out less-modeled names
