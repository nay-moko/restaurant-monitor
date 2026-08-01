"""
test_event_dispatcher_smoke_e2e.py
------------------------------------
Task 9's required "one real, full end-to-end smoke test": drives the real,
unmodified EventEngine (src/events/event_engine.py, Task 6) with a sequence
of FrameOutput/TrackOutput objects -- the same typed, stable data contract
LivePipeline actually produces (src/core/pipeline_output.py) and the same
technique tests/test_event_engine.py already uses to test the engine -- far
enough to trigger all 8 event rules in one continuous run, feeds every
event dict EventEngine emits into the real EventDispatcher, and asserts
real rows/keys actually landed in restaurant_db and the real local Redis
instance (queried back and printed with `-s` as proof).

Why synthetic FrameOutputs instead of a literal LivePipeline run
-------------------------------------------------------------------
Task 9 is scoped to the *dispatcher's* storage-routing correctness, not the
CV pipeline's frame-processing correctness -- that was already covered
exhaustively by Tasks 1-6's own test suites, and this task's instructions
explicitly forbid touching live_pipeline.py. EventEngine.process_frame()
cannot tell a synthetic FrameOutput from one LivePipeline actually produced
(it is the exact same dataclass), so this test exercises the identical,
real EventEngine -> EventDispatcher -> Postgres/Redis code path production
traffic would use, without the cost/nondeterminism of running real
YOLO/pose/Re-ID inference against real video for a storage-routing test.

Uses the same real-Postgres/real-Redis fixtures as test_event_dispatcher.py
(same db 14 for Redis, same disposable-camera_id pattern for Postgres).

Run with:  python -m pytest tests/test_event_dispatcher_smoke_e2e.py -v -s
"""

from __future__ import annotations

import sys
import uuid
from pathlib import Path

import pytest
from sqlalchemy import select

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.models import Alert, EventLog, TableState, WorkerState  # noqa: E402

from src.core.pipeline_output import FrameOutput, TrackOutput  # noqa: E402
from src.events.event_dispatcher import EventDispatcher  # noqa: E402
from src.events.event_engine import EventEngine  # noqa: E402

from tests.test_event_dispatcher import (  # noqa: E402 -- reuse the same real-service fixtures/skip markers
    camera_with_zones,
    db_session,
    dispatcher,
    pytestmark,
    redis_client,
)


def make_track(track_id, global_id, role, zone_id, zone_type, action=None) -> TrackOutput:
    return TrackOutput(
        track_id=track_id, global_id=global_id, bbox=[0.0, 0.0, 10.0, 10.0],
        zone_id=zone_id, zone_type=zone_type, role=role, confidence=0.99, action=action,
    )


async def test_full_pipeline_event_engine_dispatcher_smoke(
    dispatcher: EventDispatcher, db_session, redis_client, camera_with_zones, capsys
):
    camera_id, table_zone, service_zone = camera_with_zones
    customer_gid = f"smoke_customer_{uuid.uuid4().hex[:6]}"
    worker_gid = f"smoke_worker_{uuid.uuid4().hex[:6]}"

    # Small, real config overrides (not a modification of event_engine.py --
    # EventEngine already reads these from its own `config` constructor
    # argument) so STAFF_IDLE/DELAY_ALERT fire within a handful of frames
    # instead of needing 300 frames / 900 real seconds.
    engine = EventEngine(config={
        "events": {
            "staff_idle_threshold_frames": 3,
            "delay_alert_threshold_seconds": 1.0,
            "zone_transition_min_interval_seconds": 0.0,
        }
    })

    def frame(idx, t, track1_zone, track1_type, track2_zone, table_state) -> FrameOutput:
        return FrameOutput(
            camera_id=camera_id, video_id="smoke_video", frame_index=idx, time_seconds=t,
            tracks=[
                make_track(1, customer_gid, "customer", track1_zone, track1_type),
                make_track(2, worker_gid, "worker", track2_zone, "service"),
            ],
            table_states={table_zone: table_state},
        )

    frames = [
        frame(0, 0.0, None, None, service_zone, "free"),           # first sighting -- bootstraps state, no events
        frame(1, 1.0, table_zone, "table", service_zone, "occupied"),   # CUSTOMER_SEATED, ZONE_TRANSITION, ZONE_OCCUPANCY_CHANGE, TABLE_STATE_CHANGED
        frame(2, 1.2, table_zone, "table", service_zone, "occupied"),   # idle_counter=2 for the worker
        frame(3, 1.3, table_zone, "table", service_zone, "occupied"),   # idle_counter=3 -> STAFF_IDLE
        frame(4, 2.5, None, None, table_zone, "occupied"),              # CUSTOMER_LEFT, ZONE_TRANSITION, WORKER_ACTIVE, DELAY_ALERT, ZONE_OCCUPANCY_CHANGE
    ]

    all_events: list[dict] = []
    for f in frames:
        all_events.extend(engine.process_frame(f))

    fired_types = {e["event_type"] for e in all_events}
    expected_types = {
        "CUSTOMER_SEATED", "CUSTOMER_LEFT", "STAFF_IDLE", "WORKER_ACTIVE",
        "DELAY_ALERT", "ZONE_TRANSITION", "ZONE_OCCUPANCY_CHANGE", "TABLE_STATE_CHANGED",
    }
    assert expected_types <= fired_types, (
        f"the real EventEngine did not fire every rule this smoke test needs -- "
        f"missing {expected_types - fired_types}. Got: {all_events}"
    )

    result = await dispatcher.dispatch(all_events)
    await db_session.commit()

    assert result.failed == 0, f"dispatch had unexpected failures: {result.failures}"
    assert result.succeeded == len(all_events)

    # ---- Real proof: query real rows back out of restaurant_db and real ----
    # ---- keys back out of Redis, and print them (`-s`) for the report. -----
    logs = (await db_session.execute(
        select(EventLog).where(EventLog.camera_id == camera_id).order_by(EventLog.id)
    )).scalars().all()
    worker_states = (await db_session.execute(
        select(WorkerState).where(WorkerState.entity_id == worker_gid)
    )).scalars().all()
    table_states = (await db_session.execute(
        select(TableState).where(TableState.zone_id == table_zone)
    )).scalars().all()
    alerts = (await db_session.execute(
        select(Alert).where(Alert.camera_id == camera_id)
    )).scalars().all()

    print("\n=== Task 9 end-to-end smoke test: real rows in restaurant_db ===")
    print(f"-- events_log ({len(logs)} rows) --")
    for row in logs:
        print(f"  id={row.id} type={row.event_type} entity_id={row.entity_id} "
              f"role={row.role} zone_id={row.zone_id} prev={row.previous_state} "
              f"new={row.new_state} details={row.details}")
    print(f"-- worker_states ({len(worker_states)} rows) --")
    for row in worker_states:
        print(f"  entity_id={row.entity_id} status={row.status} zone_id={row.zone_id} "
              f"last_seen_at={row.last_seen_at}")
    print(f"-- table_states ({len(table_states)} rows) --")
    for row in table_states:
        print(f"  zone_id={row.zone_id} state={row.state} state_started_at={row.state_started_at}")
    print(f"-- alerts ({len(alerts)} rows) --")
    for row in alerts:
        print(f"  id={row.id} type={row.alert_type} zone_id={row.zone_id} message={row.message!r}")

    print("=== Task 9 end-to-end smoke test: real keys in Redis (db 14) ===")
    redis_keys = {
        f"worker:{worker_gid}:status": await redis_client.get(f"worker:{worker_gid}:status"),
        f"zone:{camera_id}:{table_zone}:last_seen": await redis_client.get(f"zone:{camera_id}:{table_zone}:last_seen"),
        f"zone:{camera_id}:{table_zone}:count": await redis_client.get(f"zone:{camera_id}:{table_zone}:count"),
        f"table:{table_zone}:status": await redis_client.get(f"table:{table_zone}:status"),
    }
    for key, value in redis_keys.items():
        print(f"  {key} = {value!r}")

    # ---- Assertions on that same real, queried-back proof ----
    assert len(logs) >= 4  # CUSTOMER_SEATED, CUSTOMER_LEFT, STAFF_IDLE, TABLE_STATE_CHANGED, DELAY_ALERT all insert events_log rows
    assert {r.event_type for r in logs} >= {
        "CUSTOMER_SEATED", "CUSTOMER_LEFT", "STAFF_IDLE", "TABLE_STATE_CHANGED", "DELAY_ALERT",
    }
    assert len(worker_states) == 1
    assert worker_states[0].status.value == "ACTIVE"  # last event for this worker was WORKER_ACTIVE
    assert len(table_states) == 1
    assert table_states[0].state.value == "OCCUPIED"
    assert len(alerts) == 1
    assert alerts[0].alert_type == "DELAY_ALERT"

    assert redis_keys[f"worker:{worker_gid}:status"] == "ACTIVE"
    assert redis_keys[f"zone:{camera_id}:{table_zone}:last_seen"] is not None
    assert redis_keys[f"zone:{camera_id}:{table_zone}:count"] is not None
    assert redis_keys[f"table:{table_zone}:status"] == "OCCUPIED"
