# Changelog

## v0.1.0-alpha — Alpha Release

### Added
- **CI Pipeline**: GitHub Actions workflow running tests + case validation on PRs
- **Batch command**: `reposcale batch` discovers and runs all valid case packs
- **Judge stability**: `--repeat N` on score command; mean, stddev, and unstable dimension detection
- **Expanded corpus**: 12 cases across 3 tracks (diagnose, intent, plan) and 3 difficulty levels
- **Corpus manifest**: `cases/CORPUS.md` with inventory, coverage matrix, and case type reference
- **Case authoring guide**: `docs/case-authoring.md` with templates and difficulty calibration
- **Multi-run comparison**: `reposcale compare` command with side-by-side tables
- **Baseline script**: `scripts/run-baselines.sh` for GPT-4o and Claude baselines
- **Schema extensions**: evaluation schema now supports stability metadata, hallucinations, strengths, weaknesses

### Changed
- `case_type` enum extended with 6 new types for expanded corpus
- README updated to reflect alpha status and new commands
- CONTRIBUTING.md updated with case authoring guide reference

## v0.0.1 — MVP Pipeline

### Added
- Core package: validate, run, score, summary pipeline
- CLI: `reposcale validate`, `run`, `score`, `summary`
- 3 seed cases (diagnose-001, intent-001, plan-001)
- 3-layer scoring: structural, heuristic, LLM judge
- JSON schemas for case, response, and evaluation
- 31 tests
