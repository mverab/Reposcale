"""Results summary — per-case, per-track, and run-level aggregation."""

from __future__ import annotations

import json
import math
from pathlib import Path

from rich.console import Console
from rich.table import Table

from reposcale.config import RESULTS_DIR


def load_evaluation(eval_path: Path) -> dict:
    with open(eval_path) as f:
        return json.load(f)


def case_summary(evaluation: dict) -> dict:
    return {
        "case_id": evaluation.get("case_id", ""),
        "track": evaluation.get("track", ""),
        "composite_score": evaluation.get("composite_score", 0.0),
        "dimension_scores": evaluation.get("scores", {}),
        "layers_available": list(evaluation.get("layers", {}).keys()),
    }


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    avg = _mean(values)
    variance = sum((v - avg) ** 2 for v in values) / (len(values) - 1)
    return math.sqrt(variance)


def track_summary(evaluations: list[dict]) -> dict:
    if not evaluations:
        return {"track": "", "count": 0, "composite_mean": 0.0, "composite_std": 0.0}

    track = evaluations[0].get("track", "")
    composites = [e.get("composite_score", 0.0) for e in evaluations]

    all_dims: dict[str, list[float]] = {}
    for e in evaluations:
        for dim, score in e.get("scores", {}).items():
            all_dims.setdefault(dim, []).append(score)

    dimension_stats = {}
    for dim, scores in all_dims.items():
        dimension_stats[dim] = {
            "mean": round(_mean(scores), 3),
            "std": round(_std(scores), 3),
        }

    return {
        "track": track,
        "count": len(evaluations),
        "composite_mean": round(_mean(composites), 3),
        "composite_std": round(_std(composites), 3),
        "dimensions": dimension_stats,
    }


def run_summary(run_dir: Path) -> dict:
    if not run_dir.exists():
        return {"run_id": run_dir.name, "cases": 0, "tracks": {}, "overall_composite": 0.0}

    evaluations = []
    for eval_path in sorted(run_dir.rglob("evaluation.json")):
        evaluations.append(load_evaluation(eval_path))

    by_track: dict[str, list[dict]] = {}
    for e in evaluations:
        track = e.get("track", "unknown")
        by_track.setdefault(track, []).append(e)

    track_summaries = {
        track: track_summary(evals)
        for track, evals in by_track.items()
    }

    all_composites = [e.get("composite_score", 0.0) for e in evaluations]

    return {
        "run_id": run_dir.name,
        "cases": len(evaluations),
        "tracks": track_summaries,
        "overall_composite": round(_mean(all_composites), 3),
    }


def print_summary(summary_data: dict, as_json: bool = False) -> None:
    if as_json:
        print(json.dumps(summary_data, indent=2))
        return

    console = Console()

    console.print(f"\n[bold]Run:[/bold] {summary_data.get('run_id', 'N/A')}")
    console.print(f"[bold]Cases:[/bold] {summary_data.get('cases', 0)}")
    console.print(
        f"[bold]Overall composite:[/bold] {summary_data.get('overall_composite', 0.0):.3f}"
    )

    tracks = summary_data.get("tracks", {})
    if tracks:
        table = Table(title="Per-track summary")
        table.add_column("Track", style="cyan")
        table.add_column("Cases", justify="right")
        table.add_column("Composite (mean)", justify="right")
        table.add_column("Composite (std)", justify="right")

        for track_name, data in tracks.items():
            table.add_row(
                track_name,
                str(data.get("count", 0)),
                f"{data.get('composite_mean', 0.0):.3f}",
                f"{data.get('composite_std', 0.0):.3f}",
            )

        console.print(table)

        for track_name, data in tracks.items():
            dims = data.get("dimensions", {})
            if dims:
                dim_table = Table(title=f"Dimensions — {track_name}")
                dim_table.add_column("Dimension", style="cyan")
                dim_table.add_column("Mean", justify="right")
                dim_table.add_column("Std", justify="right")

                for dim_name, stats in dims.items():
                    dim_table.add_row(
                        dim_name,
                        f"{stats['mean']:.3f}",
                        f"{stats['std']:.3f}",
                    )

                console.print(dim_table)

    console.print()


def multi_run_summary(run_dirs: list[Path]) -> dict:
    summaries = []
    for rd in run_dirs:
        summaries.append(run_summary(rd))

    comparison = {
        "runs": [],
        "comparison_table": [],
    }

    for s in summaries:
        comparison["runs"].append({
            "run_id": s["run_id"],
            "cases": s["cases"],
            "overall_composite": s["overall_composite"],
        })

    all_case_ids: set[str] = set()
    run_case_scores: dict[str, dict[str, float]] = {}

    for rd, s in zip(run_dirs, summaries):
        run_id = s["run_id"]
        run_case_scores[run_id] = {}
        for eval_path in sorted(rd.rglob("evaluation.json")):
            ev = load_evaluation(eval_path)
            cid = ev.get("case_id", "")
            all_case_ids.add(cid)
            run_case_scores[run_id][cid] = ev.get("composite_score", 0.0)

    for cid in sorted(all_case_ids):
        row = {"case_id": cid}
        for s in summaries:
            rid = s["run_id"]
            score = run_case_scores.get(rid, {}).get(cid)
            row[rid] = round(score, 3) if score is not None else None
        comparison["comparison_table"].append(row)

    return comparison


def print_multi_run(comparison: dict, as_json: bool = False) -> None:
    if as_json:
        print(json.dumps(comparison, indent=2))
        return

    console = Console()

    runs_table = Table(title="Multi-Run Overview")
    runs_table.add_column("Run ID", style="cyan")
    runs_table.add_column("Cases", justify="right")
    runs_table.add_column("Composite", justify="right")

    for r in comparison["runs"]:
        runs_table.add_row(r["run_id"], str(r["cases"]), f"{r['overall_composite']:.3f}")
    console.print(runs_table)

    if comparison["comparison_table"]:
        run_ids = [r["run_id"] for r in comparison["runs"]]
        comp_table = Table(title="Per-Case Comparison")
        comp_table.add_column("Case", style="cyan")
        for rid in run_ids:
            comp_table.add_column(rid, justify="right")

        for row in comparison["comparison_table"]:
            values = []
            for rid in run_ids:
                v = row.get(rid)
                values.append(f"{v:.3f}" if v is not None else "—")
            comp_table.add_row(row["case_id"], *values)

        console.print(comp_table)

    console.print()
