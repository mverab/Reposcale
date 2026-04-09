"""Scoring coordinator — runs all layers and merges results."""

from __future__ import annotations

import json
import logging
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


def score_response(
    case: dict,
    response: dict,
    judge_model: str | None = None,
    skip_judge: bool = False,
) -> dict:
    scorers: list[Scorer] = [
        StructuralScorer(),
        HeuristicScorer(),
    ]

    if not skip_judge and judge_model:
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
