"""Tests for eval runner and response parser."""

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
import yaml

from reposcale.runner import (
    assemble_prompt,
    generate_run_id,
    load_case,
)
from reposcale.parser import parse_response, _extract_sections, _extract_evidence


@pytest.fixture
def case_dir(tmp_path):
    case = tmp_path / "test-case"
    case.mkdir()

    repo = case / "repo"
    repo.mkdir()
    (repo / "main.py").write_text("print('hello')")
    (repo / "utils.py").write_text("def helper(): pass")

    case_data = {
        "id": "diagnose-001",
        "track": "diagnose",
        "title": "Test case",
        "description": "A test case.",
        "case_type": "mvp_incomplete",
        "difficulty": "easy",
        "tags": ["python"],
        "repo_source": "snapshot",
        "supported_modes": ["prompt_only"],
        "expected_sections": ["project_summary"],
        "version": "1.0",
    }
    with open(case / "case.yaml", "w") as f:
        yaml.dump(case_data, f)

    return case


class TestPromptAssembly:
    def test_prompt_includes_case_metadata(self, case_dir):
        case_data = load_case(case_dir)
        prompt = assemble_prompt(case_data, case_dir)
        assert "Test case" in prompt
        assert "diagnose" in prompt
        assert "mvp_incomplete" in prompt

    def test_prompt_includes_file_tree(self, case_dir):
        case_data = load_case(case_dir)
        prompt = assemble_prompt(case_data, case_dir)
        assert "main.py" in prompt

    def test_prompt_includes_file_contents(self, case_dir):
        case_data = load_case(case_dir)
        prompt = assemble_prompt(case_data, case_dir)
        assert "print('hello')" in prompt

    def test_prompt_ignores_generated_python_artifacts(self, case_dir):
        pycache_dir = case_dir / "repo" / "__pycache__"
        pycache_dir.mkdir()
        (pycache_dir / "main.cpython-310.pyc").write_bytes(b"compiled")

        case_data = load_case(case_dir)
        prompt = assemble_prompt(case_data, case_dir)

        assert "__pycache__" not in prompt
        assert "main.cpython-310.pyc" not in prompt

    def test_prompt_includes_history_when_present(self, case_dir):
        history = [
            {"hash": "abc1234", "message": "initial commit"}
        ]
        with open(case_dir / "history.json", "w") as f:
            json.dump(history, f)

        case_data = load_case(case_dir)
        prompt = assemble_prompt(case_data, case_dir)
        assert "abc1234" in prompt


class TestRunIdGeneration:
    def test_run_id_contains_model_name(self):
        run_id = generate_run_id("gpt-4o")
        assert "gpt4o" in run_id

    def test_run_id_contains_timestamp(self):
        run_id = generate_run_id("test-model")
        assert len(run_id) > 15


class TestSectionExtraction:
    def test_extracts_headings(self):
        text = "# 1. Summary\nSome content.\n## 2. Gaps\nMore content."
        sections = _extract_sections(text)
        assert "summary" in sections
        assert "gaps" in sections

    def test_raw_output_when_no_headings(self):
        text = "Just plain text without any headings."
        sections = _extract_sections(text)
        assert "raw_output" in sections


class TestEvidenceExtraction:
    def test_detects_evidence_tags(self):
        text = "The auth module [evidence: src/auth.py] is unused."
        evidence = _extract_evidence(text)
        assert any(e["ref"] == "src/auth.py" for e in evidence)

    def test_detects_file_references(self):
        text = "The file `config.py` contains the settings."
        evidence = _extract_evidence(text)
        assert any(e["ref"] == "config.py" for e in evidence)

    def test_detects_commit_references(self):
        text = "As seen in [evidence: a3f8c21] the pivot happened."
        evidence = _extract_evidence(text)
        assert any(e["type"] == "commit" for e in evidence)


class TestParseResponse:
    def test_produces_valid_structure(self):
        raw = "# 1. Project Summary\nThis is a CLI tool.\n# 2. Gaps\nMissing tests."
        case_data = {"id": "diagnose-001", "track": "diagnose"}
        result = parse_response(raw, case_data, model="gpt-4o")

        assert result["case_id"] == "diagnose-001"
        assert result["track"] == "diagnose"
        assert result["mode"] == "prompt_only"
        assert result["model"]["name"] == "gpt-4o"
        assert "project_summary" in result["sections"]
        assert "timestamp" in result
