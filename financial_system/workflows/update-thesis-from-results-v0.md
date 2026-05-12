# Workflow: Update Thesis From Results v0

## Purpose

Maintain a company thesis after new earnings-related information appears.

This workflow is qualitative-first. Quantitative valuation remains primarily in the user's Excel model unless the user provides a summary or uploaded model.

## Trigger examples

- New earnings press release.
- New investor presentation.
- New 10-Q / 10-K / 8-K.
- New earnings call transcript.
- User uploads a revised thesis or Excel model.
- User asks: "actualiza la tesis de UBER con estos resultados".

## Inputs

Required:

- `ticker`
- current company thesis state
- one or more source documents or links

Optional:

- user notes
- Excel/model file
- prior agent conversation export
- specific questions from the user

## Steps

### 1. Register sources

For each document, record:

- source id
- title
- type
- date
- upload/link location
- reliability
- notes

### 2. Extract facts

Extract only verifiable claims.

Each fact must include:

- claim
- source id
- date
- location/page/section if available
- confidence

### 3. Identify qualitative changes

Classify changes into:

- business momentum
- segment performance
- margin/efficiency
- market structure
- competition
- regulation/legal
- management commentary
- capital allocation
- guidance/outlook

### 4. Map to thesis

For every relevant change, decide whether it:

- supports existing thesis,
- weakens existing thesis,
- is neutral,
- creates a new open question,
- requires user review.

### 5. Produce thesis diff

For material changes, output:

- previous view
- new evidence
- proposed updated view
- affected drivers/risks/catalysts
- confidence
- whether dashboard update is recommended

### 6. Review gate

No direct write to final thesis without review.

Review options:

- accept
- reject
- revise
- ask user

### 7. Update accepted state

If accepted, update:

- company thesis state
- source register
- change log
- dashboard fields if relevant

## Output contract

```json
{
  "ticker": "UBER",
  "workflow": "update-thesis-from-results-v0",
  "status": "proposed",
  "sources": [],
  "facts": [],
  "qualitative_changes": [],
  "thesis_diff": [],
  "dashboard_update_proposal": {},
  "open_questions": [],
  "review_required": true
}
```
