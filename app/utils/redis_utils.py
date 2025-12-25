import redis
import json
from typing import Any, Optional

# Create a Redis connection (adjust host/port/db as needed)


def get_redis_connection(
    host: str = "localhost",
    port: int = 6379,
    db: int = 0
) -> redis.Redis:
    """
    Returns a Redis connection object.
    """
    return redis.Redis(host=host, port=port, db=db, decode_responses=True)


# Set a key with optional TTL
def set_cache(
    conn: redis.Redis,
    key: str,
    value: Any,
    ttl: Optional[int] = None
) -> None:
    """
    Store a value in Redis with optional TTL (seconds).
    Value is serialized to JSON.
    """
    conn.set(key, json.dumps(value), ex=ttl)


# Get a key
def get_cache(conn: redis.Redis, key: str) -> Optional[Any]:
    """
    Retrieve a value from Redis.
    Returns None if key does not exist.
    """
    data = conn.get(key)
    return json.loads(data) if data else None


# Delete a key
def delete_cache(conn: redis.Redis, key: str) -> None:
    """
    Delete a key from Redis.
    """
    conn.delete(key)


# Check if key exists
def exists_cache(conn: redis.Redis, key: str) -> bool:
    """
    Check if a key exists in Redis.
    """
    return conn.exists(key) == 1
