# Company Thesis Workflow v0

## Objective

Define the first operating contract for maintaining portfolio company theses in the financial research system.

The pilot company is **UBER** because it is the most developed thesis and can be used to calibrate quality against the user's existing understanding.

## Product direction

The system is not intended to replace the user's quantitative Excel model.

Separation of responsibilities:

- **Quantitative work:** primarily maintained by the user in Excel and uploaded/shared with the system when relevant.
- **Qualitative thesis maintenance:** owned by the financial research system: earnings presentations, press releases, filings, narrative changes, drivers, risks, catalysts, management commentary, and thesis evolution.

## Core principle

Qualitative updates must be traceable, auditable, and conservative.

No agent should silently rewrite the final thesis. Material changes require evidence, explicit reasoning, and review.

## Storage model

### Discord

Discord is the operating conversation layer.

Recommended structure:

- `#financial-project`: project coordination, architecture, decisions.
- `#portfolio`: portfolio thesis workspace.
- One thread per company, starting with `UBER`.

The company thread is used for:

- uploading thesis documents,
- uploading Excel valuation files,
- discussing company-specific updates,
- recording user comments,
- triggering thesis maintenance workflows,
- asking follow-up questions.

### Repository

The repo is the structured memory and audit layer.

Recommended paths:

```text
financial_system/companies/<TICKER>/company-thesis-state-v0.json
financial_system/companies/<TICKER>/source-register.md
financial_system/companies/<TICKER>/change-log.md
financial_system/workflows/update-thesis-from-results-v0.md
```

The dashboard should be rendered from structured state, not directly from conversation history.

## Company thesis state

Each company should have a structured state with these sections:

- identity
- thesis_snapshot
- qualitative_drivers
- risks
- catalysts
- assumptions
- open_questions
- source_register
- latest_updates
- dashboard_fields
- review_status

## Workflow: update thesis from new results

Input:

- company ticker,
- current thesis state,
- new source document(s), e.g. earnings presentation, press release, 10-Q/10-K, transcript,
- optional user notes,
- optional Excel/model summary.

Output:

- factual summary,
- extracted relevant data points,
- qualitative changes,
- impact on thesis,
- risks/catalysts affected,
- proposed dashboard changes,
- open questions,
- source references,
- confidence level.

## Agent architecture

Use reusable functional analysts, not permanent per-company analysts.

Avoid:

```text
UBER analyst
MSFT analyst
NFLX analyst
...
```

Prefer:

```text
filing-results-analyst + UBER context
financial-analyst + UBER context
thesis-analyst + UBER context
report-editor + UBER context
```

## Model routing

Use a hybrid model strategy.

### Local/Ollama candidates

Good for high-volume, lower-risk operations:

- preliminary document summaries,
- extraction of candidate facts,
- classification of news/documents,
- first-pass bullet generation,
- duplicate detection,
- source indexing.

### Strong LLM candidates

Required for high-judgment operations:

- thesis impact assessment,
- assumption review,
- contradiction detection,
- materiality judgment,
- final synthesis,
- dashboard update decisions.

Rule of thumb:

> Local for digestion. Strong model for judgment. Charlie for final decision.

## Anti-hallucination controls

Mandatory controls:

1. Every factual figure needs source and date.
2. Separate facts, inferences, and opinion.
3. No source means no factual claim.
4. Assumptions must live in structured state.
5. Material changes require a diff: previous view, new view, evidence, confidence.
6. Agents propose changes; Charlie/review step accepts them.
7. Dashboard reflects accepted state only.

## Acceptance criteria for UBER pilot

The pilot is usable when:

- UBER has an initial structured thesis state.
- User-provided documents can be registered as sources.
- A new results document can produce a structured update proposal.
- The proposal separates facts/inferences/opinion.
- Material changes include evidence and confidence.
- Accepted changes can be reflected in the dashboard state.

## Next implementation steps

1. Create initial UBER thesis state skeleton.
2. Create UBER source register and change log.
3. Define the update workflow document.
4. Add a lightweight ingestion convention for user-uploaded files.
5. After user uploads UBER materials, populate the initial thesis state.
