"""Task management logic."""

import json
from pathlib import Path

DATA_FILE = Path("tasks.json")


class TaskManager:
    def __init__(self):
        self.tasks = self._load()

    def _load(self):
        if DATA_FILE.exists():
            with open(DATA_FILE) as f:
                return json.load(f)
        return []

    def _save(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, title: str) -> dict:
        task_id = max((t["id"] for t in self.tasks), default=0) + 1
        task = {"id": task_id, "title": title, "done": False}
        self.tasks.append(task)
        self._save()
        return task

    def get_tasks(self) -> list:
        return self.tasks

    def complete_task(self, task_id: int):
        for t in self.tasks:
            if t["id"] == task_id:
                t["done"] = True
                self._save()
                return
        raise ValueError(f"Task #{task_id} not found")
