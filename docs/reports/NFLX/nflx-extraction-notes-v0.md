# NFLX extraction notes v0 — financial data & Netflix-specific economics

Scope: source-backed extraction for a future Deep Dive, not the final report. Figures are in **US$ billions** unless noted. Fiscal year ends Dec. 31. Companyfacts source: SEC XBRL API for Netflix CIK 1065280 (`https://data.sec.gov/api/xbrl/companyfacts/CIK0001065280.json`). Primary filing URLs are listed below each block.

## 1) P&L / cash flow, FY2021-FY2025

| Fiscal year | Revenue | Operating income | Op. margin | Net income | OCF | Capex | FCF | Capex / revenue | FCF / net income |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2021 | 29.698 | 6.195 | 20.9% | 5.116 | 0.393 | 0.525 | -0.132 | 1.8% | -2.6% |
| 2022 | 31.616 | 5.633 | 17.8% | 4.492 | 2.026 | 0.408 | 1.619 | 1.3% | 36.0% |
| 2023 | 33.723 | 6.954 | 20.6% | 5.408 | 7.274 | 0.349 | 6.926 | 1.0% | 128.1% |
| 2024 | 39.001 | 10.418 | 26.7% | 8.712 | 7.361 | 0.440 | 6.922 | 1.1% | 79.5% |
| 2025 | 45.183 | 13.327 | 29.5% | 10.981 | 10.149 | 0.688 | 9.461 | 1.5% | 86.2% |

Notes:
- FCF is derived as operating cash flow minus purchases of property and equipment. Netflix reports content cash spend within operating cash flow, not capex.
- Major regime shift: OCF/FCF conversion improved sharply from 2023 onward as revenue growth resumed and cash content dynamics normalized after the earlier heavy investment cycle.

Sources:
- SEC companyfacts: tags `Revenues`, `OperatingIncomeLoss`, `NetIncomeLoss`, `NetCashProvidedByUsedInOperatingActivities`, `PaymentsToAcquirePropertyPlantAndEquipment`.
- FY2025 10-K filed 2026-01-23: `https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm`.

## 2) Balance sheet / liquidity, FY2021-FY2025

| Fiscal year | Assets | Equity | Cash & equivalents | Short-term investments | Cash + STI | Long-term debt | Net debt / (cash) | Debt / equity |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2021 | 44.585 | 15.849 | 6.028 | n/a | 6.028 | 14.693 | 8.665 | 92.7% |
| 2022 | 48.595 | 20.777 | 5.147 | 0.911 | 6.058 | 14.353 | 8.295 | 69.1% |
| 2023 | 48.732 | 20.588 | 7.117 | 0.021 | 7.138 | 14.143 | 7.005 | 68.7% |
| 2024 | 53.630 | 24.744 | 7.805 | 1.779 | 9.584 | 13.798 | 4.214 | 55.8% |
| 2025 | 55.597 | 26.615 | 9.034 | 0.029 | 9.062 | 13.464 | 4.402 | 50.6% |

Q1 2026 update:

| Period | Assets | Equity | Cash & equivalents | Short-term investments | Long-term debt | Net debt / (cash) |
|---|---:|---:|---:|---:|---:|---:|
| 2026 Q1 | 61.016 | 31.126 | 12.260 | 0.029 | 13.361 | 1.073 |

Notes:
- Leverage fell materially from 2021 through 2025 despite sizable repurchases, mainly due to cash generation and retained earnings.
- Q1 2026 liquidity increased sharply; context matters because Netflix had announced/was working through the Warner Bros. Discovery transaction financing package.

Sources:
- SEC companyfacts: `Assets`, `StockholdersEquity`, `CashAndCashEquivalentsAtCarryingValue`, `ShortTermInvestments`, `LongTermDebtNoncurrent`.
- FY2025 10-K: `https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm`.
- Q1 2026 10-Q filed 2026-04-17: `https://www.sec.gov/Archives/edgar/data/1065280/000106528026000138/nflx-20260331.htm`.

## 3) Capital allocation

| Fiscal year | Dividends | Share repurchases | FCF | Repurchases / FCF |
|---:|---:|---:|---:|---:|
| 2021 | 0.000 | 0.600 | -0.132 | n/m |
| 2022 | 0.000 | 0.000 | 1.619 | 0.0% |
| 2023 | 0.000 | 6.045 | 6.926 | 87.3% |
| 2024 | 0.000 | 6.264 | 6.922 | 90.5% |
| 2025 | 0.000 | 9.127 | 9.461 | 96.5% |
| Q1 2026 | 0.000 | 1.271 | 5.094 | 25.0% |

Notes:
- No common dividends identified in companyfacts for the period; returns are via buybacks.
- Buybacks absorbed nearly all FCF in 2023-2025. For valuation, treat repurchases as discretionary capital return rather than operating reinvestment.

Sources:
- SEC companyfacts: `PaymentsForRepurchaseOfCommonStock`; dividends tag absent in companyfacts for FY2021-FY2025.
- FY2025 10-K and Q1 2026 10-Q URLs above.

## 4) Content assets, liabilities, and cash/content economics

| Metric | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| Additions to streaming content assets | 12.555 | 16.224 | 17.097 |
| Change in streaming content liabilities | -0.586 | -0.779 | -0.611 |
| Content amortization | 14.197 | 15.302 | 16.422 |
| Year-end content assets, net | n/a | 32.452 | 32.778 |
| Current content liabilities | n/a | 4.394 | 4.085 |
| Non-current content liabilities | n/a | 1.781 | 1.579 |
| Recognized content liabilities, total | n/a | 6.174 | 5.664 |

Policy / economics notes:
- Netflix capitalizes licensed and produced content as `Content assets, net`. For licensed content, the company records a liability when the license period begins, cost is known, title is accepted and available for streaming. For produced content, Netflix capitalizes production/development/direct/overhead costs as incurred.
- Content assets are amortized in cost of revenues over the shorter of contractual availability, estimated use, or ten years, beginning when available. Amortization is accelerated because viewing is typically front-loaded; Netflix says on average over 90% of a licensed or produced content asset is expected to be amortized within four years after availability.
- Cash payments for additions to content assets and related liability changes are classified in operating cash flow, not investing capex. This is central to Netflix FCF comparability: classic capex is small, but content cash spend is embedded in OCF.
- FY2025 filing states recognized content liabilities were $4.1B current and $1.6B non-current, with a further $18.4B of obligations not on the balance sheet because they did not meet recognition criteria.

Sources:
- FY2025 10-K, content accounting policy and Note 4 / Note 9: `https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm`.
- Extracted inline XBRL tags from FY2025 10-K: `nflx:AdditionstoStreamingContentAssets`, `nflx:ChangeInStreamingContentLiabilities`, `nflx:CostofServicesAmortizationofStreamingContentAssets`, `nflx:ContentAssetsNetNoncurrent`, `nflx:ContentLiabilitiesCurrent`, `nflx:ContentLiabilitiesNoncurrent`.

## 5) Recent guidance / outlook

### FY2026 outlook from Q4 2025 shareholder letter

| Item | Management outlook |
|---|---|
| FY2026 revenue | $50.7B-$51.7B, +12%-14% Y/Y |
| FY2026 operating margin | 31.5% |
| Advertising revenue | Expected to roughly double |
| Q1 2026 forecast revenue | $12.157B, +15.3% Y/Y |
| Q1 2026 forecast operating income | $3.906B |
| Q1 2026 forecast operating margin | 32.1% |
| Q1 2026 forecast net income | $3.264B |
| Q1 2026 forecast diluted EPS | $0.76, split-adjusted |

Context from letter:
- 2025 delivered $45.2B revenue (+16% reported, +17% FX-neutral), 29.5% operating margin, ad revenue over $1.5B and up more than 2.5x.
- Q4 2025 revenue grew 18% Y/Y; Netflix crossed 325M paid memberships during Q4 2025.
- 2026 focus areas: improve core service/slate; more content categories including video podcasts and games; close Warner Bros. acquisition; sustain healthy growth.

Sources:
- Q4 2025 shareholder letter, Exhibit 99.1 to 8-K filed 2026-01-20: `https://www.sec.gov/Archives/edgar/data/1065280/000106528026000033/ex991_q425.htm`.
- Q4 2025 8-K: `https://www.sec.gov/Archives/edgar/data/1065280/000106528026000033/nflx-20260120.htm`.

### Q1 2026 actuals from 10-Q/companyfacts

| Metric | Q1 2026 actual |
|---|---:|
| Revenue | 12.250 |
| Operating income | 3.957 |
| Operating margin | 32.3% |
| Net income | 5.283 |
| OCF | 5.290 |
| Capex | 0.196 |
| FCF | 5.094 |
| Share repurchases | 1.271 |

Sources:
- Q1 2026 10-Q filed 2026-04-17: `https://www.sec.gov/Archives/edgar/data/1065280/000106528026000138/nflx-20260331.htm`.
- SEC companyfacts tags listed above.

## 6) Risks / open questions for the Deep Dive

- **Content accounting sensitivity:** accelerated amortization judgments and useful-life/viewing estimates matter; Netflix says content assets are assessed as a group and impairment has not been triggered to date. Need stress case for content ROI deterioration.
- **Cash-content cycle:** FCF quality is high post-2023, but content obligations not on balance sheet remain large. Need bridge from additions, amortization, cash spend and recognized/unrecognized obligations.
- **Advertising business:** Q4 2025 letter says ad revenue >$1.5B in 2025 and expected to roughly double in 2026. Need confirm ad margin profile, inventory/pricing maturity and incremental operating leverage.
- **Warner Bros. / WBD transaction:** FY2025 10-K subsequent event references amended merger agreement and bridge facility commitments increased to $42.2B. This can radically change leverage, content library, regulatory risk and capital allocation.
- **Capital allocation:** 2023-2025 repurchases used ~87%-97% of derived FCF. Need assess whether buybacks pause/slow under WBD financing or if balance sheet remains target-light.
- **Competition and price elasticity:** valuation must test paid membership growth, ARPU/pricing, ad tier migration and churn response in a saturated/increasingly bundled market.
- **FX:** management reports FX-neutral revenue in shareholder letters; future margin/revenue forecasts should separate reported vs constant-currency.

## 7) Source map

- SEC companyfacts CIK 1065280: `https://data.sec.gov/api/xbrl/companyfacts/CIK0001065280.json`
- SEC submissions index: `https://data.sec.gov/submissions/CIK0001065280.json`
- FY2025 10-K: `https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm`
- Q1 2026 10-Q: `https://www.sec.gov/Archives/edgar/data/1065280/000106528026000138/nflx-20260331.htm`
- Q4 2025 shareholder letter / Exhibit 99.1: `https://www.sec.gov/Archives/edgar/data/1065280/000106528026000033/ex991_q425.htm`
- Q4 2025 8-K cover: `https://www.sec.gov/Archives/edgar/data/1065280/000106528026000033/nflx-20260120.htm`
- Q1 2026 8-K cover: `https://www.sec.gov/Archives/edgar/data/1065280/000106528026000139/nflx-20260422.htm`

## 8) Data caveats

- FY2021-FY2025 financial statement tables are sourced from SEC companyfacts annual 10-K facts. Derived metrics are computed locally.
- Content detail is extracted from FY2025 10-K inline XBRL and provides clean 2023-2025 comparable rows in that filing; older 2021-2022 content detail not extracted in this v0 note.
- Short-term investments were not found for FY2021 in the selected companyfacts tag; table marks it n/a rather than inferring zero.
