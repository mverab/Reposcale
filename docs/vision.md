# Vision

## Thesis

RepoScale is an open-source eval suite for measuring a capability poorly covered by traditional coding benchmarks:

> The ability of an LLM to **understand, continue, scale, and evolve** an existing software project coherently with its history, architecture, and product direction.

It does not just measure "if it can code."
It measures if it can operate on a living codebase with judgment.

## Core capability

The compound capability RepoScale measures can be defined as:

> **Repo continuation intelligence**: the ability to read an existing codebase, reconstruct its original intent, detect technical and product gaps, and propose or execute useful extensions without breaking continuity with what has already been built.

## Subcapabilities

The suite decomposes this capability into six axes:

### A. Contextual comprehension
- Understand repo structure
- Distinguish core from scaffolding from noise
- Identify what actually exists vs. what is claimed

### B. Historical reconstruction
- Infer original intent from artifacts
- Use commits, changelogs, docs, and harness logs
- Detect pivots, abandoned features, and drift

### C. Critical diagnosis
- Identify technical debt
- Detect inconsistencies between docs and code
- Locate product blind spots
- Notice relevant absences

### D. Useful creativity
- Propose non-obvious extensions
- Maintain coherence with stack and intent
- Avoid generic brainstorming

### E. Prioritization and strategy
- Order by impact, effort, risk, and dependency
- Design a plausible evolution sequence

### F. Executive continuity
- Convert analysis into plans, tickets, patches, or real implementations

## What RepoScale is not

RepoScale does **not** aim to be:

- A LeetCode-style algorithmic benchmark
- An autocomplete benchmark
- An isolated bug-fixing benchmark
- A greenfield code generation benchmark
- A "how many tests pass" benchmark

It does not reward:

- Overengineering
- Enterprise-by-default recommendations
- Rewrite bias
- Generic checklists recyclable across any repo

## Design principles

1. **Evidence-first** — every evaluation must reward grounding and penalize invention
2. **Creativity-with-constraints** — creativity only counts if useful, plausible, and contextual
3. **Continuity-over-rewrite** — favor coherent evolution, not rewrite reflex
4. **Multi-mode, same capability** — the same capability should be measurable with and without tools
5. **Open and inspectable** — cases, prompts, rubrics, and results must be auditable
6. **Human-calibrated** — the most interesting parts of this capability cannot depend solely on automated scoring
