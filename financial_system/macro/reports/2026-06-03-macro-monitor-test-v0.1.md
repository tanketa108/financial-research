# Macro Monitor Test v0.1 — 2026-06-03

Status: test report / first usable macro monitor draft
Scope: US macro monitor
Owner: Charlie / Financial Research System

## 1. Executive macro summary

- Current macro regime: **incomplete data spine; liquidity block usable, rates/inflation/labor/growth still pending live series.** Treat this as a liquidity-and-calendar monitor, not a full macro regime call.
- Main change since last monitor: **the liquidity section now closes the TGA + RRP + reserve balances triangle** using public/keyless sources.
- Highest-signal release/event ahead: **FOMC Rate Decision / Statement / SEP on 2026-06-17 at 14:00 ET**, because policy guidance and SEP dots can reset the interpretation of rates, liquidity and risk appetite.
- Key uncertainty: whether the apparent liquidity cross-current — **TGA rising, RRP falling, reserve balances rising over the selected window** — persists or reverses once the next weekly reserve balance observation and Treasury cash movements arrive.

Bottom line: **monitor-only.** The current liquidity picture is mixed rather than cleanly supportive or restrictive. Rising TGA is a mechanical reserve drain; falling RRP partly offsets; reserve balances are up over the 10-observation window but down on the latest weekly change. Do not convert this into a standalone bullish/bearish portfolio signal.

Caveat: this v0.1 test report uses official/public source tracking and explicit placeholders where the data spine is not yet connected. It is suitable for workflow testing, not publication-grade macro research.

## 2. Upcoming releases

Window: 2026-06-03 to 2026-08-02

- **2026-06-17 14:00 ET** — FOMC Rate Decision / Statement / SEP (June 2026 FOMC); status: `confirmed_official_calendar`; source: <https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm>
- **2026-06-25 08:30 ET** — Gross Domestic Product (Q1 2026 third estimate); status: `confirmed_official_calendar`; source: <https://www.bea.gov/news/schedule>
- **2026-06-25 08:30 ET** — Personal Income and Outlays / PCE Prices (May 2026); status: `confirmed_official_calendar`; source: <https://www.bea.gov/news/schedule>
- **2026-07-30 08:30 ET** — Gross Domestic Product (Q2 2026 advance estimate); status: `confirmed_official_calendar`; source: <https://www.bea.gov/news/schedule>
- **2026-07-30 08:30 ET** — Personal Income and Outlays / PCE Prices (June 2026); status: `confirmed_official_calendar`; source: <https://www.bea.gov/news/schedule>

Pending manual confirmation:
- Consumer Price Index — BLS schedule page must be checked manually or through an approved access method; automated fetch returned 403.
- Employment Situation / Nonfarm Payrolls — BLS schedule page must be checked manually or through an approved access method; automated fetch returned 403.

## 3. Rates & curve

Data status: `pending FRED_API_KEY / data spine`

Current read: **not enough live rate data connected for a rates regime call.** This is the most important gap before the monitor can be considered macro-complete.

To track next:

- Fed funds / target range
- 2Y Treasury yield
- 10Y Treasury yield
- 30Y Treasury yield
- 10Y-2Y and/or 10Y-3M spread

Interpretation:

- Curve signal: `not available yet`
- Policy expectations signal: `not available yet`
- Risk / caveat: liquidity context without rates can mislead; rates/curve should be the next source block.

## 4. Inflation

Data status: `partial calendar ready; historical data pending FRED_API_KEY / official release ingestion`

Current read: **calendar visibility exists, inflation momentum does not yet.** PCE release dates are confirmed via BEA; CPI requires BLS access workaround/manual confirmation.

To track:

- CPI headline/core MoM and YoY
- PCE headline/core MoM and YoY
- PPI where useful for pipeline/PCE read-through

Interpretation placeholder:

- Inflation momentum: `pending`
- Services/shelter/core pressure: `pending`
- Fed relevance: important once linked, especially before/after FOMC and PCE releases.

## 5. Labor market

Data status: `calendar pending BLS manual confirmation; historical data pending FRED_API_KEY / official release ingestion`

Current read: **not connected.** Labor cannot yet be used in the macro summary except as a known missing pillar.

To track:

- Nonfarm payrolls
- Unemployment rate
- Participation rate
- Average hourly earnings
- Initial/continued claims
- JOLTS openings/quits

Interpretation placeholder:

- Labor demand: `pending`
- Wage pressure: `pending`
- Cooling/tightness signal: `pending`

## 6. Growth / activity

Data status: `BEA calendar ready for GDP; other Census/Fed releases require event confirmation`

Current read: **release calendar is partially usable; live activity indicators are not yet connected.** GDP/PCE dates can drive monitoring, but not yet a growth call.

To track:

- GDP and domestic private demand
- Retail sales / control group
- Durable goods / core capex
- Industrial production
- Housing starts/permits

Interpretation placeholder:

- Growth momentum: `pending`
- Consumer/capex split: `pending`
- Cyclical risk: `pending`

## 7. Liquidity / Treasury

Data status: `Treasury FiscalData, NY Fed Markets and FRED public CSV reachable; TGA/RRP/reserve balances extraction v0 active`

### Treasury General Account

- Source: Treasury FiscalData Daily Treasury Statement; record date: **2026-06-01**; units: `USD millions`.
- TGA opening balance: **$903,881mn**.
- Total TGA deposits: **$280,267mn**.
- Total TGA withdrawals: **$327,307mn**.
- TGA one-day change: **+$54,171mn** vs prior available DTS record.
- TGA 10-record trend (2026-05-18 → 2026-06-01): **+$145,062mn**; direction: `rising`.
- Recent TGA history, latest first:
  - 2026-06-01: $903,881mn
  - 2026-05-29: $849,710mn
  - 2026-05-28: $842,660mn
  - 2026-05-27: $881,329mn
  - 2026-05-26: $825,550mn
- Source URL: <https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance>
- Caveat: Treasury accounting fields need exact source definitions; treat this as liquidity context, not a standalone signal.

### NY Fed reverse repo

- Source: NY Fed Markets API; latest operation date: **2026-06-02**; units: `USD billions`.
- Total accepted RRP amount: **$2.502bn**.
- Accepted counterparties: **32.0**; award/offering rate: **3.5%**.
- RRP one-day change: **+$1.200bn** vs prior available operation.
- RRP 10-operation trend (2026-05-19 → 2026-06-02): **-$10.409bn**; direction: `falling`.
- Recent RRP history, latest first:
  - 2026-06-02: $2.502bn
  - 2026-06-01: $1.302bn
  - 2026-05-29: $11.677bn
  - 2026-05-28: $1.163bn
  - 2026-05-27: $1.853bn
- Source URL: <https://markets.newyorkfed.org/api/rp/reverserepo/all/results/last/10.csv>
- Caveat: reverse repo take-up is useful liquidity context, not a standalone macro/portfolio signal.

### Fed reserve balances

- Source: FRED public CSV `WRESBAL` / Reserve Balances with Federal Reserve Banks; latest observation: **2026-05-27**; units: `USD millions`.
- Reserve balances: **$3,066,560mn**.
- Reserve balances one-period change: **-$63,002mn** vs prior available observation.
- Reserve balances 10-observation trend (2026-03-25 → 2026-05-27): **+$72,605mn**; direction: `rising`.
- Recent reserve balances history, latest first:
  - 2026-05-27: $3,066,560mn
  - 2026-05-20: $3,129,562mn
  - 2026-05-13: $3,102,810mn
  - 2026-05-06: $3,032,588mn
  - 2026-04-29: $2,918,599mn
- Source URL: <https://fred.stlouisfed.org/graph/fredgraph.csv?id=WRESBAL&cosd=2026-01-01>
- Caveat: reserve balances improve the liquidity read, but still need funding-market context before portfolio conclusions.

### Liquidity interpretation

- Automatic liquidity read: **mixed liquidity context: rising TGA is a reserve drain, while falling RRP can partly offset by releasing cash from the facility.**
- Inputs: TGA trend `rising` (+$145,062mn over window); RRP trend `falling` (-$10.409bn over window).
- Cross-check: reserve balances trend `rising` (+$72,605mn over window), but latest weekly reserve balance change was negative (-$63,002mn). This argues for **monitoring persistence**, not making a clean call.
- Portfolio use: **monitor net effect; do not collapse it into a single bullish/bearish signal.**
- Caveat: this is a rules-based context note, not an investment conclusion; funding spreads and market plumbing stress indicators are still outside the v0 data spine.

## 8. Portfolio context

Operating rule: macro informs portfolio context; it does not make portfolio decisions.

- Portfolio areas potentially affected: broad risk appetite, banks/financials, rate-sensitive growth, cyclicals and USD/liquidity-sensitive assets.
- Relevant company/sector links: `portfolio mapping pending`; no company-specific task should be created from this liquidity read alone.
- Actionability: **monitor only.** No model update, no thesis change, no company task yet.

Escalation rule for future monitors:

- Create a portfolio task only if liquidity/rates data shows a persistent move that changes valuation sensitivity, financing conditions, or sector risk.
- Otherwise enrich Company State / Portfolio Review context without creating noise.

## 9. Open questions

- Should rates/curve be the next source block? Recommendation: **yes**, because rates are the missing bridge between macro context and portfolio valuation sensitivity.
- Do we want BLS CPI/NFP handled manually first, or solve BLS access now? Recommendation: **manual confirmation in v0.1**, automate later if friction repeats.
- Should funding stress indicators be added before inflation/labor? Recommendation: **after rates/curve**, unless the goal is specifically market-plumbing monitoring.

## 10. Source discipline

- Official source URLs must be cited for every factual release claim.
- Consensus/surprise must be omitted unless explicitly sourced.
- Revisions must be stated explicitly where relevant.
- Any missing data should remain marked as pending/not found rather than inferred.

## 11. Test verdict

The report is **usable as a first monitor**, but only with a narrow label: **US Macro Monitor v0.1 — liquidity/calendar test**.

What works:

- Source discipline is acceptable.
- Liquidity section is useful and not overclaiming.
- The output naturally identifies next missing blocks.
- Portfolio actionability is constrained to monitor-only.

What does not work yet:

- Too many macro pillars remain placeholders.
- Rates/curve absence limits practical portfolio relevance.
- BLS access is unresolved.
- No charting yet; the liquidity section would benefit from a simple TGA/RRP/reserves visual.

Next build recommendation:

1. Add rates/curve keyless via FRED public CSV: Fed funds, 2Y, 10Y, 10Y-2Y.
2. Add one simple liquidity chart.
3. Then rerun Macro Monitor v0.2 and compare readability/actionability.
