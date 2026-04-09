## 1. Project structure and dependencies

- [x] 1.1 Create `src/reposcale/__init__.py` with version constant — new file `src/reposcale/__init__.py`
- [x] 1.2 Create `src/reposcale/config.py` with project paths (SCHEMAS_DIR, PROMPTS_DIR, CASES_DIR, RESULTS_DIR) — new file `src/reposcale/config.py`
- [x] 1.3 Update `pyproject.toml` to add `click`, `litellm`, `httpx` deps, register `reposcale` console script entrypoint, and set `src/` as package dir — modifies `pyproject.toml`
- [x] 1.4 Move validation logic from `scripts/validate_case_pack.py` into `src/reposcale/validate.py` as importable functions; keep script as thin wrapper — new file `src/reposcale/validate.py`, modifies `scripts/validate_case_pack.py`
- [x] 1.5 Move runner logic from `scripts/run_eval.py` into `src/reposcale/runner.py`; keep script as thin wrapper — new file `src/reposcale/runner.py`, modifies `scripts/run_eval.py`

## 2. Case validation enhancements

- [x] 2.1 Add repo snapshot non-empty check (exclude `.gitkeep`) to `src/reposcale/validate.py` — modifies `src/reposcale/validate.py`
- [x] 2.2 Add `hints.yaml` structure validation (expected fields: `known_gaps`, `original_intent`, `key_files`) to `src/reposcale/validate.py` — modifies `src/reposcale/validate.py`
- [x] 2.3 Add batch validation with pass/fail summary reporting — modifies `src/reposcale/validate.py`
- [x] 2.4 Write tests for validation: valid case, missing fields, empty repo, malformed hints — new file `tests/test_validate.py`

## 3. Seed cases

- [x] 3.1 Curate Diagnose seed case (`diagnose-001`): select a real OSS repo (<5MB), create snapshot, write `case.yaml`, `hints.yaml`, and `tree.txt` — new directory `cases/diagnose/diagnose-001/`
- [x] 3.2 Curate Intent seed case (`intent-001`): select a repo with visible pivots or divergent docs, create full case pack — new directory `cases/intent/intent-001/`
- [x] 3.3 Curate Plan seed case (`plan-001`): select a functional-but-not-scalable repo, create full case pack — new directory `cases/plan/plan-001/`
- [x] 3.4 Validate all seed cases pass `reposcale validate` with zero errors — runs validation against all `cases/*/`

## 4. Eval runner (prompt_only mode)

- [x] 4.1 Implement prompt assembly in `src/reposcale/runner.py`: combine track template + case context (metadata, file tree, docs, history) — modifies `src/reposcale/runner.py`
- [x] 4.2 Implement LLM invocation via `litellm.completion()` with configurable `--model` flag — modifies `src/reposcale/runner.py`
- [x] 4.3 Implement response parser: extract sections by headings, detect `[evidence]` tags, map to `schemas/response.schema.json` — new file `src/reposcale/parser.py`
- [x] 4.4 Implement response persistence: save `response.json` to `results/<run-id>/<case-id>/` — modifies `src/reposcale/runner.py`
- [x] 4.5 Implement `--dry-run` flag that prints assembled prompt without API call — modifies `src/reposcale/runner.py`
- [x] 4.6 Implement run ID generation (`YYYYMMDD-HHMMSS-<model-short>`) — modifies `src/reposcale/runner.py`
- [x] 4.7 Implement batch run across a track directory — modifies `src/reposcale/runner.py`
- [x] 4.8 Write tests for prompt assembly and response parsing (mock LLM calls) — new file `tests/test_runner.py`

## 5. Scoring pipeline

- [x] 5.1 Create scorer interface in `src/reposcale/scoring/__init__.py`: base `Scorer` class with `score(case, response) → dict` method — new file `src/reposcale/scoring/__init__.py`
- [x] 5.2 Implement structural scorer (Layer 1): format check, sections completeness, evidence marking — new file `src/reposcale/scoring/structural.py`
- [x] 5.3 Implement heuristic scorer (Layer 2): file reference density, genericity score, prioritization detection — new file `src/reposcale/scoring/heuristic.py`
- [x] 5.4 Implement LLM judge scorer (Layer 3): invoke judge model with `prompts/judge.md`, parse dimension scores — new file `src/reposcale/scoring/llm_judge.py`
- [x] 5.5 Implement scoring coordinator: run all available layers, merge results, compute composite score, save `evaluation.json` — new file `src/reposcale/scoring/coordinator.py`
- [x] 5.6 Write tests for structural and heuristic scorers with fixture responses — new file `tests/test_scoring.py`

## 6. Results summary

- [x] 6.1 Implement per-case summary: load `evaluation.json`, format composite + dimension scores — new file `src/reposcale/summary.py`
- [x] 6.2 Implement per-track aggregation: mean ± std across cases in a track — modifies `src/reposcale/summary.py`
- [x] 6.3 Implement run-level summary: totals, per-track breakdown, overall composite — modifies `src/reposcale/summary.py`
- [x] 6.4 Implement Rich terminal table output and `--json` flag for file output — modifies `src/reposcale/summary.py`

## 7. CLI entrypoint

- [x] 7.1 Create `src/reposcale/cli.py` with Click group and four subcommands: `validate`, `run`, `score`, `summary` — new file `src/reposcale/cli.py`
- [x] 7.2 Wire `validate` subcommand to `src/reposcale/validate.py` — modifies `src/reposcale/cli.py`
- [x] 7.3 Wire `run` subcommand with `--model`, `--dry-run`, and optional `--run-id` flags — modifies `src/reposcale/cli.py`
- [x] 7.4 Wire `score` subcommand with `--judge-model` flag — modifies `src/reposcale/cli.py`
- [x] 7.5 Wire `summary` subcommand with `--json` flag — modifies `src/reposcale/cli.py`

## 8. Integration and verification

- [x] 8.1 Run full pipeline end-to-end on one seed case: validate → run (dry-run) → verify prompt output — manual verification
- [x] 8.2 Run full pipeline with real model call on one seed case: validate → run → score → summary — manual verification
- [x] 8.3 Verify all output files conform to their respective JSON schemas — modifies `tests/test_validate.py`
- [ ] 8.4 Update `README.md` with quickstart instructions for the pipeline — modifies `README.md`
