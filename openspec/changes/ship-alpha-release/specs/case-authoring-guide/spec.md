## ADDED Requirements

### Requirement: Case authoring documentation
The system SHALL include a `docs/case-authoring.md` guide that describes how to create a new case pack from scratch.

#### Scenario: Contributor reads the guide
- **WHEN** a contributor opens `docs/case-authoring.md`
- **THEN** they find step-by-step instructions covering: directory structure, required files (`case.yaml`, `hints.yaml`, `repo/`, `tree.txt`), field definitions, and a worked example

### Requirement: Case pack template
The guide SHALL include a copyable template directory structure and minimal `case.yaml` + `hints.yaml` with all required fields.

#### Scenario: Contributor copies template
- **WHEN** a contributor follows the template section
- **THEN** the resulting case pack passes `reposcale validate` with zero errors

### Requirement: Difficulty calibration guidance
The guide SHALL define what constitutes `easy`, `medium`, and `hard` difficulty for each track.

#### Scenario: Author assigns difficulty
- **WHEN** an author reads the difficulty section
- **THEN** they find concrete criteria (e.g., easy = single module, obvious gaps; hard = multi-module, conflicting signals)
