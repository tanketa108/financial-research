# financial-research

Repositorio inicial propuesto para el Financial System.

## Principios
- El repo es **fuente de verdad de trabajo**, no dump completo de la VPS.
- Se versiona código, contratos, documentación y estado analítico canónico.
- Se evita subir caches, snapshots previos y artefactos derivados de bajo valor.

## Qué entra
- `financial_system/tools/`
- `financial_system/config/`
- `financial_system/docs/`
- `financial_system/positions.json`
- `financial_system/registry/ticker_cik_map.json`
- `financial_system/registry/dashboard_state.json`
- `financial_system/registry/thesis_monitor_input.json`
- `financial_system/registry/thesis_monitor_output.json`
- `financial_system/valuations/*-valuation-state-v1.json`
- `financial_system/valuations/*-valuation-display-v1.md`
- `financial_dashboard/`

## Qué no entra de inicio
- `*previous.json`
- snapshots intermedios pesados
- outputs JSON mecánicos poco legibles
- rutas locales de VPS
- secretos / credenciales / tokens

## Objetivo inmediato
Permitir:
- versionado serio del stack
- revisión remota
- base futura para GitHub Pages o delivery estático del dashboard

## Siguiente paso
1. Crear repo GitHub vacío.
2. Copiar esta estructura canónica.
3. Hacer primer commit limpio.
4. Decidir si `financial_dashboard/output/` se publica o solo se genera.
