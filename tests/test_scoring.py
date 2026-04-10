"""Tests for RepoScale scoring layers."""

from reposcale.scoring.coordinator import score_response, _compute_stability
from reposcale.scoring.heuristic import HeuristicScorer
from reposcale.scoring.structural import StructuralScorer


def test_structural_scorer_reports_complete_sections_and_evidence():
    case = {"expected_sections": ["Project Summary", "Gaps"]}
    response = {
        "sections": {
            "project_summary": {
                "content": "Overview [evidence: src/main.py]",
                "evidence": [{"type": "file", "ref": "src/main.py"}],
            },
            "gaps": {
                "content": "Missing tests [hypothesis]",
            },
        }
    }

    result = StructuralScorer().score(case, response)
    layer = result["layers"]["structural"]

    assert layer["format_valid"] is True
    assert layer["sections_complete"] is True
    assert layer["evidence_marked"] is True
    assert "passed" in layer["notes"].lower()


def test_heuristic_scorer_tracks_reference_density_and_prioritization():
    response = {
        "sections": {
            "gaps": {
                "content": (
                    "1. Fix `src/main.py` first. "
                    "Then review `src/tasks.py` for cleanup. "
                    "These changes are the highest impact."
                )
            }
        }
    }

    result = HeuristicScorer().score({}, response)
    layer = result["layers"]["heuristic"]

    assert layer["file_reference_density"] > 0
    assert layer["genericity_score"] == 0
    assert layer["prioritization_present"] is True


def test_score_response_merges_layers_without_judge():
    case = {
        "id": "diagnose-001",
        "track": "diagnose",
        "expected_sections": ["Project Summary"],
    }
    response = {
        "case_id": "diagnose-001",
        "model": {"name": "gpt-4o-mini"},
        "sections": {
            "project_summary": {
                "content": "Investigate `src/main.py` [evidence: src/main.py]",
                "evidence": [{"type": "file", "ref": "src/main.py"}],
            }
        },
    }

    result = score_response(case, response, skip_judge=True)

    assert result["case_id"] == "diagnose-001"
    assert result["track"] == "diagnose"
    assert "structural" in result["layers"]
    assert "heuristic" in result["layers"]
    assert result["scores"] == {}
    assert result["composite_score"] == 0.0


def test_stability_computation_with_consistent_runs():
    runs = [
        {"overall_score": 0.8, "dimension_scores": {"project_understanding": 0.9, "evidence_grounding": 0.7}},
        {"overall_score": 0.8, "dimension_scores": {"project_understanding": 0.9, "evidence_grounding": 0.7}},
        {"overall_score": 0.8, "dimension_scores": {"project_understanding": 0.9, "evidence_grounding": 0.7}},
    ]
    result = _compute_stability(runs)

    assert result["runs"] == 3
    assert result["mean"] == 0.8
    assert result["stddev"] == 0.0
    assert result["unstable_dimensions"] == []
    assert result["per_dimension"]["project_understanding"]["stddev"] == 0.0


def test_stability_flags_unstable_dimensions():
    runs = [
        {"overall_score": 0.5, "dimension_scores": {"actionability": 0.3}},
        {"overall_score": 0.9, "dimension_scores": {"actionability": 0.9}},
        {"overall_score": 0.7, "dimension_scores": {"actionability": 0.6}},
    ]
    result = _compute_stability(runs)

    assert result["runs"] == 3
    assert "actionability" in result["unstable_dimensions"]
    assert result["per_dimension"]["actionability"]["stddev"] > 0.1


def test_stability_returns_empty_for_single_run():
    result = _compute_stability([{"overall_score": 0.8, "dimension_scores": {}}])
    assert result == {}
