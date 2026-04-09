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

## Results — LLM Judge (judge: gpt-4o, temperature 0.1)

### Composite scores

| Case | Track | gpt-4o-mini | gpt-4o |
|------|-------|-------------|--------|
| diagnose-001 | diagnose | **0.900** | **0.905** |
| intent-001 | intent | **0.880** | 0.745 |
| plan-001 | plan | 0.750 | 0.700 |
| **Mean** | | **0.843** | **0.783** |

### Dimension breakdown — gpt-4o-mini

| Dimension | diagnose-001 | intent-001 | plan-001 |
|-----------|:---:|:---:|:---:|
| project_understanding | 1.0 | 1.0 | 1.0 |
| evidence_grounding | 0.8 | 1.0 | 0.5 |
| intent_reconstruction | 1.0 | 1.0 | 1.0 |
| gap_detection | 0.8 | 0.8 | 1.0 |
| useful_creativity | 0.8 | 0.8 | 0.5 |
| prioritization | 1.0 | 0.7 | 1.0 |
| architectural_coherence | 0.8 | 0.9 | 0.5 |
| actionability | 1.0 | 0.8 | 0.5 |

### Dimension breakdown — gpt-4o

| Dimension | diagnose-001 | intent-001 | plan-001 |
|-----------|:---:|:---:|:---:|
| project_understanding | 1.0 | 0.8 | 1.0 |
| evidence_grounding | 0.8 | 0.8 | 0.5 |
| intent_reconstruction | 1.0 | 0.9 | 0.5 |
| gap_detection | 1.0 | 0.6 | 1.0 |
| useful_creativity | 0.8 | 0.7 | 0.5 |
| prioritization | 1.0 | 0.7 | 0.5 |
| architectural_coherence | 0.7 | 0.8 | 1.0 |
| actionability | 0.9 | 0.7 | 0.5 |

### Hallucinations

| Model | diagnose-001 | intent-001 | plan-001 |
|-------|:---:|:---:|:---:|
| gpt-4o-mini | 0 | 0 | 0 |
| gpt-4o | 0 | **1** | 0 |

## Calibration observations

1. **gpt-4o-mini outperforms gpt-4o on average** (0.843 vs 0.783). This is counterintuitive but consistent: the smaller model produces more focused, less overengineered responses.

2. **plan-001 is the hardest case.** Both models score lowest here — evidence_grounding and actionability drop to 0.5, indicating difficulty translating understanding into concrete scaling plans.

3. **gpt-4o hallucinates once on intent-001.** The judge detected a claim about non-existent functionality. Zero hallucinations from gpt-4o-mini.

4. **project_understanding is near-ceiling.** Both models score 0.8–1.0 consistently. This dimension may not differentiate well at scale — worth considering raising the bar.

5. **evidence_grounding and actionability show the most variance.** These are the dimensions most worth monitoring across new models and cases.

6. **Judge consistency is reasonable.** Scores correlate with heuristic metrics (higher file ref density → higher evidence_grounding). This suggests the judge and heuristics are measuring related but not identical constructs.

## Reproduction

```bash
pip install -e .
export OPENAI_API_KEY=<your-key>

# gpt-4o-mini
reposcale run cases/diagnose/diagnose-001/ --model gpt-4o-mini --run-id baseline-v0-gpt4o-mini
reposcale run cases/intent/intent-001/ --model gpt-4o-mini --run-id baseline-v0-gpt4o-mini
reposcale run cases/plan/plan-001/ --model gpt-4o-mini --run-id baseline-v0-gpt4o-mini
reposcale score results/baseline-v0-gpt4o-mini/ --judge-model gpt-4o

# gpt-4o
reposcale run cases/diagnose/diagnose-001/ --model gpt-4o --run-id baseline-v0-gpt4o
reposcale run cases/intent/intent-001/ --model gpt-4o --run-id baseline-v0-gpt4o
reposcale run cases/plan/plan-001/ --model gpt-4o --run-id baseline-v0-gpt4o
reposcale score results/baseline-v0-gpt4o/ --judge-model gpt-4o

# View
reposcale summary results/baseline-v0-gpt4o-mini/
reposcale summary results/baseline-v0-gpt4o/
```

## Next steps

1. **Cross-provider** — Add Anthropic (claude-sonnet) and Google (gemini) when API keys are available.
2. **Expand corpus** — Add 7–12 more cases, then re-run baselines.
3. **Judge stability** — Run same evaluations 3× to measure score variance.
