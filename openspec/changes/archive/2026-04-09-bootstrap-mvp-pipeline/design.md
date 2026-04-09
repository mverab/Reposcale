## Context

RepoScale's Phase 0 scaffolding is complete: `docs/`, `schemas/`, `prompts/`, and `cases/example/` define the evaluation framework. Two scripts exist (`scripts/validate_case_pack.py` and `scripts/run_eval.py`) but neither completes a full eval cycle. There is no scoring, no model invocation, no result persistence, and no real benchmark cases.

The project needs to go from "well-defined spec" to "working pipeline that can produce its first eval results."

### Current state
- **`schemas/`**: 3 JSON Schemas (case, response, evaluation) — stable, well-structured
- **`prompts/`**: 4 prompt templates (diagnose, intent, plan, judge) — usable as-is
- **`scripts/validate_case_pack.py`**: validates `case.yaml` against schema, checks required files
- **`scripts/run_eval.py`**: assembles prompts from case packs, no model invocation
- **`cases/example/`**: reference case pack, no real repo snapshot

## Goals / Non-Goals

**Goals:**
- A functional end-to-end pipeline: `validate → run → score → summarize`
- Support `prompt_only` execution mode only (simplest, no tool infra needed)
- Produce structured results conforming to `schemas/response.schema.json` and `schemas/evaluation.schema.json`
- 3–5 real seed cases that exercise the pipeline
- A single `reposcale` CLI that wraps all commands

**Non-Goals:**
- Agentic modes or tool-augmented execution
- Multi-provider model routing or cost optimization
- Web UI, dashboards, or real-time monitoring
- Tracks beyond Phase 1 (Diagnose, Intent, Plan)
- Distributed execution or job queuing

## Decisions

### D1: Python package structure → `src/reposcale/`

**Choice**: Move core logic into a proper `src/reposcale/` package; keep `scripts/` as thin CLI wrappers that import from the package.

**Why**: Scripts with inline logic don't scale. A package allows proper imports, testing, and a registered CLI entrypoint. The current `scripts/` files are ~100 lines each — easy to refactor now, painful later.

**Alternative considered**: Keep everything in `scripts/`. Rejected because it blocks testing, reuse, and CLI registration.

### D2: LLM integration → `litellm`

**Choice**: Use `litellm` as the LLM abstraction layer.

**Why**: `litellm` provides a unified interface to OpenAI, Anthropic, Google, and 100+ providers with a single `completion()` call. This avoids vendor lock-in and lets contributors run evals with whichever model they have API access to. Configuration via env vars (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.).

**Alternative considered**: Direct `openai` SDK. Rejected because it limits contributors to OpenAI models only. `litellm` adds one dependency but removes the provider constraint.

### D3: CLI framework → `click`

**Choice**: Use `click` for the CLI.

**Why**: Already a transitive dependency of many Python tools, well-documented, supports subcommands naturally (`reposcale validate`, `reposcale run`, `reposcale score`, `reposcale summary`).

**Alternative considered**: `argparse`. Rejected because subcommand composition is verbose. `typer` was also considered but adds a `typing_extensions` dependency chain for minimal benefit at this scale.

### D4: Result storage → filesystem (JSON/YAML files)

**Choice**: Store all results as structured files in a `results/` directory tree mirroring the case structure.

**Why**: No database needed at this scale. Files are inspectable, diffable, and versionable. Structure: `results/<run-id>/<case-id>/response.json`, `results/<run-id>/<case-id>/evaluation.json`.

**Alternative considered**: SQLite. Rejected as premature for MVP — introduces schema migration concerns without clear benefit at <100 eval runs.

### D5: Scoring engine → modular scorers with registry

**Choice**: Each scoring layer (structural, heuristic, llm_judge) is a Python module with a common interface: `score(case, response) → partial evaluation dict`. A coordinator merges partial results into the final `evaluation.json`.

**Why**: Matches the multi-layer scoring design in `docs/scoring.md`. New layers (execution, human) can be added later without changing the coordinator.

### D6: Seed cases → snapshot real OSS repos

**Choice**: Seed cases use static snapshots of real open-source repos (frozen at a specific commit). Stored directly in `cases/<track>/<case-id>/repo/`.

**Why**: Reproducibility requires frozen snapshots. Git submodules or URL references introduce external dependencies that can break. Snapshots are large but reliable. Use `.gitignore` patterns for binaries and node_modules.

**Alternative considered**: Git submodules or cloning at runtime. Rejected for reproducibility — the same eval must produce the same inputs regardless of upstream changes.

## Risks / Trade-offs

- **Repo snapshot size** → Mitigation: choose small repos (<5MB) for seed cases; document size guidelines in `CONTRIBUTING.md`.
- **LLM API costs** → Mitigation: `prompt_only` mode is the cheapest. Document expected cost per eval in README. Add `--dry-run` flag to CLI.
- **`litellm` stability** → Mitigation: pin version in `pyproject.toml`; thin wrapper so swapping is easy.
- **Schema drift** → Mitigation: `validate_case_pack.py` runs in CI; schemas are the source of truth.
- **Judge reliability** → Mitigation: human review remains mandatory for leaderboard claims; LLM judge is a signal, not ground truth.

## Open Questions

1. **Model for LLM judge**: Should we pin a specific judge model (e.g., `gpt-4o`) or let contributors choose? Pinning improves consistency; flexibility improves accessibility.
2. **Case licensing**: How do we handle licensing for repo snapshots of third-party OSS projects? Need to verify that snapshot + redistribution is covered by original license.
3. **Result format versioning**: Should `results/` include a format version for future compatibility?
