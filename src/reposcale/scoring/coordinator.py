"""Scoring coordinator — runs all layers and merges results."""

from __future__ import annotations

import json
import logging
import statistics
from datetime import datetime, timezone
from pathlib import Path

from reposcale.config import RESULTS_DIR, EVALUATION_SCHEMA_PATH
from reposcale.scoring import Scorer
from reposcale.scoring.structural import StructuralScorer
from reposcale.scoring.heuristic import HeuristicScorer
from reposcale.scoring.llm_judge import LLMJudgeScorer

logger = logging.getLogger(__name__)

DEFAULT_WEIGHTS = {
    "project_understanding": 0.15,
    "evidence_grounding": 0.15,
    "intent_reconstruction": 0.10,
    "gap_detection": 0.15,
    "useful_creativity": 0.10,
    "prioritization": 0.10,
    "architectural_coherence": 0.10,
    "actionability": 0.15,
}


def _deep_merge(base: dict, overlay: dict) -> dict:
    result = base.copy()
    for key, value in overlay.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _compute_composite(evaluation: dict) -> float:
    judge_data = evaluation.get("layers", {}).get("llm_judge", {})
    dimension_scores = judge_data.get("dimension_scores", {})

    if not dimension_scores:
        return 0.0

    total_weight = 0.0
    weighted_sum = 0.0
    for dim, weight in DEFAULT_WEIGHTS.items():
        if dim in dimension_scores:
            weighted_sum += dimension_scores[dim] * weight
            total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(weighted_sum / total_weight, 3)


def _compute_stability(runs: list[dict]) -> dict:
    if len(runs) < 2:
        return {}

    composites = [r.get("overall_score", 0.0) for r in runs]
    all_dims: dict[str, list[float]] = {}
    for r in runs:
        for dim, val in r.get("dimension_scores", {}).items():
            all_dims.setdefault(dim, []).append(val)

    per_dim = {}
    unstable = []
    for dim, vals in all_dims.items():
        m = statistics.mean(vals)
        s = statistics.stdev(vals) if len(vals) > 1 else 0.0
        per_dim[dim] = {"mean": round(m, 3), "stddev": round(s, 3)}
        if s > 0.1:
            unstable.append(dim)

    return {
        "runs": len(runs),
        "mean": round(statistics.mean(composites), 3),
        "stddev": round(statistics.stdev(composites) if len(composites) > 1 else 0.0, 3),
        "per_dimension": per_dim,
        "unstable_dimensions": unstable,
    }


def score_response(
    case: dict,
    response: dict,
    judge_model: str | None = None,
    skip_judge: bool = False,
    repeat: int = 1,
) -> dict:
    scorers: list[Scorer] = [
        StructuralScorer(),
        HeuristicScorer(),
    ]

    use_judge = not skip_judge and judge_model
    if use_judge:
        scorers.append(LLMJudgeScorer(judge_model=judge_model))

    evaluation = {
        "case_id": case.get("id", ""),
        "response_id": f"{response.get('case_id', '')}-{response.get('model', {}).get('name', '')}",
        "track": case.get("track", ""),
        "scores": {},
        "layers": {},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    for scorer in scorers:
        try:
            partial = scorer.score(case, response)
            evaluation = _deep_merge(evaluation, partial)
        except Exception as e:
            logger.error(f"Scorer '{scorer.name}' failed: {e}")
            evaluation["layers"][scorer.name] = {"notes": f"Scorer failed: {e}"}

    if use_judge and repeat > 1:
        judge = LLMJudgeScorer(judge_model=judge_model)
        judge_runs = [evaluation.get("layers", {}).get("llm_judge", {})]
        for _ in range(repeat - 1):
            try:
                extra = judge.score(case, response)
                judge_runs.append(extra.get("layers", {}).get("llm_judge", {}))
            except Exception as e:
                logger.warning(f"Judge repeat run failed: {e}")

        stability = _compute_stability(judge_runs)
        if stability:
            evaluation["layers"]["llm_judge"]["stability"] = stability
            if stability.get("per_dimension"):
                evaluation["layers"]["llm_judge"]["dimension_scores"] = {
                    dim: vals["mean"]
                    for dim, vals in stability["per_dimension"].items()
                }

    judge_scores = evaluation.get("layers", {}).get("llm_judge", {}).get("dimension_scores", {})
    if judge_scores:
        evaluation["scores"] = judge_scores

    evaluation["composite_score"] = _compute_composite(evaluation)

    return evaluation


def persist_evaluation(evaluation: dict, run_id: str, case_id: str) -> Path:
    out_dir = RESULTS_DIR / run_id / case_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "evaluation.json"
    with open(out_path, "w") as f:
        json.dump(evaluation, f, indent=2)
    return out_path
