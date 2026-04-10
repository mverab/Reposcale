"""User API endpoints."""

from app.models.user import get_user, create_user


def register(name: str, email: str) -> dict:
    user = create_user(name, email)
    return {"user_id": user["id"], "status": 201}


def profile(user_id: str) -> dict:
    user = get_user(user_id)
    if not user:
        return {"error": "Not found", "status": 404}
    return {"user": user, "status": 200}
