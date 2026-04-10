"""Auth tests — mix session and JWT inconsistently."""

from app.auth_session import create_session, validate_session
from app.auth_jwt import create_token, validate_token
from app.routes import get_profile, get_data


def test_session_login():
    sid = create_session("user-1")
    result = validate_session(sid)
    assert result["user_id"] == "user-1"


def test_jwt_token():
    token = create_token("user-2", "jwt-secret-key-v2")
    result = validate_token(token, "jwt-secret-key-v2")
    assert result["user_id"] == "user-2"


def test_profile_with_session():
    sid = create_session("user-3")
    result = get_profile({"X-Session-ID": sid})
    assert result["status"] == 200


def test_data_with_jwt():
    token = create_token("user-4", "jwt-secret-key-v2")
    result = get_data({"Authorization": f"Bearer {token}"})
    assert result["status"] == 200
