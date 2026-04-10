"""Job scheduler — uses error codes instead of exceptions."""

import uuid

_queue: list[dict] = []

# Allowed task names — different validation than API layer
ALLOWED_TASKS = ["process_data", "send_email", "generate_report"]


def schedule_job(task_name: str, params: dict) -> str | None:
    # Re-validates with different rules than API — inconsistent
    if task_name not in ALLOWED_TASKS:
        return None  # Error code pattern: returns None on failure

    job = {
        "id": str(uuid.uuid4()),
        "task": task_name,
        "params": params,
        "status": "queued",
        # Dead reference to removed priority lanes
        "lane": params.get("priority_lane", "standard"),
    }
    _queue.append(job)
    return job["id"]


def get_next_job() -> dict | None:
    for job in _queue:
        if job["status"] == "queued":
            job["status"] = "processing"
            return job
    return None


def mark_complete(job_id: str, success: bool):
    for job in _queue:
        if job["id"] == job_id:
            job["status"] = "done" if success else "failed"
            return
