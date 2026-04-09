## ADDED Requirements

### Requirement: Per-case summary
The system SHALL produce a summary for each case showing composite score and per-dimension scores from the evaluation.

#### Scenario: Single case summary
- **WHEN** `results/<run-id>/diagnose-001/evaluation.json` exists
- **THEN** the system outputs the case ID, composite score, and a table of dimension scores

### Requirement: Per-track aggregation
The system SHALL aggregate results across all cases in a track, computing mean and standard deviation for each metric.

#### Scenario: Track summary with 3 cases
- **WHEN** 3 evaluation files exist for the `diagnose` track in a run
- **THEN** the system outputs a table with mean ± std for each primary metric across the 3 cases

### Requirement: Run-level summary
The system SHALL produce an overall summary across all tracks in a run, including total cases evaluated, cases per track, and overall composite score.

#### Scenario: Full run summary
- **WHEN** a run contains evaluations for 3 diagnose cases and 2 intent cases
- **THEN** summary shows: 5 total cases, per-track breakdowns, and an overall composite score

### Requirement: Output formats
The system SHALL support output as both a Rich-formatted terminal table and a JSON summary file.

#### Scenario: Terminal output
- **WHEN** `reposcale summary <run-id>` is called without flags
- **THEN** results are printed as a formatted table in the terminal

#### Scenario: JSON output
- **WHEN** `--json` flag is passed
- **THEN** results are written to `results/<run-id>/summary.json`
