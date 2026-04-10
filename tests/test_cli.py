"""Tests for the RepoScale CLI entrypoint."""

from pathlib import Path

import yaml
from click.testing import CliRunner

from reposcale.cli import cli


def test_cli_help_lists_available_commands():
    runner = CliRunner()

    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "validate" in result.output
    assert "run" in result.output
    assert "batch" in result.output


def test_validate_command_reports_success(tmp_path: Path):
    case_dir = tmp_path / "diagnose-001"
    case_dir.mkdir()

    repo_dir = case_dir / "repo"
    repo_dir.mkdir()
    (repo_dir / "main.py").write_text("print('hello')")

    with open(case_dir / "case.yaml", "w") as fh:
        yaml.safe_dump(
            {
                "id": "diagnose-001",
                "track": "diagnose",
                "title": "CLI validation case",
                "description": "Validates the CLI wrapper.",
                "case_type": "mvp_incomplete",
                "difficulty": "easy",
                "repo_source": "snapshot",
                "supported_modes": ["prompt_only"],
                "expected_sections": ["project_summary"],
                "version": "1.0",
            },
            fh,
        )

    with open(case_dir / "hints.yaml", "w") as fh:
        yaml.safe_dump(
            {
                "known_gaps": ["Missing observability"],
                "original_intent": "Simple CLI utility",
                "key_files": ["main.py"],
            },
            fh,
        )

    runner = CliRunner()
    result = runner.invoke(cli, ["validate", str(case_dir)])

    assert result.exit_code == 0
    assert "valid case pack" in result.output


def _make_case(parent: Path, case_id: str, track: str) -> Path:
    case_dir = parent / track / case_id
    case_dir.mkdir(parents=True)
    repo_dir = case_dir / "repo"
    repo_dir.mkdir()
    (repo_dir / "main.py").write_text("print('hello')")
    with open(case_dir / "case.yaml", "w") as fh:
        yaml.safe_dump(
            {
                "id": case_id,
                "track": track,
                "title": f"Test case for {case_id} evaluation",
                "description": "A synthetic test case for batch CLI testing.",
                "case_type": "mvp_incomplete",
                "difficulty": "easy",
                "repo_source": "snapshot",
                "supported_modes": ["prompt_only"],
                "expected_sections": ["project_summary"],
                "version": "1.0",
            },
            fh,
        )
    with open(case_dir / "hints.yaml", "w") as fh:
        yaml.safe_dump(
            {
                "known_gaps": ["Gap"],
                "original_intent": "Intent",
                "key_files": ["main.py"],
            },
            fh,
        )
    return case_dir


def test_batch_command_discovers_and_runs_cases(tmp_path: Path):
    _make_case(tmp_path, "test-001", "diagnose")
    _make_case(tmp_path, "test-002", "diagnose")

    runner = CliRunner()
    result = runner.invoke(cli, ["batch", str(tmp_path), "--model", "gpt-4o", "--dry-run"])

    assert result.exit_code == 0
    assert "2 cases" in result.output
    assert "2 completed" in result.output


def test_batch_command_skips_invalid_cases(tmp_path: Path):
    _make_case(tmp_path, "good-001", "diagnose")
    bad_dir = tmp_path / "diagnose" / "bad-001"
    bad_dir.mkdir(parents=True)
    (bad_dir / "case.yaml").write_text("not: valid")

    runner = CliRunner()
    result = runner.invoke(cli, ["batch", str(tmp_path), "--model", "gpt-4o", "--dry-run"])

    assert result.exit_code == 0
    assert "skipped" in result.output
