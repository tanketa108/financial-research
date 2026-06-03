# NVO — Valuation Input Sheet v0.1

Date: 2026-05-23  
Task: `TASK-2026-05-17-001`  
Status: PM-ready model input scaffold, not a valuation and not an investment recommendation  
Company: Novo Nordisk A/S (`NVO`)  
Currency: DKK unless stated otherwise

## 1. Purpose

This sheet converts the NVO Deep Dive and Q1 2026 primary extraction into model-ready assumptions. It deliberately stops before producing a fair value. The goal is to give the Portfolio Manager a clean set of base/downside/upside inputs and open decisions for a DCF, reverse DCF or scenario model.

Core question:

> Is 2026 a temporary pricing/capacity reset before GLP-1 growth normalizes, or the start of structurally lower economics for Novo Nordisk?

## 2. Source-backed anchors

| Area | Anchor | Source |
|---|---:|---|
| FY2025 sales | DKK 309.064bn, +6% reported / +10% CER | Novo Nordisk Annual Report 2025 / Company Announcement No. 4 2026 |
| FY2025 operating profit | DKK 127.658bn, -1% reported / +6% CER | Novo Nordisk Annual Report 2025 / Company Announcement No. 4 2026 |
| FY2025 net profit | DKK 102.434bn, +1% | Novo Nordisk Annual Report 2025 |
| FY2025 diluted EPS | DKK 23.03, +2% | Novo Nordisk Annual Report 2025 |
| FY2025 obesity care sales | DKK 82.347bn, +26% reported / +31% CER | Novo Nordisk Annual Report 2025 |
| FY2025 diabetes care sales | DKK 207.109bn, flat reported / +4% CER | Novo Nordisk Annual Report 2025 |
| FY2025 rare disease sales | DKK 19.608bn, +5% reported / +9% CER | Novo Nordisk Annual Report 2025 |
| FY2025 gross margin | 81.0% vs 84.7% in 2024 | Novo Nordisk Annual Report 2025 |
| FY2025 FCF | DKK 28.3bn | Novo Nordisk Annual Report 2025 |
| FY2025 PPE capex | DKK 60.1bn | Novo Nordisk Annual Report 2025 |
| Initial FY2026 adjusted sales/OP guidance | -5% to -13% CER | Company Announcement No. 4 2026 |
| Q1 2026 adjusted sales | DKK 70.063bn, -4% CER | Q1 2026 Investor Presentation, p. 10 |
| Q1 2026 adjusted operating profit | DKK 32.858bn, -6% CER | Q1 2026 Investor Presentation, p. 10 |
| Q1 2026 adjusted operating margin | 46.9% | Q1 2026 Investor Presentation, p. 10 |
| FY2026 updated adjusted sales/OP guidance | -4% to -12% CER | Q1 2026 Investor Presentation, p. 11 |
| FY2026 capex guide | Around DKK 55bn | Q1 2026 Investor Presentation, p. 11 |
| FY2026 FCF guide | DKK 36-46bn | Q1 2026 Investor Presentation, p. 11 |
| US Wegovy weekly TRx | ~475k total US Wegovy weekly TRx | Q1 2026 Investor Presentation, p. 4 |
| US Wegovy pill weekly TRx | ~207k weekly TRx | Q1 2026 Investor Presentation, p. 4 |
| Wegovy pill cumulative patients | >1m patients since US launch / >2m cumulative prescriptions | Q1 2026 Investor Presentation, pp. 4, 6 |
| Wegovy launched internationally | >55 countries; Wegovy pill selected markets in H2 2026 | Q1 2026 Investor Presentation, p. 9 |
| Pipeline checkpoints | Wegovy 7.2mg approved US/EU/UK; CagriSema submitted US; zenagamtide phase 3 initiated/to be initiated | Q1 2026 Investor Presentation, pp. 12, 16, 24, 48 |

## 3. Model architecture recommendation

Use a three-layer model, not a single top-line CAGR:

1. **Segment revenue layer**
   - Diabetes care
   - Obesity care
   - Rare disease
   - Optional product bridge: Ozempic, Wegovy injectable, Wegovy pill, Rybelsus if data granularity is sufficient.

2. **Economic pressure layer**
   - US realised price / gross-to-net pressure.
   - Lilly share pressure.
   - Oral Wegovy incrementality vs cannibalisation.
   - International semaglutide exclusivity/pricing effects.

3. **Cash conversion layer**
   - Gross margin recovery vs structural pressure.
   - R&D and S&D reinvestment.
   - Catalent/capacity D&A drag.
   - Capex normalization after 2025-2026 peak.
   - FCF conversion and terminal margin.

## 4. Scenario assumptions — 2027-2030

These are deliberately framed as ranges. The PM should select point estimates before valuation.

### 4.1 Revenue growth after 2026 reset

| Driver | Downside | Base | Upside | Rationale |
|---|---:|---:|---:|---|
| 2026 adjusted sales growth CER | -12% | -8% | -4% | Company updated range is -4% to -12% CER; base uses midpoint. |
| 2027 sales growth CER | 0-3% | 4-7% | 8-11% | Downside: reset persists; base: partial normalization; upside: oral Wegovy and obesity volumes offset price. |
| 2028-2030 sales CAGR CER | 2-4% | 6-8% | 9-12% | TAM remains large, but economics depend on price/share. Avoid assuming old hypergrowth economics. |
| Obesity care growth 2027-2030 | mid-single-digit | high-single/low-double-digit | low/mid-teens | Volume growth remains strongest driver; net price and Lilly competition cap economics. |
| Diabetes care growth 2027-2030 | low-single-digit decline to flat | low-single-digit growth | mid-single-digit growth | Diabetes is more mature; Novo lost diabetes value share in 2025. |
| Rare disease growth | flat/low-single-digit | low/mid-single-digit | mid-single-digit | Not thesis-critical. |

### 4.2 US pricing and competition

| Assumption | Downside | Base | Upside | Notes |
|---|---:|---:|---:|---|
| US realised price pressure | Severe / continuing | Material but stabilizing | Mostly absorbed by 2026 reset | Key swing factor. Company cites lower realised prices, MFN, Medicaid coverage and non-repeat of 2025 gross-to-net positives. |
| Lilly share pressure | Sustained Novo share loss | Novo loses some US share but defends global leadership | Novo stabilizes share via oral Wegovy / pipeline | Need primary Lilly extraction before final model. |
| International semaglutide exclusivity/pricing | Material drag | Manageable drag | Offset by volume/new launches | Company flags semaglutide molecule exclusivity loss in certain IO markets. |

### 4.3 Oral Wegovy incrementality

| Assumption | Downside | Base | Upside | Notes |
|---|---:|---:|---:|---|
| Incremental demand vs cannibalisation | 20-30% incremental | 40-60% incremental | 65-80% incremental | Oral route can expand TAM, but self-pay/channel mix and cannibalisation are unresolved. |
| Net price / access quality | Lower-quality/self-pay mix | Mixed reimbursed + self-pay | Strong access and reimbursement | Q1 indicates commercial access and telehealth/self-pay channels; net economics need PM judgment. |
| Persistence/adherence | Inferior to injectable | Mixed | Comparable enough | Clinical efficacy is strong, but real-world persistence is still an open variable. |

### 4.4 Margins and cash conversion

| Metric | Downside | Base | Upside | Source / reasoning |
|---|---:|---:|---:|---|
| Gross margin normalized | 78-80% | 80-82% | 82-84% | FY2025 gross margin was 81.0%, down from 84.7% in 2024. |
| Adjusted operating margin normalized | 38-40% | 41-44% | 44-47% | Q1 2026 adjusted operating margin was 46.9%, but guidance implies pressure; use normalized range, not one-off reported OP. |
| FY2026 capex | ~DKK 55bn | ~DKK 55bn | ~DKK 55bn | Company guide. |
| 2027-2030 capex trend | stays elevated | gradual normalization | sharper normalization | Capacity build is central to FCF; PM must decide if 2025-2026 is peak. |
| FY2026 FCF | DKK 36-46bn | DKK 36-46bn | DKK 36-46bn | Company guide. |
| FCF conversion 2027-2030 | weak recovery | gradual recovery | strong recovery | Depends on capex/D&A/capacity and pricing stabilization. |

## 5. Suggested base case skeleton

A conservative base case should probably look like this before PM override:

- **2026:** adjusted sales and adjusted operating profit down around the midpoint of company guidance at CER.
- **2027:** return to positive sales growth, but not to historical GLP-1 hypergrowth economics.
- **2028-2030:** mid/high-single-digit CER sales CAGR if oral Wegovy contributes and obesity volume continues to expand.
- **Margins:** partial recovery from 2025-2026 pressure, but not immediate return to 2024 gross margin.
- **FCF:** 2026 guided FCF remains depressed versus earnings because capex is high; recovery requires capex normalization.
- **Terminal:** do not use a pharma mega-cap terminal multiple unless the model explicitly shows durable price/share and FCF recovery.

## 6. Sensitivities the valuation should expose

Minimum sensitivity grid:

1. 2027-2030 revenue CAGR.
2. Normalized operating margin.
3. Capex as % of sales or annual capex normalization path.
4. Terminal growth / terminal multiple.
5. Oral Wegovy incrementality.
6. US net price decline.

Best practical output: a 3x3 matrix with:

- Rows: normalized operating margin.
- Columns: 2027-2030 sales CAGR.
- Secondary toggle: capex normalization / FCF conversion.

## 7. PM decisions required before final valuation

1. **2026 midpoint:** use company midpoint or bias toward high/low end of -4% to -12% CER?
2. **Oral Wegovy:** treat as mostly incremental or partly cannibalising?
3. **Lilly:** how much share loss is acceptable in the base case?
4. **Margins:** assume 2024 gross margin is recoverable, or use 2025 as the new anchor?
5. **Capex:** is 2025-2026 peak investment or a structurally higher capital intensity period?
6. **Pipeline:** include explicit probability-weighted value for CagriSema / semaglutide 7.2mg / zenagamtide, or keep it as qualitative upside?

## 8. Red flags / model guardrails

- Do not value reported Q1 2026 operating profit as normalized because it includes the 340B provision reversal effect in reported figures.
- Do not model oral Wegovy as 100% incremental without explicit PM approval.
- Do not extrapolate historical GLP-1 growth rates without haircut for price, coverage and Lilly competition.
- Do not treat FCF weakness as purely temporary unless capex normalization is shown explicitly.
- Do not infer portfolio action. This output prepares valuation work only.

## 9. Open data gaps

- Primary Lilly Q1 2026 extraction for Mounjaro/Zepbound/oral obesity competitive data.
- More granular Novo product-level quarterly sales split post oral Wegovy launch.
- Realized net price / gross-to-net assumptions by US channel.
- Long-range capex and D&A bridge after Catalent/capacity ramp.
- PM-selected WACC / terminal methodology / target currency.

## 10. Close recommendation for task ledger

`TASK-2026-05-17-001` can be marked **done** for its stated close criteria if this sheet is accepted as the structured valuation input sheet. Remaining work should be a separate PM-selected valuation/model build task, not kept inside the extraction task.
