# Valuation Template v1

## Objetivo
Tener una plantilla de análisis y valoración suficientemente rica para uso buy-side, pero sin caer en modelos excesivamente complejos o llenos de líneas irrelevantes.

La filosofía es:
- entender drivers
- entender sensibilidad
- entender escenarios
- mantener la tesis viva

No se busca falsa precisión.
Se busca un marco útil para pensar, actualizar y decidir.

---

## Principios
1. **Modelo ligero, no modelo de banca de inversión**
2. **Varios métodos de valoración, no un número mágico**
3. **Sensibilidad como pieza central**
4. **Escenarios sin falsa precisión probabilística**
5. **La valoración se alimenta también de la tesis cualitativa**
6. **El output final debe ser legible y operativo**

---

# Estructura de la plantilla

## 1. Thesis Snapshot
### Objetivo
Capturar la idea de inversión de forma breve.

### Campos
- ticker
- nombre
- thesis short
- current stance
- what would change my mind

---

## 2. Business Model & Segments
### Objetivo
Entender cómo gana dinero la compañía y cómo se distribuye ese valor entre líneas de negocio.

### Campos
- descripción del modelo de negocio
- segmentos / líneas de negocio
- peso relativo de cada línea
- tasa de crecimiento por línea
- margen por línea
- implicaciones del mix

### Nota
En compañías simples, esta sección puede ser más ligera.
En compañías como UBER o LVMH, es central.

---

## 3. Key Drivers
### Objetivo
Identificar qué variables explican realmente el valor del negocio.

### Ejemplos
- top-line growth
- gross margin
- operating margin / EBITDA margin
- mix shift
- operating leverage
- capex intensity
- working capital intensity
- user/network effects
- pricing power

---

## 4. Quality of Business: DuPont + ROIC
### Objetivo
Evaluar la calidad económica del negocio y la creación de valor.

### Bloques
#### A. DuPont / ROE analysis
- net margin
- asset turnover
- financial leverage
- evolución histórica

#### B. ROIC analysis
- ROIC histórico
- ROIC esperado
- incremental ROIC (si se puede estimar razonablemente)

#### C. ROIC vs WACC
- WACC base
- EVA spread / value creation spread
- lectura cualitativa de si el negocio crea valor estructuralmente

### Por qué importa
Esto evita mirar solo crecimiento y margen sin entender si ese crecimiento crea valor real.

---

## 5. Debt Structure & Debt Service
### Objetivo
Entender si la deuda soporta o compromete la tesis.

### Campos
- deuda total
- caja
- deuda neta
- coste de deuda
- vencimientos relevantes
- cobertura de intereses
- capacidad de repago
- riesgo de refinanciación
- relación con FCF

---

## 6. Working Capital & Cash Conversion
### Objetivo
Entender la calidad de la conversión de resultados a caja.

### Bloques
#### A. Working capital
- inventarios
- cuentas a cobrar
- cuentas a pagar
- evolución

#### B. Cash Conversion Cycle
- DIO
- DSO
- DPO
- CCC
- evolución histórica

#### C. Profit-to-cash bridge
- EBIT / EBITDA
- cash taxes
- capex
- working capital impact
- FCF conversion

---

## 7. Capital Allocation & Dilution
### Objetivo
Evaluar cómo usa el management el capital generado por el negocio.

### Campos
- reinversión
- buybacks
- dividendos
- M&A
- deuda vs desapalancamiento
- SBC / stock-based compensation si aplica
- diluted share count
- evolución de la dilución

---

## 8. Brief Comparable Analysis
### Objetivo
Tener un contraste de mercado sin que la plantilla dependa demasiado de peers.

### Campos
- peer set corto
- múltiplos clave
- prima/descuento relativa
- breve lectura cualitativa

### Nota
Debe ser un bloque breve y disciplinado.

---

## 9. Historical Financial Base
### Objetivo
Construir el punto de partida de la valoración.

### Campos mínimos
- revenue histórico
- gross margin histórico
- operating margin / EBITDA margin histórico
- net income histórico
- FCF histórico
- capex histórico
- diluted shares histórico

### Objetivo práctico
No solo mirar el presente, sino entender trayectoria y normalización posible.

---

## 10. Valuation Engine
### Objetivo
Obtener una valoración por varios métodos.

### Métodos iniciales
- DCF
- Gordon Growth / perpetuity style
- terminal value with exit multiple

### Inputs clave
- revenue growth assumptions
- margin assumptions
- tax assumptions
- capex / reinvestment assumptions
- working capital assumptions
- discount rate
- terminal growth
- exit multiple

### Output por método
- price target / equity value per share
- rango razonable
- supuestos clave
- notas

### Output agregado
- rango total
- media / referencia central
- dispersión entre métodos

---

## 11. Sensitivity Analysis
### Objetivo
Ver cómo varía el valor ante cambios en las variables relevantes dentro de un mismo escenario.

### Tipos
#### A. One-way sensitivity
- growth
- EBITDA / operating margin
- discount rate
- terminal growth
- exit multiple

#### B. Two-way sensitivity tables
Ejemplos:
- discount rate vs g
- margin vs growth
- growth vs exit multiple

### Filosofía
La sensibilidad es central.
No es un accesorio.

---

## 12. Scenario Analysis
### Objetivo
Capturar escenarios donde cambia la naturaleza del negocio y no solo un supuesto aislado.

### Campos por escenario
- scenario name
- scenario description
- business model implication
- key assumptions
- segment / mix implication
- margin implication
- capital intensity implication
- valuation implication

### Nota importante
En v1:
- sí a escenarios
- no a probabilidades explícitas si no aportan claridad

### Distinción crítica
- sensibilidad = dispersión dentro de un escenario
- escenarios = dispersión entre estructuras de negocio distintas

---

## 13. Catalysts / Signposts
### Objetivo
Definir qué hechos nos dirán si la tesis o un escenario ganan o pierden fuerza.

### Campos
- próximos hitos relevantes
- señales positivas
- señales negativas
- indicadores de que un escenario gana probabilidad cualitativa

---

## 14. Risk Register
### Objetivo
Mantener explícitos los riesgos que amenazan la tesis o la valoración.

### Tipos de riesgo
- competitivo
- regulatorio
- ejecución
- financiero
- disrupción
- asignación de capital
- tecnológico

### Campos sugeridos
- riesgo
- descripción
- por qué importa
- qué lo haría más grave
- qué lo mitigaría

---

## 15. Qualitative Thesis Layer
### Objetivo
Conectar valoración, escenarios y seguimiento real del negocio.

### Campos
- why this business matters
- moat / advantage
- fragilidades
- management quality notes
- industry structure notes
- thesis evolution notes
- links to Knowledge Project

### Importancia
Esta sección alimentará la tesis viva.

---

# Qué es core en v1
Estas piezas deberían estar sí o sí:
- Thesis Snapshot
- Business Model & Segments
- Key Drivers
- DuPont + ROIC + ROIC vs WACC
- Debt Structure & Debt Service
- Working Capital & Cash Conversion
- Capital Allocation & Dilution
- Historical Financial Base
- Valuation Engine
- Sensitivity Analysis
- Scenario Analysis
- Catalysts / Signposts
- Risk Register
- Qualitative Thesis Layer

# Qué puede ser más ligero en v1
- Comparable analysis
- Incremental ROIC cuando no se pueda estimar bien
- Segment detail cuando el negocio sea muy simple

---

# Output ideal para el futuro dashboard
El dashboard v1 de capa 2 debería poder leer de esta plantilla:
- target por método
- rango agregado
- sensibilidad principal
- escenario central actual
- riesgos clave
- catalysts principales
- estado de tesis

---

# Conclusión
La plantilla v1 no busca ser perfecta ni definitiva.
Busca ser:
- suficientemente rigurosa
- modular
- viva
- útil para pensar como buy-side
- y compatible con una tesis que evoluciona con el tiempo
