### Perfecto — te dejo un draft fundacional del proyecto

Voy a asumir que quieres **las dos cosas juntas**:

1. **arquitectura completa de la suite**, y  
2. **un README/spec fundacional** que ya puedas usar como base del repositorio open source.

Voy a usar **`RepoScale`** como nombre de trabajo porque encaja bastante bien, pero lo puedes cambiar después.

## Arquitectura conceptual de la suite

### 1. Tesis del proyecto

`RepoScale` es una **open-source eval suite** para medir una capacidad poco cubierta por benchmarks tradicionales de coding:

> la capacidad de un LLM para **entender, continuar, escalar y evolucionar** un proyecto de software existente de forma coherente con su historia, arquitectura y dirección de producto.

No mide solo “si programa”.  
Mide si puede operar sobre una codebase viva con criterio.

### 2. Qué capacidad mide realmente

La capacidad compuesta se puede definir así:

> **Repo continuation intelligence**: habilidad para leer una codebase existente, reconstruir su intención original, detectar gaps técnicos y de producto, y proponer o ejecutar extensiones útiles sin romper continuidad con lo ya construido.

### 3. Subcapacidades

La suite debería separar esta capacidad en varios ejes:

#### A. Comprensión contextual
- entender estructura del repo
- entender qué existe realmente
- distinguir núcleo vs scaffolding vs ruido

#### B. Reconstrucción histórica
- inferir intención original
- usar commits, changelogs, docs y artefactos históricos
- detectar pivots, features abandonadas y derivas

#### C. Diagnóstico crítico
- identificar deuda técnica
- detectar inconsistencias
- localizar puntos ciegos del producto
- notar ausencias relevantes

#### D. Creatividad útil
- proponer extensiones no obvias
- mantener coherencia con stack e intención
- evitar brainstorming genérico

#### E. Priorización y estrategia
- ordenar por impacto, esfuerzo, riesgo y dependencia
- diseñar una secuencia plausible de evolución

#### F. Continuidad ejecutiva
- convertir el análisis en planes, tickets, patches o implementaciones reales

## Estructura de la suite

### 4. La suite no debe ser un benchmark monolítico

`RepoScale` debería ser una **familia de evals** con distintos tracks.

### 5. Tracks propuestos

#### `RepoScale-Diagnose`
Evalúa diagnóstico del estado actual.

**Pregunta central:**  
¿El modelo entiende qué hay, qué falta y qué está roto o incompleto?

**Output esperado:**  
diagnóstico estructurado con evidencia.

#### `RepoScale-Intent`
Evalúa reconstrucción de intención original.

**Pregunta central:**  
¿Puede inferir qué producto o sistema se quería construir y qué tanto se cumplió?

**Output esperado:**  
lectura de intención, cumplimiento y desviaciones.

#### `RepoScale-Plan`
Evalúa capacidad de escalar el proyecto conceptualmente.

**Pregunta central:**  
¿Puede diseñar un roadmap realista para llevar el proyecto más allá de su MVP/beta?

**Output esperado:**  
roadmap por fases, top apuestas, riesgos y primer sprint.

#### `RepoScale-Extend`
Evalúa creatividad disciplinada.

**Pregunta central:**  
¿Puede proponer features/extensiones plausibles y coherentes con el repo?

**Output esperado:**  
nuevas capacidades justificadas por evidencia y contexto.

#### `RepoScale-Implement`
Evalúa continuación técnica acotada.

**Pregunta central:**  
¿Puede implementar una mejora realista y pequeña en un proyecto existente?

**Output esperado:**  
patch/diff/tests/notas técnicas.

#### `RepoScale-Agent`
Evalúa ciclo completo agentic.

**Pregunta central:**  
¿Puede inspeccionar, planear, ejecutar, validar y justificar cambios en una codebase?

**Output esperado:**  
traza agentic + artefactos + resultados.

## Modos de ejecución

### 6. Execution modes

La misma tarea puede correrse en distintos modos para aislar capacidades.

#### Modo 1: `prompt_only`
- sin tools
- solo contexto textual empaquetado

Útil para medir razonamiento puro.

#### Modo 2: `read_only_repo`
- acceso de lectura al repo
- sin modificar nada

Útil para medir comprensión real sobre estructura.

#### Modo 3: `history_aware`
- incluye commit history, changelogs, logs del arnés

Útil para medir razonamiento histórico.

#### Modo 4: `tool_augmented`
- puede buscar archivos, leer módulos, consultar tests, inspeccionar metadata

Útil para medir trabajo realista con herramientas.

#### Modo 5: `agentic_budgeted`
- acceso tipo coding agent
- con presupuesto de pasos, lecturas, ediciones o tiempo

Útil para comparar agentes bajo restricciones equivalentes.

#### Modo 6: `full_continuation`
- analiza
- propone
- implementa
- corre validaciones
- entrega cambios

Útil para benchmark end-to-end.

## Casos del benchmark

### 7. Qué contiene un caso

Cada caso debería ser un **case pack** con estructura consistente.

#### Recomendado
- snapshot del repo
- árbol de archivos
- docs relevantes
- historial de commits
- issues/TODOs opcionales
- changelog opcional
- log del arnés opcional
- metadata del caso
- prompt/protocolo aplicable
- hints de evaluación interna

### 8. Tipos de caso

#### Tipo A: MVP incompleto
- intención clara
- implementación parcial
- gaps visibles

#### Tipo B: Beta divergente
- docs y código ya no coinciden del todo
- commits muestran pivots

#### Tipo C: Scaffold inflado
- mucho andamiaje
- poco producto real
- buena prueba para detectar humo

#### Tipo D: Producto funcional pero no escalable
- sirve para medir criterio de evolución
- evita respuestas tipo “reescríbelo todo”

#### Tipo E: Repo erosionado
- deuda fuerte
- señales mezcladas
- buena prueba de ordenamiento bajo ambigüedad

## Contratos de salida

### 9. Qué formatos necesitas

Aquí sí entra fuerte lo que hablábamos antes: la suite debe tener varios contratos, no uno solo.

#### A. `case schema`
Describe el caso.

#### B. `response schema`
Describe la salida del modelo/agente.

#### C. `evaluation schema`
Describe el scoring y observaciones del juez.

#### D. `artifact schema`
Describe diffs, tests, logs, patches, planes, tickets u otros artefactos.

## Evaluación

### 10. Capas de scoring

La suite debería mezclar varias capas.

#### Capa 1: Validación estructural
- ¿cumplió el formato?
- ¿entregó todas las secciones?
- ¿marcó evidencia vs hipótesis?

#### Capa 2: Heurísticas automáticas
- densidad de referencias a archivos/commits
- genericidad de recomendaciones
- longitud/estructura
- presencia de priorización

#### Capa 3: LLM judge
- evalúa calidad semántica con rúbrica fija

#### Capa 4: Validación ejecutiva
Para tracks de implementación:
- ¿compila?
- ¿pasan tests?
- ¿introdujo regresiones?
- ¿se alinea con el plan?

#### Capa 5: Revisión humana
Necesaria para:
- calibración
- creatividad útil
- casos ambiguos
- auditoría de leaderboard

## Métricas

### 11. Métricas primarias

Estas deberían aparecer en casi todos los tracks.

- comprensión del proyecto
- grounding en evidencia
- reconstrucción de intención
- detección de gaps
- creatividad útil
- priorización
- coherencia arquitectónica
- accionabilidad

### 12. Métricas secundarias

- tasa de alucinación
- tasa de genericidad
- rewrite bias
- sensibilidad al historial
- estabilidad entre corridas
- dependencia del modo agentic

### 13. Métricas específicas para agent mode

- número de pasos
- uso de herramientas
- archivos inspeccionados
- cobertura de contexto relevante
- calidad del diff
- tests pasados
- costo/token budget
- alineación entre plan y ejecución

## Diseño OSS

### 14. Componentes del repositorio

Yo estructuraría el repo así:

```text
reposcale/
  README.md
  LICENSE
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md

  docs/
    vision.md
    benchmark_design.md
    scoring.md
    task_taxonomy.md
    dataset_format.md
    judge_protocol.md
    roadmap.md

  cases/
    diagnose/
    intent/
    plan/
    extend/
    implement/
    agent/

  schemas/
    case.schema.json
    response.schema.json
    evaluation.schema.json
    artifact.schema.json

  prompts/
    diagnose.md
    intent.md
    plan.md
    extend.md
    implement.md
    judge.md

  runners/
    local/
    batch/
    agentic/

  scorers/
    structural/
    heuristic/
    llm_judge/
    execution/

  baselines/
    prompt_only/
    tool_augmented/
    agentic/

  reports/
    leaderboard/
    case_studies/
    failure_modes/

  scripts/
    validate_case_pack.py
    run_eval.py
    score_eval.py
    summarize_results.py
```

## Principios de diseño

### 15. Principios que deberían regir el proyecto

#### 1. Evidence-first
Toda evaluación debe premiar grounding y penalizar invención.

#### 2. Creativity-with-constraints
La creatividad solo cuenta si es útil, plausible y contextual.

#### 3. Continuity-over-rewrite
La suite debe favorecer evolución coherente, no reflejo de reescritura.

#### 4. Multi-mode, same capability
La misma capacidad debe poder medirse con y sin tools.

#### 5. Open and inspectable
Casos, prompts, rúbricas y resultados deben ser auditables.

#### 6. Human-calibrated
La parte más interesante de esta capacidad no debe depender solo de scoring automático.

## Qué no es la suite

### 16. Non-goals

Importante dejar esto clarísimo en el spec.

`RepoScale` **no** busca ser:

- un benchmark de algoritmos estilo LeetCode
- un benchmark de autocomplete
- un benchmark de bug-fixing aislado
- un benchmark de code generation greenfield
- un benchmark de “cuántos tests pasa” solamente

Tampoco busca premiar:
- overengineering
- recomendaciones enterprise por defecto
- rewrite bias
- checklists genéricas reciclables para cualquier repo

## Roadmap del proyecto

### 17. Roadmap sugerido por fases

#### Fase 0: definición
- fijar capability model
- fijar taxonomía de tareas
- definir rúbrica
- definir formatos

#### Fase 1: MVP público
- 10 a 15 casos
- 3 tracks iniciales: `Diagnose`, `Intent`, `Plan`
- scoring híbrido
- primeras baselines

#### Fase 2: continuation técnica
- agregar `Extend` e `Implement`
- introducir validación ejecutable
- primeras corridas con coding agents

#### Fase 3: suite madura
- `Agent` track end-to-end
- leaderboard
- contribuciones externas
- análisis por failure modes

#### Fase 4: estandarización
- benchmarking reproducible
- paquetes de casos versionados
- benchmark cards
- integración con herramientas externas

---

# README / Spec fundacional

Aquí te dejo un borrador ya en tono de repo open source.

## `README.md` — borrador

### RepoScale

**RepoScale** is an open-source evaluation suite for measuring how well LLMs can understand, continue, and scale existing software projects.

Unlike traditional coding benchmarks that focus on isolated tasks or greenfield code generation, RepoScale evaluates a harder and more realistic capability:

> can a model read an existing codebase, infer what it is trying to become, identify what is missing, and propose or execute a coherent path forward?

### Why RepoScale?

Most real software work does not start from a blank file.

It starts with:
- an existing repository,
- partial implementations,
- inconsistent documentation,
- historical baggage,
- unfinished ideas,
- architectural constraints,
- and a moving product target.

RepoScale measures whether a model can operate in that environment with real judgment.

### What RepoScale evaluates

RepoScale focuses on **repo continuation intelligence**, including:

- project understanding
- historical reasoning from commits and docs
- intent reconstruction
- gap detection
- useful creativity
- prioritization under constraints
- architectural coherence
- actionable continuation planning
- scoped implementation in existing codebases

### What RepoScale does not evaluate

RepoScale is **not** primarily a benchmark for:

- isolated algorithmic coding
- autocomplete
- one-function bug fixing
- greenfield app generation
- raw pass@k on synthetic tasks

### Benchmark tracks

RepoScale is organized into multiple tracks:

- **Diagnose**: understand the project and assess its current state
- **Intent**: infer the original product/system direction
- **Plan**: propose a realistic roadmap to scale the project
- **Extend**: suggest coherent missing capabilities or product extensions
- **Implement**: make a scoped, meaningful change in the existing codebase
- **Agent**: full analyze-plan-execute-validate loop with tools

### Execution modes

Each task can be evaluated under different modes:

- `prompt_only`
- `read_only_repo`
- `history_aware`
- `tool_augmented`
- `agentic_budgeted`
- `full_continuation`

This allows comparison between pure reasoning, tool use, and agentic continuation.

### Core principles

- **Evidence first**: claims should be grounded in the repo, docs, or history.
- **Creativity with constraints**: useful ideas beat generic brainstorming.
- **Continuity over rewrite**: preserve coherence with what already exists.
- **Multi-layer evaluation**: structure, semantics, execution, and human review all matter.
- **Open and reproducible**: cases, protocols, and scoring should be inspectable.

### Evaluation dimensions

RepoScale scores models across dimensions such as:

- project understanding
- evidence fidelity
- original intent reconstruction
- gap detection
- useful creativity
- prioritization quality
- architectural coherence
- actionability

Additional metrics include hallucination rate, genericity rate, rewrite bias, and agentic execution quality.

### Repository structure

```text
cases/        benchmark case packs
schemas/      JSON schemas for cases, responses, and evaluations
prompts/      task and judge prompts
runners/      local and agentic execution runners
scorers/      structural, heuristic, LLM-judge, and execution scorers
baselines/    baseline configurations and benchmark runs
reports/      leaderboards, breakdowns, and failure analyses
docs/         design specs and governance documents
```

### Project status

RepoScale is currently in early design / bootstrap phase.

Initial goals:
- define the capability model
- publish the first task taxonomy
- release the first 10 to 15 curated cases
- ship the first public scoring pipeline
- establish baseline results across several models

### Contributing

We welcome contributions in:
- case curation
- rubric design
- judge calibration
- runner implementations
- scoring heuristics
- failure mode analysis
- documentation and benchmark governance

### Long-term vision

RepoScale aims to become a standard open benchmark for evaluating how LLMs evolve existing codebases—not just how they generate code from scratch.

---

## Documento fundacional corto

Si quieres algo todavía más tipo manifesto/spec, este párrafo sirve muy bien:

> RepoScale is an open-source evaluation suite for measuring a model’s ability to continue existing software systems. It focuses on whether a model can understand a repository in context, reconstruct its historical and product intent, detect gaps and inconsistencies, and propose or execute coherent next steps that scale the system without discarding its accumulated structure. RepoScale emphasizes evidence, continuity, prioritization, and useful creativity over generic coding fluency.

## Qué haría yo como siguiente paso inmediato

Si quieres convertir esto ya en proyecto serio, el orden correcto sería:

### Paso 1
Congelar un **capability model** de una página.

### Paso 2
Definir la **task taxonomy v0**:
- Diagnose
- Intent
- Plan
- Extend
- Implement
- Agent

### Paso 3
Definir los **3 schemas base**:
- `case`
- `response`
- `evaluation`

### Paso 4
Armar **5 a 10 casos semilla** bien curados.

### Paso 5
Diseñar la **rúbrica v0** y el judge protocol.

### Paso 6
Correr primeras baselines y analizar failure modes.

## Mi recomendación editorial

No vendas esto como “benchmark de creatividad”.  
Véndelo como algo más fuerte y más serio:

> **benchmark / eval suite de continuidad evolutiva de codebases**

o en inglés:

> **evaluation suite for codebase continuation and scaling intelligence**

“Creatividad” sigue dentro, pero como un componente de más alto nivel.

Si quieres, en el siguiente mensaje te preparo cualquiera de estas tres piezas:

1. **`docs/vision.md`** listo para pegar,  
2. **`task_taxonomy.md`** con todos los tracks bien definidos,  
3. **los 3 JSON schemas base** para empezar a implementarlo.