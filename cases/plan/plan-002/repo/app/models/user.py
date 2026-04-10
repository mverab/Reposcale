"""User model — in-memory store."""

import uuid

_users: dict[str, dict] = {}


def create_user(name: str, email: str) -> dict:
    user = {"id": str(uuid.uuid4()), "name": name, "email": email}
    _users[user["id"]] = user
    return user


def get_user(user_id: str) -> dict | None:
    return _users.get(user_id)
