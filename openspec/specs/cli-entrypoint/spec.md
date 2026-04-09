## ADDED Requirements

### Requirement: Unified CLI with subcommands
The system SHALL provide a `reposcale` CLI registered as a console script in `pyproject.toml`, with subcommands: `validate`, `run`, `score`, `summary`.

#### Scenario: CLI help
- **WHEN** user runs `reposcale --help`
- **THEN** the system displays available subcommands with brief descriptions

### Requirement: Validate subcommand
The `reposcale validate` subcommand SHALL accept one or more case pack directories and run full validation.

#### Scenario: Validate a case pack
- **WHEN** user runs `reposcale validate cases/diagnose/diagnose-001/`
- **THEN** the system validates the case pack and prints pass/fail with details

### Requirement: Run subcommand
The `reposcale run` subcommand SHALL accept a case pack or track directory, a `--model` flag, and an optional `--dry-run` flag.

#### Scenario: Run eval on a single case
- **WHEN** user runs `reposcale run cases/diagnose/diagnose-001/ --model gpt-4o`
- **THEN** the system runs the eval and saves the response to `results/<run-id>/diagnose-001/response.json`

#### Scenario: Run eval on a track
- **WHEN** user runs `reposcale run cases/diagnose/ --model gpt-4o`
- **THEN** the system runs the eval for all case packs in the directory

### Requirement: Score subcommand
The `reposcale score` subcommand SHALL accept a run ID and score all responses in that run.

#### Scenario: Score a run
- **WHEN** user runs `reposcale score <run-id> --judge-model gpt-4o`
- **THEN** the system scores all responses and saves evaluation files alongside them

### Requirement: Summary subcommand
The `reposcale summary` subcommand SHALL accept a run ID and display aggregated results.

#### Scenario: Display run summary
- **WHEN** user runs `reposcale summary <run-id>`
- **THEN** the system prints a formatted table with per-case and per-track scores

### Requirement: Run ID generation
The system SHALL auto-generate a unique run ID based on timestamp and model name (e.g., `20250115-143000-gpt4o`).

#### Scenario: Auto-generated run ID
- **WHEN** user runs `reposcale run` without specifying a run ID
- **THEN** the system generates a run ID in the format `YYYYMMDD-HHMMSS-<model-short-name>`
