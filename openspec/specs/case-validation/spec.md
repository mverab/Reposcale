## ADDED Requirements

### Requirement: Validate case metadata against schema
The system SHALL validate `case.yaml` against `schemas/case.schema.json` and report all validation errors with their JSON path.

#### Scenario: Valid case metadata
- **WHEN** `case.yaml` conforms to the case schema
- **THEN** validation passes with no errors

#### Scenario: Invalid case metadata
- **WHEN** `case.yaml` has a missing required field (e.g., `track`)
- **THEN** the system reports the specific field path and error message

### Requirement: Check required case pack files
The system SHALL verify that all required files exist in the case pack directory: `case.yaml` and `repo/` directory.

#### Scenario: Complete case pack
- **WHEN** case directory contains `case.yaml` and a non-empty `repo/` directory
- **THEN** validation passes the file presence check

#### Scenario: Missing repo directory
- **WHEN** case directory contains `case.yaml` but no `repo/` directory
- **THEN** the system reports a missing required directory error

### Requirement: Warn on missing recommended files
The system SHALL emit warnings (not errors) for missing recommended files: `hints.yaml`, `tree.txt`.

#### Scenario: Missing hints file
- **WHEN** case directory has no `hints.yaml`
- **THEN** the system emits a warning but validation still passes

### Requirement: Validate hints file structure
The system SHALL validate `hints.yaml` against expected fields (`known_gaps`, `original_intent`, `key_files`) when the file exists.

#### Scenario: Valid hints file
- **WHEN** `hints.yaml` contains `known_gaps` as a list and `original_intent` as a string
- **THEN** hints validation passes

#### Scenario: Malformed hints file
- **WHEN** `hints.yaml` contains invalid YAML or unexpected types
- **THEN** the system reports the specific parsing or type error

### Requirement: Validate repo snapshot is non-empty
The system SHALL verify that the `repo/` directory contains at least one file (excluding `.gitkeep`).

#### Scenario: Empty repo snapshot
- **WHEN** `repo/` contains only `.gitkeep` or is empty
- **THEN** the system reports that the repo snapshot is empty

### Requirement: Batch validation of multiple case packs
The system SHALL accept multiple case pack directories and validate each one, reporting a summary with pass/fail counts.

#### Scenario: Batch validation with mixed results
- **WHEN** 3 case packs are provided and 1 has errors
- **THEN** the system reports individual results for each and a summary showing 2 passed, 1 failed
