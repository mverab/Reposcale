## ADDED Requirements

### Requirement: Judge stability metadata
When `--repeat N` is used, the evaluation output SHALL include a `layers.llm_judge.stability` object with `runs`, `mean`, `stddev`, and `per_dimension` breakdowns.

#### Scenario: Stability metadata structure
- **WHEN** scoring runs with `--repeat 3` and all 3 judge invocations succeed
- **THEN** `evaluation.json` contains `layers.llm_judge.stability.runs = 3`, `mean`, `stddev`, and per-dimension mean/stddev values

### Requirement: Judge stability schema extension
The `schemas/evaluation.schema.json` SHALL accept an optional `stability` object within the `llm_judge` layer.

#### Scenario: Schema validation with stability
- **WHEN** an evaluation with `stability` data is validated against the schema
- **THEN** validation passes without errors
