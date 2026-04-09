# Baseline v0 — First Results

**Date:** 2026-04-09
**Corpus:** v0 (3 cases)
**Mode:** `prompt_only`
**Scoring layers:** structural + heuristic (no LLM judge)

## Configuration

| Parameter | Value |
|-----------|-------|
| Pipeline version | 0.1.0 |
| Python | 3.10 |
| litellm | latest |
| Temperature | default (1.0) |
| Max tokens | default |

## Models tested

| Model | Provider | Run ID |
|-------|----------|--------|
| gpt-4o-mini | OpenAI | `baseline-v0-gpt4o-mini` |
| gpt-4o | OpenAI | `baseline-v0-gpt4o` |

## Results — Structural layer

| Case | Track | gpt-4o-mini | gpt-4o |
|------|-------|-------------|--------|
| diagnose-001 | diagnose | sections=**incomplete**, evidence=✓ | sections=**incomplete**, evidence=✓ |
| intent-001 | intent | sections=✓, evidence=✓ | sections=✓, evidence=✓ |
| plan-001 | plan | sections=✓, evidence=✓ | sections=✓, evidence=✓ |

**Note:** Both models miss `what_is_broken` on diagnose-001 — they merge it into adjacent sections rather than producing a standalone heading.

## Results — Heuristic layer

| Case | Track | Metric | gpt-4o-mini | gpt-4o |
|------|-------|--------|-------------|--------|
| diagnose-001 | diagnose | File ref density (/100w) | 4.25 | 6.02 |
| diagnose-001 | diagnose | Genericity | 0.000 | 0.177 |
| diagnose-001 | diagnose | Prioritization | ✓ | ✓ |
| intent-001 | intent | File ref density (/100w) | 0.18 | 0.54 |
| intent-001 | intent | Genericity | 0.000 | 0.000 |
| intent-001 | intent | Prioritization | ✗ | ✗ |
| plan-001 | plan | File ref density (/100w) | 0.69 | 1.81 |
| plan-001 | plan | Genericity | 0.000 | 0.000 |
| plan-001 | plan | Prioritization | ✓ | ✓ |

## Observations

1. **gpt-4o produces 2–3× more file references** than gpt-4o-mini across all cases. This suggests better grounding in the actual codebase.

2. **Neither model prioritizes on intent-001.** The intent track asks for reconstruction, not action items — so absence of prioritization is expected behavior, not a flaw.

3. **gpt-4o shows slight genericity on diagnose-001** (0.177) — it uses some "best practices" phrasing that gpt-4o-mini avoids. Worth monitoring at scale.

4. **Section heading compliance is imperfect.** Both models merge `what_is_broken` into other sections on diagnose. The structural scorer catches this, which validates its utility.

5. **Composite score is 0.0 for all.** This is expected — composite requires LLM judge dimension scores, which were not run in this baseline. Next step: LLM judge calibration.

## Reproduction

```bash
pip install -e .
export OPENAI_API_KEY=<your-key>

# gpt-4o-mini
reposcale run cases/diagnose/diagnose-001/ --model gpt-4o-mini --run-id baseline-v0-gpt4o-mini
reposcale run cases/intent/intent-001/ --model gpt-4o-mini --run-id baseline-v0-gpt4o-mini
reposcale run cases/plan/plan-001/ --model gpt-4o-mini --run-id baseline-v0-gpt4o-mini
reposcale score results/baseline-v0-gpt4o-mini/

# gpt-4o
reposcale run cases/diagnose/diagnose-001/ --model gpt-4o --run-id baseline-v0-gpt4o
reposcale run cases/intent/intent-001/ --model gpt-4o --run-id baseline-v0-gpt4o
reposcale run cases/plan/plan-001/ --model gpt-4o --run-id baseline-v0-gpt4o
reposcale score results/baseline-v0-gpt4o/

# View
reposcale summary results/baseline-v0-gpt4o-mini/
reposcale summary results/baseline-v0-gpt4o/
```

## Next steps

1. **LLM judge calibration** — Run `reposcale score --judge-model gpt-4o` to get dimension scores and composite.
2. **Cross-provider** — Add Anthropic (claude-sonnet) and Google (gemini) when API keys are available.
3. **Expand corpus** — Add 7–12 more cases, then re-run baselines.
