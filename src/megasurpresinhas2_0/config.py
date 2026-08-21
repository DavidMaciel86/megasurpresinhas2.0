from __future__ import annotations

import os
from pathlib import Path

from platformdirs import user_cache_dir


def _number(name: str, default: float, cast):
    try:
        return cast(os.getenv(name, str(default)))
    except ValueError:
        return default


class Config:
    APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT = _number("APP_PORT", 5000, int)
    DEBUG = os.getenv("FLASK_ENV", "production").lower() == "development"
    LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "INFO").upper()
    API_BASE_URL = os.getenv("LOTTERY_API_BASE_URL", "https://api.guidi.dev.br/loteria").rstrip("/")
    API_TIMEOUT = (_number("API_CONNECT_TIMEOUT", 3.05, float), _number("API_READ_TIMEOUT", 10.0, float))
    CACHE_DIR = Path(os.getenv("CACHE_DIR") or user_cache_dir("MegaSurpresinhas2", "DavidMaciel_SmartSolutions"))
    MAX_CONTENT_LENGTH = 16 * 1024
