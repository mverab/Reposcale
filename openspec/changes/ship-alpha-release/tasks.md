## 1. CI Pipeline

- [ ] 1.1 Create `.github/workflows/ci.yml` — pytest + validate on PR (ubuntu-latest, Python 3.10)
- [ ] 1.2 Test CI locally with `act` or push a test branch to verify workflow runs
- [ ] 1.3 Add branch protection rule for `main` requiring CI pass

## 2. Batch Command

- [ ] 2.1 Add `batch` subcommand to `src/reposcale/cli.py` — discovers cases recursively, runs all with `--model` and `--run-id`
- [ ] 2.2 Handle invalid case packs during batch (skip + warn, don't abort)
- [ ] 2.3 Add test for batch command in `tests/test_cli.py`

## 3. Judge Stability

- [ ] 3.1 Add `--repeat N` flag to `score` subcommand in `src/reposcale/cli.py`
- [ ] 3.2 Implement repeat logic in `src/reposcale/scoring/coordinator.py` — run judge N times, collect all scores
- [ ] 3.3 Compute and store stability metadata (mean, stddev, per_dimension) in `src/reposcale/scoring/llm_judge.py`
- [ ] 3.4 Flag unstable dimensions (stddev > 0.1) in evaluation output and CLI
- [ ] 3.5 Extend `schemas/evaluation.schema.json` with optional `stability` object in llm_judge layer
- [ ] 3.6 Add tests for stability computation in `tests/test_scoring.py`

## 4. Expanded Corpus — Diagnose Track

- [ ] 4.1 Create `cases/diagnose/diagnose-002/` — medium difficulty, multi-module with missing integration tests
- [ ] 4.2 Create `cases/diagnose/diagnose-003/` — easy, single-file script with obvious bugs
- [ ] 4.3 Create `cases/diagnose/diagnose-004/` — hard, multi-module with conflicting signals and red herrings

## 5. Expanded Corpus — Intent Track

- [ ] 5.1 Create `cases/intent/intent-002/` — medium, API that pivoted authentication strategy
- [ ] 5.2 Create `cases/intent/intent-003/` — hard, project with multiple abandoned feature branches and conflicting commits
- [ ] 5.3 Create `cases/intent/intent-004/` — easy, clear README-vs-code divergence

## 6. Expanded Corpus — Plan Track

- [ ] 6.1 Create `cases/plan/plan-002/` — medium, monolith needing service extraction
- [ ] 6.2 Create `cases/plan/plan-003/` — hard, multi-language repo with complex deployment needs
- [ ] 6.3 Create `cases/plan/plan-004/` — easy, well-structured app needing only CI/CD and monitoring

## 7. Corpus Validation & Manifest

- [ ] 7.1 Run `reposcale validate` on all 12 cases, fix any failures
- [ ] 7.2 Update `cases/CORPUS_V0.md` → `cases/CORPUS.md` with full inventory (ID, track, type, difficulty, description)
- [ ] 7.3 Generate SHA-256 checksums for all case files

## 8. Case Authoring Guide

- [ ] 8.1 Create `docs/case-authoring.md` — directory structure, required files, field definitions, difficulty criteria
- [ ] 8.2 Include a copyable template (`case.yaml` + `hints.yaml` skeleton) in the guide
- [ ] 8.3 Add a worked example (walk through creating a case from scratch)

## 9. Multi-Run Summary Comparison

- [ ] 9.1 Extend `reposcale summary` to accept multiple run dirs in `src/reposcale/summary.py`
- [ ] 9.2 Render side-by-side comparison table with Rich in `src/reposcale/summary.py`
- [ ] 9.3 Include stability indicators (mean ± stddev) when available
- [ ] 9.4 Add test for multi-run comparison in `tests/test_scoring.py` or `tests/test_cli.py`

## 10. Multi-Provider Baseline

- [ ] 10.1 Run `reposcale batch cases/ --model claude-sonnet-4-20250514 --run-id baseline-v1-claude` (requires ANTHROPIC_API_KEY)
- [ ] 10.2 Score with `--judge-model gpt-4o --repeat 3` for stability data
- [ ] 10.3 Run `reposcale batch cases/ --model gpt-4o-mini --run-id baseline-v1-gpt4o-mini` + score with repeat
- [ ] 10.4 Run `reposcale batch cases/ --model gpt-4o --run-id baseline-v1-gpt4o` + score with repeat

## 11. Alpha Release Documentation

- [ ] 11.1 Update `README.md` — alpha positioning, expanded quickstart, contribution call, badge for CI
- [ ] 11.2 Update `docs/baseline-v0.md` → `docs/baseline-v1.md` with 12-case, multi-provider results
- [ ] 11.3 Review and update `CONTRIBUTING.md` — link to case authoring guide, PR workflow
- [ ] 11.4 Create `CHANGELOG.md` with v0.1.0-baseline and v0.2.0-alpha entries

## 12. Release

- [ ] 12.1 Tag `v0.2.0-alpha` on main
- [ ] 12.2 Create GitHub Release with changelog and summary of capabilities
- [ ] 12.3 Verify the clone → install → validate → run flow works from a clean checkout
