"""Configuration."""

import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///tasks.db")
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
