"""Note storage — in-memory for now."""

import uuid
from datetime import datetime


class NoteStore:
    def __init__(self):
        self._notes: dict[str, dict] = {}

    def create(self, title: str, body: str = "") -> dict:
        note_id = str(uuid.uuid4())
        note = {
            "id": note_id,
            "title": title,
            "body": body,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._notes[note_id] = note
        return note

    def get(self, note_id: str) -> dict | None:
        return self._notes.get(note_id)

    def list_all(self) -> list[dict]:
        return list(self._notes.values())

    def delete(self, note_id: str) -> bool:
        return self._notes.pop(note_id, None) is not None
