# RepoScale Launch Kit

This document packages the public-facing assets needed to launch RepoScale as an honest, visual alpha release.

## Positioning

**Primary framing**

RepoScale is an alpha benchmark for repo continuation intelligence.

**Supporting framing**

It helps builders evaluate how well models read existing codebases, infer intent, detect gaps, and propose coherent next steps.

**Claims that are safe to make**

- 12 curated cases across Diagnose, Intent, and Plan
- Reproducible CLI pipeline
- Judge stability support via repeated scoring
- Public alpha, not benchmark-grade final methodology

**Claims to avoid**

- "definitive benchmark"
- "neutral leaderboard"
- "production-ready methodology"
- "real OSS snapshot benchmark" unless the corpus provenance changes

## Suggested Repository Topics

Add these topics in the GitHub repository settings:

- `llm-evals`
- `benchmark`
- `llm-benchmark`
- `ai-agents`
- `agent-evals`
- `developer-tools`
- `python`
- `open-source`
- `evaluation`
- `ai-engineering`

## Social Preview

Recommended repo social preview asset:

- `docs/assets/social-preview.jpg`

Suggested setup:
1. Open repository settings.
2. Go to General -> Social preview.
3. Upload `docs/assets/social-preview.jpg`.
4. Keep `docs/assets/repo-visual-source.png` as the editable source image for future iterations.

Recommended alt text:

`RepoScale — alpha benchmark for repo continuation intelligence with 12 curated cases and a reproducible CLI pipeline`

## GitHub Release

### Suggested release title

`v0.1.0-alpha — public alpha for repo continuation evaluation`

### Suggested release body

```md
RepoScale is now public as an alpha benchmark for repo continuation intelligence.

This release packages a runnable evaluation pipeline for measuring how well models understand and continue existing software projects instead of isolated coding tasks.

### What ships in this alpha

- 12 curated cases across Diagnose, Intent, and Plan
- CLI workflow: validate, batch, score, summary, compare
- Structural, heuristic, and LLM-judge scoring
- Judge stability support with repeated scoring
- Corpus manifest, case authoring guide, and baseline scripts
- GitHub Actions CI

### Good use cases right now

- Evaluate models on repo understanding and continuation-style tasks
- Run small reproducible baselines across providers
- Contribute new cases and scoring improvements

### Important alpha caveats

- Methodology is still evolving
- Judge neutrality is not yet benchmark-grade final
- Corpus size is useful but still small

Start here:

- README: https://github.com/mverab/Reposcale
- Corpus: https://github.com/mverab/Reposcale/blob/main/cases/CORPUS.md
- Case authoring guide: https://github.com/mverab/Reposcale/blob/main/docs/case-authoring.md
```

## X Post

```text
RepoScale is now public.

It’s an alpha benchmark for repo continuation intelligence:
how well models read existing codebases, infer intent, detect gaps, and propose coherent next steps.

Current alpha:
• 12 curated cases
• Diagnose / Intent / Plan tracks
• reproducible CLI pipeline
• judge stability scoring

GitHub: https://github.com/mverab/Reposcale
```

## LinkedIn Post

```text
I just made RepoScale public.

RepoScale is an alpha benchmark for repo continuation intelligence: evaluating how well models work with existing software projects instead of isolated greenfield prompts.

The current alpha includes:
- 12 curated cases across Diagnose, Intent, and Plan
- a reproducible CLI pipeline for validate -> batch -> score -> compare
- structural, heuristic, and LLM-judge scoring
- judge stability support for repeated evaluations

It is intentionally labeled alpha: useful today, but still evolving in corpus size and methodology.

Project:
https://github.com/mverab/Reposcale
```

## Public Launch Checklist

- README headline and quickstart are clear in under 20 seconds
- Social preview image is configured in GitHub settings
- Repository topics are added
- GitHub Release is published
- `v0.1.0-alpha` or newer tag matches the public messaging
- README links to corpus, baseline, authoring guide, and changelog
- One public post on X and one on LinkedIn are ready
- Repo is pinned on the GitHub profile

## Optional Follow-up Assets

- Short terminal GIF running `reposcale batch` and `reposcale compare`
- Screenshot of the comparison table for release notes
- One issue labeled `good first issue` for contributor conversion
