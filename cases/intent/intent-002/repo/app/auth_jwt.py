"""JWT-based authentication — added after mobile client pivot."""

import hmac
import hashlib
import json
import base64
import time


def create_token(user_id: str, secret: str, ttl: int = 3600) -> str:
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256"}).encode()).decode()
    payload_data = {"user_id": user_id, "exp": int(time.time()) + ttl}
    payload = base64.urlsafe_b64encode(json.dumps(payload_data).encode()).decode()
    signature = hmac.new(secret.encode(), f"{header}.{payload}".encode(), hashlib.sha256).hexdigest()
    return f"{header}.{payload}.{signature}"


def validate_token(token: str, secret: str) -> dict | None:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header, payload, signature = parts
        expected = hmac.new(secret.encode(), f"{header}.{payload}".encode(), hashlib.sha256).hexdigest()
        if signature != expected:
            return None
        data = json.loads(base64.urlsafe_b64decode(payload + "=="))
        if data.get("exp", 0) < time.time():
            return None
        return data
    except Exception:
        return None
