# Portfolio Review v0.1 — 2026-05-22

Report type: corrected ad hoc baseline / first portfolio reporting pass
Universe reviewed: current `portfolio/company-registry.json` companies after user correction
Caveat: this report is not an investment recommendation. It structures research state, model state, risks, open questions and next review priorities for the Portfolio Manager.

## Executive summary

- Current registry universe: 9 companies: MSFT, UBER, RACE, NVO, NFLX, DVN, AMZN, LVMH, EOG.
- Portfolio companies: MSFT, UBER, RACE, NVO, NFLX, DVN, LVMH, EOG.
- Watchlist/idea names: AMZN.
- Readiness split: high=2, medium_high=4, medium=2, medium_low=1.
- Open company tasks: 1. Current open task is primarily NVO valuation/model input work.
- User correction incorporated: EOG is in portfolio; LVMH is in portfolio; AMZN is not in portfolio and should be treated as idea/watchlist; UBER is in portfolio but low priority because the thesis is comparatively more developed.
- Main PM attention items now: NVO valuation setup, DVN model review, AMZN watchlist decision, RACE/LVMH/EOG valuation assumptions if wanted. UBER should not crowd out less-developed names.

## Portfolio coverage dashboard

| Ticker | Type | Status | Priority | Readiness | Deep Dive | Model | Thesis | Last update | Next action |
|---|---|---|---|---|---|---|---|---|---|
| MSFT | portfolio | active | high | high | yes | yes | yes | 2026-05-18 | Monitorizar eventos y revisar solo si cambian drivers/model assumptions. |
| NFLX | portfolio | active | high | high | yes | yes | implicit_in_deep_dive | 2026-05-13 | Monitorizar eventos y revisar solo si cambian drivers/model assumptions. |
| EOG | portfolio | active | medium | medium_high | yes | pending_valuation_step | implicit_in_deep_dive | 2026-05-18 | Portfolio: construir valoración/sensibilidad WTI/HH/NGL si se quiere completar cobertura. |
| LVMH | portfolio | active | medium | medium_high | yes | pending_valuation_step | implicit_in_deep_dive | 2026-05-22 | Portfolio: pasar a valuation/model assumptions si se quiere completar cobertura. |
| RACE | portfolio | active | medium | medium_high | yes | pending_valuation_step | implicit_in_deep_dive | 2026-05-21 | Pasar a valuation/model assumptions si se quiere completar cobertura. |
| UBER | portfolio | active | low | medium_high | not_in_repo_or_not_linked | exists_outside_repo_or_not_linked | developed_but_not_fully_linked | 2026-05-22 | Baja prioridad: tesis comparativamente más trabajada; solo enlazar artefactos/modelo cuando convenga. |
| DVN | portfolio | research_pending | high | medium | yes | yes_needs_review | implicit_in_preliminary_and_model | 2026-05-22 | Revisar modelo v1.1: supuestos, fórmulas, sensibilidad commodities y FCF. |
| NVO | portfolio | research_pending | high | medium | yes | open_task | implicit_in_deep_dive | 2026-05-17 | Cerrar valoración/model inputs abiertos antes de tratarla como fully covered. |
| AMZN | watchlist | research_pending | medium | medium_low | no_preliminary_only | no | preliminary | 2026-05-15 | Idea/watchlist: decidir si merece Deep Dive/modelo; no tratar como cartera actual. |

## Company review blocks

### MSFT — Microsoft Corporation

Type: portfolio | Status: active | Priority: high | Reporting readiness: high

Current thesis state:
- Status: valuation_integrated
- Conviction: unknown
- PM decision: None
- Summary: Deep Dive v1.2, user valuation model v1.2 and thesis memo v1.1 integrated. Current framing: high-quality enterprise software/cloud compounder with AI upside, but valuation depends primarily on AI capex normalization and FCF conversion.

Key drivers:
- Enterprise software switching costs and distribution strength across Office, Windows, Azure, GitHub and security.
- Azure scale, growth and margin quality as the core cloud value driver.
- Copilot/AI monetization converting infrastructure spend into higher ARPU and retention.
- Operating margin resilience while absorbing AI infrastructure, D&A and R&D intensity.
- FCF recovery as capex/revenue normalizes after the FY26-FY27 investment cycle.

Key risks:
- AI capex remains structurally high and depresses FCF conversion.
- Multiple compression if AI economics look more like capital-intensive infrastructure than software.
- Azure growth or Copilot monetization disappoints relative to the capex base.
- Cloud competition and pricing pressure from AWS, Google and other infrastructure providers.
- Regulatory/antitrust constraints around bundling, platform power and AI partnerships.

Watch metrics:
- Azure growth and AI contribution commentary
- Copilot adoption, pricing, retention and ARPU evidence
- Capex/revenue and capital lease trajectory
- D&A/revenue and maintenance capex signals
- FCF margin / FCFF revenue conversion versus model assumptions

Recent material events:
- 2026-05-13 — deep_dive: MSFT Deep Dive v1.2 approved as recurring pre-valuation methodology sample.
- 2026-05-18 — valuation_model: User MSFT valuation model v1.2 integrated into repo/dashboard. Median target $463.7, average $476.4, range $357-$604, probabilistic value ~$474; thesis remains capex-normalization dependent.
- 2026-05-18 — thesis_update: MSFT thesis refined around enterprise switching costs, Azure quality and AI upside, with capex/FCF conversion and multiple compression as the primary underwriting risk.

Research / model artifacts:
- Deep Dive: yes — financial-research/financial_system/deep_dives/MSFT/MSFT-research-deep-dive-v1.2-prevaluation-report.pdf
- Model: yes — financial-research/financial_system/deep_dives/MSFT/MSFT_v1_2_valuation_model.xlsx
- Thesis: yes — financial-research/financial_system/deep_dives/MSFT/MSFT-investment-thesis-v1.1-qualitative.md

Open questions:
- Can terminal capex/revenue normalize toward the model’s ~15% assumption without impairing AI/cloud growth?
- How much of AI capex is offensive ROI-generating capacity versus defensive participation cost?
- What valuation multiple is justified if AI structurally lowers FCF conversion versus the historical software profile?
- At what price range does MSFT compensate enough for capex and multiple-compression risk?

Next action: Monitorizar eventos y revisar solo si cambian drivers/model assumptions.

### NFLX — Netflix, Inc.

Type: portfolio | Status: active | Priority: high | Reporting readiness: high

Current thesis state:
- Status: research_pack_completed
- Conviction: unknown
- PM decision: None
- Summary: NFLX Deep Dive v1.0 completed as pre-valuation pack. No new valuation workflow is active; prior workflow opening was a misunderstanding of a DVN request.

Key drivers:
- Revenue growth by subscription/pricing/ads
- Advertising revenue scale and incremental margin
- Content spend efficiency and content amortization
- Operating margin sustainability above 30%
- FCF conversion after content cash spend

Key risks:
- Paid-sharing tailwind normalizes faster than expected
- Pricing elasticity/churn in mature markets
- Content hit-rate or cost inflation weakens FCF
- Advertising execution or cannibalization risk
- WBD transaction adds debt, integration and regulatory risk

Watch metrics:
- Revenue growth and FX-neutral growth
- Operating margin
- OCF and FCF
- Content additions and amortization
- Content liabilities/obligations

Recent material events:
- 2026-05-13 — deep_dive_requested: User requested NFLX as next Deep Dive and asked to keep Netflix discussion in dedicated portfolio thread.
- 2026-05-13 — deep_dive_completed: NFLX Deep Dive v1.0 pre-valuation pack completed with 5Y financials, content accounting, guidance/outlook, scenario matrix and valuation checklist.

Research / model artifacts:
- Deep Dive: yes — financial-research/financial_system/deep_dives/NFLX/NFLX-research-deep-dive-v1.0-prevaluation-report.pdf
- Model: yes — financial-research/financial_system/deep_dives/NFLX/NFLX_v1_valuation_model.xlsx
- Thesis: implicit_in_deep_dive — n/a

Open questions:
- Build standalone and post-WBD valuation scenarios separately.
- Confirm Q1 2026 net income one-offs before annualizing.
- Estimate ads margin and cannibalization effects.
- Normalize paid-sharing/pricing tailwinds for 2027+.

Next action: Monitorizar eventos y revisar solo si cambian drivers/model assumptions.

### EOG — EOG Resources, Inc.

Type: portfolio | Status: active | Priority: medium | Reporting readiness: medium_high

Current thesis state:
- Status: preliminary
- Conviction: unknown
- PM decision: in portfolio; valuation sensitivity work pending if needed
- Summary: EOG Deep Dive completed as pre-valuation pack. Portfolio name per user clarification. Core analytical focus is through-cycle shale FCF, oil/gas/NGL sensitivity, capital discipline, Encino/Utica impact and balance sheet resilience.

Key drivers:
- WTI/HH/NGL realized prices
- Well productivity and drilling returns
- Capital discipline and reinvestment rate
- Encino/Utica contribution and integration
- FCF conversion through cycle

Key risks:
- Commodity price downside
- Cost inflation and service costs
- Well productivity degradation
- M&A/integration risk
- Regulatory/environmental constraints

Watch metrics:
- Production volumes and mix
- Realized prices
- Capex/reinvestment rate
- FCF and FCF yield
- Net debt/leverage

Recent material events:
- 2026-05-18 — deep_dive_completed: EOG Deep Dive pre-valuation PDF completed with 5-year financials, production/guidance, Encino/Utica impact, balance sheet, risks and scenario matrix.

Research / model artifacts:
- Deep Dive: yes — financial-research/financial_system/deep_dives/EOG/EOG-research-deep-dive-prevaluation-report.pdf
- Model: pending_valuation_step — n/a
- Thesis: implicit_in_deep_dive — n/a

Open questions:
- What mid-cycle WTI/HH/NGL deck should anchor valuation?
- How much incremental value does Encino/Utica create after integration costs?
- What peer multiple/sensitivity framework best captures EOG quality premium?
- How resilient are capital returns in downside commodity scenarios?

Next action: Portfolio: construir valoración/sensibilidad WTI/HH/NGL si se quiere completar cobertura.

### LVMH — LVMH Moët Hennessy Louis Vuitton SE

Type: portfolio | Status: active | Priority: medium | Reporting readiness: medium_high

Current thesis state:
- Status: preliminary
- Conviction: unknown
- PM decision: in portfolio; valuation/model step pending if user wants deeper work
- Summary: Deep Dive completed. Thesis work should focus on whether Fashion & Leather Goods can normalize growth/margins after the current luxury slowdown, with Sephora/Jewelry offset, China/US demand, FX and FCF quality as key variables.

Key drivers:
- Fashion & Leather Goods organic growth recovery
- Louis Vuitton/Dior brand desirability and pricing power
- Sephora and Jewelry offset to luxury soft patch
- China/Asia and US luxury demand normalization
- Operating leverage and cost discipline

Key risks:
- Prolonged luxury demand downturn
- Brand dilution or pricing fatigue
- China weakness lasting longer than expected
- FX and tourism flow headwinds
- Wines & Spirits inventory/channel pressure

Watch metrics:
- Fashion & Leather Goods organic revenue growth
- Segment operating margin
- China/Asia ex-Japan and US revenue trends
- Sephora selective retailing growth/margin
- Wines & Spirits organic growth and inventory commentary

Recent material events:
- 2026-05-22 — deep_dive_completed: LVMH Deep Dive completed with FY2021-2025 financials, Q1 2026 update, segment/geography analysis, FCF/debt review, risks and scenario matrix.

Research / model artifacts:
- Deep Dive: yes — financial-research/financial_system/deep_dives/LVMH/LVMH-research-deep-dive-prevaluation-report.pdf
- Model: pending_valuation_step — n/a
- Thesis: implicit_in_deep_dive — n/a

Open questions:
- What normalized F&LG growth/margin should be used after the luxury slowdown?
- How much of current weakness is cyclical vs brand-specific?
- What valuation multiple is justified versus Hermes/Kering/Richemont under slower growth?
- How resilient is FCF after leases, capex and working capital normalization?

Next action: Portfolio: pasar a valuation/model assumptions si se quiere completar cobertura.

### RACE — Ferrari N.V.

Type: portfolio | Status: active | Priority: medium | Reporting readiness: medium_high

Current thesis state:
- Status: research_completed_prevaluation
- Conviction: unknown
- PM decision: None
- Summary: RACE Deep Dive pre-valuation completed. Thesis work should focus on scarcity-compatible growth, ASP/mix/personalization, EV transition economics, normalized EBIT margin and industrial FCF durability.

Key drivers:
- Volume discipline and scarcity
- Pricing and personalization mix
- Order book depth
- Margin resilience
- Electrification transition without brand dilution

Key risks:
- Brand dilution from volume growth
- Luxury demand slowdown
- Execution risk in EV/hybrid transition
- FX and geographic mix
- Formula 1/brand perception volatility

Watch metrics:
- Shipments
- ASP/mix
- EBITDA margin
- Order book commentary
- Personalization contribution

Recent material events:
- 2026-05-21 — deep_dive_completed: Ferrari RACE pre-valuation Deep Dive PDF completed.
- 2026-05-05 — results: Q1 2026 results: guidance confirmed, EBITDA margin 39.1%, industrial FCF €653m, order book toward end-2027.

Research / model artifacts:
- Deep Dive: yes — financial-research/financial_system/deep_dives/RACE/RACE-research-deep-dive-prevaluation-report.pdf
- Model: pending_valuation_step — n/a
- Thesis: implicit_in_deep_dive — n/a

Open questions:
- How much volume growth is compatible with scarcity?
- Can EV transition preserve Ferrari economics?
- What normalized margin is sustainable through cycles?

Next action: Pasar a valuation/model assumptions si se quiere completar cobertura.

### UBER — Uber Technologies, Inc.

Type: portfolio | Status: active | Priority: low | Reporting readiness: medium_high

Current thesis state:
- Status: not_started
- Conviction: unknown
- PM decision: in portfolio; low reporting priority because thesis/model are comparatively better developed
- Summary: Initial Company State placeholder. User thesis has not been formalized in the system yet.

Key drivers:
- Mobility bookings and take-rate quality
- Delivery margin durability
- Uber One adoption and cross-platform frequency
- Advertising and marketplace monetization
- Autonomous vehicle strategy/partnerships

Key risks:
- Regulatory/labor classification pressure
- Local competition and incentives
- Delivery margin fragility
- Insurance/legal cost inflation
- AV disintermediation risk

Watch metrics:
- Gross bookings by segment
- Trips / MAPCs
- Take rate
- Adjusted EBITDA by segment
- FCF conversion

Recent material events:
- No recent material events recorded in Company State.

Research / model artifacts:
- Deep Dive: not_in_repo_or_not_linked — n/a
- Model: exists_outside_repo_or_not_linked — n/a
- Thesis: developed_but_not_fully_linked — n/a

Open questions:
- How durable is Delivery margin expansion?
- Can Mobility sustain pricing/take-rate without demand damage?
- Does AV become margin tailwind or platform risk?

Next action: Baja prioridad: tesis comparativamente más trabajada; solo enlazar artefactos/modelo cuando convenga.

### DVN — Devon Energy Corporation

Type: portfolio | Status: research_pending | Priority: high | Reporting readiness: medium

Current thesis state:
- Status: preliminary_report_completed
- Conviction: unknown
- PM decision: None
- Summary: DVN preliminary report completed. Main issue: assess combined Devon/Coterra through-cycle FCF and capital returns under conservative commodity assumptions before considering a full Deep Dive.

Key drivers:
- Oil/gas price realization
- Production volumes and well productivity
- Capex discipline
- FCF generation through cycle
- Dividend/buyback framework

Key risks:
- Commodity price downside
- Cost inflation
- Reserve/productivity deterioration
- M&A integration/execution
- Capital allocation procyclicality

Watch metrics:
- Production volumes
- Realized prices
- Capex
- FCF
- Net debt/leverage

Recent material events:
- 2026-05-15 — preliminary_report_requested: User requested dedicated DVN thread and preliminary report.
- 2026-05-22 — valuation_model_received: User supplied DVN valuation model v1.1; model stored and surfaced in the GitHub dashboard.

Research / model artifacts:
- Deep Dive: yes — financial-research/financial_system/deep_dives/DVN/DVN-research-prevaluation-v0.2-report.pdf
- Model: yes_needs_review — financial-research/docs/models/DVN/DVN_Valoracion_v1_1.xlsx
- Thesis: implicit_in_preliminary_and_model — n/a

Open questions:
- What mid-cycle oil/gas price supports current FCF thesis?
- Is capital return sustainable through commodity downturns?
- Does M&A improve or dilute asset quality?

Next action: Revisar modelo v1.1: supuestos, fórmulas, sensibilidad commodities y FCF.

### NVO — Novo Nordisk A/S

Type: portfolio | Status: research_pending | Priority: high | Reporting readiness: medium

Current thesis state:
- Status: under_review
- Conviction: unknown
- PM decision: None
- Summary: Novo Nordisk is in research-pending status after a growth/price reset. Initial read: the company remains a GLP-1 leader with strong obesity/diabetes assets, but 2026 guidance embeds material pricing/competition pressure and lower US realised prices.

Key drivers:
- Global GLP-1 volume expansion in obesity and diabetes.
- Wegovy and oral Wegovy uptake, access and channel mix.
- Ozempic durability in diabetes despite market share pressure.
- US realised prices, rebates, Medicaid/coverage and MFN effects.
- Manufacturing capacity expansion and gross margin recovery.

Key risks:
- 2026 adjusted sales and operating profit guidance implies decline at CER due to lower realised prices and competition.
- US Operations pressure from pricing, coverage changes and competition.
- Global diabetes value share declined in 2025.
- Gross margin pressure from Catalent-site depreciation/amortisation, restructuring and capacity expansion costs.
- Patent/compound expiry impacts for semaglutide in certain International Operations markets.

Watch metrics:
- Obesity care sales growth and branded GLP-1 obesity volume share.
- Wegovy prescription trends, including oral Wegovy launch metrics.
- Ozempic sales growth and GLP-1 diabetes value share.
- US vs International Operations sales growth.
- Gross margin and operating margin bridge, including restructuring/Catalent effects.

Recent material events:
- 2026-02-03 — results_outlook: Novo Nordisk reported 2025 sales of DKK 309.064bn (+6% reported, +10% CER) and operating profit of DKK 127.658bn (-1% reported, +6% CER). 2026 adjusted sales and adjusted operating profit growth guidance: -5% to -13% at CER.
- 2025-12-22 — product_approval: US FDA approved once-daily oral semaglutide 25 mg for obesity under Wegovy pill; launched 5 January 2026 with around 50,000 weekly prescriptions as of 23 January, per company announcement.
- 2026-05-06 — earnings_release: Q1 2026 investor presentation: adjusted sales DKK 70.063bn (-4% CER) and adjusted operating profit DKK 32.858bn (-6% CER); outlook raised to adjusted sales and adjusted operating profit growth of -4% to -12% CER, driven by higher GLP-1 expectations. Wegovy pill reached >1m US patients since launch and ~207k weekly TRx as of 17 Apr 2026.

Research / model artifacts:
- Deep Dive: yes — financial-research/financial_system/deep_dives/NVO/NVO-research-deep-dive-prevaluation-report.pdf
- Model: open_task — TASK-2026-05-17-001
- Thesis: implicit_in_deep_dive — n/a

Open questions:
- What is the normalised 2027-2030 revenue/margin trajectory after 2026 pricing reset?
- How much oral Wegovy is incremental vs cannibalising injectable Wegovy/GLP-1 demand?
- What share and price assumptions are required for Novo to defend premium valuation vs Lilly?
- How should we adjust margins for restructuring, Catalent integration and capacity ramp costs?

Next action: Cerrar valoración/model inputs abiertos antes de tratarla como fully covered.

### AMZN — Amazon.com, Inc.

Type: watchlist | Status: research_pending | Priority: medium | Reporting readiness: medium_low

Current thesis state:
- Status: preliminary_report_completed
- Conviction: unknown
- PM decision: idea/watchlist; not current portfolio position
- Summary: AMZN preliminary report completed. Core issue: separate AWS/AI, advertising, and retail/logistics economics; test whether AI/cloud capex produces enough incremental return to justify lower near-term FCF conversion.

Key drivers:
- AWS growth and AI infrastructure ROI
- Advertising growth and incremental margin
- Retail/logistics efficiency
- Prime engagement and marketplace take rate
- Capex intensity and FCF conversion

Key risks:
- AI capex fails to earn attractive returns
- AWS growth/pricing pressure from Azure/GCP
- Retail/logistics margin pressure
- Regulatory/antitrust intervention
- International profitability drag

Watch metrics:
- AWS revenue growth and operating margin
- Advertising growth
- Operating income by segment
- OCF, capex and lease-adjusted FCF
- Capex/revenue

Recent material events:
- 2026-05-15 — preliminary_report_requested: User requested preliminary report on Amazon and dedicated AMZN workflow was opened.

Research / model artifacts:
- Deep Dive: no_preliminary_only — financial-research/financial_system/preliminary_reports/AMZN/AMZN-preliminary-report-v0.md
- Model: no — n/a
- Thesis: preliminary — n/a

Open questions:
- How much of current capex is AI/cloud vs fulfillment/logistics?
- What normalized AWS margin is realistic after AI depreciation?
- What is advertising revenue/margin contribution by channel?
- What consolidated FCF conversion should be normalized for valuation?

Next action: Idea/watchlist: decidir si merece Deep Dive/modelo; no tratar como cartera actual.

## Open tasks and workflow

- TASK-2026-05-17-001 — NVO — financial_extract — medium: Translate NVO research findings into valuation/model inputs: normalized 2027-2030 revenue/margin trajectory, US pricing pressure, oral Wegovy contribution, CAPEX/FCF and pipeline scenario assumptions. Close criteria: Valuation input sheet or structured model assumptions completed with source-backed base/downside/upside cases and open questions for Portfolio Manager review.

Recently closed relevant tasks:
- TASK-2026-05-13-002 — PORTFOLIO — dashboard_update — closed 2026-05-17: Closed: dashboard consumes registry, task pipeline, company states and daily radar files; build validated during Phase 1.5 operational pass.
- TASK-2026-05-17-002 — SYSTEM — workflow_hardening — closed 2026-05-17: Controlled foundation rehearsal completed: task routed to ops_maintenance lane, output created and registered, events logged, portfolio mirror synced, dashboard rebuilt, robustness/system-health run, and validation passed with only known accepted warnings.
- TASK-2026-05-17-003 — SYSTEM — source_pack — closed 2026-05-17: Scout completed first read-only source-finding pilot successfully: primary company sources used, page/URL references included, confidence and missing data explicit, no state mutation or external action performed.
- TASK-2026-05-17-004 — SYSTEM — monitoring_followup — closed 2026-05-17: Scout completed second read-only monitoring-style pilot successfully: official company sources used, source existence/date/type identified, confidence and missing data explicit, no state mutation or external action performed.
- TASK-2026-05-18-001 — EOG — deep_dive — closed 2026-05-18: EOG Deep Dive pre-valuation PDF completed with 5-year financials, production/guidance, Encino/Utica impact, balance sheet, risks and scenario matrix.
- TASK-2026-05-21-001 — RACE — deep_dive — closed 2026-05-21: RACE Deep Dive pre-valuation PDF completed with 5-year financials, Q1 2026/guidance, scarcity economics, balance sheet, capital allocation, risks and scenario matrix.
- TASK-2026-05-22-001 — LVMH — deep_dive — closed 2026-05-22: LVMH Deep Dive completed with FY2021-2025 financials, segment/geography analysis, FCF/debt review, Q1 2026 update, risks and scenario matrix.

## Coverage gaps

- AMZN: idea/watchlist only; preliminary report exists but no Deep Dive/model yet.
- NVO: Deep Dive complete but valuation/model inputs still open.
- DVN: model exists but needs review/checking before full confidence reporting.
- RACE/LVMH/EOG: Deep Dives complete; explicit valuation/model assumptions pending.
- UBER: in portfolio but should be low priority; thesis/model are comparatively more developed, although repo links are incomplete.

## PM review queue

1. NVO — close valuation/model input task or define next concrete output.
2. DVN — review user model v1.1 assumptions/formulas and commodity sensitivities.
3. AMZN — as watchlist/idea, decide whether to convert preliminary report into full Deep Dive/model work.
4. RACE/LVMH/EOG — decide whether to proceed to valuation/model assumptions.
5. UBER — low priority; optionally link existing thesis/model artifacts later, but do not prioritize over less-developed names.

## v0.1 limitations

- No live market prices, weights, benchmark attribution or portfolio sizing included.
- No automatic earnings calendar yet.
- No buy/sell/trim/add recommendations.
- Readiness is based on repository artifacts and Company State metadata, not on a fresh external news sweep.

## Sources

- `portfolio/company-registry.json`
- `portfolio/companies/*.json`
- `portfolio/task-pipeline.json`
- `portfolio/portfolio-reporting-coverage-audit-v0.1.md`
- `portfolio/PORTFOLIO_REPORTING_V0_1.md`
