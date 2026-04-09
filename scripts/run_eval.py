#!/usr/bin/env python3
"""Run a RepoScale evaluation on a case pack.

This is a minimal runner for prompt_only mode. It loads a case pack,
constructs a prompt from the case context and track prompt template,
and outputs the assembled prompt for manual or piped execution.

Future versions will support tool_augmented and agentic modes.
"""

import json
import sys
from pathlib import Path

import yaml
from rich.console import Console
from rich.panel import Panel

console = Console()

PROJECT_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"


def load_case(case_dir: Path) -> dict:
    case_file = case_dir / "case.yaml"
    if not case_file.exists():
        console.print(f"[red]Error:[/red] No case.yaml found in {case_dir}")
        sys.exit(1)

    with open(case_file) as f:
        return yaml.safe_load(f)


def load_prompt_template(track: str) -> str:
    prompt_file = PROMPTS_DIR / f"{track}.md"
    if not prompt_file.exists():
        console.print(f"[red]Error:[/red] No prompt template for track '{track}'")
        sys.exit(1)

    return prompt_file.read_text()


def build_file_tree(repo_dir: Path) -> str:
    if not repo_dir.exists():
        return "(no repo snapshot available)"

    lines = []
    for item in sorted(repo_dir.rglob("*")):
        if item.name.startswith("."):
            continue
        rel = item.relative_to(repo_dir)
        indent = "  " * (len(rel.parts) - 1)
        prefix = "├── " if item.is_file() else "└── "
        lines.append(f"{indent}{prefix}{item.name}")

    return "\n".join(lines) if lines else "(empty repo snapshot)"


def assemble_prompt(case_data: dict, case_dir: Path) -> str:
    track = case_data["track"]
    template = load_prompt_template(track)

    # Build context block
    repo_dir = case_dir / "repo"
    file_tree = build_file_tree(repo_dir)

    context = f"""## Case: {case_data['title']}

**Description**: {case_data['description']}
**Track**: {track}
**Case type**: {case_data['case_type']}
**Difficulty**: {case_data['difficulty']}

### File tree
```
{file_tree}
```
"""

    # Load additional docs if present
    docs_dir = case_dir / "docs"
    if docs_dir.exists():
        for doc_file in sorted(docs_dir.glob("*")):
            content = doc_file.read_text()
            context += f"\n### {doc_file.name}\n```\n{content}\n```\n"

    # Load history if present
    history_file = case_dir / "history.json"
    if history_file.exists():
        with open(history_file) as f:
            history = json.load(f)
        context += f"\n### Commit history (last {len(history)} commits)\n"
        for commit in history[:20]:
            context += f"- `{commit.get('hash', '?')[:7]}` {commit.get('message', '')}\n"

    return f"{template}\n\n---\n\n{context}"


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
