# Delhi + Financial Phase 2 Status v1

_Last updated: 2026-05-03_

## Objective
Exploit Delhi as a cheap first-pass worker inside Financial System Phase 2 before opening new fronts.

## Implemented pieces
### Delhi core
- `delhi_v0/delhi_worker.py`
- local Ollama-backed worker interface
- tasks:
  - `summarize_change`
  - `classify_materiality`
  - `draft_note`
  - `extract_points`

### Financial wrappers
- `delhi_v0/financial_ingest.py`
- `delhi_v0/financial_pipeline.py`

### Financial tasks already working
- `filing_summary`
- `filing_materiality`
- `filing_draft_note`
- `data_delta_summary`

## Guardrails added
- stricter prompts to reduce overclaiming
- mandatory `escalate=true` for materiality `media` or `alta`
- grounding via `entity` + `company_name`
- lightweight post-validation for entity drift warnings
- pipeline-level guardrails with aggregated `grounding_warnings`

## Pipeline v1
Current chained first-pass for one entity:
1. `filing_summary`
2. `filing_materiality`
3. `filing_draft_note`

Outputs include:
- compact review focus
- materiality first-pass
- escalation signal
- draft note for Charlie review

## Artifact routing now covered
### filing deltas
- summary
- materiality

### thesis monitor input
- draft note

### data deltas
- compact summary

## Current quality assessment
### What already works well
- architecture is real, not conceptual
- local cheap worker is reusable
- financial artifacts can be routed through Delhi consistently
- Charlie can stay above the monkey job layer

### Main weaknesses still present
- model can still sound too confident
- some outputs are generic unless tightly constrained
- notes/drafts still need Charlie review
- more post-validation would help on numerical/semantic consistency

## Recommended next steps
1. add a compact `phase2_review_packet` builder that combines:
   - filing summary
   - materiality
   - draft note
   - data delta summary (if changed)
2. add lightweight consistency checks for:
   - suspicious metric commentary
   - missing mention of key changed metrics
   - empty/weak next steps
3. optionally route thesis-monitor draft generation through Delhi before Charlie review
4. keep Knowledge Project on hold until Phase 2 feels sufficiently advanced

## Practical conclusion
Delhi is now a usable first-pass worker inside Financial System Phase 2.
It is not final judgment, but it already removes a meaningful amount of repetitive reading/summarization work.
