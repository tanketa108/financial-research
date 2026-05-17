# MSFT — Valuation model integration addendum v1.3

**Model received:** `MSFT_v1_2_valuation_model.xlsx`  
**Valuation date in model:** 15-May-2026  
**Purpose:** incorporate the user's valuation model into the MSFT Deep Dive / pre-valuation analysis as the first explicit valuation layer after the v1.2 research pack.

## 1. Executive valuation read-through

The model moves the MSFT work from a pure pre-valuation research pack to an investable valuation framework. It is built around 8 valuation methods and uses the median as the central target to reduce outlier dependence.

| Item | Model output |
|---|---:|
| Spot price used | $408 |
| Median target price, 8 methods | $463.7 |
| Average target price, 8 methods | $476.4 |
| Implied upside vs spot | +13.7% median / +16.8% average |
| Valuation range | $357 – $604 |
| Probabilistic scenario value | ~$474 |

**Interpretation:** the model supports a moderately favourable risk/reward, but not a screamingly cheap entry. It is consistent with a **HOLD / accumulate on dips** conclusion: attractive below ~$380-400, materially more compelling near/below ~$360, less attractive above ~$450 unless capex normalization and Copilot/Azure upside become more visible.

## 2. Key valuation methods

| Method | Implied price | vs $408 spot |
|---|---:|---:|
| DCF Gordon Growth | $357.0 | -12.5% |
| DCF H-Model fade | $400.8 | -1.8% |
| DCF Exit EV/EBITDA | $604.4 | +48.1% |
| DCF Exit EV/EBIT | $566.4 | +38.8% |
| DCF Exit EV/Revenue | $464.1 | +13.7% |
| NTM P/E × FY27E EPS | $463.4 | +13.6% |
| NTM EV/EBITDA × FY27E EBITDA | $539.7 | +32.3% |
| NTM EV/Revenue × FY27E Revenue | $415.2 | +1.8% |

**Analytical consequence:** the valuation is highly sensitive to terminal method selection. Pure Gordon/H-Model is conservative to near-fair; exit multiple methods produce significant upside. The median is therefore the right central anchor because it avoids over-weighting high terminal multiple cases.

## 3. Main operating assumptions to connect with the Deep Dive

The model’s core debate matches the v1.2 Deep Dive: **AI capex vs durable AI/cloud monetization**.

### Forecast revenue growth by segment

| Segment | FY26E | FY27E | FY28E | FY29E | FY30E | Terminal |
|---|---:|---:|---:|---:|---:|---:|
| Productivity & Business Processes | 14.2% | 13.0% | 11.5% | 10.0% | 9.0% | 4.5% |
| Intelligent Cloud | 22.5% | 25.0% | 22.0% | 18.0% | 14.0% | 4.5% |
| More Personal Computing | 2.0% | 4.0% | 4.0% | 3.5% | 3.0% | 3.0% |

### Margin / capital intensity assumptions

| Driver | FY26E | FY27E | FY28E | FY29E | FY30E | Terminal |
|---|---:|---:|---:|---:|---:|---:|
| Consolidated operating margin | 44.9% | 44.6% | 44.7% | 45.3% | 45.8% | 46.4% |
| Capex / revenue | 33.0% | 29.0% | 23.5% | 20.0% | 17.5% | 15.0% |
| D&A / revenue | 11.7% | 13.5% | 15.0% | 15.0% | 14.5% | 14.0% |
| FCFF / revenue | 16.0% | 21.6% | 28.2% | 32.2% | 34.6% | 37.0% |

**Analytical consequence:** the model is not blindly bullish. It explicitly prices a very heavy AI capex cycle in FY26-FY27, then assumes gradual normalization. The core underwriting question becomes whether terminal capex/revenue can realistically normalize toward 15% without damaging Azure/Copilot growth.

## 4. Reverse DCF: what the market prices at $408

At the spot price used in the model, the market appears to require some combination of:

| Variable | Base case | Implied by spot | Read-through |
|---|---:|---:|---|
| Terminal growth | 3.0% | ~4.1% | Spot needs stronger long-run growth if other variables unchanged. |
| WACC | 9.12% | ~8.32% | Spot is easier to justify with lower required return / lower rate environment. |
| FY30 EBIT margin | 45.8% | ~55.6% | Unrealistic alone; shows that margin alone cannot explain spot. |
| Terminal capex/revenue | 15.0% | ~9.5% | Market may be assuming faster AI capex normalization than the model. |
| FY25-FY30 revenue CAGR | 13.9% | ~17.9% | Spot needs stronger growth if ratios are held constant. |

**Interpretation:** current price is not obviously expensive, but it embeds a non-trivial expectation that AI capex intensity eventually falls and/or revenue growth remains stronger than the base case. If capex stays structurally high, the upside narrows sharply.

## 5. Scenario framing added to the analysis

| Scenario | Probability | Value range | Core assumptions |
|---|---:|---:|---|
| Bear | 25% | $280-340 | Capex/revenue remains >20%, Azure decelerates, IC margin stays compressed. |
| Base | 45% | $430-490 | Capex normalizes toward 17% terminal, Azure remains strong, margins hold 45-46%. |
| Bull | 30% | $580-680 | Faster GPU efficiency, Copilot adoption accelerates, Azure sustains 25%+ longer, OpenAI optionality contributes. |
| Probability-weighted | — | ~$474 | Close to the 8-method average/median zone. |

## 6. Integration into the MSFT Deep Dive thesis

The valuation model reinforces and sharpens three points from the v1.2 research pack:

1. **The investment debate is capex normalization, not current quality.** MSFT remains an exceptional business operationally, but valuation depends on whether AI infrastructure converts into durable high-margin revenue.
2. **RPO and Azure growth make the capex cycle more defensible.** $627B commercial RPO and Azure +40% constant-currency growth reduce the probability that capex is purely speculative.
3. **Entry discipline matters.** At ~$408, the model shows moderate upside. The best risk/reward appears in drawdowns, especially if price approaches the $360-380 range without thesis impairment.

## 7. Files added to repo

- `financial_system/deep_dives/MSFT/MSFT_v1_2_valuation_model.xlsx` — original user valuation model.
- `financial_system/deep_dives/MSFT/MSFT-valuation-model-integration-v1.3.md` — this integration addendum.

