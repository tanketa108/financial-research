# DVN — Valuation Model Review v0.1

Date: 2026-05-23  
Company: Devon Energy Corporation (`DVN`)  
Reviewed artifact: `financial-research/financial_system/valuations/DVN/DVN_Valoracion_v1_1.xlsx`  
Related dashboard output: `financial-research/financial_system/valuations/DVN-valuation-display-v1.md`  
Status: model review memo; not an investment recommendation

## 1. Executive conclusion

The DVN model is directionally useful and materially better than a simple top-down commodity multiple: it separates oil, gas and NGL volumes/prices, models pro-forma Devon+Coterra, includes WACC, explicit FCFF, multiple cross-checks, reverse DCF and sensitivity tables.

However, I would **not yet treat the model output as fully decision-grade** without analyst/PM review. The central issue is not formula breakage; it is **assumption confidence**.

Main finding:

> The model’s base case already assumes meaningful post-merger execution: 100% synergy run-rate from FY2027, large FY2026 pro-forma volume step-up, improving gas margins, stable mid-cycle oil prices and capital intensity around 21.5-22.5% of revenue. Under those assumptions, upside versus spot appears limited to moderate depending on terminal method. The investment case needs explicit downside testing around commodity deck, synergy realization and maintenance capex.

## 2. Workbook structure reviewed

Sheets identified:

- `Resumen`
- `Hipotesis`
- `Historico`
- `Modelo`
- `DuPont_WC`
- `Reverse_DCF`
- `Conclusiones`
- `Fuentes`

Formula density is high and appropriate for a valuation workbook:

- `Resumen`: 28 formulas
- `Hipotesis`: 13 formulas
- `Historico`: 199 formulas
- `Modelo`: 397 formulas
- `DuPont_WC`: 115 formulas
- `Reverse_DCF`: 61 formulas
- `Conclusiones`: 1 formula

No obvious structural corruption was detected from workbook XML inspection. Full Excel recalculation was not available in this environment, so formula review is static plus manual recalculation of core mechanics.

## 3. Key model inputs

### Market / cost of capital

| Input | Model value | Comment |
|---|---:|---|
| Spot price | $49.49 | Source note: Devon IR / market data, 15-May-2026 EOD. |
| Diluted shares post-merger | 1,153m | 616m DVN + 0.70x × 767m CTRA. |
| Risk-free rate | 4.5% | Reasonable for 10Y UST assumption. |
| ERP | 4.5% | Damodaran-style implied ERP; reasonable. |
| Beta | 1.20 | Uses sector E&P beta, not observed low Google beta; I agree with using sector beta. |
| Pre-tax cost of debt | 5.5% | Reasonable for BBB+/IG energy spread assumption. |
| Tax rate | 22% | Reasonable normalized rate. |
| Total debt pro-forma | $12.2bn | Needs final cross-check against post-close balance sheet. |
| Cash + ST investments | $1.93bn | Needs final cross-check against post-close balance sheet. |
| Equity investments | $715m | Matterhorn/Catalyst/etc.; included in equity bridge. |
| Computed WACC | ~8.9% | Manual recalculation gives ~8.91%. |

### Commodity / operating assumptions

| Driver | FY2026E | FY2030E | Terminal | Comment |
|---|---:|---:|---:|---|
| Oil production growth | +45% | +1.5% | 0% | FY2026 pro-forma jump reflects Coterra contribution. |
| Gas production growth | +215% | +2.0% | 0% | Very large merger-driven step-up; critical to pro-forma validity. |
| NGL production growth | +45% | +2.0% | 0% | Merger + liquids-rich gas growth. |
| Oil realized price | $67/bbl | $62/bbl | $62/bbl | Conservative vs Q1 spot, but still above severe downside. |
| Gas realized price | $2.20/mcf | $2.80/mcf | $2.80/mcf | Assumes improving gas realization / Marcellus benefit. |
| NGL realized price | $19/bbl | $20.5/bbl | $20.5/bbl | Reasonable but volatile. |
| Oil contribution margin | 40% | 43% | 42% | High sensitivity to oil deck. |
| Gas contribution margin | 10% | 22% | 20% | Important optimistic swing: gas margin expansion matters. |
| NGL contribution margin | 18% | 22% | 20% | Reasonable but should be stressed. |

### Capital allocation / FCFF

| Driver | Model value | Comment |
|---|---:|---|
| Synergies target | $1.0bn pre-tax annual | Core merger assumption. |
| Synergy ramp | 40% FY2026, 100% FY2027+ | Needs downside case at 50-75%. |
| Capex / revenue | 22.5% FY2026, 21.5% FY2028-FY2030, 22% terminal | Plausible, but maintenance capex is the key downside risk. |
| D&A / revenue | 15.5-16.0%, 15% terminal | Lower than historical DVN DD&A/revenue; depends on Coterra mix and accounting. |
| ΔWC / revenue | 0.5% FY2026, 0.3% FY2027, 0% thereafter | Reasonable simplification. |
| Buybacks + dividends / FCF | 65-70% | Matches cash-return thesis but should not drive valuation directly unless share count is modeled. |

## 4. Manual model sanity check

Using the extracted assumptions, I manually rebuilt the core FCFF logic:

| Year | Revenue | EBIT incl. synergies | EBIT margin | Capex | FCFF |
|---|---:|---:|---:|---:|---:|
| FY2026E | ~$19.5bn | ~$6.7bn | ~34.2% | ~$4.4bn | ~$3.7bn |
| FY2027E | ~$19.9bn | ~$7.8bn | ~39.0% | ~$4.4bn | ~$4.8bn |
| FY2028E | ~$20.6bn | ~$8.2bn | ~39.9% | ~$4.4bn | ~$5.3bn |
| FY2029E | ~$21.0bn | ~$8.4bn | ~40.0% | ~$4.5bn | ~$5.3bn |
| FY2030E | ~$21.6bn | ~$8.7bn | ~40.2% | ~$4.7bn | ~$5.5bn |

Manual Gordon-style DCF sanity check with ~8.9% WACC and 2.0% terminal growth gives a value in the broad mid-$50s per share depending on exact equity bridge and timing convention. The workbook’s own extracted/ingested dashboard output references a central/gordon output around ~$59.8, while the workbook conclusion text says median across methods around ~$46 and probabilistic mean around ~$47.

This difference is important but not necessarily an error: it reflects method dispersion. Gordon DCF is very terminal-sensitive; exit multiple and probability-weighted scenario approaches are more conservative.

## 5. What looks solid

1. **Segmentation by commodity is the right architecture.**  
   Oil/gas/NGL separation is necessary for DVN; a single revenue CAGR would hide the thesis.

2. **Sector beta is preferable to short-term observed beta.**  
   Using beta 1.20 is more conservative and more economically sensible than a distorted observed beta.

3. **Reverse DCF is useful.**  
   The model asks what the market is pricing at $49.49 rather than only producing a target price.

4. **Sensitivity framework exists.**  
   The workbook has WACC/g, WACC/margin, capex/g and EV/EBITDA matrices.

5. **Source sheet is unusually strong.**  
   It cites DVN 10-K, Q1 2026 8-K, Devon/Coterra merger agreement, closing filing, Coterra 10-K, Fed and Damodaran sources.

## 6. Main concerns / required review items

### 6.1 Merger pro-forma assumptions are doing heavy lifting

The FY2026 model assumes:

- oil production +45%;
- NGL production +45%;
- gas production +215%;
- $400m synergy benefit in FY2026;
- $1.0bn full annual synergy from FY2027 onward.

These may be directionally reasonable for Devon+Coterra, but they are the largest bridge from historical DVN to model economics. I would make this a visible scenario switch:

- 50% synergy case;
- 75% synergy case;
- 100% synergy case;
- delayed synergy case.

### 6.2 Gas margin improvement is a major swing factor

Gas contribution margin rises from 10% in FY2026 to 22% by FY2030. That is plausible if Marcellus mix and basis improve, but it should be stressed because Coterra makes the combined company more gas-weighted.

Recommended downside test:

- keep gas realized price at $2.20-2.40/mcf;
- cap gas contribution margin at 12-15%;
- compare FCFF and price impact.

### 6.3 Capex / maintenance capex needs a harder shale test

The model assumes total capex around 21.5-22.5% of revenue and terminal maintenance capex 95% of total capex. The workbook itself says maintenance capex per Boe above $15 would be expensive and below $8 optimistic.

Recommended review:

- calculate maintenance capex per Boe in each forecast year;
- compare against DVN historical $/Boe and peer shale maintenance capital intensity;
- stress +$1/Boe, +$2/Boe, +$3/Boe maintenance capex impact.

### 6.4 D&A / revenue may be too benign versus historical DVN

The model notes DVN FY2025 DD&A around 21% of revenue, but forecast D&A/revenue is 15.5-16.0%, falling to 15.0% terminal. This may be justified by Coterra mix, but it should be explicitly reconciled.

This matters less for FCFF than capex, but it affects EBITDA/EBIT bridge, exit multiples and accounting earnings.

### 6.5 Buyback authorization should be separated from valuation

The $8bn buyback is economically important, but the model mostly values the business on current pro-forma shares. If buybacks are included as capital allocation upside, the model needs an explicit share-count roll-forward and repurchase price assumption.

Guardrail:

> Do not credit the $8bn buyback as value creation unless repurchase price is below intrinsic value and leverage/cycle risk remains acceptable.

### 6.6 Model output dispersion should be shown as a warning, not averaged mechanically

The workbook has 8 valuation methods. For a cyclical E&P, the median is useful, but the spread is analytically meaningful. Gordon DCF can overstate value if terminal FCFF is based on favorable commodity/capex assumptions.

I would prefer final PM framing:

- Primary: scenario-weighted commodity/capex/synergy cases.
- Secondary: EV/EBITDA cross-check.
- Tertiary: Gordon DCF as sensitivity, not headline.

## 7. Formula / structural observations

No obvious broken formulas were found in static inspection. Formula chains in `Modelo`, `Reverse_DCF` and summary sheets reference sensible inputs.

Notable formulas reviewed:

- WACC = E/V × Ke + D/V × after-tax Kd.
- FCFF = NOPAT + D&A − capex − ΔWC.
- Gordon terminal value = FY2030 FCFF × (1+g) / (WACC−g).
- Equity bridge = EV + cash + equity investments − debt.
- Sensitivity tables use WACC/g, WACC/op margin, capex/g and EV/EBITDA.

Potential technical cleanup:

- The workbook should be recalculated in Excel/LibreOffice and saved with cached values so ingestion tools do not produce inconsistent extracted values.
- The dashboard ingestion currently labels the output as `extracted_not_validated`; that is correct and should remain until PM/analyst review.

## 8. Recommended scenario grid before PM decision

Minimum cases:

| Case | Oil realized | Gas realized | Synergies | Capex / revenue | View |
|---|---:|---:|---:|---:|---|
| Bear | $55-58/bbl | $1.75-2.25/mcf | 50% | 24-25% | Commodity/cost downside; capital returns slow. |
| Base | $62-67/bbl | $2.20-2.80/mcf | 75-100% | 21.5-22.5% | Current model-like case, but with explicit synergy confidence. |
| Bull | $75-85/bbl | $3.00-4.00/mcf | 100%+ | 20-21.5% | Strong commodity deck and full execution. |

The model conclusion already frames approximate scenario prices:

- Bear: ~$30
- Base: ~$46
- Bull: ~$70
- Probability-weighted mean: ~$47

I would keep this as the headline until the model is recalculated and scenario tables are refreshed.

## 9. PM decision points

Before relying on DVN for portfolio action, PM should decide:

1. What is the right mid-cycle oil deck: $55, $62, $67 or $75+?
2. Should gas be modeled as structural upside after Coterra, or as low-margin volatility?
3. What probability should be assigned to 100% synergy realization?
4. Is 21.5-22.5% capex/revenue enough to hold production flat through cycle?
5. Should capital returns be treated as distribution of value or incremental value creation?
6. Should the primary valuation anchor be scenario-weighted FCF yield / EV-EBITDA rather than Gordon DCF?

## 10. Acceptance status

Recommended status for the current model:

- **Formula integrity:** preliminary pass, pending Excel recalculation.
- **Source quality:** good, source sheet is strong.
- **Assumption quality:** medium; needs PM review for commodity deck, synergies and maintenance capex.
- **Dashboard readiness:** improve from `yes_needs_review` to `reviewed_needs_pm_assumptions`.
- **Remaining gap:** PM-selected scenario weights and recalculated scenario output.

## 11. Next action

Create a smaller DVN scenario input sheet or update the Excel with three explicit toggles:

1. Commodity deck: bear/base/bull.
2. Synergy realization: 50% / 75% / 100% / 120%.
3. Capex intensity: 21.5% / 23.0% / 25.0% of revenue.

That would make the model genuinely PM-ready rather than just structurally impressive.
