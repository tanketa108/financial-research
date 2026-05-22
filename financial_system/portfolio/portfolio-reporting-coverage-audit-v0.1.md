# Portfolio Reporting Coverage Audit v0.1

Date: 2026-05-22
Owner: Charlie
Purpose: Hito 1 for Portfolio Reporting v0.1 — audit current company coverage before normalizing Company State and producing recurring portfolio reporting.

## Executive summary

The portfolio now has enough real coverage to start Portfolio Reporting v0.1. Coverage is uneven, but that is acceptable: the first reporting layer should explicitly distinguish between fully covered companies, partially covered companies, and companies still requiring model/thesis completion.

Current universe in `portfolio/company-registry.json`: 9 companies after user correction.

- Full or near-full reporting candidates: MSFT, NFLX, RACE, LVMH, EOG, and UBER from user thesis/model context.
- Good research base but next model/valuation work pending: NVO, DVN.
- Early/preliminary state: AMZN, explicitly idea/watchlist rather than portfolio.
- UBER is in portfolio but low priority because user clarified it is one of the better-developed theses; repo links should be improved later but it should not drive near-term work.
- EOG corrected into portfolio registry.

Key conclusion: start with a pragmatic report that surfaces coverage quality rather than pretending every company has equal maturity.

## Coverage table

| Ticker | Type | Registry status | Priority | Company State | Deep Dive | User model / valuation artifact | Thesis artifact | Open tasks | Thread | Reporting readiness |
|---|---|---|---|---|---|---|---|---:|---|---|
| MSFT | portfolio | active | high | yes | yes, v1.2 | yes, valuation model v1.2 + integration | yes, qualitative thesis | 0 | yes | high |
| NFLX | portfolio | active | high | yes | yes, v1.0 | yes, valuation model files present | no standalone thesis file detected | 0 | yes | high |
| RACE | portfolio | active | medium | yes | yes | valuation/model references present, valuation step still pending | no standalone thesis file detected | 0 | yes | medium-high |
| LVMH | watchlist | active | medium | no | yes | valuation/model references present, valuation step pending | no standalone thesis file detected | 0 | yes | medium-high, needs Company State |
| NVO | portfolio | research_pending | high | yes | yes | valuation input task open | no standalone thesis file detected | 1 | yes | medium, needs valuation/model normalization |
| DVN | portfolio | research_pending | high | yes | yes | yes, user valuation model v1.1 stored in dashboard path | no standalone thesis file detected | 0 | yes | medium, needs status cleanup and model review |
| AMZN | portfolio | research_pending | high | yes | no, preliminary report only | no | no standalone thesis file detected | 0 | yes | medium-low |
| UBER | portfolio | monitoring | medium | yes | no | no | no | 0 | no | low |
| EOG | not in registry | n/a | n/a | no | yes | valuation step pending | no standalone thesis file detected | 0 | yes | candidate to add/decide |

## Artifact evidence

### Strong coverage

- MSFT
  - Deep Dive: `financial-research/financial_system/deep_dives/MSFT/MSFT-research-deep-dive-v1.2-prevaluation-report.pdf`
  - User model: `financial-research/financial_system/deep_dives/MSFT/MSFT_v1_2_valuation_model.xlsx`
  - Model integration: `financial-research/financial_system/deep_dives/MSFT/MSFT-valuation-model-integration-v1.3.md`
  - Thesis artifacts: multiple `MSFT-investment-thesis-*` and `MSFT-tesis-cualitativa-*` files.

- NFLX
  - Deep Dive: `financial-research/financial_system/deep_dives/NFLX/NFLX-research-deep-dive-v1.0-prevaluation-report.pdf`
  - Model: `financial-research/financial_system/deep_dives/NFLX/NFLX_v1_valuation_model.xlsx`
  - Model integration: `financial-research/financial_system/deep_dives/NFLX/NFLX-valuation-model-integration-v1.0.md`

- RACE
  - Deep Dive: `financial-research/financial_system/deep_dives/RACE/RACE-research-deep-dive-prevaluation-report.pdf`
  - Valuation/model next step remains explicit rather than completed.

- LVMH
  - Deep Dive: `financial-research/financial_system/deep_dives/LVMH/LVMH-research-deep-dive-prevaluation-report.pdf`
  - Missing canonical `portfolio/companies/LVMH.json` Company State.

### Partial coverage

- NVO
  - Deep Dive: `financial-research/financial_system/deep_dives/NVO/NVO-research-deep-dive-prevaluation-report.pdf`
  - Open task: `TASK-2026-05-17-001` for valuation/model inputs.
  - Issue: local Company State uses `status: research_active`, which is outside current schema allowed statuses. Needs normalization.

- DVN
  - Deep Dive/report: `financial-research/financial_system/deep_dives/DVN/DVN-research-prevaluation-v0.2-report.pdf`
  - User model: `financial-research/docs/models/DVN/DVN_Valoracion_v1_1.xlsx` and system valuation path referenced in Company State.
  - Needs model review/formula/sensitivity pass.

- AMZN
  - Preliminary report recorded in Company State.
  - No Deep Dive/model yet.

### Weak coverage / cleanup

- UBER
  - Company State exists but no thread, Deep Dive, model or research output.
  - Should be included in reporting as `monitoring / insufficient coverage`, not treated as fully covered.

- EOG
  - Completed Deep Dive exists and task is closed.
  - Not currently in `portfolio/company-registry.json` and no canonical Company State.
  - Need user/Core decision: add as portfolio/watchlist/idea or leave outside current reporting universe.

## Issues to fix in Hito 2

1. Create canonical `portfolio/companies/LVMH.json`.
2. EOG enters the reporting universe as portfolio; add registry + Company State. Completed.
3. Normalize NVO Company State status from non-schema `research_active` to allowed status. Completed as `research_pending`.
4. Ensure registry `lastDeepDive` fields match actual completed outputs for NVO and DVN.
5. Add a lightweight reporting coverage block to each Company State:
   - `coverage.deepDive`: yes/no/path/date
   - `coverage.model`: yes/no/path/date/status
   - `coverage.thesis`: yes/no/status
   - `coverage.reportingReadiness`: high/medium/low
6. Keep `UBER` visible but clearly marked as low readiness.

## Recommended sequencing

Hito 2 should not try to rewrite all research. It should normalize metadata only:

- complete missing Company State for LVMH,
- fix invalid statuses,
- add coverage/readiness metadata,
- mirror to `financial-research/financial_system/portfolio/*`,
- validate task ledger and dashboard build.

Then Hito 3 can define the recurrent Portfolio Report format using real coverage tiers.
