# RepoScale Corpus v1 — 12 Cases

## Inventory

| ID | Track | Type | Difficulty | Description |
|----|-------|------|-----------|-------------|
| diagnose-001 | diagnose | mvp_incomplete | easy | Incomplete task CLI with unwired auth middleware |
| diagnose-002 | diagnose | mvp_incomplete | medium | E-commerce cart with missing integration tests |
| diagnose-003 | diagnose | single_file_buggy | easy | CSV processor with off-by-one and encoding bugs |
| diagnose-004 | diagnose | multi_module_tangled | hard | Job system with conflicting error handling patterns |
| intent-001 | intent | divergent_beta | medium | Analytics dashboard pivoted from real-time to batch |
| intent-002 | intent | divergent_beta | medium | REST API pivoting from session-based to JWT auth |
| intent-003 | intent | abandoned_rewrite | hard | CMS with abandoned v1→v2 plugin rewrite |
| intent-004 | intent | readme_code_divergence | easy | Weather CLI where README overpromises features |
| plan-001 | plan | functional_not_scalable | medium | URL shortener that works but won't scale |
| plan-002 | plan | functional_not_scalable | medium | Monolith needing service extraction for scaling |
| plan-003 | plan | multi_language_unscalable | hard | Multi-language platform with manual deploy, no DevOps |
| plan-004 | plan | needs_ops_layer | easy | Clean Flask app needing CI/CD and monitoring |

## Coverage

| Track | Easy | Medium | Hard | Total |
|-------|------|--------|------|-------|
| diagnose | 2 | 1 | 1 | 4 |
| intent | 1 | 2 | 1 | 4 |
| plan | 1 | 2 | 1 | 4 |
| **Total** | **4** | **5** | **3** | **12** |

## Case types (8 unique)

- `mvp_incomplete` — Project with missing features or unwired components
- `single_file_buggy` — Single-file script with obvious bugs
- `multi_module_tangled` — Multi-module project with inconsistent patterns
- `divergent_beta` — Project that pivoted direction mid-development
- `abandoned_rewrite` — Codebase with abandoned rewrite attempt
- `readme_code_divergence` — README describes features that don't exist
- `functional_not_scalable` — Works but has fundamental scaling limitations
- `multi_language_unscalable` — Multi-language project lacking operational infrastructure
- `needs_ops_layer` — Good code quality but missing operational tooling

## Validation

All 12 cases pass `reposcale validate` with zero errors.
