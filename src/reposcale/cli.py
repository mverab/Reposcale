"""RepoScale CLI — unified command-line interface."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

console = Console()


@click.group()
@click.version_option(package_name="reposcale")
def cli():
    """RepoScale — evaluation suite for codebase continuation intelligence."""
    pass


# --- validate ---

@cli.command()
@click.argument("case_dirs", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path))
def validate(case_dirs: tuple[Path, ...]):
    """Validate one or more case packs against the schema."""
    from reposcale.validate import validate_batch

    batch = validate_batch(list(case_dirs))

    for result in batch.results:
        name = result.case_dir.name
        if result.errors:
            console.print(Panel(
                "\n".join(f"  ✗ {e}" for e in result.errors),
                title=f"[red]FAIL[/red] — {name}",
                border_style="red",
            ))
        if result.warnings:
            console.print(Panel(
                "\n".join(f"  ⚠ {w}" for w in result.warnings),
                title=f"[yellow]WARNINGS[/yellow] — {name}",
                border_style="yellow",
            ))
        if not result.errors and not result.warnings:
            console.print(f"[green]✓[/green] {name} — valid case pack")
        elif not result.errors:
            console.print(f"[yellow]~[/yellow] {name} — valid with warnings")

    if batch.total > 1:
        console.print(f"\n{batch.passed}/{batch.total} passed, {batch.failed} failed")

    raise SystemExit(0 if batch.all_valid else 1)


# --- run ---

@cli.command(name="run")
@click.argument("case_path", type=click.Path(exists=True, path_type=Path))
@click.option("--model", required=True, help="LLM model identifier (e.g. gpt-4o, claude-3-opus)")
@click.option("--dry-run", is_flag=True, help="Print assembled prompt without calling the model")
@click.option("--run-id", default=None, help="Custom run ID. Auto-generated if omitted.")
def run_eval(case_path: Path, model: str, dry_run: bool, run_id: str | None):
    """Run evaluation on a case or track directory."""
    from reposcale.runner import run_single, run_batch, generate_run_id

    if run_id is None:
        run_id = generate_run_id(model)

    is_track_dir = case_path.is_dir() and not (case_path / "case.yaml").exists()

    if is_track_dir:
        console.print(f"[bold]Batch run:[/bold] {case_path.name} | model={model} | run_id={run_id}")
        results = run_batch(case_path, model, run_id, dry_run)
        if dry_run:
            for i, prompt in enumerate(results):
                console.print(Panel(str(prompt)[:500] + "...", title=f"Case {i+1}"))
        else:
            console.print(f"[green]✓[/green] {len(results)} cases evaluated → results/{run_id}/")
    else:
        console.print(f"[bold]Single run:[/bold] {case_path.name} | model={model} | run_id={run_id}")
        result = run_single(case_path, model, run_id, dry_run)
        if dry_run:
            print(result)
        else:
            console.print(f"[green]✓[/green] Response saved → results/{run_id}/")


# --- score ---

@cli.command()
@click.argument("run_dir", type=click.Path(exists=True, path_type=Path))
@click.option("--judge-model", default=None, help="LLM model for judge scoring. Skip judge if omitted.")
def score(run_dir: Path, judge_model: str | None):
    """Score responses in a run directory."""
    import json
    import yaml
    from reposcale.scoring.coordinator import score_response, persist_evaluation
    from reposcale.config import CASES_DIR

    response_files = sorted(run_dir.rglob("response.json"))
    if not response_files:
        console.print("[red]No response.json files found in run directory.[/red]")
        raise SystemExit(1)

    run_id = run_dir.name

    for resp_path in response_files:
        with open(resp_path) as f:
            response = json.load(f)

        case_id = response.get("case_id", "")
        track = response.get("track", "")
        console.print(f"  Scoring {case_id}...")

        case_data = _find_case(case_id, track)
        if case_data is None:
            console.print(f"  [yellow]⚠ Could not find case metadata for {case_id}, using minimal.[/yellow]")
            case_data = {"id": case_id, "track": track}

        skip_judge = judge_model is None
        evaluation = score_response(case_data, response, judge_model=judge_model, skip_judge=skip_judge)
        persist_evaluation(evaluation, run_id, case_id)
        console.print(f"  [green]✓[/green] {case_id} — composite={evaluation['composite_score']:.3f}")

    console.print(f"\n[green]✓[/green] Scored {len(response_files)} responses → results/{run_id}/")


def _find_case(case_id: str, track: str) -> dict | None:
    from reposcale.config import CASES_DIR
    import yaml

    def _load(case_dir: Path) -> dict | None:
        case_file = case_dir / "case.yaml"
        if not case_file.exists():
            return None
        with open(case_file) as f:
            data = yaml.safe_load(f)
        data["_case_dir"] = str(case_dir)
        hints_file = case_dir / "hints.yaml"
        if hints_file.exists():
            with open(hints_file) as f:
                data["hints"] = yaml.safe_load(f)
        return data

    if track:
        direct = CASES_DIR / track / case_id
        result = _load(direct)
        if result:
            return result

    for track_dir in CASES_DIR.iterdir():
        if not track_dir.is_dir():
            continue
        result = _load(track_dir / case_id)
        if result:
            return result
    return None


# --- summary ---

@cli.command()
@click.argument("run_dir", type=click.Path(exists=True, path_type=Path))
@click.option("--json", "as_json", is_flag=True, help="Output summary as JSON")
def summary(run_dir: Path, as_json: bool):
    """Show summary for a completed run."""
    from reposcale.summary import run_summary, print_summary

    data = run_summary(run_dir)
    print_summary(data, as_json=as_json)
