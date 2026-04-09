"""URL storage — JSON file backend."""

import json
import string
import random
from pathlib import Path

DATA_FILE = Path("urls.json")


class URLStore:
    def __init__(self):
        self.urls = self._load()

    def _load(self) -> dict:
        if DATA_FILE.exists():
            with open(DATA_FILE) as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.urls, f, indent=2)

    def _generate_code(self, length: int = 6) -> str:
        chars = string.ascii_letters + string.digits
        while True:
            code = "".join(random.choices(chars, k=length))
            if code not in self.urls:
                return code

    def create(self, url: str) -> str:
        code = self._generate_code()
        self.urls[code] = url
        self._save()
        return code

    def get(self, code: str) -> str | None:
        return self.urls.get(code)

    def delete(self, code: str) -> bool:
        if code in self.urls:
            del self.urls[code]
            self._save()
            return True
        return False
