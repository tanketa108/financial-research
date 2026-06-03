# Macro Monitor Streamlit UI v0

Interactive visualization layer for the generated Macro Monitor data.

## Source of truth

The app only reads existing generated artifacts:

- `financial_system/macro/data/*.json`
- `financial_system/macro/reports/*-macro-monitor-v*.md`
- `financial_system/macro/charts/*.svg`

Do not make Streamlit the source of truth. Fetchers and renderers own the data/report pipeline.

## Install

From workspace root:

```bash
python3 -m pip install -r financial-research/financial_system/macro/app/requirements.txt
```

## Run

```bash
streamlit run financial-research/financial_system/macro/app/streamlit_macro_monitor.py
```

## Current tabs

- Report
- Rates
- Inflation
- Labor
- Growth
- Liquidity
- Raw state

## Refresh data before running

```bash
python3 financial-research/financial_system/tools/fetch_fred_rates_curve_state.py
python3 financial-research/financial_system/tools/fetch_fred_inflation_labor_state.py
python3 financial-research/financial_system/tools/fetch_fred_growth_activity_state.py
python3 financial-research/financial_system/tools/fetch_treasury_tga_state.py
python3 financial-research/financial_system/tools/fetch_nyfed_rrp_state.py
python3 financial-research/financial_system/tools/fetch_fred_reserve_balances_state.py
python3 financial-research/financial_system/tools/render_macro_liquidity_svg.py
python3 financial-research/financial_system/tools/render_macro_monitor.py --date 2026-06-03 --out financial-research/financial_system/macro/reports/2026-06-03-macro-monitor-v0.4.md
```
