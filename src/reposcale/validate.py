"""Case pack validation against RepoScale schemas."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from reposcale.config import CASE_SCHEMA_PATH

REQUIRED_FILES = ["case.yaml"]
RECOMMENDED_FILES = ["hints.yaml", "repo"]

HINTS_EXPECTED_FIELDS = {
    "known_gaps": list,
    "original_intent": str,
    "key_files": list,
}


@dataclass
class ValidationResult:
    case_dir: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return len(self.errors) == 0


def load_case_schema() -> dict:
    with open(CASE_SCHEMA_PATH) as f:
        return json.load(f)


def _validate_case_yaml(case_dir: Path, result: ValidationResult) -> dict | None:
    case_file = case_dir / "case.yaml"
    if not case_file.exists():
        result.errors.append("Missing required file: case.yaml")
        return None

    try:
        with open(case_file) as f:
            case_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        result.errors.append(f"Invalid YAML in case.yaml: {e}")
        return None

    try:
        schema = load_case_schema()
    except (json.JSONDecodeError, FileNotFoundError) as e:
        result.errors.append(f"Cannot load case schema: {e}")
        return None

    validator = Draft202012Validator(schema)
    for error in validator.iter_errors(case_data):
        path = " → ".join(str(p) for p in error.absolute_path) or "(root)"
        result.errors.append(f"Schema: {path}: {error.message}")

    return case_data


def _validate_required_files(case_dir: Path, result: ValidationResult) -> None:
    for filename in REQUIRED_FILES:
        if not (case_dir / filename).exists():
            result.errors.append(f"Missing required file: {filename}")


def _validate_recommended_files(case_dir: Path, result: ValidationResult) -> None:
    for filename in RECOMMENDED_FILES:
        if not (case_dir / filename).exists():
            result.warnings.append(f"Missing recommended file/directory: {filename}")


def _validate_repo_snapshot(case_dir: Path, result: ValidationResult) -> None:
    repo_dir = case_dir / "repo"
    if not repo_dir.exists():
        return

    real_files = [
        f for f in repo_dir.rglob("*")
        if f.is_file() and f.name != ".gitkeep"
    ]
    if not real_files:
        result.errors.append("Repo snapshot is empty (no files besides .gitkeep)")


def _validate_hints(case_dir: Path, result: ValidationResult) -> None:
    hints_file = case_dir / "hints.yaml"
    if not hints_file.exists():
        return

    try:
        with open(hints_file) as f:
            hints_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        result.errors.append(f"Invalid YAML in hints.yaml: {e}")
        return

    if not isinstance(hints_data, dict):
        result.errors.append("hints.yaml must be a YAML mapping")
        return

    for field_name, expected_type in HINTS_EXPECTED_FIELDS.items():
        if field_name not in hints_data:
            result.warnings.append(f"hints.yaml missing recommended field: {field_name}")
        elif not isinstance(hints_data[field_name], expected_type):
            result.errors.append(
                f"hints.yaml field '{field_name}' should be {expected_type.__name__}, "
                f"got {type(hints_data[field_name]).__name__}"
            )


def validate_case_pack(case_dir: Path) -> ValidationResult:
    result = ValidationResult(case_dir=case_dir)

    if not case_dir.is_dir():
        result.errors.append(f"{case_dir} is not a directory")
        return result

    _validate_required_files(case_dir, result)
    _validate_case_yaml(case_dir, result)
    _validate_recommended_files(case_dir, result)
    _validate_repo_snapshot(case_dir, result)
    _validate_hints(case_dir, result)

    return result


@dataclass
class BatchResult:
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.valid)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if not r.valid)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def all_valid(self) -> bool:
        return all(r.valid for r in self.results)


def validate_batch(case_dirs: list[Path]) -> BatchResult:
    batch = BatchResult()
    for case_dir in case_dirs:
        batch.results.append(validate_case_pack(case_dir))
    return batch
