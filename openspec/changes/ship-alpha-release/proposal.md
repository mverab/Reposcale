## Why

RepoScale has a functional pipeline (validate → run → score → summary) with 3 seed cases and calibrated LLM judge scoring, but it's not credible as a public benchmark. The corpus is too small, there's no CI, only one provider is tested, the judge has no stability data, and there's no onboarding for external contributors. Shipping as a labeled **alpha** with these gaps closed makes it usable by early adopters and sets the foundation for community contributions.

## What Changes

- Expand corpus from 3 to 12+ cases across all three tracks (diagnose, intent, plan)
- Add GitHub Actions CI (tests + validation on every PR)
- Add case authoring guide so external contributors can write cases
- Run judge stability test (3× same eval, measure variance)
- Add at least one non-OpenAI provider to baselines (Anthropic or Google)
- Update README and docs for public-facing alpha positioning
- Create GitHub release `v0.2.0-alpha` with changelog

## Non-goals

- Full judge calibration against human raters (post-alpha)
- Web dashboard or hosted service
- Support for agent-mode evaluation (Phase 2+)
- Automated case generation

## Capabilities

### New Capabilities
- `ci-pipeline`: GitHub Actions workflow for tests, validation, and linting on PRs
- `case-authoring-guide`: Documentation for how to create new case packs from scratch
- `judge-stability`: Tooling and methodology to measure judge score variance across repeated runs
- `expanded-corpus`: 9+ new cases bringing total to 12+ with balanced track coverage

### Modified Capabilities
- `seed-cases`: Rename to reflect expanded corpus, add new case types and difficulty levels
- `scoring-pipeline`: Add judge stability metadata to evaluation output
- `cli-entrypoint`: Add `reposcale batch` command for running all cases in one shot
- `results-summary`: Support multi-run comparison tables for cross-model and cross-provider results

## Impact

- `cases/` — 9+ new case directories with full packs
- `cases/CORPUS_V0.md` → `cases/CORPUS.md` — expanded manifest
- `.github/workflows/` — new CI configuration
- `docs/` — case authoring guide, updated baseline, alpha README
- `src/reposcale/scoring/llm_judge.py` — stability metadata fields
- `src/reposcale/scoring/coordinator.py` — stability tracking
- `src/reposcale/cli.py` — batch command
- `src/reposcale/summary.py` — comparison tables
- `tests/` — new tests for batch, stability, expanded validation
- `schemas/evaluation.schema.json` — optional stability fields
