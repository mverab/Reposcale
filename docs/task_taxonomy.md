# Task taxonomy

## Tracks

RepoScale is a **family of evals**, not a monolithic benchmark. Each track isolates a different facet of repo continuation intelligence.

### RepoScale-Diagnose

Evaluates diagnosis of the current project state.

- **Central question**: Does the model understand what exists, what is missing, and what is broken or incomplete?
- **Expected output**: Structured diagnosis with evidence from the repo.
- **Subcapabilities tested**: Contextual comprehension, critical diagnosis.

### RepoScale-Intent

Evaluates reconstruction of original intent.

- **Central question**: Can the model infer what product or system was intended and how much of that intent was fulfilled?
- **Expected output**: Intent reading, fulfillment assessment, and deviation analysis.
- **Subcapabilities tested**: Historical reconstruction, contextual comprehension.

### RepoScale-Plan

Evaluates ability to scale the project conceptually.

- **Central question**: Can the model design a realistic roadmap to take the project beyond its current MVP/beta?
- **Expected output**: Phased roadmap, top bets, risks, and first sprint.
- **Subcapabilities tested**: Prioritization and strategy, useful creativity.

### RepoScale-Extend

Evaluates disciplined creativity.

- **Central question**: Can the model propose plausible and coherent features or extensions for the repo?
- **Expected output**: New capabilities justified by evidence and context.
- **Subcapabilities tested**: Useful creativity, contextual comprehension.

### RepoScale-Implement

Evaluates scoped technical continuation.

- **Central question**: Can the model implement a realistic, small improvement in an existing project?
- **Expected output**: Patch/diff, tests, technical notes.
- **Subcapabilities tested**: Executive continuity, contextual comprehension.

### RepoScale-Agent

Evaluates the full agentic cycle.

- **Central question**: Can the model inspect, plan, execute, validate, and justify changes in a codebase?
- **Expected output**: Agentic trace + artifacts + results.
- **Subcapabilities tested**: All six subcapabilities.

## Execution modes

The same task can be run under different modes to isolate capabilities.

### Mode 1: `prompt_only`
- No tools, only packed textual context.
- Measures pure reasoning.

### Mode 2: `read_only_repo`
- Read access to the repo, no modifications.
- Measures real structural comprehension.

### Mode 3: `history_aware`
- Includes commit history, changelogs, harness logs.
- Measures historical reasoning.

### Mode 4: `tool_augmented`
- Can search files, read modules, query tests, inspect metadata.
- Measures realistic tool-assisted work.

### Mode 5: `agentic_budgeted`
- Coding agent access with a budget of steps, reads, edits, or time.
- Measures agent efficiency under equivalent constraints.

### Mode 6: `full_continuation`
- Analyze → propose → implement → validate → deliver.
- End-to-end benchmark.

## Phase rollout

| Phase | Tracks available |
|-------|------------------|
| **Phase 1 (MVP)** | Diagnose, Intent, Plan |
| **Phase 2** | + Extend, Implement |
| **Phase 3** | + Agent (end-to-end) |
