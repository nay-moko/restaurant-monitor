"""
إدارة الاتصال بـ Redis (Pub/Sub & Fast State Store)
-----------------------------------------------------
Minimal async Redis client wrapper for the FastAPI/dispatcher layer.

Mirrors the connection-parameter style already established and proven
working in src/core/central_identity_store.py (Task 7/8): host/port/db read
from Settings, decode_responses=True, explicit socket timeouts so an
unreachable Redis fails fast instead of hanging a request/event dispatch.

The one deliberate difference from that module: this uses redis.asyncio
instead of the sync `redis` package, since this project's FastAPI/dispatcher
code is async end-to-end (backend/app/core/database.py's AsyncSession).
Unlike get_db()/AsyncSessionLocal, there is no separate lightweight
"session" object to build per call here -- a redis.asyncio.Redis instance
already IS a connection pool and is meant to be constructed once and
reused, so get_redis_client() just hands out the one shared client instead
of building a new one per request.
"""

from __future__ import annotations

from typing import AsyncGenerator

import redis.asyncio as redis

from app.core.config import settings

# redis.asyncio.Redis() does not connect eagerly -- constructing this
# client never touches the network, so an unreachable Redis cannot fail
# app startup. The first real connection attempt happens on first command.
redis_client: redis.Redis = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
    socket_timeout=5.0,
    socket_connect_timeout=5.0,
)


async def get_redis_client() -> AsyncGenerator[redis.Redis, None]:
    """Dependency لتمرير عميل Redis للـ Endpoints, same call shape as get_db()."""
    yield redis_client
