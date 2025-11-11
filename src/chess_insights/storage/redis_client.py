from __future__ import annotations

from typing import Any
import os
import json

import redis
from dotenv import load_dotenv

_client: redis.Redis | None = None
_env_loaded = False


def _ensure_env_loaded() -> None:
    global _env_loaded
    if not _env_loaded:
        load_dotenv()
        _env_loaded = True


def get_redis_client() -> redis.Redis:
    """
    Lazily initialize and return a Redis client using environment variables.

    REDIS_HOST and REDIS_PORT are read from the environment (with sensible defaults).
    """
    global _client
    _ensure_env_loaded()

    if _client is None:
        host = os.getenv("REDIS_HOST", "localhost")
        port = int(os.getenv("REDIS_PORT", "6379"))
        _client = redis.Redis(host=host, port=port, decode_responses=True)

    return _client


def get_cached_stats(player: str) -> dict[str, Any] | None:
    """
    Retrieve cached stats for a given player from Redis, if present.
    """
    client = get_redis_client()
    raw = client.get(f"stats:{player}")
    if raw is None:
        return None
    return json.loads(raw)


def set_cached_stats(player: str, stats: dict[str, Any]) -> None:
    """
    Store stats for a given player in Redis, as JSON, with an expiration time.
    """
    client = get_redis_client()
    client.set(f"stats:{player}", json.dumps(stats), ex=3600)  # 1h TTL
