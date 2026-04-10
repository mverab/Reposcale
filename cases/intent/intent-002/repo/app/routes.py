"""API routes — mixed auth strategies."""

from app.auth_session import validate_session
from app.auth_jwt import validate_token
from app.config import JWT_SECRET


def get_profile(headers: dict) -> dict:
    """Uses session auth (original strategy)."""
    session_id = headers.get("X-Session-ID")
    if not session_id:
        return {"error": "No session", "status": 401}

    session = validate_session(session_id)
    if not session:
        return {"error": "Invalid session", "status": 401}

    return {"user_id": session["user_id"], "status": 200}


def get_data(headers: dict) -> dict:
    """Uses JWT auth (new strategy)."""
    auth = headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return {"error": "No token", "status": 401}

    token = auth[7:]
    payload = validate_token(token, JWT_SECRET)
    if not payload:
        return {"error": "Invalid token", "status": 401}

    return {"user_id": payload["user_id"], "data": [], "status": 200}


def update_settings(headers: dict, body: dict) -> dict:
    """Unclear which auth — tries both."""
    session_id = headers.get("X-Session-ID")
    auth = headers.get("Authorization", "")

    user_id = None
    if session_id:
        session = validate_session(session_id)
        if session:
            user_id = session["user_id"]

    if not user_id and auth.startswith("Bearer "):
        payload = validate_token(auth[7:], JWT_SECRET)
        if payload:
            user_id = payload["user_id"]

    if not user_id:
        return {"error": "Unauthorized", "status": 401}

    return {"user_id": user_id, "updated": True, "status": 200}
