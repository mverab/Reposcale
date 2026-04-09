## ADDED Requirements

### Requirement: Assemble evaluation prompt from case pack
The system SHALL construct a complete evaluation prompt by combining the track prompt template (`prompts/<track>.md`) with case context (metadata, file tree, docs, history).

#### Scenario: Prompt assembly for diagnose track
- **WHEN** a case pack with `track: diagnose` is loaded
- **THEN** the system combines `prompts/diagnose.md` with the case's file tree, description, and any available docs into a single prompt

### Requirement: Invoke LLM via litellm
The system SHALL invoke an LLM using `litellm.completion()` with the assembled prompt and a configurable model identifier.

#### Scenario: Successful model invocation
- **WHEN** the user specifies `--model gpt-4o` and a valid case pack
- **THEN** the system sends the prompt to the specified model and receives a text response

#### Scenario: Missing API key
- **WHEN** the required API key environment variable is not set
- **THEN** the system reports a clear error indicating which env var is needed

### Requirement: Parse response into structured format
The system SHALL parse the model's raw text response into the `schemas/response.schema.json` format, extracting sections and evidence references.

#### Scenario: Well-structured model response
- **WHEN** the model returns a response with clear section headings matching expected_sections
- **THEN** the system maps each section to the response schema's `sections` object

#### Scenario: Unstructured model response
- **WHEN** the model returns a response without clear section headings
- **THEN** the system stores the full response under a single `raw_output` section and logs a warning

### Requirement: Persist response to disk
The system SHALL save the structured response as `response.json` in `results/<run-id>/<case-id>/`.

#### Scenario: Response persistence
- **WHEN** an eval run completes successfully
- **THEN** `results/<run-id>/<case-id>/response.json` exists and validates against `schemas/response.schema.json`

### Requirement: Dry run mode
The system SHALL support a `--dry-run` flag that assembles and displays the prompt without invoking any LLM API.

#### Scenario: Dry run output
- **WHEN** `--dry-run` is passed
- **THEN** the system prints the assembled prompt to stdout and exits without making API calls

### Requirement: Run against multiple cases
The system SHALL accept a directory of case packs (e.g., `cases/diagnose/`) and run the eval sequentially for each case.

#### Scenario: Batch eval run
- **WHEN** `cases/diagnose/` contains 3 case packs
- **THEN** the system runs the eval for each case and saves 3 separate response files
