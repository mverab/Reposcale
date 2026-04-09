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
