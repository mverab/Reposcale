"""Tests for task management."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from src.tasks import TaskManager


def test_add_task():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp = Path(f.name)

    with patch("src.tasks.DATA_FILE", tmp):
        tm = TaskManager()
        task = tm.add_task("Test task")
        assert task["title"] == "Test task"
        assert task["done"] is False
        assert task["id"] == 1

    tmp.unlink(missing_ok=True)


def test_complete_task():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp = Path(f.name)

    with patch("src.tasks.DATA_FILE", tmp):
        tm = TaskManager()
        tm.add_task("Test task")
        tm.complete_task(1)
        assert tm.tasks[0]["done"] is True

    tmp.unlink(missing_ok=True)
