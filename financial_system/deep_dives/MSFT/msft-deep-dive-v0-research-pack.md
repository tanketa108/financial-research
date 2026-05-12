# MSFT Deep Dive v0 — Research Pack

**Estado:** working draft / research pack, no tesis final  
**Fecha de corte:** 2026-05-13  
**Objetivo:** preparar información digerida para análisis del usuario, no emitir recomendación de inversión.

## 1. Fuentes primarias iniciales

- Microsoft FY2025 Annual Report / Form 10-K, FY ended 2025-06-30: https://www.microsoft.com/investor/reports/ar25/index.html
- Microsoft FY2026 Q3 earnings release, quarter ended 2026-03-31, published 2026-04-29: https://www.microsoft.com/en-us/Investor/earnings/FY-2026-Q3/press-release-webcast
- Microsoft FY2026 Q3 earnings call / event page, 2026-04-29: https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3
- Microsoft SEC filings portal: https://www.microsoft.com/en-us/investor/sec-filings

## 2. Mapa del modelo de negocio

Microsoft es una plataforma tecnológica diversificada con tres motores principales:

1. **Productivity and Business Processes** — Microsoft 365, Office, Teams, Copilot, LinkedIn, Dynamics, Power Platform.
2. **Intelligent Cloud** — Azure, server products, GitHub, Nuance Healthcare, Enterprise Services.
3. **More Personal Computing** — Windows OEM/Devices, Xbox/Gaming, Search/Bing/Edge/Copilot consumer.

La capa estratégica transversal es **AI infrastructure + AI applications/agents**. La lógica económica de management: la IA debería aumentar consumo de Azure y monetización en aplicaciones por usuario/consumo: M365 Copilot, GitHub Copilot, Dynamics agents, Security Copilot, Copilot Studio, Foundry y Fabric.

## 3. Cómo gana dinero

### Suscripción por usuario / asiento

- Microsoft 365 Commercial y Consumer.
- Dynamics 365.
- LinkedIn Premium / Talent / Sales / Marketing Solutions.
- GitHub Copilot, con evolución parcial hacia monetización basada en uso.

### Consumo cloud

- Azure IaaS/PaaS.
- Azure AI / Foundry.
- Data, analytics, storage, compute, networking.
- Copilot Credits y consumo de agentes.

### Licencias transaccionales / on-prem

- Windows Server, SQL Server, Office on-prem, Windows Commercial.
- Menos estratégico por migración a cloud, pero todavía relevante por base instalada enterprise.

### Publicidad

- Bing, Edge, Microsoft News, Copilot consumer surfaces.
- LinkedIn Marketing Solutions.

### Gaming y hardware

- Xbox content/services, Game Pass, first-party/third-party content.
- Xbox hardware y Surface/dispositivos; menor margen y más cíclico.

## 4. Segmentos — economía, crecimiento y margen

### FY2025

| Segmento | Revenue FY2025 | Crecimiento | Operating income | Margen operativo aprox. |
|---|---:|---:|---:|---:|
| Productivity and Business Processes | $120.8B | +13% | $69.8B | ~57.8% |
| Intelligent Cloud | $106.3B | +21% | $44.6B | ~42.0% |
| More Personal Computing | $54.6B | +7% | $14.2B | ~25.9% |
| Total | $281.7B | +15% | $128.5B | ~45.6% |

### FY2026 Q3

| Segmento | Revenue Q3 FY26 | Crecimiento YoY | Comentario |
|---|---:|---:|---|
| Productivity and Business Processes | $35.0B | +17%, +13% CC | M365 Commercial cloud +19%; Dynamics 365 +22%; LinkedIn +12% |
| Intelligent Cloud | $34.7B | +30%, +28% CC | Azure +40%, +39% CC |
| More Personal Computing | $13.2B | -1%, -3% CC | Windows OEM/Devices -2%; Xbox content/services -5%; Search ex-TAC +12% |
| Total | $82.9B | +18%, +15% CC | Microsoft Cloud $54.5B, +29% |

## 5. Segmento: Productivity and Business Processes

### Componentes

- Microsoft 365 Commercial cloud/products.
- Microsoft 365 Consumer.
- LinkedIn.
- Dynamics 365 / Power Platform.

### Drivers

- Seat growth de Microsoft 365.
- Expansión de ARPU por Copilot y planes premium.
- Migración Office on-prem a cloud.
- Dynamics 365 y Power Platform.
- Engagement y monetización de LinkedIn.
- Agentes y Copilot Credits.

### Datos relevantes

FY2025:

- Revenue: $120.8B, +13%.
- Operating income: $69.8B, +17%.
- Microsoft 365 Commercial cloud revenue +15%.
- Microsoft 365 Commercial seat growth +6%.
- Microsoft 365 Consumer subscribers: 89.0M, +8%.
- Dynamics 365 revenue +19%.
- LinkedIn revenue +9%.

Q3 FY2026:

- Revenue: $35.0B, +17%.
- M365 Commercial cloud revenue +19%.
- M365 Consumer cloud revenue +33%.
- LinkedIn +12%.
- Dynamics 365 +22%.
- Segment operating margin según call: ~60%.

### Copilot / AI

Management destacó:

- Más de 20M paid Microsoft 365 Copilot seats.
- Net seat adds +250% YoY.
- Customers >50k seats se cuadruplicaron YoY.
- Accenture >740k seats.
- Copilot queries per user +~20% QoQ.
- First-party agent monthly active usage +6x YTD.

**Lectura:** es el segmento de mayor margen. La cuestión clave es si Copilot aumenta ARPU y retención suficiente para compensar coste incremental de inferencia/AI infrastructure.

## 6. Segmento: Intelligent Cloud / Azure

### Componentes

- Azure and other cloud services.
- Azure AI / Azure AI Foundry.
- GitHub cloud services / GitHub Copilot.
- Nuance Healthcare cloud.
- Server products: SQL Server, Windows Server, Visual Studio, System Center.
- Enterprise and Partner Services.

### Drivers

- Consumo Azure.
- Capacidad disponible de datacenter/GPU/CPU.
- Utilización de infraestructura.
- Mix AI vs non-AI workloads.
- Eficiencia de inferencia y entrenamiento.
- Migración de workloads on-prem a cloud.
- GitHub Copilot adoption y pricing basado en uso.

### Datos relevantes

FY2025:

- Revenue: $106.3B, +21%.
- Operating income: $44.6B, +18%.
- Azure and other cloud services +34%.
- Azure superó $75B de revenue en FY2025, +34%.
- Gross margin % bajó por escalado de AI infrastructure, parcialmente compensado por eficiencia en Azure.

Q3 FY2026:

- Revenue: $34.7B, +30%.
- Azure and other cloud services +40%, +39% CC.
- Segment operating margin según call: ~40%.
- Management: demanda Azure sigue excediendo capacidad disponible.

### AI infrastructure

Según Q3 FY2026 call:

- AI business ARR >$37B, +123% YoY.
- Microsoft Cloud revenue: $54.5B, +29%.
- Añadieron 1 GW de capacidad en el trimestre.
- En camino a duplicar footprint total en dos años.
- Dock-to-live times para nuevas GPUs -~20% desde inicio de año en regiones grandes.
- Inference throughput +40% para modelos más usados en Copilot.
- Maia 200: >30% mejor tokens/dólar frente a latest silicon en fleet.
- Cobalt CPU desplegado en casi la mitad de regiones de datacenter.
- Foundry: >10,000 customers han usado más de un modelo.
- Fabric: 35,000 paid customers, +60% YoY.
- >15,000 customers usan Foundry + Fabric.

**Lectura:** Azure es el vector de crecimiento principal, pero el cuello de botella es capital/capacidad. La rentabilidad futura depende de utilización, coste de GPUs/datacenters, eficiencia de inferencia y pricing.

## 7. Segmento: More Personal Computing

### Componentes

- Windows OEM and Devices.
- Gaming / Xbox.
- Search and news advertising: Bing, Edge, Microsoft News, Copilot consumer.

### Drivers

- Ciclo de PCs y Windows OEM.
- Windows 10 end-of-support / AI PC category.
- Search ex-TAC y monetización publicitaria.
- Game Pass y contenido first-party.
- Xbox hardware, más bajo margen y más cíclico.

### FY2026 Q3

- Segment revenue: $13.2B, -1% YoY, -3% CC.
- Windows OEM/Devices -2%.
- Xbox content/services -5%.
- Search ex-TAC +12%.

**Lectura:** segmento menos atractivo económicamente que PBP/Cloud. Search puede mejorar con AI/Copilot, pero gaming/hardware y Windows OEM tienen más ciclicidad y menor margen.

## 8. Working capital — hipótesis de análisis

Pendiente de completar con extracción directa de cash-flow statement y balance Q3/10-K.

Aspectos clave a analizar:

- **Deferred revenue / contract liabilities:** Microsoft cobra por adelantado muchas suscripciones enterprise/cloud, lo que mejora caja y working capital.
- **Receivables:** crecimiento cloud/enterprise puede elevar cuentas por cobrar, pero calidad de cobro debería ser alta.
- **Payables/accruals:** capex de datacenters y compras de infraestructura pueden aumentar payables y accrued expenses.
- **Cash conversion:** históricamente alta, pero AI capex puede reducir FCF conversion aunque earnings sigan fuertes.

Pregunta central: ¿cuánto del deterioro/normalización de FCF es inversión temporal en capacidad AI y cuánto es nueva intensidad estructural de capital?

## 9. Capital flow

Puntos ya identificados:

- Capex de cloud/AI es el mayor swing factor.
- Management está aumentando capacidad agresivamente: +1 GW en Q3 FY2026 y objetivo de duplicar footprint en dos años.
- AI infra reduce gross margin % en Azure, aunque eficiencias operativas compensan parcialmente.
- Buybacks/dividendos siguen siendo relevantes, pero deben analizarse frente a capex AI.
- SBC/dilución debe incorporarse al análisis de retorno de capital.

Pendiente de cuantificar:

- Capex FY2025 y YTD FY2026.
- Operating cash flow / FCF / FCF margin.
- Dividends y buybacks FY2025/YTD.
- SBC y net share count evolution.

## 10. Deuda, liquidez y capacidad de pago

Pendiente de completar con schedule exacto de vencimientos del 10-K.

Hipótesis preliminar:

- Microsoft tiene balance sheet de altísima calidad.
- Deuda no parece restricción estratégica.
- El análisis relevante no es solvencia, sino coste de capital implícito frente a retorno de inversión AI/cloud.

A completar:

- Cash, equivalents and short-term investments.
- Total debt.
- Maturity schedule por año.
- Interest expense.
- Coste medio aproximado.
- Cobertura EBIT/interest.
- Capacidad de pago/refinanciación.

## 11. Dinámicas de mercado / sector

### Cloud infrastructure

- Competidores: AWS, Google Cloud, Oracle, infraestructura privada/híbrida.
- Drivers: migración cloud, AI workloads, data platforms, security/compliance.
- Riesgo: capex race, margin compression, supply constraints, customer optimization.

### Enterprise software / productivity

- Microsoft tiene distribución excepcional con M365.
- Copilot puede ser ARPU uplift si el ROI es claro.
- Riesgo: saturación de seats, resistencia al pricing, competencia puntual de Google/Slack/Salesforce/Atlassian/AI-native tools.

### AI applications / agents

- Oportunidad: monetizar workflows existentes con agentes.
- Riesgo: coste de inferencia y valor real por usuario.
- Métrica clave: paid seats, usage/query growth, retention, expansion, gross margin.

### Gaming / consumer

- Menos central para tesis de calidad enterprise/cloud.
- Puede aportar optionality, pero también complejidad y menor margen.

## 12. Guidance / outlook

Pendiente de extraer y resumir de earnings call/IR.

Temas que ya aparecen:

- Demanda Azure por encima de capacidad disponible.
- Capex y capacidad AI/datacenter seguirán elevados.
- Crecimiento de Microsoft Cloud muy fuerte.
- Copilot adoption acelerando, pero todavía debe probar monetización y margen a escala.

## 13. Fortalezas preliminares

- Distribución enterprise global única.
- Alto peso de ingresos recurrentes/subscripción.
- Segmento PBP con márgenes extraordinarios.
- Azure como plataforma de crecimiento estructural.
- Balance sheet muy fuerte.
- Capacidad de invertir en AI infra a escala que pocos competidores pueden igualar.
- Ecosistema integrado: productivity + cloud + security + data + developer tools + AI.

## 14. Debilidades / riesgos preliminares

- AI capex puede deteriorar FCF conversion.
- Azure growth depende de capacidad y demanda AI sostenible.
- Copilot necesita demostrar ROI y willingness-to-pay.
- Competencia fuerte: AWS, Google, Salesforce, OpenAI/AI-native apps, etc.
- Riesgo regulatorio/antitrust.
- Gaming/hardware diluyen calidad relativa.
- Margen de Azure puede presionarse por coste de GPU/inferencia.

## 15. Preguntas clave para la tesis

1. ¿Qué parte del crecimiento Azure es AI incremental vs migración cloud tradicional?
2. ¿Cuál es la intensidad de capital normalizada de Microsoft post-AI?
3. ¿Copilot será ARPU expansion de alto margen o monetización con COGS estructuralmente más alto?
4. ¿Qué FCF margin sostenible tiene Microsoft con este nivel de capex?
5. ¿Cuánto margen puede proteger PBP frente a AI compute cost?
6. ¿La valoración actual exige que Azure mantenga >30% growth durante demasiado tiempo?
7. ¿Qué retorno sobre invested capital generará la expansión de datacenters?
8. ¿Qué riesgos regulatorios pueden limitar bundling/distribución de Copilot?
9. ¿La relación con OpenAI reduce o aumenta moat a largo plazo?
10. ¿Cuál es el downside si AI demand se normaliza o hay overcapacity?

## 16. Próximos pasos de análisis

1. Extraer cash-flow statement FY2025 y Q3/YTD FY2026.
2. Construir bridge: net income → operating cash flow → FCF.
3. Extraer debt maturity schedule del FY2025 10-K.
4. Calcular interest coverage y coste medio aproximado de deuda.
5. Extraer capex por periodo y comparar contra D&A.
6. Añadir guidance explícito por segmento de la Q3 FY2026 call.
7. Completar peer/sector framework: AWS/Google Cloud, Salesforce, Google Workspace, AI apps.
8. Preparar dashboard update MSFT con deep-dive status.

## 17. Addendum — ROE DuPont analysis required

User requested that the MSFT deep dive include a DuPont analysis of ROE to understand the source of profitability.

To complete in v0.1:

- ROE trend.
- Net profit margin.
- Asset turnover.
- Equity multiplier.
- Extended DuPont if useful:
  - tax burden,
  - interest burden,
  - operating margin,
  - asset turnover,
  - financial leverage.

Analytical objective:

- Determine whether Microsoft’s return profile is mainly driven by exceptional margins, asset-light software economics, leverage, buybacks/equity base effects, or a mix of these.
- Separate genuine business quality from accounting/capital-structure effects.

## 18. Addendum — working capital and cash conversion cycle required

User requested a deeper working capital analysis including cash conversion cycle and its components.

To complete in v0.1:

- DSO — days sales outstanding.
- DIO — days inventory outstanding.
- DPO — days payable outstanding.
- CCC — DSO + DIO - DPO.
- Receivables trend.
- Inventory trend.
- Payables/accruals trend.
- Deferred revenue / contract liabilities trend.
- Operating cash conversion: net income → operating cash flow.

Analytical nuance for Microsoft:

- Inventory is likely less important than in industrial/retail companies, though devices/Xbox/hardware still matter.
- Deferred revenue and contract liabilities are central because subscription/enterprise billing can fund operations upfront.
- Capex payables/accruals may matter more as AI/cloud infrastructure investment scales.
- The key question is whether working capital remains structurally favorable or whether cloud/AI capex changes cash conversion.


## 19. Financial forensics — MSFT v0.1

**Fuentes primarias usadas:** Microsoft FY2025 Form 10-K / Annual Report, ejercicio cerrado el 30-jun-2025, filed 30-jul-2025 ([Microsoft Annual Report FY2025](https://www.microsoft.com/investor/reports/ar25/index.html), [SEC 10-K](https://www.sec.gov/Archives/edgar/data/789019/000095017025100235/msft-20250630.htm)); Microsoft FY2026 Q3 Form 10-Q, periodo cerrado el 31-mar-2026, filed 29-abr-2026 ([Microsoft FY26 Q3 earnings](https://www.microsoft.com/en-us/Investor/earnings/FY-2026-Q3/press-release-webcast), [SEC 10-Q](https://www.sec.gov/Archives/edgar/data/789019/000119312526191507/msft-20260331.htm)). Cifras en USD miles de millones salvo indicación contraria.

### 19.1 Puente de caja: net income → operating cash flow → FCF

| Métrica | FY2025 | 9M FY2026 |
|---|---:|---:|
| Net income | 101.8 | 98.0 |
| Operating cash flow | 136.2 | 127.5 |
| Capex / additions to PP&E | (64.6) | (80.1) |
| Free cash flow, simple: OCF - capex | 71.6 | 47.3 |
| OCF / net income | 134% | 130% |
| FCF / net income | 70% | 48% |

**Lectura:** Microsoft sigue convirtiendo beneficios en caja operativa de forma muy fuerte, pero el FCF está claramente comprimido por el ciclo de inversión en infraestructura cloud/AI. En FY2025 generó $136.2bn de OCF y $71.6bn de FCF; en los primeros 9 meses de FY2026 el OCF ya fue $127.5bn, pero el capex de $80.1bn redujo el FCF a $47.3bn.

La propia compañía atribuye el mayor uso de caja de inversión en 9M FY2026 principalmente a un aumento de $32.7bn en additions to property and equipment y $9.1bn en otros usos de inversión para facilitar compra de componentes.

### 19.2 Capex vs D&A

| Métrica | FY2025 | 9M FY2026 |
|---|---:|---:|
| Capex | 64.6 | 80.1 |
| Depreciation | 22.0 | 24.0 |
| Capex / depreciation | 2.9x | 3.3x |
| Capex / revenue | 22.9% | 33.1% |

**Lectura:** el capex está muy por encima de la depreciación, señal de expansión acelerada de base de activos, no solo mantenimiento. Esto es consistente con inversión en datacenters, cloud y AI. El punto crítico para el PM no es la solvencia actual, sino la normalización futura: si capex/ventas permanece en >30%, la calidad del FCF estructural baja frente al histórico.

### 19.3 Shareholder returns: dividendos, buybacks, SBC y dilución

| Métrica | FY2025 | 9M FY2026 |
|---|---:|---:|
| Dividendos pagados | 24.1 | 19.7 |
| Recompras | 18.4 | 17.7 |
| Total retorno cash a accionistas | 42.5 | 37.4 |
| Total retorno / FCF | 59% | 79% |
| SBC | 12.0 | 9.3 |
| SBC / revenue | 4.3% | 3.8% |
| Diluted shares avg | 7.465bn | 7.457bn |

**Lectura:** la política de retorno sigue siendo material pero no agresiva frente a la capacidad de caja. En FY2025 dividendos + buybacks consumieron ~59% del FCF; en 9M FY2026 suben a ~79% por la presión de capex sobre FCF. La SBC es relevante pero manejable; las recompras exceden SBC, y el diluted share count baja ligeramente, lo que indica que las recompras están compensando más que la dilución por equity comp.

### 19.4 ROE y análisis DuPont

**FY2025 DuPont:**

- ROE sobre equity promedio: **33.3%**
- Net margin: **36.1%**
- Asset turnover: **0.50x**
- Equity multiplier: **1.85x**

Fórmula:

`ROE = net margin × asset turnover × equity multiplier`

`33.3% ≈ 36.1% × 0.50x × 1.85x`

**9M FY2026, anualizado aproximado:**

- ROE anualizado sobre equity promedio: **34.5%**
- Net margin: **40.5%**
- Asset turnover anualizado: **0.49x**
- Equity multiplier: **1.73x**

**Lectura:** el ROE está impulsado principalmente por margen neto extraordinario, no por apalancamiento financiero. El equity multiplier baja en 9M FY2026 mientras el margen mejora, por lo que la rentabilidad sobre equity sigue siendo de alta calidad. El riesgo a vigilar es que el crecimiento de activos por capex presione el asset turnover antes de que la nueva capacidad compute/cloud genere ingresos proporcionales.

### 19.5 Working capital y cash conversion cycle

| Métrica | FY2025 | 9M FY2026 |
|---|---:|---:|
| Accounts receivable final | 69.9 | 60.0 |
| Inventory final | 0.9 | 1.2 |
| Accounts payable final | 27.7 | 37.5 |
| Unearned revenue / contract liabilities | 67.3 | 53.7 |
| DSO aprox. | 82 días | 74 días |
| DIO aprox. | 5 días | 4 días |
| DPO aprox. | 103 días | 116 días |
| CCC aprox. | -17 días | -39 días |

**Fórmulas:**

- `DSO = average accounts receivable / revenue × days`
- `DIO = average inventory / cost of revenue × days`
- `DPO = average accounts payable / cost of revenue × days`
- `CCC = DSO + DIO - DPO`

Para 9M FY2026 se usan aproximadamente 274 días del periodo julio-marzo.

**Lectura:** Microsoft tiene ciclo de caja negativo, favorecido por payables elevados y cobros/prepagos de contratos. La unearned revenue baja desde $67.3bn en jun-2025 a $53.7bn en mar-2026 por estacionalidad y reconocimiento de ingresos, pero el backlog contractual aumenta de forma muy fuerte: RPO de $375bn a jun-2025 a $633bn a mar-2026. El 10-Q indica que espera reconocer ~30% del RPO total en los próximos 12 meses y que el RPO comercial era $627bn con duración media de ~2.5 años.

### 19.6 Deuda, liquidez y capacidad de refinanciación

| Métrica | Jun-2025 | Mar-2026 |
|---|---:|---:|
| Cash & equivalents | 30.2 | 32.1 |
| Short-term investments | 64.3 | 46.2 |
| Cash + ST investments | 94.6 | 78.3 |
| Long-term debt, incl. current | 43.2 | 40.3 |
| Net cash vs debt | +51.4 | +38.0 |
| Interest expense | 2.4 FY | 2.2 9M |
| Operating income / interest expense | 53.9x | 51.8x |

**Maturity schedule:**

FY2025 10-K, long-term debt maturities as of 30-jun-2025:

- FY2026: $3.0bn
- FY2027: $9.25bn
- FY2028: $0
- FY2029: $2.05bn
- FY2030: $0
- Thereafter: $34.9bn
- Total principal: $49.2bn

FY2026 Q3 10-Q, maturities as of 31-mar-2026:

- Remainder FY2026: $0
- FY2027: $9.25bn
- FY2028: $0
- FY2029: $2.02bn
- FY2030: $0
- Thereafter: $34.9bn
- Total principal: $46.2bn

**Lectura:** balance extremadamente líquido. Aunque cash + short-term investments bajan a $78.3bn por el ciclo inversor, Microsoft continúa en posición net cash frente a deuda financiera. La cobertura de intereses >50x implica riesgo de refinanciación bajo. La compañía declara explícitamente que espera que caja, inversiones de corto plazo, cash flow operativo y acceso a mercados sean suficientes para operaciones, dividendos, recompras, vencimientos de deuda y capex material durante al menos los próximos 12 meses y posteriormente en el futuro previsible.

### 19.7 Conclusión financiera forense

Microsoft mantiene una calidad financiera excepcional: márgenes altos, ROE >30%, bajo apalancamiento económico, liquidez neta positiva y conversión de beneficio a OCF muy fuerte. La única tensión real está en FCF, no por deterioro operativo sino por intensidad de capex vinculada al despliegue AI/cloud. Para un portfolio manager, el debate clave es si la inversión actual en infraestructura producirá suficiente crecimiento incremental y margen futuro para justificar un FCF temporalmente más bajo.

**Variables críticas a monitorizar:**

1. Capex / revenue y capex / depreciation.
2. FCF conversion frente a net income.
3. Evolución de RPO comercial y revenue recognition.
4. Azure/cloud growth vs crecimiento de PP&E.
5. Shareholder returns como % de FCF.
6. Margen operativo ante mayor depreciación futura.

