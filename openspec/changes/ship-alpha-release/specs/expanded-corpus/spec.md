## ADDED Requirements

### Requirement: Minimum 12 cases across tracks
The corpus SHALL contain at least 12 case packs: minimum 4 per track (diagnose, intent, plan).

#### Scenario: Corpus inventory
- **WHEN** `reposcale validate cases/*/` is run on the full corpus
- **THEN** at least 12 cases pass validation with representation across all 3 tracks

### Requirement: Difficulty distribution
Each track SHALL include at least one case of each difficulty level (easy, medium, hard).

#### Scenario: Track coverage check
- **WHEN** the corpus manifest is reviewed
- **THEN** each track (diagnose, intent, plan) has cases at easy, medium, and hard difficulty

### Requirement: Case types variety
The corpus SHALL include at least 4 distinct `case_type` values to ensure diversity of evaluation scenarios.

#### Scenario: Case type coverage
- **WHEN** all `case.yaml` files are parsed
- **THEN** at least 4 unique `case_type` values are present (e.g., `mvp_incomplete`, `divergent_beta`, `functional_not_scalable`, `multi_module_tangled`)

### Requirement: Corpus manifest
A `cases/CORPUS.md` file SHALL list all cases with ID, track, type, difficulty, and brief description.

#### Scenario: Manifest matches reality
- **WHEN** `cases/CORPUS.md` is compared against actual case directories
- **THEN** every case directory has an entry and every entry has a corresponding directory
