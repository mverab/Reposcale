# Background Job System

Task queue with API ingestion, scheduling, and worker execution.

## Architecture
- `api/` — HTTP routes for job submission
- `core/` — Job scheduler and queue management
- `workers/` — Task execution with retry logic

## Running
```
pytest tests/
```
