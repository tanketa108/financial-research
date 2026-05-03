# Model Ingestion Workflow v1

## Objetivo
Convertir un workbook de analista en señales de valoración integradas en el valuation workflow sin depender de lectura manual completa del Excel.

## Pasos
1. Inventory del `.xlsx`
2. Extracción heurística de señales de valoración
3. Aplicación prudente al `valuation-state`
4. Render del display

## Runner único
```bash
python3 financial_system/tools/run_model_ingestion_workflow.py <TICKER> <MODEL.xlsx>
```

## Outputs esperados
- `valuations/extracted/*-inventory.json`
- `valuations/extracted/*-inventory.md`
- `valuations/extracted/<TICKER>-model-signals.json`
- `valuations/<TICKER>-valuation-state-v1.json`
- `valuations/<TICKER>-valuation-display-v1.md`

## Principios
- No tratar el Excel como verdad absoluta.
- Conservar trazabilidad a fórmulas / señales extraídas.
- Separar output extraído de output validado por el analista.
