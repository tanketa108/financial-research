# Model Ingestion — Next Test Checklist

## Objetivo
Validar que `analyst-model-ingestion` no está sobreajustada al modelo de UBER.

## Qué probar con el siguiente modelo
- workbook `.xlsx` de otro analista
- idealmente con estructura distinta a UBER
- mejor si contiene:
  - summary/output
  - DCF o terminal multiple
  - supuestos explícitos
  - hojas auxiliares

## Comando único
```bash
python3 /data/.openclaw/workspace/financial_system/tools/run_model_ingestion_workflow.py <TICKER> <MODEL.xlsx>
```

## Qué comprobar
### 1. Inventory
- detecta hojas correctamente
- encuentra filas no vacías relevantes
- captura labels / formulas / cached values

### 2. Signals
- encuentra outputs explícitos
- asigna confidence razonable
- separa `extracted_not_validated`
- genera summary útil

### 3. Valuation state
- no rompe campos previos
- integra model outputs con trazabilidad
- no sobreescribe juicio del analista

### 4. Display
- refleja métodos y rango
- deja claro qué está extraído vs validado

## Red flags
- central reference absurda
- señales mezcladas entre métodos
- celdas importantes no detectadas
- demasiada dependencia de refs fijas tipo `O54`

## Siguiente mejora si falla
- añadir heurísticas por layout
- detectar merged cells / named ranges / styles si compensa
- crear adaptadores por familia de modelos si aparecen patrones repetidos
