# Portfolio Review v0.2 — 2026-05-22

Report type: architecture hardening baseline / ad hoc portfolio review
Universe: canonical registry after user correction
Caveat: not an investment recommendation. This report structures portfolio state, research coverage, model gaps and PM review actions.

## Portfolio Review Digest

- Portfolio universe corrected and canonicalized: portfolio = MSFT, UBER, RACE, NVO, NFLX, DVN, LVMH, EOG; watchlist/idea = AMZN.
- State contract hardened: Company States now expose `coverageGaps`, `nextReviewAction`, `portfolioPosition` and `reporting`.
- Highest-priority PM workflow items: NVO valuation/model inputs; DVN model review; then RACE/LVMH/EOG valuation assumptions if selected.
- UBER remains portfolio but low priority because the thesis is comparatively better worked; AMZN is watchlist/idea, not portfolio.
- No portfolio weights/prices or investment actions are inferred.

Top PM actions:
1. DVN — Review DVN valuation model v1.1: formulas, assumptions, commodity sensitivity, FCF durability, capital returns, leverage and merger execution.
2. NVO — Complete NVO valuation/model input sheet: normalized 2027-2030 revenue/margin, US pricing, oral Wegovy, CAPEX/FCF and scenarios.
3. EOG — Build valuation/sensitivity framework for WTI, Henry Hub, NGLs, peer multiples and Encino/Utica contribution if selected.

## Portfolio coverage dashboard

| Ticker | Type | Status | Priority | Readiness | Deep Dive | Model | Thesis | Next review | Gaps |
|---|---|---|---|---|---|---|---|---|---:|
| DVN | portfolio | research_pending | high | medium | yes | yes_needs_review | implicit_in_preliminary_and_model | high: Review DVN valuation model v1.1: formulas, assumptions, commodity sensitivity, FCF durabil… | 1 |
| NVO | portfolio | research_pending | high | medium | yes | open_task | implicit_in_deep_dive | high: Complete NVO valuation/model input sheet: normalized 2027-2030 revenue/margin, US pricing,… | 1 |
| EOG | portfolio | active | medium | medium_high | yes | pending_valuation_step | implicit_in_deep_dive | medium: Build valuation/sensitivity framework for WTI, Henry Hub, NGLs, peer multiples and Encino/… | 1 |
| LVMH | portfolio | active | medium | medium_high | yes | pending_valuation_step | implicit_in_deep_dive | medium: Build valuation/model assumptions for F&LG recovery, margin normalization, China/US demand… | 1 |
| RACE | portfolio | active | medium | medium_high | yes | pending_valuation_step | implicit_in_deep_dive | medium: Build valuation/model assumptions for shipments, ASP/mix, EBIT margin and industrial FCF i… | 1 |
| MSFT | portfolio | active | high | high | yes | yes | yes | low: Monitor events and revisit only if AI capex normalization, Azure/Copilot monetization or F… | 0 |
| NFLX | portfolio | active | high | high | yes | yes | implicit_in_deep_dive | low: Monitor streaming economics, ads scale, pricing/paid-sharing normalization and FCF; revisi… | 1 |
| UBER | portfolio | active | low | medium_high | not_in_repo_or_not_linked | exists_outside_repo_or_not_linked | developed_but_not_fully_linked | low: Keep UBER low priority; optionally link existing thesis/model artifacts when convenient, b… | 1 |
| AMZN | watchlist | research_pending | medium | medium_low | no_preliminary_only | no | preliminary | medium: Decide whether AMZN as watchlist/idea should be promoted into full Deep Dive/model work. | 1 |

## Portfolio companies

### DVN — Devon Energy Corporation

Type: portfolio | Status: research_pending | Priority: high | Readiness: medium

Thesis state:
- Status: preliminary_report_completed
- Conviction: unknown
- PM decision: None
- Summary: DVN preliminary report completed. Main issue: assess combined Devon/Coterra through-cycle FCF and capital returns under conservative commodity assumptions before considering a full Deep Dive.

Coverage:
- Deep Dive: yes — financial-research/financial_system/deep_dives/DVN/DVN-research-prevaluation-v0.2-report.pdf
- Model: yes_needs_review — financial-research/docs/models/DVN/DVN_Valoracion_v1_1.xlsx
- Thesis: implicit_in_preliminary_and_model — n/a

Next review action:
- Action: Review DVN valuation model v1.1: formulas, assumptions, commodity sensitivity, FCF durability, capital returns, leverage and merger execution.
- Priority: high
- Owner: Charlie
- Trigger/due: User model uploaded and incorporated / n/a

Coverage gaps:
- high / model: User valuation model v1.1 exists but needs formula/assumption/sensitivity review before full reporting confidence. Recommended: Review model assumptions, formulas, commodity sensitivity, FCF durability, capital returns and leverage.

Open questions:
- What mid-cycle oil/gas price supports current FCF thesis?
- Is capital return sustainable through commodity downturns?
- Does M&A improve or dilute asset quality?

### NVO — Novo Nordisk A/S

Type: portfolio | Status: research_pending | Priority: high | Readiness: medium

Thesis state:
- Status: under_review
- Conviction: unknown
- PM decision: None
- Summary: Novo Nordisk is in research-pending status after a growth/price reset. Initial read: the company remains a GLP-1 leader with strong obesity/diabetes assets, but 2026 guidance embeds material pricing/competition pressure and lower US realised prices.

Coverage:
- Deep Dive: yes — financial-research/financial_system/deep_dives/NVO/NVO-research-deep-dive-prevaluation-report.pdf
- Model: open_task — TASK-2026-05-17-001
- Thesis: implicit_in_deep_dive — n/a

Next review action:
- Action: Complete NVO valuation/model input sheet: normalized 2027-2030 revenue/margin, US pricing, oral Wegovy, CAPEX/FCF and scenarios.
- Priority: high
- Owner: Charlie
- Trigger/due: Open task TASK-2026-05-17-001 / n/a

Coverage gaps:
- high / model: Open task exists for valuation/model inputs after Deep Dive. Recommended: Complete TASK-2026-05-17-001 with source-backed base/downside/upside assumptions.

Open questions:
- What is the normalised 2027-2030 revenue/margin trajectory after 2026 pricing reset?
- How much oral Wegovy is incremental vs cannibalising injectable Wegovy/GLP-1 demand?
- What share and price assumptions are required for Novo to defend premium valuation vs Lilly?
- How should we adjust margins for restructuring, Catalent integration and capacity ramp costs?

### EOG — EOG Resources, Inc.

Type: portfolio | Status: active | Priority: medium | Readiness: medium_high

Thesis state:
- Status: preliminary
- Conviction: unknown
- PM decision: in portfolio; valuation sensitivity work pending if needed
- Summary: EOG Deep Dive completed as pre-valuation pack. Portfolio name per user clarification. Core analytical focus is through-cycle shale FCF, oil/gas/NGL sensitivity, capital discipline, Encino/Utica impact and balance sheet resilience.

Coverage:
- Deep Dive: yes — financial-research/financial_system/deep_dives/EOG/EOG-research-deep-dive-prevaluation-report.pdf
- Model: pending_valuation_step — n/a
- Thesis: implicit_in_deep_dive — n/a

Next review action:
- Action: Build valuation/sensitivity framework for WTI, Henry Hub, NGLs, peer multiples and Encino/Utica contribution if selected.
- Priority: medium
- Owner: Charlie
- Trigger/due: PM selects EOG as next valuation step / n/a

Coverage gaps:
- medium / model: Deep Dive is complete but valuation/sensitivity model is pending. Recommended: Build WTI/HH/NGL sensitivity and peer valuation framework if PM selects EOG.

Open questions:
- What mid-cycle WTI/HH/NGL deck should anchor valuation?
- How much incremental value does Encino/Utica create after integration costs?
- What peer multiple/sensitivity framework best captures EOG quality premium?
- How resilient are capital returns in downside commodity scenarios?

### LVMH — LVMH Moët Hennessy Louis Vuitton SE

Type: portfolio | Status: active | Priority: medium | Readiness: medium_high

Thesis state:
- Status: preliminary
- Conviction: unknown
- PM decision: in portfolio; valuation/model step pending if user wants deeper work
- Summary: Deep Dive completed. Thesis work should focus on whether Fashion & Leather Goods can normalize growth/margins after the current luxury slowdown, with Sephora/Jewelry offset, China/US demand, FX and FCF quality as key variables.

Coverage:
- Deep Dive: yes — financial-research/financial_system/deep_dives/LVMH/LVMH-research-deep-dive-prevaluation-report.pdf
- Model: pending_valuation_step — n/a
- Thesis: implicit_in_deep_dive — n/a

Next review action:
- Action: Build valuation/model assumptions for F&LG recovery, margin normalization, China/US demand and FCF quality if selected.
- Priority: medium
- Owner: Charlie
- Trigger/due: PM selects LVMH as next valuation step / n/a

Coverage gaps:
- medium / model: Deep Dive is complete but explicit valuation/model assumptions are pending. Recommended: Build valuation assumptions around F&LG recovery, segment margins, FX, Sephora/Jewelry offset and FCF quality.

Open questions:
- What normalized F&LG growth/margin should be used after the luxury slowdown?
- How much of current weakness is cyclical vs brand-specific?
- What valuation multiple is justified versus Hermes/Kering/Richemont under slower growth?
- How resilient is FCF after leases, capex and working capital normalization?

### RACE — Ferrari N.V.

Type: portfolio | Status: active | Priority: medium | Readiness: medium_high

Thesis state:
- Status: research_completed_prevaluation
- Conviction: unknown
- PM decision: None
- Summary: RACE Deep Dive pre-valuation completed. Thesis work should focus on scarcity-compatible growth, ASP/mix/personalization, EV transition economics, normalized EBIT margin and industrial FCF durability.

Coverage:
- Deep Dive: yes — financial-research/financial_system/deep_dives/RACE/RACE-research-deep-dive-prevaluation-report.pdf
- Model: pending_valuation_step — n/a
- Thesis: implicit_in_deep_dive — n/a

Next review action:
- Action: Build valuation/model assumptions for shipments, ASP/mix, EBIT margin and industrial FCF if this becomes next analytical priority.
- Priority: medium
- Owner: Charlie
- Trigger/due: PM selects RACE as next valuation step / n/a

Coverage gaps:
- medium / model: Deep Dive is complete but explicit valuation/model assumptions are pending. Recommended: Build valuation assumption sheet if PM wants to complete coverage.

Open questions:
- How much volume growth is compatible with scarcity?
- Can EV transition preserve Ferrari economics?
- What normalized margin is sustainable through cycles?

### MSFT — Microsoft Corporation

Type: portfolio | Status: active | Priority: high | Readiness: high

Thesis state:
- Status: valuation_integrated
- Conviction: unknown
- PM decision: None
- Summary: Deep Dive v1.2, user valuation model v1.2 and thesis memo v1.1 integrated. Current framing: high-quality enterprise software/cloud compounder with AI upside, but valuation depends primarily on AI capex normalization and FCF conversion.

Coverage:
- Deep Dive: yes — financial-research/financial_system/deep_dives/MSFT/MSFT-research-deep-dive-v1.2-prevaluation-report.pdf
- Model: yes — financial-research/financial_system/deep_dives/MSFT/MSFT_v1_2_valuation_model.xlsx
- Thesis: yes — financial-research/financial_system/deep_dives/MSFT/MSFT-investment-thesis-v1.1-qualitative.md

Next review action:
- Action: Monitor events and revisit only if AI capex normalization, Azure/Copilot monetization or FCF conversion assumptions change.
- Priority: low
- Owner: Charlie
- Trigger/due: Material event, earnings update, or model assumption change / n/a

Coverage gaps:
- None material for current reporting purposes.

Open questions:
- Can terminal capex/revenue normalize toward the model’s ~15% assumption without impairing AI/cloud growth?
- How much of AI capex is offensive ROI-generating capacity versus defensive participation cost?
- What valuation multiple is justified if AI structurally lowers FCF conversion versus the historical software profile?
- At what price range does MSFT compensate enough for capex and multiple-compression risk?

### NFLX — Netflix, Inc.

Type: portfolio | Status: active | Priority: high | Readiness: high

Thesis state:
- Status: research_pack_completed
- Conviction: unknown
- PM decision: None
- Summary: NFLX Deep Dive v1.0 completed as pre-valuation pack. No new valuation workflow is active; prior workflow opening was a misunderstanding of a DVN request.

Coverage:
- Deep Dive: yes — financial-research/financial_system/deep_dives/NFLX/NFLX-research-deep-dive-v1.0-prevaluation-report.pdf
- Model: yes — financial-research/financial_system/deep_dives/NFLX/NFLX_v1_valuation_model.xlsx
- Thesis: implicit_in_deep_dive — n/a

Next review action:
- Action: Monitor streaming economics, ads scale, pricing/paid-sharing normalization and FCF; revisit on material event or model change.
- Priority: low
- Owner: Charlie
- Trigger/due: Material event, earnings update, or model assumption change / n/a

Coverage gaps:
- low / thesis: Standalone thesis memo is less explicit than MSFT; thesis is mostly embedded in Deep Dive/model artifacts. Recommended: Create standalone thesis memo only if PM wants committee-style output.

Open questions:
- Build standalone and post-WBD valuation scenarios separately.
- Confirm Q1 2026 net income one-offs before annualizing.
- Estimate ads margin and cannibalization effects.
- Normalize paid-sharing/pricing tailwinds for 2027+.

### UBER — Uber Technologies, Inc.

Type: portfolio | Status: active | Priority: low | Readiness: medium_high

Thesis state:
- Status: not_started
- Conviction: unknown
- PM decision: in portfolio; low reporting priority because thesis/model are comparatively better developed
- Summary: Initial Company State placeholder. User thesis has not been formalized in the system yet.

Coverage:
- Deep Dive: not_in_repo_or_not_linked — n/a
- Model: exists_outside_repo_or_not_linked — n/a
- Thesis: developed_but_not_fully_linked — n/a

Next review action:
- Action: Keep UBER low priority; optionally link existing thesis/model artifacts when convenient, but do not allocate near-term analytical capacity.
- Priority: low
- Owner: Charlie
- Trigger/due: Housekeeping pass or PM requests UBER refresh / n/a

Coverage gaps:
- low / state_quality: Repo links to existing thesis/model artifacts are incomplete, but user clarified the thesis is comparatively well developed. Recommended: Optionally link existing thesis/model artifacts later; do not prioritize over less-developed names.

Open questions:
- How durable is Delivery margin expansion?
- Can Mobility sustain pricing/take-rate without demand damage?
- Does AV become margin tailwind or platform risk?

## Watchlist / ideas

### AMZN — Amazon.com, Inc.

Type: watchlist | Status: research_pending | Priority: medium | Readiness: medium_low
Next action: Decide whether AMZN as watchlist/idea should be promoted into full Deep Dive/model work.
Coverage gaps:
- medium / deep_dive: AMZN is watchlist/idea with preliminary report only; no Deep Dive/model yet.

## Open tasks and workflow

- TASK-2026-05-17-001 — NVO — financial_extract — medium: Translate NVO research findings into valuation/model inputs: normalized 2027-2030 revenue/margin trajectory, US pricing pressure, oral Wegovy contribution, CAPEX/FCF and pipeline scenario assumptions. Close criteria: Valuation input sheet or structured model assumptions completed with source-backed base/downside/upside cases and open questions for Portfolio Manager review.

## Recent registered outputs

- OUT-2026-05-17-006 — SCOUT — system_report — Scout Pilot 2 Report v0.1 — SCOUT_PILOT_2_REPORT_V0_1.md
- OUT-2026-05-18-001 — MSFT — valuation_inputs — MSFT valuation model v1.2 — financial-research/financial_system/deep_dives/MSFT/MSFT_v1_2_valuation_model.xlsx
- OUT-2026-05-18-002 — MSFT — memo — MSFT qualitative thesis memo v1.1 — financial-research/financial_system/deep_dives/MSFT/MSFT-tesis-cualitativa-comite-v1.1.pdf
- OUT-2026-05-22-001 — DVN — valuation_inputs — DVN valuation model v1.1 — financial-research/docs/models/DVN/DVN_Valoracion_v1_1.xlsx
- OUT-2026-05-22-002 — PORTFOLIO — system_report — Portfolio Review v0.1 — 2026-05-22 — financial-research/financial_system/portfolio/reports/2026-05-22-portfolio-review-v0.1.md
- OUT-2026-05-22-003 — PORTFOLIO — system_report — Portfolio Reporting v0.1 Validation Notes — portfolio/portfolio-reporting-v0.1-validation-notes.md

## Coverage gaps summary

- DVN: high/model — User valuation model v1.1 exists but needs formula/assumption/sensitivity review before full reporting confidence.
- NVO: high/model — Open task exists for valuation/model inputs after Deep Dive.
- EOG: medium/model — Deep Dive is complete but valuation/sensitivity model is pending.
- LVMH: medium/model — Deep Dive is complete but explicit valuation/model assumptions are pending.
- RACE: medium/model — Deep Dive is complete but explicit valuation/model assumptions are pending.
- NFLX: low/thesis — Standalone thesis memo is less explicit than MSFT; thesis is mostly embedded in Deep Dive/model artifacts.
- UBER: low/state_quality — Repo links to existing thesis/model artifacts are incomplete, but user clarified the thesis is comparatively well developed.
- AMZN: medium/deep_dive — AMZN is watchlist/idea with preliminary report only; no Deep Dive/model yet.

## PM review queue

1. DVN (portfolio) — high — Review DVN valuation model v1.1: formulas, assumptions, commodity sensitivity, FCF durability, capital returns, leverage and merger execution. Owner: Charlie.
2. NVO (portfolio) — high — Complete NVO valuation/model input sheet: normalized 2027-2030 revenue/margin, US pricing, oral Wegovy, CAPEX/FCF and scenarios. Owner: Charlie.
3. EOG (portfolio) — medium — Build valuation/sensitivity framework for WTI, Henry Hub, NGLs, peer multiples and Encino/Utica contribution if selected. Owner: Charlie.
4. LVMH (portfolio) — medium — Build valuation/model assumptions for F&LG recovery, margin normalization, China/US demand and FCF quality if selected. Owner: Charlie.
5. RACE (portfolio) — medium — Build valuation/model assumptions for shipments, ASP/mix, EBIT margin and industrial FCF if this becomes next analytical priority. Owner: Charlie.
6. AMZN (watchlist) — medium — Decide whether AMZN as watchlist/idea should be promoted into full Deep Dive/model work. Owner: Portfolio Manager.
7. MSFT (portfolio) — low — Monitor events and revisit only if AI capex normalization, Azure/Copilot monetization or FCF conversion assumptions change. Owner: Charlie.
8. NFLX (portfolio) — low — Monitor streaming economics, ads scale, pricing/paid-sharing normalization and FCF; revisit on material event or model change. Owner: Charlie.
9. UBER (portfolio) — low — Keep UBER low priority; optionally link existing thesis/model artifacts when convenient, but do not allocate near-term analytical capacity. Owner: Charlie.

## Limitations

- No live market prices, weights, benchmark attribution or sizing included.
- No investment action recommendation.
- No fresh external Daily Radar/news sweep in this architecture-hardening pass.
- PortfolioPosition fields are placeholders unless user supplies weights/prices.

## Sources

- `portfolio/company-registry.json`
- `portfolio/companies/*.json`
- `portfolio/task-pipeline.json`
- `portfolio/output-registry.json`
- `portfolio/PORTFOLIO_STATE_CONTRACT_V0_2.md`
- `workflows/portfolio-review-v0.2.md`
