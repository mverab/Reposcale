## ADDED Requirements

### Requirement: Structural validation scoring (Layer 1)
The system SHALL check whether a response meets format requirements: all expected sections present, evidence tags used, hypothesis markers present.

#### Scenario: All sections present with evidence
- **WHEN** response contains all `expected_sections` from `case.yaml` and uses `[evidence]` tags
- **THEN** structural validation scores `format_valid: true`, `sections_complete: true`, `evidence_marked: true`

#### Scenario: Missing sections
- **WHEN** response is missing 2 of 5 expected sections
- **THEN** structural validation scores `sections_complete: false` and lists the missing sections in notes

### Requirement: Heuristic scoring (Layer 2)
The system SHALL compute heuristic metrics: file reference density, genericity score, and prioritization presence.

#### Scenario: High file reference density
- **WHEN** response references 8 specific file paths across 500 words
- **THEN** `file_reference_density` is calculated as references per 100 words (1.6)

#### Scenario: Generic response detection
- **WHEN** response contains no file-specific references and uses only generic advice
- **THEN** `genericity_score` is high (>0.7) indicating the response could apply to any repo

#### Scenario: Prioritization detection
- **WHEN** response includes numbered or explicitly ordered recommendations with justification
- **THEN** `prioritization_present: true`

### Requirement: LLM judge scoring (Layer 3)
The system SHALL invoke an LLM judge using `prompts/judge.md` with the case context, hints, and model response, producing dimension scores per the rubric.

#### Scenario: Judge produces valid scores
- **WHEN** the judge is invoked with a complete case + response
- **THEN** the system receives and parses scores for all 8 primary dimensions (0.0–1.0 each)

#### Scenario: Judge invocation failure
- **WHEN** the judge model API call fails
- **THEN** the system logs the error and marks the llm_judge layer as incomplete (does not fail the entire scoring)

### Requirement: Compose evaluation result
The system SHALL merge scores from all available layers into a single `evaluation.json` conforming to `schemas/evaluation.schema.json`.

#### Scenario: Full scoring pipeline
- **WHEN** structural, heuristic, and llm_judge layers all complete
- **THEN** `evaluation.json` contains all three layers and a `composite_score` computed as a weighted average

#### Scenario: Partial scoring (judge failed)
- **WHEN** structural and heuristic layers complete but llm_judge fails
- **THEN** `evaluation.json` contains the two completed layers, `composite_score` is computed from available layers only, and notes indicate the judge failure

### Requirement: Persist evaluation to disk
The system SHALL save `evaluation.json` alongside the response in `results/<run-id>/<case-id>/`.

#### Scenario: Evaluation persistence
- **WHEN** scoring completes for a case
- **THEN** `results/<run-id>/<case-id>/evaluation.json` exists and validates against `schemas/evaluation.schema.json`
