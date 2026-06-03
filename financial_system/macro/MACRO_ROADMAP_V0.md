# Macro Research & Dashboard Roadmap v0

Date: 2026-05-30
Owner: Charlie / Financial Project
Status: draft for discussion

## 1. Product intent

Build a macroeconomic layer parallel to the existing portfolio/research system.

The macro layer should:

- provide a GitHub-published dashboard for core macro indicators;
- ingest public data from reliable sources, starting with FRED/St. Louis Fed and the U.S. Treasury;
- support ad hoc questions and analysis around macro data releases;
- evolve into recurring macro publication reports;
- feed portfolio context without replacing company-level thesis work.

Operating rule:

> Macro informs the portfolio context; it does not make portfolio decisions.

## 2. Recommended v0 scope

v0 should be deliberately narrow. The goal is not to build a complete macro terminal; it is to create a working spine that can ingest data, render a useful dashboard and produce repeatable reports.

### v0 data sources

1. FRED / St. Louis Fed API
   - rates and yield curve;
   - inflation;
   - labor market;
   - growth/activity;
   - credit/liquidity where available.

2. U.S. Treasury source
   - Treasury General Account / cash balance;
   - public debt / issuance-related datasets if technically straightforward;
   - later: auction schedule and issuance details.

### v0 dashboard modules

1. Rates & curve
   - Fed funds / policy rate proxy;
   - 2Y, 10Y, 30Y Treasury yields;
   - 10Y-2Y and/or 10Y-3M spread.

2. Inflation
   - CPI YoY / MoM;
   - Core CPI;
   - PCE / Core PCE if easily available;
   - market-implied inflation later.

3. Labor
   - unemployment rate;
   - nonfarm payrolls;
   - initial claims;
   - wage growth if available.

4. Growth / activity
   - real GDP;
   - industrial production;
   - retail sales;
   - ISM/PMI proxy only if data source is stable/public.

5. Liquidity / Treasury
   - Treasury General Account;
   - reverse repo later if from FRED;
   - debt/issuance metrics later.

### v0 outputs

- `docs/macro.html`: static dashboard published through GitHub Pages.
- `financial_system/macro/macro-series-registry.json`: canonical list of macro series.
- `financial_system/macro/macro-state.json`: latest readings and derived signals.
- `financial_system/macro/reports/YYYY-MM-DD-macro-monitor.md`: periodic macro monitor template.
- build script under `financial_dashboard/` or `financial_system/tools/` to regenerate the page.

## 3. Architecture

Recommended approach: extend the current financial-research repo with a modular macro subsystem.

Proposed structure:

```text
financial-research/
  docs/
    macro.html
  financial_dashboard/
    build_macro_dashboard.py
  financial_system/
    macro/
      MACRO_ROADMAP_V0.md
      macro-series-registry.json
      macro-state.json
      reports/
      sources/
        fred.py
        treasury.py
```

Keep it as a monolith/module inside the existing repo. Do not create a new repo or agent system yet.

## 4. Data contract v0

Each macro series should have explicit metadata:

- `id`: internal stable id;
- `source`: `fred` / `treasury` / future source;
- `sourceSeriesId` or endpoint;
- `name`;
- `category`;
- `frequency`;
- `units`;
- `releaseLag` if known;
- `importance`: high / medium / low;
- `defaultTransform`: level / YoY / MoM / spread / z-score;
- `interpretationHint`;
- `sourceUrl`.

Derived metrics should be separately declared instead of hidden inside chart code.

## 5. Reporting v0

Start with a monthly/weekly manual Macro Monitor before automating too much.

Suggested sections:

1. Executive macro summary
2. Rates & curve
3. Inflation
4. Labor market
5. Growth/activity
6. Liquidity/Treasury
7. Market/portfolio implications
8. Data releases to watch
9. Open questions

Important discipline: distinguish current data, interpretation and portfolio implication.

## 6. Implementation phases

### Phase 0 — Design lock

- Agree v0 scope and first list of series.
- Decide whether FRED API key is already available or must be configured.
- Confirm which Treasury dataset/endpoints from the old project are worth reusing.

Acceptance: roadmap approved and series registry draft created.

### Phase 1 — Data spine

- Create macro directory and series registry.
- Implement FRED fetcher with cache/local JSON output.
- Implement minimal Treasury fetcher.
- Generate `macro-state.json` with latest observations.

Acceptance: one command refreshes data and writes reproducible local state.

### Phase 2 — Dashboard v0

- Build `docs/macro.html` with key cards and charts.
- Link it from `docs/index.html` and/or portfolio dashboard.
- Keep design consistent with existing financial dashboard.

Acceptance: dashboard opens locally and can be published through GitHub Pages.

### Phase 3 — Macro Monitor report v0

- Create first `YYYY-MM-DD-macro-monitor.md` using actual data.
- Register output if we want it in the output registry.
- Add a simple workflow/preflight checklist.

Acceptance: first manual macro report exists and is repeatable.

### Phase 4 — Incremental hardening

- Add release calendar tracking.
- Add more sources.
- Add derived signals and change detection.
- Add periodic radar/reporting once the manual workflow proves useful.

Acceptance: automation only after the manual workflow has demonstrated value.

## 7. Risks and constraints

- API keys/secrets must not be committed.
- Source definitions must be explicit; avoid chart code with hidden assumptions.
- Do not overbuild a macro terminal before we know which indicators matter to the workflow.
- Macro data revisions matter; the first version can use latest vintage, but future versions may need vintage-aware handling for serious analysis.
- Release calendars and actual historical series are different products; do not conflate them too early.

## 8. Open decisions

1. Should v0 focus only on U.S. macro, or include Europe from the start?
2. Do we want the dashboard to be mostly monitoring cards/charts, or more report-oriented narrative?
3. Is the old Treasury/FRED project available in the workspace, and should we import parts of it?
4. How often should the Macro Monitor run initially: weekly, monthly, or only around major releases?

## 9. Charlie recommendation

Start with U.S. macro only, using FRED + Treasury, and build a simple dashboard plus a manually generated Macro Monitor. Once the workflow is useful, add release calendars, Europe, more sources and automated alerts.

This mirrors the successful portfolio system pattern: first create the state, contract and manual workflow; then automate around proven friction.
