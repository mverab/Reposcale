"""Session-based authentication — original auth strategy."""

_sessions: dict[str, dict] = {}


def create_session(user_id: str) -> str:
    import uuid
    session_id = str(uuid.uuid4())
    _sessions[session_id] = {"user_id": user_id, "active": True}
    return session_id


def validate_session(session_id: str) -> dict | None:
    session = _sessions.get(session_id)
    if session and session.get("active"):
        return session
    return None


def destroy_session(session_id: str):
    if session_id in _sessions:
        _sessions[session_id]["active"] = False
