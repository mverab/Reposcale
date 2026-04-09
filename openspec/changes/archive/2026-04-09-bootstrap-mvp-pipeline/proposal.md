## Why

RepoScale has a complete definition layer (docs, schemas, prompts) but no functional pipeline. The scaffolding in `scripts/`, `schemas/`, and `prompts/` defines *what* the system should do, but nothing actually runs end-to-end yet. Without a working pipeline — validate cases → run evals → score responses — the project cannot produce its first baseline results or accept external case contributions with confidence.

Phase 0 (definition) is complete. This change bootstraps Phase 1: a minimal but functional eval pipeline that can validate case packs, run prompt-only evaluations, score responses, and produce structured results.

## What Changes

- **Case validation** (`scripts/validate_case_pack.py`): already exists as a basic schema validator. Needs to handle all case pack artifacts (repo snapshot checks, hints validation, tree consistency).
- **Eval runner** (`scripts/run_eval.py`): currently only assembles prompts. Needs to invoke LLM APIs, capture responses in `response.schema.json` format, and persist results.
- **Scoring pipeline** (new `scripts/score_eval.py`): does not exist yet. Needs to implement Layer 1 (structural validation) and Layer 2 (heuristic scoring) from `docs/scoring.md`, plus an LLM judge integration for Layer 3.
- **Results summarization** (new `scripts/summarize_results.py`): does not exist yet. Needs to aggregate evaluation results into a per-case and per-track summary.
- **First seed cases**: `cases/diagnose/`, `cases/intent/`, and `cases/plan/` are empty. Need 3–5 curated cases using real repos to validate the pipeline.
- **CLI entrypoint** (new): a unified `reposcale` CLI that wraps validate, run, score, and summarize.

## Non-goals

- Agentic execution modes (`tool_augmented`, `agentic_budgeted`, `full_continuation`) — deferred to Phase 2.
- Leaderboard or public reporting — deferred to Phase 3.
- Extend, Implement, or Agent tracks — deferred to Phase 2.
- Human review UI — deferred indefinitely; manual for now.
- Production-grade infra (containers, CI/CD, rate limiting) — premature.

## Capabilities

### New Capabilities
- `case-validation`: Full case pack validation against `schemas/case.schema.json` with structural checks on repo snapshots, hints, and tree consistency.
- `eval-runner`: LLM-backed eval runner for `prompt_only` mode that invokes models via API, captures responses in `schemas/response.schema.json` format, and persists results to disk.
- `scoring-pipeline`: Multi-layer scoring engine implementing structural validation (Layer 1), heuristic scoring (Layer 2), and LLM judge integration (Layer 3) per `docs/scoring.md`.
- `results-summary`: Aggregation of evaluation results into per-case and per-track summaries with composite scores.
- `cli-entrypoint`: Unified `reposcale` CLI wrapping validate, run, score, and summarize commands.
- `seed-cases`: First 3–5 curated benchmark cases for Diagnose, Intent, and Plan tracks using real open-source repos.

### Modified Capabilities
<!-- No existing specs to modify -->

## Impact

- **Scripts**: `scripts/validate_case_pack.py` and `scripts/run_eval.py` will be rewritten/extended. New files: `scripts/score_eval.py`, `scripts/summarize_results.py`.
- **New package**: `src/reposcale/` Python package with CLI entrypoint registered in `pyproject.toml`.
- **Schemas**: may need minor additions to `schemas/response.schema.json` and `schemas/evaluation.schema.json` as implementation reveals gaps.
- **Dependencies**: new deps in `pyproject.toml` — `click` (CLI), `openai` or `litellm` (LLM API), `httpx` (HTTP client).
- **Cases**: 3–5 new case pack directories under `cases/diagnose/`, `cases/intent/`, `cases/plan/`.
