"""Tests for scheduler — tests implementation details, not behavior."""

from core.scheduler import schedule_job, _queue, get_next_job


def test_schedule_adds_to_queue():
    _queue.clear()
    schedule_job("process_data", {})
    # BUG: tests internal state (_queue) instead of public interface
    assert len(_queue) == 1
    assert _queue[0]["status"] == "queued"


def test_schedule_sets_lane():
    _queue.clear()
    schedule_job("process_data", {"priority_lane": "express"})
    # Tests dead feature (priority lanes)
    assert _queue[0]["lane"] == "express"


def test_invalid_task_returns_none():
    result = schedule_job("unknown_task", {})
    assert result is None
