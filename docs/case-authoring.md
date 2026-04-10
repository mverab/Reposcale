# Case Authoring Guide

How to create a new case pack for RepoScale.

## Directory structure

```
cases/<track>/<case-id>/
├── case.yaml        # Required — case metadata
├── hints.yaml       # Required — evaluation hints for the judge
├── tree.txt         # Required — file tree of the repo snapshot
└── repo/            # Required — repository snapshot
    ├── src/
    ├── tests/
    └── README.md
```

## Required files

### `case.yaml`

```yaml
id: diagnose-005            # Unique ID: <track>-<3-digit-number>
track: diagnose              # One of: diagnose, intent, plan
title: Short descriptive title (10-120 chars)
description: >
  A longer description of the repo and what the case tests.
  Must be at least 10 characters. Explain the scenario clearly.
case_type: mvp_incomplete    # See case types below
difficulty: easy             # One of: easy, medium, hard
repo_source: snapshot        # Always "snapshot" for now
supported_modes:
  - prompt_only              # Always include this
expected_sections:           # Sections the model should produce
  - project_summary
  - what_works
  - what_is_broken
  - recommendations
version: "1.0"
```

**Track-specific `expected_sections`:**

| Track | Sections |
|-------|----------|
| diagnose | project_summary, what_works, what_is_broken, recommendations |
| intent | project_summary, original_intent, current_state, drift_analysis |
| plan | project_summary, bottlenecks, scaling_plan, migration_steps |

### `hints.yaml`

```yaml
known_gaps:
  - First known gap or bug
  - Second known gap
  - At least 2 entries recommended
original_intent: >
  What the project was originally trying to achieve.
key_files:
  - src/main.py
  - tests/test_main.py
  # At least 2 files that are most relevant to the case
```

### `tree.txt`

A text representation of the repo file tree. Generate with:
```bash
find repo/ -type f | sort | sed 's|^|  |' > tree.txt
```
Or use `tree repo/` if available.

### `repo/`

The repository snapshot. Must contain at least one file. Guidelines:
- Include real-looking code (not lorem ipsum)
- Include bugs, gaps, or architectural issues that match `known_gaps`
- Keep files under 8KB each for judge context
- Include README.md, tests, and config files for realism

## Case types

| Type | Description |
|------|-------------|
| `mvp_incomplete` | Missing features, unwired components |
| `single_file_buggy` | Single file with obvious bugs |
| `multi_module_tangled` | Multi-module with inconsistent patterns |
| `divergent_beta` | Pivoted direction mid-development |
| `abandoned_rewrite` | Has an abandoned rewrite attempt |
| `readme_code_divergence` | README describes non-existent features |
| `functional_not_scalable` | Works but can't scale |
| `multi_language_unscalable` | Multi-language, no operational infra |
| `needs_ops_layer` | Good code, missing operational tooling |

## Difficulty guidelines

| Difficulty | Criteria |
|-----------|----------|
| **easy** | Single module/file, obvious issues, clear intent |
| **medium** | 2-3 modules, some ambiguity, requires cross-module analysis |
| **hard** | Multiple modules, conflicting signals, red herrings, ambiguous intent |

## Worked example

Let's create a case for a logging library that silently drops messages.

**1. Create the directory:**
```bash
mkdir -p cases/diagnose/diagnose-005/repo/src
```

**2. Write the repo files:**

`repo/src/logger.py` — a logger that drops messages when buffer is full:
```python
class Logger:
    def __init__(self, max_buffer=100):
        self.buffer = []
        self.max_buffer = max_buffer

    def log(self, message):
        if len(self.buffer) >= self.max_buffer:
            pass  # BUG: silently drops messages
        self.buffer.append(message)
```

**3. Write `case.yaml`** with the metadata above.

**4. Write `hints.yaml`** with the known gap (silent message dropping).

**5. Generate `tree.txt`.**

**6. Validate:**
```bash
reposcale validate cases/diagnose/diagnose-005/
```

**7. Submit a PR** with the new case.
