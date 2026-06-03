# DVN — Scenario Toggle Sheet v0.1

Date: 2026-05-23  
Company: Devon Energy Corporation (`DVN`)  
Purpose: PM-ready scenario controls for the existing DVN valuation model v1.1  
Related files:
- `financial-research/financial_system/valuations/DVN/DVN_Valoracion_v1_1.xlsx`
- `financial-research/financial_system/valuations/DVN-model-review-v0.1.md`

## 1. Objective

This sheet converts the DVN model review into explicit scenario toggles. It does **not** replace the Excel model. It defines the scenario controls that should be added to, or used alongside, the workbook before relying on valuation outputs.

Core principle:

> DVN should be valued through commodity/capex/synergy scenarios, not a single Gordon DCF headline.

## 2. Three required toggles

### Toggle A — Commodity deck

| Case | Oil realized price | Gas realized price | NGL realized price | Interpretation |
|---|---:|---:|---:|---|
| Bear | $55-58/bbl | $1.75-2.25/mcf | $15-18/bbl | Downcycle / weak gas / limited pricing support. |
| Base | $62-67/bbl | $2.20-2.80/mcf | $19-21/bbl | Close to current workbook assumptions. |
| Bull | $75-85/bbl | $3.00-4.00/mcf | $23-28/bbl | Strong oil/gas deck; capital returns accelerate. |

Recommended default: **Base**, but show Bear first in PM review because downside durability is the thesis test.

### Toggle B — Devon/Coterra synergy realization

| Case | FY2026 realization | FY2027+ realization | Interpretation |
|---|---:|---:|---|
| Bear | 25% | 50% | Integration slower / synergy leakage. |
| Base-conservative | 40% | 75% | Gives credit but not full management target. |
| Base-management | 40% | 100% | Current workbook-like assumption. |
| Bull | 50% | 120% | Management target exceeded / operational optimization. |

Recommended default: **Base-conservative** for PM underwriting; keep Base-management as upside sensitivity unless there is evidence of execution.

### Toggle C — Capex intensity

| Case | FY2026 | FY2027-2030 | Terminal | Interpretation |
|---|---:|---:|---:|---|
| Bear | 24.5% | 24.0-25.0% | 25.0% | Higher maintenance capital required to hold production. |
| Base | 22.5% | 21.5-22.5% | 22.0% | Current workbook-like assumption. |
| Bull | 21.0% | 20.0-21.5% | 20.5% | Better productivity / lower service cost / asset quality benefit. |

Recommended default: **Base**, but stress Bear heavily. In shale, maintenance capex error can dominate the equity value.

## 3. Scenario package

### Bear case

| Input | Value |
|---|---:|
| Oil realized | $56/bbl |
| Gas realized | $2.00/mcf |
| NGL realized | $16.5/bbl |
| Synergy realization | 25% FY2026 / 50% FY2027+ |
| Capex / revenue | 24.5% FY2026 / 25.0% terminal |
| Terminal growth | 0.0-1.0% |
| WACC | 9.5-10.5% |

Narrative:
- Commodity deck weakens before synergies fully matter.
- Gas-heavy Coterra contribution does not earn high margins.
- Maintenance capex is higher than workbook base.
- Capital returns remain possible but less equity-accretive.

Use this to test: **can DVN protect balance sheet and return capital without relying on heroic oil/gas prices?**

### Base-underwriting case

| Input | Value |
|---|---:|
| Oil realized | $62-65/bbl |
| Gas realized | $2.40-2.70/mcf |
| NGL realized | $19.5-20.5/bbl |
| Synergy realization | 40% FY2026 / 75% FY2027+ |
| Capex / revenue | 22.5% FY2026 / 22.0% terminal |
| Terminal growth | 1.0-2.0% |
| WACC | ~9.0% |

Narrative:
- Similar to current workbook, but haircut full synergy realization.
- Treats Coterra as helpful but not transformational.
- Values DVN as a cash-return cyclical, not a compounder.

Use this as the primary PM underwriting case.

### Management/upside case

| Input | Value |
|---|---:|
| Oil realized | $67-75/bbl |
| Gas realized | $2.80-3.25/mcf |
| NGL realized | $21-24/bbl |
| Synergy realization | 40% FY2026 / 100% FY2027+ |
| Capex / revenue | 21.5-22.0% |
| Terminal growth | 2.0% |
| WACC | ~8.9% |

Narrative:
- Close to current workbook economics.
- Assumes synergy target is credible and gas margins improve.
- Use as upside/base-management case, not conservative underwriting.

### Bull case

| Input | Value |
|---|---:|
| Oil realized | $80/bbl |
| Gas realized | $3.50/mcf |
| NGL realized | $25/bbl |
| Synergy realization | 50% FY2026 / 120% FY2027+ |
| Capex / revenue | 20.0-21.0% |
| Terminal growth | 2.0-3.0% |
| WACC | 8.0-8.5% |

Narrative:
- Strong macro commodity case plus operational execution.
- Useful to understand upside torque, but should not anchor portfolio sizing.

## 4. Recommended PM dashboard layout

The final model/dashboard should expose:

1. Selected commodity deck: Bear / Base-underwriting / Management / Bull.
2. Selected synergy case: 50% / 75% / 100% / 120%.
3. Selected capex case: Bear / Base / Bull.
4. Resulting outputs:
   - FCFF 2026-2030;
   - implied FCF yield;
   - net debt / EBITDA;
   - dividend + buyback capacity;
   - equity value per share by EV/EBITDA;
   - equity value per share by DCF;
   - downside to spot and upside to spot.

## 5. Preferred valuation hierarchy

For DVN, use this order:

1. **Scenario-weighted FCF / EV-EBITDA** — primary.
2. **FCF yield through cycle** — primary cross-check.
3. **Reverse DCF at spot** — useful PM framing.
4. **Gordon DCF** — sensitivity only.

Reason: DVN is a cyclical E&P with depleting assets, commodity exposure and maintenance capex risk. A terminal FCFF perpetuity can easily overstate precision.

## 6. Suggested scenario weights

Initial neutral weights for discussion:

| Scenario | Weight |
|---|---:|
| Bear | 25% |
| Base-underwriting | 45% |
| Management/upside | 20% |
| Bull | 10% |

This is intentionally conservative. If PM has a stronger oil/gas macro view, weights can shift, but the default should not embed commodity bullishness silently.

## 7. Decision rules

DVN becomes more attractive if:

- Base-underwriting case shows acceptable upside to spot;
- Bear case protects balance sheet and does not impair capital return framework;
- FCF yield is attractive without assuming full $1bn synergies;
- maintenance capex sensitivity does not destroy equity value;
- management demonstrates post-close execution in the first 2-3 quarters.

DVN remains watch/review if:

- upside only exists in management/bull case;
- bear case shows leverage/capital-return fragility;
- gas margin improvement is required to make valuation work;
- buybacks are needed to manufacture EPS/value without clear intrinsic discount.

## 8. Concrete workbook changes recommended

Add to `Hipotesis`:

- `Scenario_Commodity`: Bear / Base / Management / Bull.
- `Scenario_Synergy`: 50 / 75 / 100 / 120.
- `Scenario_Capex`: Bear / Base / Bull.

Add to `Modelo`:

- linked scenario output block with FCFF, EV, equity value/share and FCF yield.
- separate table for bear/base/management/bull valuation outputs.

Add to `Conclusiones`:

- scenario-weighted value;
- spread to current spot;
- PM decision checklist;
- explicit statement that Gordon DCF is sensitivity, not headline.

## 9. Current acceptance status

- Model structure: acceptable.
- Formula integrity: preliminary pass, pending Excel recalculation.
- Assumption readiness: improved but still PM-dependent.
- Scenario framing: now explicit via this sheet.
- Remaining work: implement toggles in Excel or generate a separate scenario model file.

## 10. Next action

Recommended next action:

> Implement these toggles into a lightweight DVN scenario model or modify a copy of the Excel model, then produce a PM-ready output table with bear/base/management/bull valuation range.
