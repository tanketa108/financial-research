# Ollama Evaluation Plan for Financial System

## Objetivo
Evaluar si una capa local con Ollama puede absorber parte material del trabajo del Financial System con calidad suficiente y menor coste variable.

## Casos de uso prioritarios
1. Filing delta summary
2. Materiality classification
3. Thesis-monitor draft
4. Knowledge ingestion support (secundario)

## Routing deseado
- Python/reglas -> extracción/deltas/rendering
- Ollama -> primer razonamiento barato
- Premium -> revisión fina/ambigüedad

## Criterio de éxito
Se considera exitoso si Ollama:
- produce un primer draft usable
- clasifica materialidad con razonabilidad suficiente
- reduce necesidad de modelo premium en tareas rutinarias
- no añade complejidad operativa desproporcionada

## Criterio de fracaso
Fracasa si:
- la calidad es demasiado baja
- la latencia vuelve el flujo impráctico
- la memoria/CPU de la VPS quedan estranguladas
- la operación es demasiado frágil

## Decisión posterior
- seguir en KVM 4
- escalar a KVM 8
- o abandonar local inference en VPS
