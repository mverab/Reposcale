"""Project-wide paths and configuration."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

SCHEMAS_DIR = PROJECT_ROOT / "schemas"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
CASES_DIR = PROJECT_ROOT / "cases"
RESULTS_DIR = PROJECT_ROOT / "results"

CASE_SCHEMA_PATH = SCHEMAS_DIR / "case.schema.json"
RESPONSE_SCHEMA_PATH = SCHEMAS_DIR / "response.schema.json"
EVALUATION_SCHEMA_PATH = SCHEMAS_DIR / "evaluation.schema.json"
