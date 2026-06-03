# NVO — Valuation Model Scaffold v0.1

Date: 2026-05-26  
Task: `TASK-2026-05-26-001`  
Status: scaffold only — **not** a fair value, target price or investment recommendation  
Currency: DKK unless explicitly stated

## 1. Purpose

Convert the completed NVO Deep Dive and valuation input sheet into a model-ready DCF/scenario scaffold. This output deliberately keeps PM judgement fields explicit instead of hardcoding a portfolio decision.

## 2. Source-backed anchors

- `fy2025SalesDkkBn`: 309.064
- `fy2025OperatingProfitDkkBn`: 127.658
- `fy2025NetProfitDkkBn`: 102.434
- `fy2025GrossMarginPct`: 81.0
- `fy2025FcfDkkBn`: 28.3
- `fy2026FcfGuideDkkBn`: [36, 46]
- `fy2026CapexGuideDkkBn`: 55
- `q1_2026AdjustedOperatingMarginPct`: 46.9

## 3. Scenario defaults for first model pass

### Downside
- 2026 sales growth CER: -12%
- 2027-2030 sales CAGR: 3%
- Normalized operating margin: 39%
- Gross margin: 79%
- Oral Wegovy incrementality: 25%
- Capex normalization: slow
- Terminal growth placeholder: 1.5%
- Note: Reset persists; Lilly/pricing pressure stays severe; capex remains elevated.

### Base
- 2026 sales growth CER: -8%
- 2027-2030 sales CAGR: 7%
- Normalized operating margin: 42.5%
- Gross margin: 81%
- Oral Wegovy incrementality: 50%
- Capex normalization: gradual
- Terminal growth placeholder: 2.0%
- Note: Company midpoint reset, partial growth normalization, margins recover but not to 2024 peak.

### Upside
- 2026 sales growth CER: -4%
- 2027-2030 sales CAGR: 10.5%
- Normalized operating margin: 45.5%
- Gross margin: 83%
- Oral Wegovy incrementality: 70%
- Capex normalization: faster
- Terminal growth placeholder: 2.5%
- Note: Oral Wegovy expands TAM, share stabilizes, price reset mostly absorbed, capex normalizes.

## 4. Model blocks

- Revenue bridge: 2025 sales × 2026 reset × 2027-2030 CAGR
- Operating profit: sales × normalized operating margin
- FCF bridge: NOPAT + D&A - capex - working capital / or FCF margin proxy
- DCF: explicit FCF 2026-2030 + terminal value discounted by PM-selected WACC
- Sensitivity matrix: revenue CAGR × normalized margin; secondary capex/FCF conversion toggle

## 5. Required PM override fields

- 2026 guidance point within -4% to -12% CER
- 2027-2030 sales CAGR
- normalized EBIT/operating margin
- oral Wegovy incrementality/cannibalisation
- Lilly share-loss pressure
- capex normalization path
- WACC/discount rate
- terminal growth or terminal multiple
- target currency and ADR/share-count treatment

## 6. Sensitivity grid to build next

- Primary matrix: 2027-2030 sales CAGR × normalized operating margin.
- Secondary toggle: capex normalization / FCF conversion.
- Optional competitive toggle: Lilly pressure high/base/low and oral Wegovy incrementality.

## 7. Guardrails

- Not an investment recommendation
- No portfolio action inferred
- Do not treat oral Wegovy as 100% incremental without PM approval
- Do not normalize Q1 2026 reported OP without adjusting for one-offs
- Mark Lilly/Q1 competitive extraction as unresolved before final valuation

## 8. Open items before final valuation

- Pull/confirm Lilly Q1 2026 competitive extraction before finalizing share-pressure assumptions.
- Decide WACC/terminal method and target currency.
- Confirm ADR/share-count treatment if converting DKK enterprise/equity value to listed share/ADR reference.
- Decide whether pipeline optionality remains qualitative or receives probability-weighted explicit value.
