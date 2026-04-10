# Contributing to RepoScale

Thank you for your interest in contributing to RepoScale.

## Ways to contribute

### Case curation
The most impactful contribution right now is **curating benchmark cases** — real repositories that test specific aspects of repo continuation intelligence. See `docs/case-authoring.md` for the complete guide, `docs/dataset_format.md` for the case pack format, and `cases/CORPUS.md` for the current inventory.

### Rubric and scoring
Help define and refine evaluation criteria. See `docs/scoring.md` for the current scoring model.

### Prompts and judge protocol
Improve task prompts in `prompts/` or the LLM judge protocol in `prompts/judge.md`.

### Tooling
Improve the CLI (`src/reposcale/cli.py`), scoring layers, or build new runners and scorers.

## Development setup

```bash
# Clone the repo
git clone https://github.com/YOUR_ORG/reposcale.git
cd reposcale

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/ -v

# Validate all case packs
reposcale validate cases/diagnose/diagnose-001/ cases/intent/intent-001/
```

## Conventions

- **Commits**: use [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, etc.)
- **Schemas**: all case packs must validate against `schemas/case.schema.json`
- **Prompts**: write in English, keep them auditable and version-controlled

## Submitting a case

1. Fork the repo
2. Read `docs/case-authoring.md` for the complete guide
3. Create a new directory under `cases/<track>/` (e.g., `cases/diagnose/diagnose-005/`)
4. Include `case.yaml`, `hints.yaml`, `tree.txt`, and `repo/` with real code
5. Run `reposcale validate cases/<track>/diagnose-005/`
6. Submit a PR with a brief description of what the case tests

## Code of conduct

Be respectful, constructive, and evidence-driven — the same principles we ask of the models we evaluate.
