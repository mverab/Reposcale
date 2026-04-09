## ADDED Requirements

### Requirement: Minimum seed case count
The project SHALL include at least 3 curated seed cases, with at least 1 per Phase 1 track (Diagnose, Intent, Plan).

#### Scenario: Seed case availability
- **WHEN** a contributor clones the repository
- **THEN** at least 3 case packs exist under `cases/` with real repo snapshots

### Requirement: Seed cases use real repositories
Each seed case SHALL use a snapshot of a real open-source repository (not synthetic or generated code).

#### Scenario: Real repo verification
- **WHEN** a seed case's `repo/` directory is inspected
- **THEN** it contains a real project with meaningful commit history, documentation, and implementation code

### Requirement: Seed cases cover multiple case types
The seed cases SHALL collectively cover at least 2 different `case_type` values from the taxonomy (e.g., `mvp_incomplete`, `divergent_beta`).

#### Scenario: Case type diversity
- **WHEN** all seed case metadata files are inspected
- **THEN** at least 2 distinct `case_type` values are represented

### Requirement: Each seed case includes evaluation hints
Every seed case SHALL include a `hints.yaml` file with `known_gaps`, `original_intent`, and `key_files` to enable judge calibration.

#### Scenario: Hints completeness
- **WHEN** a seed case's `hints.yaml` is inspected
- **THEN** it contains at least 2 entries in `known_gaps`, a non-empty `original_intent`, and at least 2 entries in `key_files`

### Requirement: Seed cases validate against schema
Every seed case SHALL pass `reposcale validate` without errors.

#### Scenario: Seed case validation
- **WHEN** `reposcale validate cases/diagnose/diagnose-001/` is run
- **THEN** the validation passes with zero errors
