#!/usr/bin/env python3
"""Validate a RepoScale case pack against the case schema.

Thin wrapper — core logic lives in src/reposcale/validate.py.
"""

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

# Allow running from scripts/ without install
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from reposcale.validate import validate_batch  # noqa: E402

console = Console()


def _print_result(result):
    case_name = result.case_dir.name
    if result.errors:
        console.print(Panel(
            "\n".join(f"  ✗ {e}" for e in result.errors),
            title=f"[red]FAIL[/red] — {case_name}",
            border_style="red",
        ))
    if result.warnings:
        console.print(Panel(
            "\n".join(f"  ⚠ {w}" for w in result.warnings),
            title=f"[yellow]WARNINGS[/yellow] — {case_name}",
            border_style="yellow",
        ))
    if not result.errors and not result.warnings:
        console.print(f"[green]✓[/green] {case_name} — valid case pack")
    elif not result.errors:
        console.print(f"[yellow]~[/yellow] {case_name} — valid with warnings")


def main():
    if len(sys.argv) < 2:
        console.print("Usage: python validate_case_pack.py <case_dir> [case_dir...]")
        sys.exit(1)

    case_dirs = [Path(p) for p in sys.argv[1:]]
    batch = validate_batch(case_dirs)

    for result in batch.results:
        _print_result(result)

    if batch.total > 1:
        console.print(f"\n{batch.passed}/{batch.total} passed, {batch.failed} failed")

    sys.exit(0 if batch.all_valid else 1)


if __name__ == "__main__":
    main()
