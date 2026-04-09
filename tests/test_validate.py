"""Tests for case pack validation and schema conformance."""

import json

import pytest
import yaml
from jsonschema import Draft202012Validator

from reposcale.config import RESPONSE_SCHEMA_PATH, EVALUATION_SCHEMA_PATH
from reposcale.validate import validate_case_pack, validate_batch
from reposcale.parser import parse_response
from reposcale.scoring.coordinator import score_response


@pytest.fixture
def valid_case_dir(tmp_path):
    case_dir = tmp_path / "test-case"
    case_dir.mkdir()

    repo_dir = case_dir / "repo"
    repo_dir.mkdir()
    (repo_dir / "main.py").write_text("print('hello')")

    case_data = {
        "id": "diagnose-001",
        "track": "diagnose",
        "title": "Test case for validation",
        "description": "A test case used to validate the validation pipeline itself.",
        "case_type": "mvp_incomplete",
        "difficulty": "easy",
        "tags": ["python", "test"],
        "repo_source": "snapshot",
        "supported_modes": ["prompt_only"],
        "expected_sections": ["project_summary"],
        "created_at": "2025-01-15",
        "version": "1.0",
    }
    with open(case_dir / "case.yaml", "w") as f:
        yaml.dump(case_data, f)

    hints_data = {
        "known_gaps": ["Missing tests", "No CI config"],
        "original_intent": "A simple CLI tool",
        "key_files": ["main.py", "README.md"],
    }
    with open(case_dir / "hints.yaml", "w") as f:
        yaml.dump(hints_data, f)

    return case_dir


@pytest.fixture
def minimal_case_dir(tmp_path):
    case_dir = tmp_path / "minimal-case"
    case_dir.mkdir()

    case_data = {
        "id": "diagnose-002",
        "track": "diagnose",
        "title": "Minimal valid case",
        "description": "A minimal case with only required fields.",
        "case_type": "mvp_incomplete",
        "difficulty": "easy",
        "repo_source": "snapshot",
        "supported_modes": ["prompt_only"],
        "expected_sections": ["project_summary"],
        "version": "1.0",
    }
    with open(case_dir / "case.yaml", "w") as f:
        yaml.dump(case_data, f)

    return case_dir


class TestValidCasePack:
    def test_valid_case_passes(self, valid_case_dir):
        result = validate_case_pack(valid_case_dir)
        assert result.valid
        assert len(result.errors) == 0

    def test_valid_case_no_warnings_when_complete(self, valid_case_dir):
        result = validate_case_pack(valid_case_dir)
        assert len(result.warnings) == 0


class TestMissingFields:
    def test_missing_case_yaml(self, tmp_path):
        case_dir = tmp_path / "no-case"
        case_dir.mkdir()
        result = validate_case_pack(case_dir)
        assert not result.valid
        assert any("case.yaml" in e for e in result.errors)

    def test_missing_required_schema_field(self, tmp_path):
        case_dir = tmp_path / "bad-schema"
        case_dir.mkdir()
        case_data = {
            "id": "diagnose-003",
            "track": "diagnose",
            "title": "Missing description field",
        }
        with open(case_dir / "case.yaml", "w") as f:
            yaml.dump(case_data, f)

        result = validate_case_pack(case_dir)
        assert not result.valid
        assert any("description" in e for e in result.errors)

    def test_not_a_directory(self, tmp_path):
        file_path = tmp_path / "not-a-dir.txt"
        file_path.write_text("oops")
        result = validate_case_pack(file_path)
        assert not result.valid


class TestEmptyRepo:
    def test_empty_repo_with_only_gitkeep(self, tmp_path):
        case_dir = tmp_path / "empty-repo"
        case_dir.mkdir()

        repo_dir = case_dir / "repo"
        repo_dir.mkdir()
        (repo_dir / ".gitkeep").write_text("")

        case_data = {
            "id": "diagnose-004",
            "track": "diagnose",
            "title": "Empty repo test case",
            "description": "A case with an empty repo snapshot.",
            "case_type": "mvp_incomplete",
            "difficulty": "easy",
            "repo_source": "snapshot",
            "supported_modes": ["prompt_only"],
            "expected_sections": ["project_summary"],
            "version": "1.0",
        }
        with open(case_dir / "case.yaml", "w") as f:
            yaml.dump(case_data, f)

        result = validate_case_pack(case_dir)
        assert any("empty" in e.lower() for e in result.errors)


class TestHintsValidation:
    def test_malformed_hints_yaml(self, tmp_path):
        case_dir = tmp_path / "bad-hints"
        case_dir.mkdir()

        case_data = {
            "id": "diagnose-005",
            "track": "diagnose",
            "title": "Bad hints test case",
            "description": "A case with malformed hints.",
            "case_type": "mvp_incomplete",
            "difficulty": "easy",
            "repo_source": "snapshot",
            "supported_modes": ["prompt_only"],
            "expected_sections": ["project_summary"],
            "version": "1.0",
        }
        with open(case_dir / "case.yaml", "w") as f:
            yaml.dump(case_data, f)

        (case_dir / "hints.yaml").write_text("known_gaps: not-a-list\n")

        result = validate_case_pack(case_dir)
        assert any("known_gaps" in e for e in result.errors)

    def test_missing_hints_fields_are_warnings(self, valid_case_dir):
        with open(valid_case_dir / "hints.yaml", "w") as f:
            yaml.dump({"known_gaps": ["one"]}, f)

        result = validate_case_pack(valid_case_dir)
        assert result.valid
        assert any("original_intent" in w for w in result.warnings)

    def test_missing_recommended_files_are_warnings(self, minimal_case_dir):
        result = validate_case_pack(minimal_case_dir)
        assert result.valid
        assert any("hints.yaml" in w for w in result.warnings)
        assert any("repo" in w for w in result.warnings)


class TestBatchValidation:
    def test_batch_with_mixed_results(self, valid_case_dir, tmp_path):
        bad_dir = tmp_path / "bad-case"
        bad_dir.mkdir()

        batch = validate_batch([valid_case_dir, bad_dir])
        assert batch.total == 2
        assert batch.passed == 1
        assert batch.failed == 1
        assert not batch.all_valid

    def test_batch_all_valid(self, valid_case_dir):
        batch = validate_batch([valid_case_dir])
        assert batch.all_valid
        assert batch.passed == 1


class TestSchemaConformance:
    def test_parser_output_conforms_to_response_schema(self):
        raw = "# 1. Project Summary\nA CLI tool using `main.py` [evidence: main.py]."
        case_data = {"id": "diagnose-001", "track": "diagnose"}
        response = parse_response(raw, case_data, model="gpt-4o")

        with open(RESPONSE_SCHEMA_PATH) as f:
            schema = json.load(f)

        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(response))
        assert errors == [], f"Response schema errors: {[e.message for e in errors]}"

    def test_evaluation_output_conforms_to_evaluation_schema(self):
        case_data = {
            "id": "diagnose-001",
            "track": "diagnose",
            "expected_sections": ["project_summary"],
        }
        response = {
            "case_id": "diagnose-001",
            "track": "diagnose",
            "mode": "prompt_only",
            "model": {"name": "test"},
            "sections": {
                "project_summary": {
                    "content": "A test project with `main.py`.",
                    "evidence": [{"type": "file", "ref": "main.py"}],
                }
            },
            "timestamp": "2025-01-15T10:00:00+00:00",
        }

        evaluation = score_response(case_data, response, skip_judge=True)

        with open(EVALUATION_SCHEMA_PATH) as f:
            schema = json.load(f)

        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(evaluation))
        assert errors == [], f"Evaluation schema errors: {[e.message for e in errors]}"
