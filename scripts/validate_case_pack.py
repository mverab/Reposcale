#!/usr/bin/env python3
"""Validate a RepoScale case pack against the case schema."""

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, ValidationError
from rich.console import Console
from rich.panel import Panel

console = Console()

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "case.schema.json"

REQUIRED_FILES = ["case.yaml"]
RECOMMENDED_FILES = ["hints.yaml", "repo"]


def load_schema() -> dict:
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def validate_case_pack(case_dir: Path) -> bool:
    errors = []
    warnings = []

    if not case_dir.is_dir():
        console.print(f"[red]Error:[/red] {case_dir} is not a directory")
        return False

    # Check required files
    for filename in REQUIRED_FILES:
        if not (case_dir / filename).exists():
            errors.append(f"Missing required file: {filename}")

    # Check recommended files
    for filename in RECOMMENDED_FILES:
        if not (case_dir / filename).exists():
            warnings.append(f"Missing recommended file/directory: {filename}")

    # Validate case.yaml against schema
    case_file = case_dir / "case.yaml"
    if case_file.exists():
        try:
            with open(case_file) as f:
                case_data = yaml.safe_load(f)

            schema = load_schema()
            validator = Draft202012Validator(schema)

            for error in validator.iter_errors(case_data):
                path = " → ".join(str(p) for p in error.absolute_path) or "(root)"
                errors.append(f"Schema validation: {path}: {error.message}")

        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML in case.yaml: {e}")
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in schema: {e}")

    # Print results
    case_name = case_dir.name
    if errors:
        console.print(Panel(
            "\n".join(f"  ✗ {e}" for e in errors),
            title=f"[red]FAIL[/red] — {case_name}",
            border_style="red",
        ))
    if warnings:
        console.print(Panel(
            "\n".join(f"  ⚠ {w}" for w in warnings),
            title=f"[yellow]WARNINGS[/yellow] — {case_name}",
            border_style="yellow",
        ))
    if not errors and not warnings:
        console.print(f"[green]✓[/green] {case_name} — valid case pack")
    elif not errors:
        console.print(f"[yellow]~[/yellow] {case_name} — valid with warnings")

    return len(errors) == 0


def main():
    if len(sys.argv) < 2:
        console.print("Usage: python validate_case_pack.py <case_dir> [case_dir...]")
        sys.exit(1)

    all_valid = True
    for path_str in sys.argv[1:]:
        case_dir = Path(path_str)
        if not validate_case_pack(case_dir):
            all_valid = False

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
