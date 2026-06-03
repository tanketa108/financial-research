# NVO Source Pack — Novo Nordisk A/S

Date: 2026-05-16  
Scope: pre-valuation source pack for `TASK-2026-05-13-001`  
Status: v0, focused on GLP-1 durability, pricing reset, oral Wegovy and Novo vs Lilly.

## 1. Source backbone

### Primary / company sources

1. Novo Nordisk Annual Report 2025 — Financial performance page  
   URL: https://annualreport.novonordisk.com/2025/strategic-aspirations/financial-performance.html  
   Use: FY2025 revenue, segment/product performance, margins, cash flow, outlook language.

2. Novo Nordisk Company Announcement No. 4 / 2026 — FY2025 and 2026 outlook  
   URL: https://www.novonordisk.com/content/nncorp/global/en/news-and-media/news-and-ir-materials/news-details.html?id=916483  
   Use: official FY2025 P&L, oral Wegovy approval/launch data, 2026 guidance, pricing/competition commentary.

3. Novo Nordisk Q1 2026 Investor Presentation  
   URL: https://www.novonordisk.com/content/dam/nncorp/global/en/investors/pdfs/financial-results/2026/Q1-2026-investor-presentation.pdf  
   Use: Q1 2026 update, guidance raise, product/segment slides. PDF downloaded locally to `/tmp/q1-2026-investor-presentation.pdf` for this run; detailed extraction still needs a better PDF parser/model pass.

4. Novo Nordisk FY2024 company announcement  
   URL: https://www.novonordisk.com/news-and-media/news-and-ir-materials/news-details.html?id=915255  
   Use: FY2024 base for growth/margin comparison.

5. Wegovy pill FDA approval / Novo Nordisk US press release via PRNewswire  
   URL: https://www.prnewswire.com/news-releases/fda-approves-novo-nordisks-wegovy-pill-the-first-and-only-oral-glp-1-for-weight-loss-in-adults-302648344.html  
   Use: approval details, OASIS 4 efficacy, starting dose/self-pay information, launch timing.

### Secondary / market context

6. CNBC Q1 2026 article  
   URL: https://www.cnbc.com/2026/05/06/wegovy-glp1-weight-loss-novo-nordisk-earnings-stock-nvo-ozempic.html  
   Use: Q1 2026 market reaction, reported guidance raise, Wegovy pill sales/prescriptions, Lilly comparison. Treat as secondary until primary Q1 release is fully extracted.

## 2. Reported FY2025 anchors

From Annual Report 2025 / Company Announcement No. 4 2026:

- Sales: DKK 309.064bn, +6% reported / +10% CER.
- Operating profit: DKK 127.658bn, -1% reported / +6% CER.
- Net profit: DKK 102.434bn, +1%.
- Diluted EPS: DKK 23.03, +2%.
- US Operations sales: +3% reported / +8% CER.
- International Operations sales: +10% reported / +14% CER.
- Obesity care sales: DKK 82.347bn, +26% reported / +31% CER.
- Diabetes care sales: DKK 207.109bn, flat reported / +4% CER.
- Rare disease sales: DKK 19.608bn, +5% reported / +9% CER.
- GLP-1 diabetes products: DKK 152.202bn, +2% reported / +6% CER.
- Ozempic: DKK 127.089bn, +6% reported / +10% CER.
- Rybelsus: DKK 22.093bn, -5% reported / -2% CER.
- Victoza: DKK 3.020bn, -45% reported / -43% CER.
- Insulin: DKK 53.137bn, -4% reported / -1% CER.

## 3. Margin / cash flow anchors

From Annual Report 2025:

- Gross margin: 81.0% vs 84.7% in 2024.
- COGS: DKK 58.788bn, +32% reported / +31% CER.
- Sales & distribution: DKK 64.310bn, 20.8% of sales.
- R&D: DKK 52.039bn, 16.8% of sales.
- Administration: DKK 5.969bn, 1.9% of sales.
- Operating profit was affected by around DKK 8bn of company-wide transformation/restructuring costs and Catalent site acquisition impacts.
- Without the DKK 8bn restructuring cost, operating profit would have increased +6% reported / +13% CER.
- FCF 2025: DKK 28.3bn vs DKK -14.7bn in 2024.
- PPE capex 2025: DKK 60.1bn vs DKK 47.2bn in 2024.
- 2026 capex guide: around DKK 55bn.
- 2026 FCF guide: DKK 35-45bn under new FCF definition.

## 4. 2026 guidance / reset

From Company Announcement No. 4 / 2026 and Annual Report 2025:

Initial FY2026 outlook:

- Adjusted sales growth at CER: -5% to -13%.
- Adjusted operating profit growth at CER: -5% to -13%.
- Reported DKK sales growth expected around 3pp lower than CER.
- Reported DKK operating profit growth expected around 5pp lower than CER.
- Sales and operating profit positively impacted by USD 4.2bn reversal of sales rebate provisions related to the US 340B Drug Pricing Program.

Key management drivers of the negative outlook:

- lower realised prices;
- MFN agreement in the US;
- loss of exclusivity for semaglutide molecule in certain International Operations markets;
- intensifying competition;
- reduced obesity medication coverage in Medicaid;
- positive US gross-to-net effects from 2025 not expected to recur.

Potential offsets:

- continued GLP-1 market expansion;
- patient reach and volume growth;
- Wegovy rollout in additional markets;
- introduction of Wegovy 7.2mg in selected countries;
- uptake of Wegovy pill;
- R&D/commercial investments funded partly by transformation savings.

Q1 2026 secondary-source update from CNBC, pending primary-source extraction:

- Novo reportedly raised 2026 adjusted sales/profit guidance to -4% to -12% CER from -5% to -13%.
- Q1 sales reportedly DKK 96.8bn, +32% CER.
- Q1 operating profit reportedly DKK 59.6bn, +65% reported.
- Adjusted figures reportedly showed sales -4% and profit -6%, excluding USD 4.2bn 340B provision reversal.
- Wegovy pill sales reportedly DKK 2.26bn vs Reuters consensus DKK 1.16bn.
- Wegovy pill reportedly around 1.3m prescriptions in Q1 2026.

## 5. Obesity / diabetes competitive facts

From Annual Report 2025:

- Global branded GLP-1 obesity market volume growth: 104%.
- Novo branded volume market share in global GLP-1 obesity: 59.6%.
- Diabetes global value market share decreased by 3.6pp to 30.1%.
- Estimated global GLP-1 share of total diabetes prescriptions increased to 8.1% vs 6.7% 12 months earlier.
- Novo GLP-1 diabetes value share: 45.8%.

Secondary market context from CNBC:

- Lilly reportedly overtook Novo in key US injectable diabetes/weight-loss drugs.
- Lilly Q1 2026 GLP-1 growth cited: Mounjaro +125%, Zepbound +80%.
- Lilly launched oral obesity pill Foundayo in April 2026, per CNBC. Requires primary verification before using in final model.

## 6. Oral Wegovy facts

From Company Announcement No. 4 / 2026:

- FDA approved once-daily oral semaglutide 25mg for obesity under Wegovy pill on 22 Dec 2025.
- US launch: 5 Jan 2026.
- As of 23 Jan 2026, total weekly prescriptions around 50,000.
- Prescription uptake mainly driven by 1.5mg starter dose in self-pay channel.

From Novo/PRNewswire FDA approval release:

- Once-daily Wegovy pill is described as the first oral GLP-1 medicine for obesity in the US.
- OASIS 4, 64-week phase 3 trial, 307 adults with obesity/overweight and at least one comorbidity, without diabetes.
- Average weight loss if all patients stayed on treatment: about 17% / 16.6% vs about 3% / 2.7% placebo.
- Treatment policy estimand: about 14% / 13.6% vs about 2% / 2.4% placebo.
- Starting dose 1.5mg available in early Jan 2026 at $149/month with savings offers.
- Wegovy pill approved only in the US at time of release.

## 7. Investment questions for Deep Dive

1. Is 2026 a one-off reset or beginning of structurally lower GLP-1 profit pool?
2. What is the sustainable US net price path for obesity GLP-1s?
3. Is oral Wegovy incremental to the market or cannibalising injectable Wegovy?
4. What share can Novo retain against Lilly across injectable and oral obesity/diabetes?
5. What is normalised gross/operating margin after restructuring, Catalent integration and capacity ramp?
6. How should high capex and supply expansion affect FCF conversion and valuation multiple?
7. What probability-weighted value should be assigned to CagriSema, semaglutide 7.2mg, zenagamtide/amycretin and wider cardiometabolic pipeline?

## 8. Source quality / limitations

- FY2025 and initial 2026 outlook are strongly sourced from company primary sources.
- Q1 2026 details are partly sourced from CNBC and search snippets because primary Q1 PDF extraction is incomplete in this run. Before final PDF Deep Dive, extract and cite Q1 2026 company announcement/presentation directly.
- Lilly comparison is currently secondary-source context only; final Deep Dive should use Lilly primary Q1 release/presentation for Mounjaro/Zepbound figures.
- This source pack is not a valuation and does not recommend portfolio action.
