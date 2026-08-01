"""
test_event_dispatcher.py
--------------------------
Tests for src/events/event_dispatcher.py (Task 9) against a real local
Postgres (restaurant_db -- the same database `alembic upgrade head` already
migrated) and a real local Redis instance.

Isolation strategy
-------------------
Redis: a dedicated db index (14), flushed before/after each test -- same
pattern tests/test_central_identity_store.py already established for its
own db (15); 14 is used here specifically so the two suites never collide
if ever run concurrently.

Postgres has no equivalent of "a separate db index" available cheaply here
(the 9 tables already live in the one migrated `public` schema), so
isolation instead comes from the `camera_with_zones` fixture: every test
gets its own uniquely suffixed, disposable camera_id + two zone_ids (a
"table" zone and a "service" zone -- enough to satisfy every table's real
FK constraints: events_log/alerts/worker_states/table_states all reference
cameras.id and/or zones.id), and the fixture's teardown deletes every row
that could have been created under that camera_id -- across events_log,
alerts, worker_states, table_states, zones, cameras -- regardless of
whether the test passed or failed.

Both real services are required; tests are skipped automatically (not
failed) if either is unreachable.

Run with:  python -m pytest tests/test_event_dispatcher.py -v
"""

from __future__ import annotations

import sys
import uuid
from pathlib import Path
from typing import Any

import pytest
import redis.asyncio as aioredis
import redis as redis_sync
from sqlalchemy import delete, select

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.core.database import AsyncSessionLocal  # noqa: E402
from app.models import (  # noqa: E402
    Alert,
    AlertStatusEnum,
    Camera,
    CameraStatus,
    EventLog,
    TableState,
    TableStateEnum,
    WorkerActivityStatus,
    WorkerState,
    Zone,
)

from src.events.event_dispatcher import (  # noqa: E402
    EventDispatcher,
    UnknownEventTypeError,
)


TEST_REDIS_HOST = "127.0.0.1"  # not "localhost" -- see backend/app/core/config.py's REDIS_HOST comment
TEST_REDIS_PORT = 6379
TEST_REDIS_DB = 14  # dedicated to this test file -- test_central_identity_store.py uses 15


def _redis_reachable() -> bool:
    try:
        client = redis_sync.Redis(
            host=TEST_REDIS_HOST, port=TEST_REDIS_PORT, db=TEST_REDIS_DB,
            socket_timeout=1.0, socket_connect_timeout=1.0,
        )
        return bool(client.ping())
    except Exception:
        return False


def _postgres_reachable() -> bool:
    """A throwaway, unpooled asyncpg connection -- deliberately NOT routed
    through AsyncSessionLocal/its shared engine. This probe runs at
    collection time in its own asyncio.run() event loop, which is closed
    the instant this function returns; if it instead borrowed a connection
    from the shared engine's pool, that connection would come back bound to
    an event loop that no longer exists, and every real async test after it
    would fail with 'Event loop is closed' / 'another operation is in
    progress' the first time it touched the shared pool."""
    import asyncio

    import asyncpg

    from app.core.config import settings

    dsn = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://", 1)

    async def _check() -> bool:
        try:
            conn = await asyncpg.connect(dsn, timeout=2.0)
            await conn.close()
            return True
        except Exception:
            return False

    return asyncio.run(_check())


requires_real_redis = pytest.mark.skipif(
    not _redis_reachable(),
    reason=f"no reachable Redis at {TEST_REDIS_HOST}:{TEST_REDIS_PORT} db={TEST_REDIS_DB}",
)
requires_real_postgres = pytest.mark.skipif(
    not _postgres_reachable(), reason="no reachable Postgres (restaurant_db)"
)

pytestmark = [requires_real_redis, requires_real_postgres]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
async def redis_client():
    client = aioredis.Redis(
        host=TEST_REDIS_HOST, port=TEST_REDIS_PORT, db=TEST_REDIS_DB,
        decode_responses=True, socket_timeout=2.0, socket_connect_timeout=2.0,
    )
    await client.flushdb()
    yield client
    await client.flushdb()
    await client.aclose()


@pytest.fixture()
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture()
async def camera_with_zones(db_session: Any):
    """One disposable Camera + a 'table' Zone + a 'service' Zone -- the real
    FK targets every routing-table row under test needs. Deletes every row
    this test could have created under this camera_id afterwards, in FK-safe
    order, regardless of test outcome."""
    suffix = uuid.uuid4().hex[:8]
    camera_id = f"test9_cam_{suffix}"
    table_zone_id = f"test9_table_{suffix}"
    service_zone_id = f"test9_service_{suffix}"

    db_session.add(Camera(
        id=camera_id, name="Task9 Test Camera",
        rtsp_url="rtsp://test.invalid/stream", status=CameraStatus.OFFLINE,
    ))
    await db_session.flush()
    db_session.add(Zone(
        id=table_zone_id, camera_id=camera_id, name="Task9 Test Table",
        zone_type="table", polygon_coordinates={"points": []},
    ))
    db_session.add(Zone(
        id=service_zone_id, camera_id=camera_id, name="Task9 Test Service Area",
        zone_type="service", polygon_coordinates={"points": []},
    ))
    await db_session.commit()

    try:
        yield camera_id, table_zone_id, service_zone_id
    finally:
        await db_session.execute(delete(EventLog).where(EventLog.camera_id == camera_id))
        await db_session.execute(delete(Alert).where(Alert.camera_id == camera_id))
        await db_session.execute(delete(WorkerState).where(WorkerState.camera_id == camera_id))
        await db_session.execute(delete(TableState).where(TableState.camera_id == camera_id))
        await db_session.execute(delete(Zone).where(Zone.camera_id == camera_id))
        await db_session.execute(delete(Camera).where(Camera.id == camera_id))
        await db_session.commit()


@pytest.fixture()
def dispatcher(db_session: Any, redis_client: Any) -> EventDispatcher:
    return EventDispatcher(db=db_session, redis_client=redis_client)


def make_event(
    event_type: str,
    camera_id: str,
    *,
    zone_id: str | None = None,
    global_id: str | None = None,
    track_id: int | None = None,
    time_seconds: float = 1.0,
    details: dict | None = None,
) -> dict[str, Any]:
    """Builds a plain event dict matching EngineEvent's shape
    (src/events/event_engine.py's engine_event_to_dict output) directly --
    the dispatcher only ever sees plain dicts, so these are hand-built here
    rather than driven through a real EventEngine, per this file's
    routing-table-focused scope (see test_event_dispatcher_smoke_e2e.py for
    the real-EventEngine-driven end-to-end path)."""
    return {
        "event_type": event_type,
        "camera_id": camera_id,
        "time_seconds": time_seconds,
        "track_id": track_id,
        "global_id": global_id,
        "zone_id": zone_id,
        "details": details or {},
    }


# ---------------------------------------------------------------------------
# Routing-table tests -- one per event_type
# ---------------------------------------------------------------------------

async def test_customer_seated_inserts_events_log_row(dispatcher, db_session, camera_with_zones):
    camera_id, table_zone_id, _service_zone_id = camera_with_zones
    event = make_event(
        "CUSTOMER_SEATED", camera_id, zone_id=table_zone_id,
        global_id="test9_customer_1", track_id=1,
    )

    result = await dispatcher.dispatch([event])
    await db_session.commit()

    assert result.succeeded == 1
    assert result.failed == 0

    rows = (await db_session.execute(
        select(EventLog).where(EventLog.camera_id == camera_id)
    )).scalars().all()
    assert len(rows) == 1
    row = rows[0]
    assert row.event_type == "CUSTOMER_SEATED"
    assert row.entity_id == "test9_customer_1"
    assert row.role == "CUSTOMER"
    assert row.zone_id == table_zone_id
    assert row.new_state == "SEATED"
    assert row.event_timestamp is not None


async def test_customer_left_inserts_events_log_row(dispatcher, db_session, camera_with_zones):
    camera_id, table_zone_id, _service_zone_id = camera_with_zones
    event = make_event(
        "CUSTOMER_LEFT", camera_id, zone_id=table_zone_id,
        global_id="test9_customer_2", track_id=2,
        details={"duration_seconds": 42.0, "reason": "zone_change"},
    )

    result = await dispatcher.dispatch([event])
    await db_session.commit()

    assert result.succeeded == 1
    rows = (await db_session.execute(
        select(EventLog).where(EventLog.camera_id == camera_id)
    )).scalars().all()
    assert len(rows) == 1
    assert rows[0].event_type == "CUSTOMER_LEFT"
    assert rows[0].new_state == "LEFT"
    assert rows[0].details["duration_seconds"] == 42.0


async def test_staff_idle_then_worker_active_upserts_single_worker_state_row(
    dispatcher, db_session, redis_client, camera_with_zones
):
    camera_id, _table_zone_id, service_zone_id = camera_with_zones
    gid = "test9_worker_1"

    idle_event = make_event(
        "STAFF_IDLE", camera_id, zone_id=service_zone_id, global_id=gid, track_id=3,
        details={"idle_frames": 300, "idle_duration_seconds": 12.0, "threshold_frames": 300},
    )
    result = await dispatcher.dispatch([idle_event])
    await db_session.commit()
    assert result.succeeded == 1

    ws_rows = (await db_session.execute(
        select(WorkerState).where(WorkerState.entity_id == gid)
    )).scalars().all()
    assert len(ws_rows) == 1
    assert ws_rows[0].status == WorkerActivityStatus.IDLE
    assert ws_rows[0].camera_id == camera_id
    assert await redis_client.get(f"worker:{gid}:status") == "IDLE"

    active_event = make_event(
        "WORKER_ACTIVE", camera_id, zone_id=service_zone_id, global_id=gid, track_id=3,
        details={"idle_frames": 300, "idle_duration_seconds": 20.0},
    )
    result2 = await dispatcher.dispatch([active_event])
    await db_session.commit()
    assert result2.succeeded == 1

    ws_rows2 = (await db_session.execute(
        select(WorkerState).where(WorkerState.entity_id == gid)
    )).scalars().all()
    # Still exactly one row: an upsert (ON CONFLICT DO UPDATE on entity_id),
    # not a second, duplicate insert.
    assert len(ws_rows2) == 1
    assert ws_rows2[0].status == WorkerActivityStatus.ACTIVE
    assert await redis_client.get(f"worker:{gid}:status") == "ACTIVE"

    log_rows = (await db_session.execute(
        select(EventLog).where(EventLog.camera_id == camera_id)
    )).scalars().all()
    assert {r.event_type for r in log_rows} == {"STAFF_IDLE", "WORKER_ACTIVE"}


async def test_delay_alert_inserts_events_log_and_alert_row(dispatcher, db_session, camera_with_zones):
    camera_id, table_zone_id, _service_zone_id = camera_with_zones
    event = make_event(
        "DELAY_ALERT", camera_id, zone_id=table_zone_id,
        details={"occupied_seconds": 950.0, "threshold_seconds": 900.0},
    )

    result = await dispatcher.dispatch([event])
    await db_session.commit()
    assert result.succeeded == 1

    alerts = (await db_session.execute(
        select(Alert).where(Alert.camera_id == camera_id)
    )).scalars().all()
    assert len(alerts) == 1
    assert alerts[0].alert_type == "DELAY_ALERT"
    assert alerts[0].status == AlertStatusEnum.ACTIVE
    assert alerts[0].zone_id == table_zone_id
    assert "950" in alerts[0].message

    logs = (await db_session.execute(
        select(EventLog).where(EventLog.camera_id == camera_id)
    )).scalars().all()
    assert len(logs) == 1
    assert logs[0].event_type == "DELAY_ALERT"


async def test_zone_transition_writes_only_redis_no_db_row(
    dispatcher, db_session, redis_client, camera_with_zones
):
    camera_id, table_zone_id, _service_zone_id = camera_with_zones
    event = make_event(
        "ZONE_TRANSITION", camera_id, zone_id=table_zone_id,
        global_id="test9_g1", track_id=4,
        details={"from_zone_id": None, "to_zone_id": table_zone_id},
    )

    result = await dispatcher.dispatch([event])
    await db_session.commit()
    assert result.succeeded == 1

    logs = (await db_session.execute(
        select(EventLog).where(EventLog.camera_id == camera_id)
    )).scalars().all()
    assert logs == []

    val = await redis_client.get(f"zone:{camera_id}:{table_zone_id}:last_seen")
    assert val is not None


async def test_zone_transition_with_no_zone_id_is_a_safe_noop(dispatcher, redis_client):
    event = make_event("ZONE_TRANSITION", "test9_cam_x", zone_id=None, global_id="g", track_id=5)
    result = await dispatcher.dispatch([event])
    assert result.succeeded == 1
    assert result.failed == 0


async def test_zone_occupancy_change_sets_redis_count(dispatcher, redis_client, camera_with_zones):
    camera_id, table_zone_id, _service_zone_id = camera_with_zones
    event = make_event(
        "ZONE_OCCUPANCY_CHANGE", camera_id, zone_id=table_zone_id,
        details={"old_count": 1, "new_count": 3},
    )
    result = await dispatcher.dispatch([event])
    assert result.succeeded == 1
    assert await redis_client.get(f"zone:{camera_id}:{table_zone_id}:count") == "3"


async def test_table_state_changed_updates_db_and_redis(
    dispatcher, db_session, redis_client, camera_with_zones
):
    camera_id, table_zone_id, _service_zone_id = camera_with_zones
    event = make_event(
        "TABLE_STATE_CHANGED", camera_id, zone_id=table_zone_id,
        details={"previous_state": "free", "new_state": "occupied", "time_seconds": 5.0},
    )

    result = await dispatcher.dispatch([event])
    await db_session.commit()
    assert result.succeeded == 1

    logs = (await db_session.execute(
        select(EventLog).where(EventLog.camera_id == camera_id)
    )).scalars().all()
    assert len(logs) == 1
    assert logs[0].previous_state == "free"
    assert logs[0].new_state == "occupied"

    ts_rows = (await db_session.execute(
        select(TableState).where(TableState.zone_id == table_zone_id)
    )).scalars().all()
    assert len(ts_rows) == 1
    assert ts_rows[0].state == TableStateEnum.OCCUPIED
    assert ts_rows[0].camera_id == camera_id

    assert await redis_client.get(f"table:{table_zone_id}:status") == "OCCUPIED"

    # A second TABLE_STATE_CHANGED for the same zone must UPDATE the same
    # row (zone_id is table_states' primary key), not insert a second one.
    event2 = make_event(
        "TABLE_STATE_CHANGED", camera_id, zone_id=table_zone_id,
        details={"previous_state": "occupied", "new_state": "dirty", "time_seconds": 6.0},
    )
    result2 = await dispatcher.dispatch([event2])
    await db_session.commit()
    assert result2.succeeded == 1

    ts_rows2 = (await db_session.execute(
        select(TableState).where(TableState.zone_id == table_zone_id)
    )).scalars().all()
    assert len(ts_rows2) == 1
    assert ts_rows2[0].state == TableStateEnum.DIRTY
    assert await redis_client.get(f"table:{table_zone_id}:status") == "DIRTY"


# ---------------------------------------------------------------------------
# Requirement 4: unknown event_type -> typed error, never silently dropped
# ---------------------------------------------------------------------------

async def test_unknown_event_type_raises_typed_error(dispatcher):
    with pytest.raises(UnknownEventTypeError):
        await dispatcher.dispatch_one({"event_type": "SOMETHING_MADE_UP", "camera_id": "camX"})


# ---------------------------------------------------------------------------
# Requirement 5: one event's failure must not stop the rest of the batch
# ---------------------------------------------------------------------------

async def test_dispatch_isolates_unknown_event_type_and_keeps_processing_the_rest(
    dispatcher, db_session, camera_with_zones
):
    camera_id, table_zone_id, _service_zone_id = camera_with_zones
    good_1 = make_event("CUSTOMER_SEATED", camera_id, zone_id=table_zone_id, global_id="test9_c1", track_id=10)
    bad = {"event_type": "NOT_A_REAL_EVENT_TYPE", "camera_id": camera_id}
    good_2 = make_event(
        "CUSTOMER_LEFT", camera_id, zone_id=table_zone_id, global_id="test9_c1", track_id=10,
        details={"duration_seconds": 30.0, "reason": "zone_change"},
    )

    result = await dispatcher.dispatch([good_1, bad, good_2])
    await db_session.commit()

    assert result.succeeded == 2
    assert result.failed == 1
    assert "NOT_A_REAL_EVENT_TYPE" in result.failures[0].error

    logs = (await db_session.execute(
        select(EventLog).where(EventLog.camera_id == camera_id)
    )).scalars().all()
    assert {r.event_type for r in logs} == {"CUSTOMER_SEATED", "CUSTOMER_LEFT"}


async def test_dispatch_isolates_a_real_fk_constraint_violation_and_keeps_processing_the_rest(
    dispatcher, db_session, camera_with_zones
):
    """The critical case: a real Postgres error (not just an app-level
    missing-route dict lookup) mid-batch must not abort every event that
    comes after it in the same session/transaction. Without a per-event
    SAVEPOINT, Postgres leaves the whole transaction 'aborted' after the
    first failed statement, and every subsequent statement -- even a
    perfectly valid one -- would fail too."""
    camera_id, table_zone_id, _service_zone_id = camera_with_zones

    good_1 = make_event("CUSTOMER_SEATED", camera_id, zone_id=table_zone_id, global_id="test9_c2", track_id=11)
    # References a camera_id that does not exist -> real FK violation.
    fk_violation = make_event(
        "STAFF_IDLE", "test9_cam_does_not_exist_" + uuid.uuid4().hex[:6],
        zone_id=None, global_id="test9_worker_bad", track_id=12,
        details={"idle_frames": 300, "idle_duration_seconds": 1.0, "threshold_frames": 300},
    )
    good_2 = make_event("CUSTOMER_SEATED", camera_id, zone_id=table_zone_id, global_id="test9_c3", track_id=13)

    result = await dispatcher.dispatch([good_1, fk_violation, good_2])
    await db_session.commit()

    assert result.succeeded == 2
    assert result.failed == 1

    logs = (await db_session.execute(
        select(EventLog).where(EventLog.camera_id == camera_id)
    )).scalars().all()
    # Both CUSTOMER_SEATED rows landed despite the FK violation sandwiched
    # between them in the same batch/session.
    assert len(logs) == 2
    assert {r.entity_id for r in logs} == {"test9_c2", "test9_c3"}
