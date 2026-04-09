#!/usr/bin/env python3
"""Run a RepoScale evaluation on a case pack.

Thin wrapper — core logic lives in src/reposcale/runner.py.
"""

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

# Allow running from scripts/ without install
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from reposcale.runner import assemble_prompt, load_case  # noqa: E402

console = Console()


def main():
    if len(sys.argv) < 2:
        console.print("Usage: python run_eval.py <case_dir> [--output <file>]")
        console.print()
        console.print("Assembles the evaluation prompt for a case pack.")
        console.print("Pipe the output to your model of choice.")
        sys.exit(1)

    case_dir = Path(sys.argv[1])
    output_file = None

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_file = Path(sys.argv[idx + 1])

    case_data = load_case(case_dir)
    prompt = assemble_prompt(case_data, case_dir)

    if output_file:
        output_file.write_text(prompt)
        console.print(f"[green]✓[/green] Prompt written to {output_file}")
    else:
        console.print(Panel(
            f"Track: [bold]{case_data['track']}[/bold] | "
            f"Case: [bold]{case_data['id']}[/bold] | "
            f"Mode: prompt_only",
            title="RepoScale Eval",
            border_style="blue",
        ))
        print(prompt)


if __name__ == "__main__":
    main()
