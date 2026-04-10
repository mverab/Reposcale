## Context

RepoScale MVP pipeline is complete: validate, run, score (3 layers), summary, CLI. Baseline v0 ran gpt-4o-mini and gpt-4o across 3 seed cases with LLM judge calibration. The project is on `main` at tag `v0.1.0-baseline`.

To ship as a credible alpha, we need to cross the threshold from "demo" to "usable benchmark": more cases, CI, contributor onboarding, and multi-provider validation.

## Goals / Non-Goals

**Goals:**
- Ship a public alpha that early adopters can clone, run, and contribute to
- 12+ cases with balanced track/difficulty coverage
- Automated quality gate (CI) for every PR
- Clear contributor path for case authoring
- At least 2 providers in published baselines
- Judge stability data to establish confidence in scores

**Non-Goals:**
- Human rater calibration (post-alpha)
- Web UI or hosted evaluation service
- Agent-mode evaluation track
- Automated case generation from real OSS repos

## Decisions

### 1. Case expansion strategy: hand-crafted synthetic cases

**Choice:** Continue writing synthetic cases manually, simulating realistic OSS repo patterns.

**Alternatives considered:**
- Fork real OSS repos → licensing complexity, snapshot versioning headaches, cases become stale
- Generate cases with LLM → circular (using LLMs to build benchmarks for LLMs)

**Rationale:** Synthetic cases give full control over difficulty, gap placement, and ground truth. At 12–15 cases, manual is still feasible. Revisit at 50+.

### 2. Track/difficulty distribution

Target: 12 cases minimum (4 per track).

| Track | easy | medium | hard | Total |
|-------|------|--------|------|-------|
| diagnose | 2 | 1 | 1 | 4 |
| intent | 1 | 2 | 1 | 4 |
| plan | 1 | 2 | 1 | 4 |

Hard cases introduce: multi-module repos, conflicting signals, ambiguous intent.

### 3. CI: GitHub Actions with minimal matrix

**Choice:** Single workflow, Python 3.10, ubuntu-latest. Run `pytest` + `reposcale validate cases/*/` on every PR.

**Alternatives considered:**
- Multi-Python matrix (3.10, 3.11, 3.12) → overhead, no user demand yet
- Pre-commit hooks → adds friction for contributors without CI benefit

**Rationale:** Minimal CI catches regressions. Expand matrix when users report version issues.

### 4. Batch command for full-corpus runs

**Choice:** Add `reposcale batch <cases_dir> --model X [--run-id Y]` that runs all cases under a directory.

**Rationale:** Running 12+ cases one-by-one is impractical. Batch is the natural UX for baselines.

### 5. Judge stability: repeat-and-measure approach

**Choice:** Run the same `score --judge-model` 3 times per case, record all scores, report mean ± stddev.

**Implementation:** Add `--repeat N` flag to `reposcale score`. Store each run's judge output. Summary reports variance.

**Threshold:** If stddev > 0.1 on any dimension, flag as unstable.

### 6. Multi-provider: Anthropic as second provider

**Choice:** Add `claude-sonnet-4-20250514` as second baseline model (via litellm, already supported).

**Rationale:** Anthropic is the most requested alternative. litellm handles the API abstraction — no code changes needed for the runner. Only need API key and new baseline run.

### 7. Alpha release packaging

**Choice:** GitHub Release `v0.2.0-alpha` with changelog, not PyPI.

**Rationale:** Too early for PyPI distribution. GitHub Release gives visibility without maintenance burden of a package registry.

## Risks / Trade-offs

- **Case quality variance** → Mitigate with case authoring guide + PR review checklist
- **Judge instability at scale** → Mitigate by measuring before publishing; if unstable, document and lower confidence
- **Anthropic API cost** → Mitigate by keeping corpus small (12 cases × 1 run = ~$0.50)
- **Scope creep from contributors** → Mitigate with clear non-goals and contribution guidelines

## Open Questions

1. Should `reposcale batch` support `--judge-model` directly, or should scoring remain a separate step?
2. Do we need a `CHANGELOG.md` or is the GitHub Release notes sufficient for alpha?
