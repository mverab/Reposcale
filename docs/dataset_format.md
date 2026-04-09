# Dataset format

## Case pack structure

Each benchmark case is a **case pack** — a self-contained directory with a consistent structure.

```text
cases/<track>/<case-id>/
  case.yaml           # required — case metadata and configuration
  repo/               # required — repo snapshot (or pointer)
  tree.txt            # recommended — file tree for quick reference
  docs/               # optional — relevant extracted docs
  history.json        # optional — commit history summary
  issues.md           # optional — open issues or TODOs
  changelog.md        # optional — changelog if available
  hints.yaml          # optional — evaluation hints (not shown to model)
```

## Case metadata (`case.yaml`)

```yaml
id: "diagnose-001"
track: "diagnose"
title: "Incomplete task management CLI"
description: "A Python CLI for task management with partial implementation."
case_type: "mvp_incomplete"
difficulty: "medium"
tags: ["python", "cli", "partial-implementation"]
repo_source: "snapshot"        # snapshot | git_url | archive
supported_modes:
  - prompt_only
  - read_only_repo
  - tool_augmented
expected_sections:              # what the response should contain
  - project_summary
  - gap_analysis
  - recommendations
created_at: "2025-01-15"
version: "1.0"
```

## Case types

| Type | Description | Tests |
|------|-------------|-------|
| **A: MVP incomplete** | Clear intent, partial implementation, visible gaps | Comprehension + gap detection |
| **B: Divergent beta** | Docs and code no longer fully align, commits show pivots | Historical reasoning + diagnosis |
| **C: Inflated scaffold** | Heavy scaffolding, little real product | Signal-vs-noise discrimination |
| **D: Functional but not scalable** | Works but needs evolution | Strategic thinking, avoids "rewrite everything" |
| **E: Eroded repo** | Heavy debt, mixed signals | Ordering under ambiguity |

## Repo snapshot format

The `repo/` directory contains either:
- A **direct snapshot** of the repository files, or
- A **git repository** (with `.git/` intact for history-aware modes)

For `prompt_only` mode, the runner packs relevant context from the case pack into the prompt.

## History format (`history.json`)

```json
[
  {
    "hash": "abc1234",
    "author": "dev@example.com",
    "date": "2025-01-10T14:30:00Z",
    "message": "feat: add task creation endpoint",
    "files_changed": ["src/api/tasks.py", "tests/test_tasks.py"]
  }
]
```

## Evaluation hints (`hints.yaml`)

Not shown to the model. Used by judges and scorers to calibrate evaluation.

```yaml
known_gaps:
  - "Authentication middleware is defined but never applied"
  - "Database migration scripts are missing"
original_intent: "Full-featured task management API with team collaboration"
key_files:
  - "src/api/tasks.py"
  - "src/models/task.py"
expected_difficulty_areas:
  - "Distinguishing placeholder code from real implementation"
```
