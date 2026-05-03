# Valuation Input Contract v1

## Objetivo
Separar con claridad qué partes de una valoración pueden venir del sistema de forma estructurada y qué partes requieren juicio humano / tesis.

Esto evita dos errores:
1. pedir al sistema que adivine lo que no sabe
2. pedir al humano que rellene manualmente lo que ya podemos automatizar

---

## Tipos de input

### A. Structured system inputs
Datos que el sistema debería poder poblar total o parcialmente desde filings, extracted financials, registries o cálculos mecánicos.

### B. Analyst judgment inputs
Supuestos, tesis, escenarios, lecturas cualitativas o decisiones de modelado que deben venir del analista.

### C. Hybrid inputs
Campos donde el sistema puede proponer una base, pero el analista debe revisarla o afinarla.

---

# A. Structured system inputs

## Company identity
- ticker
- name
- cik
- latest period metadata

## Historical financial base
- revenue history
- operating income history
- net income history
- diluted EPS history
- cash and equivalents history
- debt history
- share count history
- capex history *(when available / derivable)*

## Filing and update context
- latest 10-Q / 10-K metadata
- filing delta summary
- data delta summary

## Debt block (partial)
- total debt
- net debt
- interest expense *(if extractable later)*
- cash balance

## Working capital / cash conversion (partial)
- receivables
- payables
- inventories *(when relevant)*
- working capital changes
- FCF conversion base components

## Comparable snapshot (partial)
Potentially later via market/valuation data feeds.

---

# B. Analyst judgment inputs

## Thesis layer
- thesis short
- current stance
- what would change my mind
- moat / advantage
- fragilities
- management quality judgment

## Driver assumptions
- growth assumptions by segment
- margin assumptions by segment or consolidated level
- reinvestment assumptions
- scenario definitions
- signposts / catalysts interpretation
- risk ranking

## Valuation assumptions
- discount rate / WACC choice
- terminal growth
- exit multiple choice
- method weighting if used
- central scenario choice

---

# C. Hybrid inputs

## Segments
System may help identify segment names and reported figures.
Analyst still decides:
- what matters most
- how segments should be grouped
- what future path to assume

## ROIC / EVA spread
System can calculate pieces if enough data is available.
Analyst still reviews:
- normalization
- economic interpretation
- what WACC is appropriate

## Capital allocation
System can track buybacks, dilution, debt changes, SBC.
Analyst still decides whether capital allocation quality is good or poor.

## Scenario analysis
System can store scenarios and maybe attach data.
Analyst defines the actual structural logic and its valuation implications.

---

## Practical implication for v1
The first valuation workflow should probably look like this:

1. System pre-fills structured section
2. Charlie surfaces missing fields clearly
3. Ander fills key judgment inputs
4. Charlie renders valuation view and scenario/sensitivity outputs

---

## Design principle
The valuation system should behave like a strong analytical co-pilot:
- heavy on prep
- explicit about missing pieces
- honest about uncertainty
- never pretending to know the thesis better than the analyst
