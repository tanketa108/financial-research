# UBER — Valuation Display v1

- **Status:** prefilled
- **Latest period:** 10-Q | report date 2025-09-30

## Thesis Snapshot

- **Thesis short:** Uber está consolidando un sistema operativo global de movilidad y comercio local con efectos de red, adyacencias de alto margen y una vía asset-light hacia la autonomía, lo que debería traducirse en expansión estructural de márgenes y FCF.
- **Current stance:** overweight / positiva con riesgo alto-especulativo
- **What would change my mind:** Una ruptura de la liquidez de red en Mobility, evidencia de que Delivery no sostiene mejora estructural de márgenes, una regulación laboral que destruya de forma material la economía unitaria, o una transición AV donde Uber pierda la relación con el cliente y quede desintermediada por OEMs/AV operators.

## Current Financial Base

- Revenue: 13,467,000,000 USD
- Operating income: 1,113,000,000 USD
- Net income: 6,626,000,000 USD
- Diluted EPS: 3.11 USD/share
- Cash and equivalents: 8,432,000,000 USD
- Total debt: 10,615,000,000 USD

## Key Drivers

- Liquidez de red y densidad en Mobility
- Cross-sell entre Mobility y Delivery
- Crecimiento y retención vía Uber One
- Expansión de publicidad como capa de alto margen
- Apalancamiento operativo en costes de estructura
- Estructura asset-light en autonomía / AV

## Segments

### Mobility
- Importance: motor principal de valor y rentabilidad
- Growth view: crecimiento secular apoyado por densidad de red, recuperación post-pandemia, nuevos casos de uso y expansión internacional
- Margin view: debe seguir siendo el principal contribuyente al EBITDA por pricing power, take rate resiliente y apalancamiento operativo
- Notes: La pieza más importante del caso: liquidez de red, frecuencia, pricing dinámico y posición como agregador de demanda.

### Delivery
- Importance: segunda pata estratégica; relevante por cross-sell, frecuencia y soporte al ecosistema
- Growth view: crecimiento más moderado que Mobility, pero con mayor profundidad de uso dentro de la super app y soporte de Uber One
- Margin view: la clave no es solo crecer, sino demostrar que la mejora de márgenes es sostenible vía batching, densidad, publicidad y menor CAC incremental
- Notes: Más valiosa como capa de engagement y monetización del ecosistema que como negocio aislado puramente transaccional.

### Freight / Other
- Importance: secundaria en valoración actual
- Growth view: más cíclica y menos predecible; no es el core de la tesis
- Margin view: debe evaluarse con prudencia; menor calidad que Mobility y Delivery
- Notes: Puede aportar opcionalidad, pero no debería cargar la tesis central.

## Quality of Business

- Operating margin: 0.08264646914680329
- Net margin: 0.492017524318705
- ROIC (historical): [missing]
- ROIC (expected): [missing]
- WACC: [missing]
- EVA spread: [missing]
- Note: Basic margin metrics prefilled mechanically
- Note: ROIC/WACC still require deeper balance-sheet and analyst normalization work

## Debt

- Total debt: 10,615,000,000 USD
- Cash: 8,432,000,000 USD
- Net debt: 2,183,000,000 USD
- Interest burden: 124,000,000 USD
- Refinancing risk: [missing]

## Cash Conversion

- DSO: 103.72428900274745
- DPO: 27.455632286329546
- DIO: [missing]
- CCC: 76.26865671641791
- Capex: 336,000,000 USD
- Depreciation: 719,000,000 USD

## Normalization Guardrails

- Reported operating margin: 0.08264646914680329
- Reported net margin: 0.492017524318705
- Operating-reference margin: 0.08264646914680329
- Operating-reference net debt: 2,183,000,000 USD
- Flag: reported_net_margin_far_from_operating_margin
- Flag: reported_net_income_likely_contains_non_operating_noise
- Note: Reported metrics are kept separate from operating-reference metrics.
- Note: Net income and net margin may be noisy for valuation unless analyst-normalized.
- Note: This layer is only a guardrail, not a substitute for analyst judgment.

## Valuation Methods

### dcf
- Status: model_extracted
- Source status: extracted_not_validated
- Confidence: 0.65
- Output: 103.90790947172226
- Range: [103.90790947172226, 124.65114124432701]

### gordon
- Status: model_extracted
- Source status: extracted_not_validated
- Confidence: 0.9
- Output: 103.90790947172226
- Range: [103.90790947172226, 103.90790947172226]

### terminal_multiple
- Status: model_extracted
- Source status: extracted_not_validated
- Confidence: 0.75
- Output: 126.72546442158749
- Range: [124.65114124432701, 126.72546442158749]

## Aggregate Valuation View

- Source status: extracted_not_validated
- Confidence: 0.75
- Central reference: 117.04528959437192
- Range: [103.90790947172226, 126.72546442158749]
- Dispersion: 22.817554949865226
- Notes: Central reference is confidence-weighted across workbook-derived outputs pending analyst refinement.

## Model Ingestion Context

- Source file: /data/.openclaw/media/inbound/Model_UBER---db0b01b2-9ad0-4a11-a33e-a0b894c1b45d.xlsx
- Validation status: extracted_not_validated
- Validated by analyst: False
- Extracted output signals: gordon_price, terminal_multiple_price, hybrid_formula_price
- Revenue 2025E-2029E: [51894.04, 60716.0268, 69823.43082, 78202.2425184, 86022.46677024]
- EBITDA 2025E-2029E: [7784.106, 10625.304689999999, 13964.686163999999, 17595.50456664, 21505.61669256]
- FCF 2025E-2029E: [6598.986856, 8769.00298516, 11363.915156022, 14157.3988330632, 17243.5944753072]
- Note: Outputs were extracted by the analyst-model-ingestion skill.
- Note: Workbook semantics are partially inferred; keep analyst review in the loop.

## Scenarios

### Network wins / AV integrated into existing network
- Description: Uber mantiene el control de la demanda y la interfaz con el cliente mientras la oferta AV se integra como supply partner dentro de su red.
- Business model implication: Se preserva el modelo asset-light y aumenta la calidad del negocio por mayor eficiencia de red.
- Valuation implication: Escenario muy alcista: más duración del moat, mejores márgenes y múltiplo estructural superior.

### AV ecosystem owns the customer relationship
- Description: La capa AV/OEM captura la relación primaria con el cliente y Uber queda parcialmente desintermediada.
- Business model implication: Compresión del poder de negociación y menor captura de valor económico por parte de Uber.
- Valuation implication: Escenario bajista estructural: menor duración del moat y múltiplo inferior.

### Vertical integration / asset-heavy Uber
- Description: Uber necesita controlar más activos/flotas para competir en autonomía.
- Business model implication: El negocio gana intensidad de capital y pierde parte de su calidad económica.
- Valuation implication: Escenario negativo para retornos sobre capital y para la prima de valoración.

### Hybrid asset-light central case
- Description: Uber integra AV selectivamente dentro de su red, manteniendo un modelo mayormente asset-light y una plataforma multifuncional.
- Business model implication: Combina moat de demanda, monetización incremental y mejora gradual de la economía unitaria.
- Valuation implication: Escenario central razonable: expansión de márgenes y FCF con opcionalidad AV sin exigir heroic assumptions de hardware.

## Catalysts

- Expansión de Uber Advertising y prueba de su contribución al EBITDA
- Crecimiento de Uber One y mejora de frecuencia / retención
- Evidencia adicional de FCF estructural y recompras sostenidas
- Nuevas alianzas AV que refuercen el rol de Uber como agregador de demanda
- Mayor racionalidad competitiva en movilidad y delivery

## Risks

- Riesgo regulatorio laboral en EE.UU. y Europa
- Presión competitiva de DoorDash en delivery y Lyft en movilidad
- Que la mejora de margen en Delivery no sea tan estructural como parece
- Desintermediación en un futuro AV dominado por OEMs / operadores AV
- Dependencia excesiva de ganancias no operativas para el net income reportado
