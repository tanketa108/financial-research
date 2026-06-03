# NFLX Source Pack v0 — Pre-valuation Deep Dive

Task: `TASK-2026-05-13-003`  
Dedicated Discord thread: `1504215517001420925`  
Prepared: 2026-05-13  
Scope: source pack only, not the final Deep Dive. Methodology target: approved MSFT v1.2 style, with 5Y historicals, explicit primary-source bibliography, and extraction checklist.

## 1. Primary source map

### SEC EDGAR company/source indexes

| Source | URL | Filing date / coverage | Usefulness |
|---|---|---:|---|
| SEC submissions JSON, CIK 1065280 | https://data.sec.gov/submissions/CIK0001065280.json | Live SEC index | Master filing index for latest 10-K/10-Q/8-K/DEF 14A links, accession numbers, filing dates. Use with declared User-Agent. |
| SEC Companyfacts JSON, CIK 1065280 | https://data.sec.gov/api/xbrl/companyfacts/CIK0001065280.json | Live XBRL facts | Fast extraction of standardized 5Y financials: revenue, operating income, net income, OCF, capex, cash, debt, equity, share count. Verify against 10-K tables. |
| Netflix IR SEC filings page | https://ir.netflix.net/financials/sec-filings/default.aspx | Live IR index | Company-hosted filing index; useful fallback if EDGAR navigation is blocked. |

### Annual reports / 10-Ks for 5Y base

| Filing | Period | Filed | URL | Initial extraction targets |
|---|---:|---:|---|---|
| Form 10-K | FY2025 | 2026-01-23 | https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm | 2025 P&L/CF/BS, content assets/liabilities, content amortization policy, FCF definition, share repurchases, debt/liquidity, risks, legal contingencies, business model/ads commentary. |
| Form 10-K | FY2024 | 2025-01-27 | https://www.sec.gov/Archives/edgar/data/1065280/000106528025000044/nflx-20241231.htm | 2024 historicals and compare regime shift in margins/FCF vs prior years. |
| Form 10-K | FY2023 | 2024-01-26 | https://www.sec.gov/Archives/edgar/data/1065280/000106528024000030/nflx-20231231.htm | 2023 historicals; password-sharing/paid-sharing transition context; content spend normalization. |
| Form 10-K | FY2022 | 2023-01-26 | https://www.sec.gov/Archives/edgar/data/1065280/000106528023000035/nflx-20221231.htm | 2022 downturn/reset baseline; subscriber/member growth pressure; ads launch baseline. |
| Form 10-K | FY2021 | 2022-01-27 | https://www.sec.gov/Archives/edgar/data/1065280/000106528022000036/nflx-20211231.htm | 2021 pre-reset benchmark for revenue growth, margin, content cash spend, leverage. |
| Form 10-K | FY2020 | 2021-01-28 | https://www.sec.gov/Archives/edgar/data/1065280/000106528021000040/nflx-20201231.htm | Optional 6Y context if COVID/content production distortions need a pre/post bridge. |

### Latest quarter and recent SEC updates

| Filing | Period / event | Filed | URL | Usefulness |
|---|---:|---:|---|---|
| Form 10-Q | Q1 2026 | 2026-04-17 | https://www.sec.gov/Archives/edgar/data/1065280/000106528026000138/nflx-20260331.htm | Latest run-rate financials; quarterly revenue, op income, net income, OCF/capex/FCF, cash/debt, share repurchases, updated risks. |
| Form 8-K | Q1 2026 results / exhibit | 2026-04-16 | https://www.sec.gov/Archives/edgar/data/1065280/000106528026000137/nflx-20260410.htm | Earnings release/shareholder letter exhibits; guidance and management framing. |
| Form 8-K | 2026-04-22 event | 2026-04-23 | https://www.sec.gov/Archives/edgar/data/1065280/000106528026000139/nflx-20260422.htm | Check for capital allocation, debt, acquisition, governance, or other model-relevant update. |
| Form 8-K | 2026-02-27 event | 2026-02-27 | https://www.sec.gov/Archives/edgar/data/1065280/000119312526082247/d120618d8k.htm | Check event nature before inclusion; likely only model-relevant if transaction/capital structure/governance. |
| Form 8-K | Q4 2025 results / exhibit | 2026-01-20 | https://www.sec.gov/Archives/edgar/data/1065280/000106528026000033/nflx-20260120.htm | FY2025 closing commentary, 2026 outlook bridge, ads/pricing/engagement signals. |

### Proxy / governance / compensation

| Filing | Meeting / period | Filed | URL | Usefulness |
|---|---:|---:|---|---|
| DEF 14A Proxy Statement | 2026 annual meeting | 2026-04-16 | https://www.sec.gov/Archives/edgar/data/1065280/000119312526159286/d20613ddef14a.htm | Board/governance, executive comp KPIs, ownership, shareholder proposals, capital allocation incentives. |
| Annual report to security holders (ARS) | FY2025 | 2026-04-16 | https://www.sec.gov/Archives/edgar/data/1065280/000119312526159306/d69076dars.pdf | PDF annual report presentation; usually redundant with 10-K but useful for formatting and management summary. |

### Netflix investor relations earnings materials

| Source | URL | Filing/date | Usefulness |
|---|---|---:|---|
| Netflix quarterly earnings hub | https://ir.netflix.net/financials/quarterly-earnings/default.aspx | Live IR page | Main index for shareholder letters, video interviews, financial statements and transcripts. Page may be dynamic; use browser or scrape Q4 CDN links if static fetch misses content. |
| Netflix investor events hub | https://ir.netflix.net/investor-news-and-events/investor-events/default.aspx | Live IR page | Contains event entries with earnings interview, letter, financial statements and transcript links. |
| Q4 2025 shareholder letter PDF | https://s22.q4cdn.com/959853165/files/doc_financials/2025/q4/FINAL-Q4-25-Shareholder-Letter.pdf | Q4/FY2025; surfaced by search | High-value management narrative: FY2025 revenue reportedly $45.2B, operating margin 29.5%, ad revenue >$1.5B, memberships >325M. Verify figures before final report. |
| IR content accounting slides | https://s22.q4cdn.com/959853165/files/doc_downloads/2025/IR-Content-Accounting-Slides-May-2025.pdf | May 2025 | Important for Netflix-specific accounting: content spend vs amortization, content asset useful lives, cash/content expense timing. |
| Netflix financial statements page | https://ir.netflix.net/financials/financial-statements/default.aspx | Live IR page | Quarterly supplemental financial statement downloads; useful cross-check to SEC and shareholder letters. |

### Earnings calls / transcripts

| Source | URL | Date | Usefulness / caveat |
|---|---|---:|---|
| Netflix Q1 2026 earnings call transcript, Motley Fool | https://www.fool.com/earnings/call-transcripts/2026/04/16/netflix-nflx-q1-2026-earnings-call-transcript/ | 2026-04-16 | Secondary transcript if official IR transcript is inaccessible. Extract management commentary on 2026 revenue growth, op margin, ads doubling, pricing, engagement, content slate, AI/tech, competition. Verify against official IR transcript if possible. |
| Netflix investor events hub transcript link | https://ir.netflix.net/investor-news-and-events/investor-events/default.aspx | 2026 Q1 and prior events | Preferred official transcript source; use browser if dynamic page blocks static extraction. |

## 2. Model-relevant recent news / narrative to verify

Keep news compact and only include if it changes model inputs or risk framing.

- **Advertising scale-up:** Search snippets for Q1 2026 transcript indicate management expected ad business to double to roughly $3B in 2026. Treat as unverified until extracted from official letter/transcript.
- **FY2025 performance step-up:** Q4 2025 letter snippet indicates revenue +16% to ~$45.2B, operating margin 29.5%, ad revenue >$1.5B, Q4 paid memberships >325M. Verify from PDF/8-K exhibit.
- **Capital allocation:** Recent 10-K/10-Q and proxy should be checked for buyback authorization, actual repurchases, remaining authorization, dilution from SBC, and whether capital returns exceed FCF.
- **Content accounting/content cash spend:** Netflix economics are not capex-heavy in the classic PP&E sense; valuation model must bridge net income → OCF → content asset cash spend/amortization → FCF. Use the May 2025 content-accounting slides and 10-K footnotes.
- **Pricing/paid sharing/engagement:** Extract management language on ARPU, paid sharing tailwind durability, price increases, engagement share, churn, and member count disclosure changes.

## 3. Initial extraction targets for the Deep Dive

### A. 5Y financials table, FY2021-FY2025

Extract from 10-Ks and/or SEC Companyfacts, then reconcile to filings:

- Revenue
- Operating income
- Operating margin
- Net income
- Diluted EPS and diluted weighted-average shares
- Net cash provided by operating activities
- Purchases of property/equipment/capex if material
- Free cash flow as Netflix defines it and a normalized FCF bridge
- Cash and cash equivalents + short-term investments
- Long-term debt/current debt; net cash/debt
- Total assets, total liabilities, total stockholders' equity
- Share repurchases; average repurchase price if disclosed
- SBC if needed for dilution / owner earnings bridge

### B. Netflix-specific economics

- Content assets: licensed vs produced content split if disclosed.
- Additions to content assets / cash spend on content.
- Amortization of content assets and amortization policy/useful lives.
- Content liabilities and payment schedule.
- Relationship between content amortization, operating margin and FCF.
- Whether content spend growth is structurally below revenue growth or just timing.

### C. Revenue drivers / operating KPIs

- Paid memberships, ARM/ARPU, geography mix where still disclosed.
- Ad-tier adoption, ad revenue, ad inventory/fill/pricing commentary.
- Pricing actions, paid sharing, engagement hours/share, churn signals.
- Revenue guidance: reported and FX-neutral, if disclosed.
- Operating margin guidance and long-term target language.

### D. Capital allocation and balance sheet

- Buybacks by year and remaining authorization.
- Debt maturities, coupon/cost, ratings/liquidity policy.
- Any dividend policy statement.
- Acquisition/strategic investment activity if recent 8-Ks indicate material events.
- FCF returned to shareholders vs retained for content/business investment.

### E. Risks and open questions

- Competitive intensity: YouTube, Disney/Hulu, Amazon, Apple, local streamers, gaming/social video.
- Content cost inflation and hit-rate risk.
- Ad business execution risk and cyclicality.
- Pricing power/churn elasticity after paid-sharing tailwind matures.
- Regulatory risks: content quotas, local taxes, data/privacy, app-store/payment rules.
- FX exposure and international mix.
- Accounting risk: content asset capitalization/amortization assumptions.

## 4. Next extraction checklist

1. Download/parse FY2021-FY2025 10-K financial statements and notes.
2. Pull SEC Companyfacts JSON into a raw data CSV for standardized GAAP line items.
3. Extract Netflix-defined FCF and reconcile to OCF less capex and content cash timing.
4. Read FY2025 10-K notes on content assets/liabilities and debt maturities.
5. Parse Q1 2026 10-Q and Q1 2026 8-K exhibit for latest guidance/run-rate.
6. Open Netflix IR earnings hub in browser if static fetch misses dynamic links; capture official Q1 2026 letter, financial statements and transcript.
7. Extract Q4 2025 shareholder letter key figures and FY2026 guidance.
8. Read May 2025 content-accounting slides and summarize accounting mechanics in plain language.
9. Read 2026 DEF 14A for governance, comp KPIs and buyback/incentive alignment.
10. Screen recent 8-Ks from Dec 2025-Apr 2026; include only material capital structure, transaction, or guidance events.
11. Build a clean 5Y historical snapshot table and flag any figures needing manual tie-out.
12. Prepare final Deep Dive bibliography with primary sources first, secondary transcript/news sources clearly labeled.

## 5. Known access notes

- Static `web_fetch` may receive 403 or dynamic shells for IR/SEC pages. SEC works with a declared User-Agent via script. IR pages are dynamic but raw Q4 CDN PDF links are reachable when known.
- Do not rely on search snippets for final figures. Use snippets only as pointers, then verify from the PDF, 8-K exhibit, 10-Q or transcript.
- For final report, avoid over-weighting subscriber count if Netflix has reduced KPI disclosure; focus on revenue growth, margin, FCF, ads/pricing/engagement and content spend efficiency.
