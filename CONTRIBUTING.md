# Contributing to RepoScale

Thank you for your interest in contributing to RepoScale.

## Ways to contribute

### Case curation
The most impactful contribution right now is **curating benchmark cases** — real repositories that test specific aspects of repo continuation intelligence. See `docs/dataset_format.md` for the case pack format and `cases/example/` for a reference.

### Rubric and scoring
Help define and refine evaluation criteria. See `docs/scoring.md` for the current scoring model.

### Prompts and judge protocol
Improve task prompts in `prompts/` or the LLM judge protocol in `prompts/judge.md`.

### Tooling
Improve `scripts/validate_case_pack.py` and `scripts/run_eval.py`, or build new runners and scorers.

## Development setup

```bash
# Clone the repo
git clone https://github.com/YOUR_ORG/reposcale.git
cd reposcale

# Install in development mode
pip install -e ".[dev]"

# Validate an example case
python scripts/validate_case_pack.py cases/example/
```

## Conventions

- **Commits**: use [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, etc.)
- **Schemas**: all case packs must validate against `schemas/case.schema.json`
- **Prompts**: write in English, keep them auditable and version-controlled

## Submitting a case

1. Fork the repo
2. Create a new directory under `cases/<track>/` (e.g., `cases/diagnose/my-case/`)
3. Include all required fields from the case schema
4. Run `python scripts/validate_case_pack.py cases/<track>/my-case/`
5. Submit a PR with a brief description of what the case tests

## Code of conduct

Be respectful, constructive, and evidence-driven — the same principles we ask of the models we evaluate.
