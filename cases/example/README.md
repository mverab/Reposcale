# Example case pack

This is a reference case pack for RepoScale contributors. It demonstrates the expected structure and format.

**Note**: The `repo/` directory would normally contain a snapshot of the repository being evaluated. For this example, it is left empty — real case packs must include the full repo snapshot.

## Structure

```text
cases/example/
  case.yaml       # case metadata (required)
  hints.yaml      # evaluation hints, not shown to model (optional)
  README.md       # this file (optional)
  repo/           # repo snapshot (required for real cases)
```

## How to validate

```bash
python scripts/validate_case_pack.py cases/example/
```
