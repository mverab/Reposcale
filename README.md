# RepoScale

**RepoScale** is an open-source evaluation suite for measuring how well LLMs can understand, continue, and scale existing software projects.

Unlike traditional coding benchmarks that focus on isolated tasks or greenfield code generation, RepoScale evaluates a harder and more realistic capability:

> Can a model read an existing codebase, infer what it is trying to become, identify what is missing, and propose or execute a coherent path forward?

## Why RepoScale?

Most real software work does not start from a blank file.

It starts with an existing repository, partial implementations, inconsistent documentation, historical baggage, unfinished ideas, architectural constraints, and a moving product target.

RepoScale measures whether a model can operate in that environment with real judgment.

## What RepoScale evaluates

RepoScale focuses on **repo continuation intelligence**, including:

- **Project understanding** — structural and functional comprehension
- **Historical reasoning** — from commits, changelogs, and docs
- **Intent reconstruction** — what was this project trying to become?
- **Gap detection** — what is missing, broken, or incomplete?
- **Useful creativity** — coherent extensions, not generic brainstorming
- **Prioritization** — ordering by impact, effort, risk, and dependency
- **Architectural coherence** — respecting existing structure and constraints
- **Actionable continuation** — plans, patches, and implementations that work

## What RepoScale does not evaluate

RepoScale is **not** a benchmark for:

- Isolated algorithmic coding (LeetCode-style)
- Autocomplete
- One-function bug fixing
- Greenfield app generation
- Raw pass@k on synthetic tasks

It also does not reward overengineering, enterprise-by-default recommendations, rewrite bias, or generic checklists recyclable across any repo.

## Benchmark tracks

RepoScale is organized into multiple tracks:

| Track | Question | Output |
|-------|----------|--------|
| **Diagnose** | Does the model understand what exists, what is missing, and what is broken? | Structured diagnosis with evidence |
| **Intent** | Can it infer the original product/system direction? | Intent reading, fulfillment, deviations |
| **Plan** | Can it design a realistic roadmap to scale the project? | Phased roadmap, risks, first sprint |
| **Extend** | Can it propose coherent missing capabilities? | Justified new capabilities |
| **Implement** | Can it make a scoped, meaningful change? | Patch, diff, tests, technical notes |
| **Agent** | Can it run a full analyze-plan-execute-validate loop? | Agentic trace + artifacts + results |

## Execution modes

Each task can be evaluated under different modes to isolate specific capabilities:

| Mode | Description |
|------|-------------|
| `prompt_only` | No tools, only packed textual context |
| `read_only_repo` | Read access to repo, no modifications |
| `history_aware` | Includes commit history, changelogs, harness logs |
| `tool_augmented` | Can search files, read modules, inspect metadata |
| `agentic_budgeted` | Coding agent access with step/time/token budget |
| `full_continuation` | End-to-end: analyze, propose, implement, validate |

## Core principles

- **Evidence first** — claims must be grounded in the repo, docs, or history
- **Creativity with constraints** — useful ideas beat generic brainstorming
- **Continuity over rewrite** — preserve coherence with what already exists
- **Multi-layer evaluation** — structure, semantics, execution, and human review
- **Open and reproducible** — cases, protocols, and scoring are inspectable

## Repository structure

```text
src/reposcale/  core Python package (validate, run, score, summary, CLI)
docs/           design specs and governance documents
cases/          benchmark case packs organized by track
schemas/        JSON schemas for cases, responses, and evaluations
prompts/        task and judge prompts
scripts/        thin wrappers around core logic
tests/          pytest suite
results/        evaluation outputs (gitignored)
```

## Project status

RepoScale is in **Phase 1 — MVP pipeline**.

Current goals:
- [x] Define the capability model
- [x] Publish the task taxonomy
- [x] Define base schemas (case, response, evaluation)
- [x] Ship validation, runner, scoring, and summary pipeline
- [x] Seed cases for Diagnose, Intent, and Plan tracks
- [ ] Release the first 10–15 curated cases
- [ ] Establish baseline results across models

## Quickstart

```bash
# Install
pip install -e .

# Validate case packs
reposcale validate cases/diagnose/diagnose-001/

# Run evaluation (dry-run — prints the assembled prompt)
reposcale run cases/diagnose/diagnose-001/ --model gpt-4o --dry-run

# Run evaluation (requires LLM API key, e.g. OPENAI_API_KEY)
reposcale run cases/diagnose/diagnose-001/ --model gpt-4o

# Score responses (structural + heuristic; add --judge-model for LLM judge)
reposcale score results/<run-id>/

# View summary
reposcale summary results/<run-id>/
```

## Contributing

We welcome contributions in:

- **Case curation** — real repos, real scenarios
- **Rubric design** — evaluation criteria and scoring dimensions
- **Judge calibration** — LLM judge prompts and human alignment
- **Runner implementations** — local, batch, and agentic runners
- **Scoring heuristics** — structural, semantic, and execution validators
- **Failure mode analysis** — what goes wrong and why

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

[MIT](LICENSE)
