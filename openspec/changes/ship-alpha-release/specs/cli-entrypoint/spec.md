## ADDED Requirements

### Requirement: Batch subcommand
The `reposcale batch` subcommand SHALL accept a cases root directory and `--model` flag, running all valid case packs found recursively.

#### Scenario: Batch run across all tracks
- **WHEN** user runs `reposcale batch cases/ --model gpt-4o --run-id baseline-v1`
- **THEN** the system discovers and runs all case packs under `cases/`, saving responses to `results/baseline-v1/<case-id>/`

#### Scenario: Batch with invalid case
- **WHEN** one case pack fails validation during batch
- **THEN** the system skips it, logs a warning, and continues with remaining cases

### Requirement: Repeat flag on score subcommand
The `reposcale score` subcommand SHALL accept a `--repeat N` flag for judge stability measurement.

#### Scenario: Score with repeat
- **WHEN** user runs `reposcale score results/run-1/ --judge-model gpt-4o --repeat 3`
- **THEN** the judge is invoked 3 times per case and stability metadata is included in the evaluation output
