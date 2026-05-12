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

