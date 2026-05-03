# Extractor Selection Lessons

## Lesson 1
`companyfacts` cannot be treated as a simple "pick latest row" source.

Different metrics can expose:
- different frames
- different filing dates
- older rows that still sort oddly
- period representations that do not line up cleanly just by `end`

## Practical rule
Metric selection should prioritize, in this order:
1. target form (`10-Q` / `10-K`)
2. target filing date from filing registry
3. target report date when available
4. only then latest fallback

## Why this matters
Without alignment to the filing registry, the extractor can silently mix periods across metrics.

That would be dangerous for:
- comparability
- deltas
- thesis monitoring

## Current implication
Do not aggregate multi-company extracted data until period alignment is validated for each issuer class.
