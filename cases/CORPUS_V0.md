# Corpus v0 — Frozen Dataset

**Frozen:** 2026-04-09
**Cases:** 3
**Tracks:** diagnose, intent, plan

## Cases

| ID | Track | Type | Difficulty | Files |
|----|-------|------|------------|-------|
| diagnose-001 | diagnose | mvp_incomplete | easy | 11 |
| intent-001 | intent | divergent_beta | medium | 12 |
| plan-001 | plan | functional_not_scalable | medium | 6 |

## Rules

- Do NOT modify case contents while baselines are running.
- Any case change invalidates prior baselines.
- New cases get new IDs (e.g., `diagnose-002`).

## Validation

All 3 cases pass `reposcale validate` with zero errors and zero warnings.
