"""Worker executor — uses silent retry for error handling."""

import time
import logging

from core.scheduler import get_next_job, mark_complete

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


def execute_task(task: str, params: dict) -> bool:
    """Simulate task execution."""
    if task == "process_data":
        return True
    elif task == "send_email":
        if not params.get("to"):
            return False
        return True
    elif task == "generate_report":
        return True
    return False


def run_worker():
    """Main worker loop — has infinite retry bug on certain errors."""
    while True:
        job = get_next_job()
        if job is None:
            time.sleep(1)
            continue

        retries = 0
        while retries < MAX_RETRIES:
            try:
                success = execute_task(job["task"], job["params"])
                mark_complete(job["id"], success)
                break
            except TypeError:
                # BUG: TypeError doesn't increment retries — infinite loop
                logger.warning(f"Type error on job {job['id']}, retrying...")
                time.sleep(0.5)
            except Exception:
                retries += 1
                logger.error(f"Job {job['id']} attempt {retries} failed")
                time.sleep(1)
