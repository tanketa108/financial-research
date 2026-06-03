# Macro Monitor v0 — 2026-06-03

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

Data status: `FRED public CSV reachable; rates/curve extraction v0 active`

- Curve shape 10Y-2Y: **positive/upward sloping**; spread: **0.41%**.
- 2Y trend: `falling`; 10Y trend: `falling`; 10Y-2Y curve trend: `falling`.
- Latest rates/spreads:
  - FEDFUNDS — Effective Federal Funds Rate: **3.63%** on 2026-05-01; one-period change: **-0.01pp**; 5-obs trend: **-0.01pp**.
  - DGS2 — Market Yield on U.S. Treasury Securities at 2-Year Constant Maturity: **4.05%** on 2026-06-01; one-period change: **+0.07pp**; 10-obs trend: **-0.02pp**.
  - DGS10 — Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity: **4.47%** on 2026-06-01; one-period change: **+0.02pp**; 10-obs trend: **-0.14pp**.
  - DGS30 — Market Yield on U.S. Treasury Securities at 30-Year Constant Maturity: **4.99%** on 2026-06-01; one-period change: **0.00pp**; 10-obs trend: **-0.15pp**.
  - T10Y2Y — 10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity: **0.41%** on 2026-06-02; one-period change: **-0.01pp**; 10-obs trend: **-0.13pp**.
  - T10Y3M — 10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity: **0.69%** on 2026-06-02; one-period change: **0.00pp**; 10-obs trend: **-0.31pp**.
- Source URLs:
  - FEDFUNDS: <https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS&cosd=2026-01-01>
  - DGS2: <https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS2&cosd=2026-01-01>
  - DGS10: <https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10&cosd=2026-01-01>
  - DGS30: <https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS30&cosd=2026-01-01>
  - T10Y2Y: <https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y2Y&cosd=2026-01-01>
  - T10Y3M: <https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y3M&cosd=2026-01-01>
- Caveat: rates/curve context frames valuation sensitivity and policy expectations; it is not a standalone portfolio instruction.

Interpretation:

- Curve signal: **positive but flattening curve; monitor whether long-end resilience or front-end repricing is driving the move.**
- Policy expectations signal: **rates are falling across front and long end; confirm whether this reflects easing expectations or growth risk.**
- Portfolio use: frame valuation sensitivity, especially rate-sensitive growth, financials and cyclicals; do not create company tasks from curve data alone.
- Caveat: inflation/labor data are still missing, so the rates read is context rather than a regime conclusion.

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

Data status: `Treasury FiscalData, NY Fed Markets and FRED public CSV reachable; TGA/RRP/reserve balances extraction v0 active`

![Liquidity triangle](../charts/2026-06-03-liquidity-triangle-v0.svg)

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


NY Fed reverse repo:
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


Fed reserve balances:
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

To track next:

- Treasury General Account / operating cash balance trend
- Deposits / withdrawals where useful
- Bank reserves / reserve balances trend
- Funding spreads / market plumbing stress indicators as next v0.2 extension

Interpretation:

- Automatic liquidity read: **mixed liquidity context: rising TGA is a reserve drain, while falling RRP can partly offset by releasing cash from the facility.**
- Inputs: TGA trend `rising` (+$145,062mn over window); RRP trend `falling` (-$10.409bn over window).
- Cross-check: reserve balances trend `rising` (+$72,605mn over window). This is the direct balance-sheet confirmation leg for the TGA/RRP read.
- Portfolio use: monitor net effect; do not collapse it into a single bullish/bearish signal.
- Caveat: this is a rules-based context note, not an investment conclusion; funding spreads and market plumbing stress indicators are still outside the v0 data spine.

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
