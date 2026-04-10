## ADDED Requirements

### Requirement: Multi-run comparison table
The summary system SHALL support comparing results across multiple runs side-by-side.

#### Scenario: Compare two model runs
- **WHEN** user runs `reposcale summary results/baseline-v1-gpt4o/ results/baseline-v1-claude/`
- **THEN** the system prints a comparison table with per-case composite scores for each run

### Requirement: Stability indicators in summary
When evaluation data includes judge stability metadata, the summary SHALL display mean ± stddev for composite scores.

#### Scenario: Summary with stability data
- **WHEN** evaluations contain `stability.stddev` values
- **THEN** summary table shows composite as `mean ± stddev` instead of a single value
