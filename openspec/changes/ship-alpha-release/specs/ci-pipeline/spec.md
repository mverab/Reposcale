## ADDED Requirements

### Requirement: Automated test suite on pull requests
The system SHALL run `pytest` on every pull request targeting `main` using GitHub Actions.

#### Scenario: PR with passing tests
- **WHEN** a PR is opened or updated targeting `main`
- **THEN** GitHub Actions runs `pip install -e .` and `pytest tests/ -v` and the check passes

#### Scenario: PR with failing tests
- **WHEN** a PR has test failures
- **THEN** the GitHub Actions check fails and blocks merge

### Requirement: Automated case validation on pull requests
The system SHALL run `reposcale validate` on all cases when case files are modified in a PR.

#### Scenario: PR modifies case files
- **WHEN** a PR includes changes to files under `cases/`
- **THEN** GitHub Actions runs `reposcale validate cases/*/` and reports pass/fail

#### Scenario: PR does not touch cases
- **WHEN** a PR has no changes under `cases/`
- **THEN** case validation step is skipped or passes trivially

### Requirement: Single Python version CI
The CI workflow SHALL target Python 3.10 on ubuntu-latest only.

#### Scenario: CI environment
- **WHEN** the CI workflow runs
- **THEN** it uses `ubuntu-latest` with Python 3.10 and installs the project in editable mode
