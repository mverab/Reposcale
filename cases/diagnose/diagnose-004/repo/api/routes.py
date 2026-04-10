"""API routes — uses exceptions for error handling."""

from core.scheduler import schedule_job


def create_job(payload: dict) -> dict:
    if not payload.get("task_name"):
        raise ValueError("task_name is required")
    if not isinstance(payload.get("params", {}), dict):
        raise TypeError("params must be a dict")

    # Validated here, but scheduler re-validates with different rules
    job_id = schedule_job(payload["task_name"], payload.get("params", {}))

    if job_id is None:
        raise RuntimeError("Scheduling failed")
    return {"job_id": job_id, "status": "queued"}


def cancel_job(job_id: str) -> dict:
    # TODO: implement cancellation
    return {"job_id": job_id, "status": "cancelled"}


# Dead code from removed priority lanes feature
def set_priority_lane(job_id: str, lane: str):
    """Assign job to a priority lane for faster processing."""
    # Priority lanes were removed in v2.0 but this function remains
    valid_lanes = ["express", "standard", "bulk"]
    if lane not in valid_lanes:
        raise ValueError(f"Invalid lane: {lane}")
    return {"job_id": job_id, "lane": lane}
