## ADDED Requirements

### Requirement: Repeated judge scoring
The `reposcale score` command SHALL support a `--repeat N` flag that runs the LLM judge N times per case and stores all results.

#### Scenario: Score with repeat
- **WHEN** user runs `reposcale score results/run-1/ --judge-model gpt-4o --repeat 3`
- **THEN** the judge is invoked 3 times per case, and all 3 sets of dimension scores are stored in the evaluation output

### Requirement: Stability metadata in evaluation output
The evaluation JSON SHALL include a `judge_stability` object when `--repeat` is used, containing `runs` (count), `mean`, `stddev`, and `per_dimension` breakdowns.

#### Scenario: Evaluation with stability data
- **WHEN** scoring completes with `--repeat 3`
- **THEN** `evaluation.json` contains `layers.llm_judge.stability` with `{ "runs": 3, "mean": X, "stddev": Y, "per_dimension": {...} }`

### Requirement: Instability flag
The system SHALL flag any dimension with stddev > 0.1 as unstable in the evaluation output and CLI output.

#### Scenario: Stable scores
- **WHEN** all dimensions have stddev ≤ 0.1 across repeats
- **THEN** no instability warnings are shown

#### Scenario: Unstable dimension
- **WHEN** a dimension has stddev > 0.1 across repeats
- **THEN** the CLI prints a warning and the evaluation JSON includes `"unstable_dimensions": ["dimension_name"]`
