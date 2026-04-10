## MODIFIED Requirements

### Requirement: Minimum seed case count
The project SHALL include at least 12 curated cases, with at least 4 per Phase 1 track (Diagnose, Intent, Plan).

#### Scenario: Seed case availability
- **WHEN** a contributor clones the repository
- **THEN** at least 12 case packs exist under `cases/` with balanced track representation

### Requirement: Seed cases cover multiple case types
The cases SHALL collectively cover at least 4 different `case_type` values from the taxonomy (e.g., `mvp_incomplete`, `divergent_beta`, `functional_not_scalable`, `multi_module_tangled`).

#### Scenario: Case type diversity
- **WHEN** all case metadata files are inspected
- **THEN** at least 4 distinct `case_type` values are represented
