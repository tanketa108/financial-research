# Proposed repo structure

```text
financial-research/
  README.md
  .gitignore

  financial_system/
    positions.json

    config/
    docs/
    tools/

    registry/
      ticker_cik_map.json
      dashboard_state.json
      thesis_monitor_input.json
      thesis_monitor_output.json

    valuations/
      UBER-valuation-state-v1.json
      MSFT-valuation-state-v1.json
      NFLX-valuation-state-v1.json
      DVN-valuation-state-v1.json

      UBER-valuation-display-v1.md
      MSFT-valuation-display-v1.md
      NFLX-valuation-display-v1.md
      DVN-valuation-display-v1.md

  financial_dashboard/
    README.md
    build_dashboard_html.py
    static/
```

## Critical opinion
This is intentionally narrower than the current VPS tree.

Why:
- current workspace mixes source, derived state, caches, and presentation
- GitHub should not become a dumping ground for every transient artifact
- the valuation-state files are currently the best candidate for canonical analytical state, even if they will likely evolve

## Open decision
Whether `financial_dashboard/output/` should be versioned depends on delivery choice:
- if GitHub Pages is the delivery layer, versioning output may be acceptable
- if the dashboard is rebuilt elsewhere, keep output out of git
