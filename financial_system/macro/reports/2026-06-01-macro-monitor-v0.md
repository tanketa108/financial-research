# Macro Monitor v0 — 2026-06-01

Status: draft
Scope: US macro monitor
Owner: Charlie / Financial Research System

## 1. Executive macro summary

- Current macro regime: `<to fill>`
- Main change since last monitor: `<to fill>`
- Highest-signal release/event ahead: `<to fill>`
- Key uncertainty: `<to fill>`

Caveat: this v0 monitor uses official calendar/event tracking and explicit placeholders where the data spine is not yet connected.

## 2. Upcoming releases

Window: 2026-06-01 to 2026-07-31

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

To track:

- Fed funds / target range
- 2Y Treasury yield
- 10Y Treasury yield
- 30Y Treasury yield
- 10Y-2Y and/or 10Y-3M spread

Interpretation placeholder:

- `<curve signal>`
- `<policy expectations signal>`
- `<risk / caveat>`

## 4. Inflation

Data status: `partial calendar ready; historical data pending FRED_API_KEY / official release ingestion`

To track:

- CPI headline/core MoM and YoY
- PCE headline/core MoM and YoY
- PPI where useful for pipeline/PCE read-through

Interpretation placeholder:

- `<inflation momentum>`
- `<services/shelter/core pressure>`
- `<Fed relevance>`

## 5. Labor market

Data status: `calendar pending BLS manual confirmation; historical data pending FRED_API_KEY / official release ingestion`

To track:

- Nonfarm payrolls
- Unemployment rate
- Participation rate
- Average hourly earnings
- Initial/continued claims
- JOLTS openings/quits

Interpretation placeholder:

- `<labor demand>`
- `<wage pressure>`
- `<cooling/tightness signal>`

## 6. Growth / activity

Data status: `BEA calendar ready for GDP; other Census/Fed releases require event confirmation`

To track:

- GDP and domestic private demand
- Retail sales / control group
- Durable goods / core capex
- Industrial production
- Housing starts/permits

Interpretation placeholder:

- `<growth momentum>`
- `<consumer/capex split>`
- `<cyclical risk>`

## 7. Liquidity / Treasury

Data status: `Treasury FiscalData public API reachable; TGA state extraction v0 active`

- Source: Treasury FiscalData Daily Treasury Statement; record date: **2026-05-29**; units: `USD millions`.
- TGA opening balance: **$849,710mn**.
- Total TGA deposits: **$68,288mn**.
- Total TGA withdrawals: **$14,117mn**.
- Source URL: <https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance>
- Caveat: Treasury accounting fields need exact source definitions; treat this as liquidity context, not a standalone signal.

To track next:

- Treasury General Account / operating cash balance trend
- Deposits / withdrawals where useful
- Reverse repo later via FRED if available

Interpretation placeholder:

- `<liquidity context>`
- `<TGA direction>`
- `Do not overinterpret one-day moves without broader liquidity context.`

## 8. Portfolio context

Operating rule: macro informs portfolio context; it does not make portfolio decisions.

- Portfolio areas potentially affected: `<to fill>`
- Relevant company/sector links: `<to fill>`
- Actionability: `<monitor only / research task / model update>`

## 9. Open questions

- `<question 1>`
- `<question 2>`
- `<question 3>`

## 10. Source discipline

- Official source URLs must be cited for every factual release claim.
- Consensus/surprise must be omitted unless explicitly sourced.
- Revisions must be stated explicitly where relevant.
- Any missing data should remain marked as pending/not found rather than inferred.
