# DVN readiness — next steps

## Current status
DVN (Devon Energy Corporation) has been incorporated as an active Layer 2 bootstrap case based on the analyst model already provided.

It is now considered:
- a real portfolio name
- worth follow-up
- not yet fully covered in deterministic Layer 1 monitoring

## What already exists
- `valuations/DVN-valuation-state-v1.json`
- `valuations/extracted/DVN-model-signals.json`
- `valuations/extracted/DVN-model-signals-summary.md`
- dashboard entry with `external_model_bootstrap` status

## What is missing for fuller readiness
### Layer 2 readiness
- review current DVN valuation state for usability
- decide if more explicit thesis fields are needed
- decide whether to generate a Delhi-backed packet for DVN using available model-bootstrap context

### Layer 1 readiness
- verify CIK / SEC identity path
- add DVN to filing registry coverage if justified
- add data extraction / delta coverage if justified
- bring DVN into thesis monitor flow if promoted to full covered name

## Recommended near-term approach
1. Keep DVN active in Layer 2 now.
2. Do not force full Layer 1 integration immediately if it slows more important names.
3. Promote DVN to fuller coverage when follow-up value is high enough.

## Success condition
DVN should be in one of two explicit states, not in ambiguity:
- `tracked_layer2_bootstrap`
- or `fully_covered_name`
