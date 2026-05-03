# Publishing notes

## Recommended sequence
1. Start with repo structure + canonical files only.
2. Do not push every registry/output by reflex.
3. Decide delivery model after first clean commit.

## Delivery options
### Option A — GitHub as source only
- keep `financial_dashboard/output/` out of git
- rebuild locally/VPS when needed
- cleaner repo

### Option B — GitHub Pages / static delivery
- include `financial_dashboard/output/`
- possibly move generated site to `docs/` or deploy branch later
- better remote access, but mixes source and build artifacts unless carefully separated

## Current recommendation
Do **not** publish generated HTML in the first commit.
First make the repo clean and coherent.
Then decide whether the dashboard should be a generated artifact in git or a deployment output elsewhere.
