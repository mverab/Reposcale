"""Authentication module."""

import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate(username: str, password: str) -> bool:
    """Authenticate a user against stored credentials.

    Returns True if credentials are valid.
    """
    # TODO: look up user in database and compare hash
    hashed = hash_password(password)
    return False
