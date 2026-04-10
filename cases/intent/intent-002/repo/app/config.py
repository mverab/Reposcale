"""App configuration — both auth secrets present."""

SESSION_SECRET = "session-secret-key-v1"
JWT_SECRET = "jwt-secret-key-v2"

# Unclear which is canonical
AUTH_MODE = "jwt"  # Added later, but not all routes check this
