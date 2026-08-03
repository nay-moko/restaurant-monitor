"""
event_dispatcher.py
--------------------
Task 9: routes src.events.event_engine's emitted event dicts (the 8 rules --
CUSTOMER_SEATED, CUSTOMER_LEFT, STAFF_IDLE, WORKER_ACTIVE, DELAY_ALERT,
ZONE_TRANSITION, ZONE_OCCUPANCY_CHANGE, TABLE_STATE_CHANGED -- see
src/events/event_engine.py, not modified by this task) into the real,
already-provisioned PostgreSQL database (backend/app/models/*, migrated via
`alembic upgrade head`) and the real local Redis instance.

Task 10 (see docs/TASK10_REPORT.md) extended two of those same handlers,
using event types EventEngine already produces -- no new event types, no
changes to event_engine.py/live_pipeline.py:
- CUSTOMER_SEATED/CUSTOMER_LEFT now also open/close a customer_sessions row
  (session start/last-seen/departure/total duration).
- STAFF_IDLE now also raises a WORKER_IDLE_TOO_LONG alert once
  idle_duration_seconds exceeds the configured system_settings.worker_idle_limit,
  deduped per idle episode via an in-memory set cleared on WORKER_ACTIVE.

Design
------
- EventDispatcher takes a real AsyncSession (backend/app/core/database.py's
  get_db()/AsyncSessionLocal) and a real redis.asyncio.Redis client
  (backend/app/core/redis.py's get_redis_client()) as constructor
  arguments -- both dependency-injected, never constructed internally, so
  tests can hand it a session/client pointed at disposable test data
  (see tests/test_event_dispatcher.py) instead of touching production state.
- One handler method per event_type, registered in self._routes. An
  event_type absent from that table raises UnknownEventTypeError -- it is
  never silently dropped (requirement 4).
- dispatch() is the batch entry point: each event runs through
  dispatch_one() inside its own Postgres SAVEPOINT (AsyncSession.begin_nested())
  and its own try/except, so one event's DB/Redis failure -- including an
  UnknownEventTypeError -- can never (a) stop the rest of the batch or
  (b) leave the shared session's transaction "aborted" for every event that
  follows it (Postgres aborts an entire transaction on the first failed
  statement until it sees a ROLLBACK; without a per-event SAVEPOINT, one bad
  event would silently fail every event after it too). Every failure is
  logged and returned in DispatchResult.failures so callers/tests can
  assert on it (requirement 5).

Why this file lives in src/events/ but imports backend/app/models
-------------------------------------------------------------------
This dispatcher is part of the AI-side event pipeline (consistent with
where event_engine.py already lives), but its ORM inserts/updates need the
real model classes defined under backend/app/models. Exactly like
alembic/env.py already does for the same cross-tree reason, this module
prepends backend/ to sys.path itself rather than relying on whatever the
importing caller's sys.path happens to contain.
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Awaitable, Callable

_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent / "backend"
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

import redis.asyncio as aioredis  # noqa: E402
from sqlalchemy import select  # noqa: E402
from sqlalchemy.dialects.postgresql import insert as pg_insert  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: E402

from app.models import (  # noqa: E402
    Alert,
    AlertStatusEnum,
    CustomerSession,
    CustomerSessionStatus,
    EventLog,
    SystemSetting,
    TableState,
    TableStateEnum,
    WorkerActivityStatus,
    WorkerRole,
    WorkerState,
)

logger = logging.getLogger(__name__)

# Task 10: SystemSetting.worker_idle_limit's own column default
# (backend/app/models/setting.py) -- used when the table has no row yet
# (fresh install), so a missing settings row degrades to "use the same
# default the column itself declares" rather than crashing the dispatcher.
DEFAULT_WORKER_IDLE_LIMIT_SECONDS = 60


class EventDispatcherError(Exception):
    """Base class for every typed error this module raises."""


class UnknownEventTypeError(EventDispatcherError):
    """Raised when an event's event_type has no entry in the routing table."""


@dataclass
class DispatchFailure:
    """One event that failed during a dispatch() batch, and why."""

    event: dict[str, Any]
    error: str


@dataclass
class DispatchResult:
    """Outcome of a dispatch() batch call."""

    succeeded: int = 0
    failures: list[DispatchFailure] = field(default_factory=list)

    @property
    def failed(self) -> int:
        return len(self.failures)


def _utcnow() -> datetime:
    """Naive UTC datetime for EventLog/WorkerState/TableState's plain
    (non-timezone-aware) DateTime columns.

    EngineEvent.time_seconds is video-relative (frame_index / fps, see
    pipeline_output.py), not a wall-clock value -- it cannot be turned into
    a real calendar datetime. The dispatcher instead stamps rows with the
    real time the event was *dispatched*, and preserves the original
    video-relative time_seconds inside `details` for anyone who needs it.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


class EventDispatcher:
    """Routes EventEngine's plain-dict events into Postgres/Redis.

    Parameters
    ----------
    db          : a real, already-open AsyncSession (e.g. from
                  backend.app.core.database.get_db()/AsyncSessionLocal, or a
                  fake/test-scoped session). This class never commits the
                  session -- committing (and thus making writes durable /
                  visible to other connections) is the caller's
                  responsibility, matching get_db()'s own commit-on-exit
                  contract.
    redis_client: a real, already-constructed redis.asyncio.Redis (e.g.
                  from backend.app.core.redis.get_redis_client()).
    """

    def __init__(self, db: AsyncSession, redis_client: "aioredis.Redis"):
        self._db = db
        self._redis = redis_client
        # Task 10: per-worker dedup for WORKER_IDLE_TOO_LONG alerts -- an
        # in-memory, dispatcher-instance-scoped set of entity_ids that
        # already have an alert raised for their *current* idle episode.
        # Populated in _handle_staff_idle, cleared in _handle_worker_active
        # (the episode ending is exactly what should allow the next idle
        # episode to alert again). See docs/TASK10_REPORT.md for why this
        # was chosen over a per-event "query for an existing unresolved
        # alert" check: it's a single dict lookup instead of an extra
        # round-trip to Postgres on every STAFF_IDLE event, and this class
        # already follows the same in-memory-dict-for-per-entity-state
        # pattern as CentralIdentityStore/EventEngine. Traded off: this
        # state does not survive a dispatcher restart mid-episode, so a
        # restart could in theory produce one duplicate alert for a
        # still-ongoing idle episode -- acceptable, same category of
        # limitation as CUSTOMER_LEFT's "no matching open session" case
        # below.
        self._workers_with_active_idle_alert: set[str] = set()
        self._routes: dict[str, Callable[[dict], Awaitable[None]]] = {
            "CUSTOMER_SEATED": self._handle_customer_seated,
            "CUSTOMER_LEFT": self._handle_customer_left,
            "STAFF_IDLE": self._handle_staff_idle,
            "WORKER_ACTIVE": self._handle_worker_active,
            "DELAY_ALERT": self._handle_delay_alert,
            "ZONE_TRANSITION": self._handle_zone_transition,
            "ZONE_OCCUPANCY_CHANGE": self._handle_zone_occupancy_change,
            "TABLE_STATE_CHANGED": self._handle_table_state_changed,
        }

    # -- Public API ----------------------------------------------------------

    async def dispatch(self, events: list[dict[str, Any]]) -> DispatchResult:
        """Dispatch a batch of events. Never raises for a per-event failure
        (DB error, Redis error, or an unknown event_type) -- each is caught,
        logged, and recorded in the returned DispatchResult so the rest of
        the batch keeps running."""
        result = DispatchResult()
        for event in events:
            try:
                # A per-event SAVEPOINT: if this event's handler raises
                # partway through (e.g. after the events_log insert but
                # during the Redis call), Postgres rolls back only this
                # event's own writes -- and, critically, clears the
                # transaction's "aborted" state so the *next* event in this
                # same batch/session can still run. Without this, a single
                # bad event would cascade-fail every event after it.
                async with self._db.begin_nested():
                    await self.dispatch_one(event)
                result.succeeded += 1
            except Exception as exc:  # noqa: BLE001 - intentional: isolate one bad event from the rest of the batch
                logger.error(
                    "EventDispatcher failed on event %r: %s", event, exc, exc_info=True
                )
                result.failures.append(DispatchFailure(event=event, error=str(exc)))
        return result

    async def dispatch_one(self, event: dict[str, Any]) -> None:
        """Route a single event dict. Raises UnknownEventTypeError if
        event_type has no routing rule -- callers that want batch-style
        failure isolation should go through dispatch() instead."""
        event_type = event.get("event_type")
        handler = self._routes.get(event_type)
        if handler is None:
            raise UnknownEventTypeError(
                f"No routing rule for event_type={event_type!r}"
            )
        await handler(event)

    # -- events_log helper -----------------------------------------------------

    async def _insert_event_log(
        self,
        event: dict[str, Any],
        *,
        role: str | None,
        previous_state: str | None,
        new_state: str | None,
    ) -> None:
        details = dict(event.get("details") or {})
        details.setdefault("time_seconds", event.get("time_seconds"))
        if event.get("track_id") is not None:
            details.setdefault("track_id", event["track_id"])

        self._db.add(
            EventLog(
                event_type=event["event_type"],
                entity_id=event.get("global_id"),
                role=role,
                camera_id=event.get("camera_id"),
                zone_id=event.get("zone_id"),
                previous_state=previous_state,
                new_state=new_state,
                event_timestamp=_utcnow(),
                details=details,
            )
        )

    # -- worker_states upsert ----------------------------------------------------

    async def _upsert_worker_state(
        self, event: dict[str, Any], status: WorkerActivityStatus
    ) -> None:
        now = _utcnow()
        stmt = pg_insert(WorkerState).values(
            entity_id=event["global_id"],
            role=WorkerRole.WORKER,
            camera_id=event["camera_id"],
            zone_id=event.get("zone_id"),
            status=status,
            status_started_at=now,
            last_seen_at=now,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[WorkerState.entity_id],
            set_={
                "camera_id": stmt.excluded.camera_id,
                "zone_id": stmt.excluded.zone_id,
                "status": stmt.excluded.status,
                "status_started_at": stmt.excluded.status_started_at,
                "last_seen_at": stmt.excluded.last_seen_at,
            },
        )
        await self._db.execute(stmt)
        # This is a Core-level DML statement -- the ORM unit-of-work/identity
        # map has no idea it just changed a row that might already be loaded
        # as a WorkerState instance in this same session (expire_on_commit is
        # False, see backend/app/core/database.py), so without this, a later
        # `select(WorkerState)` in the same session would silently return the
        # stale, pre-upsert in-memory object instead of re-querying Postgres.
        self._db.expire_all()

    # -- table_states upsert -----------------------------------------------------

    async def _upsert_table_state(
        self, event: dict[str, Any], state: TableStateEnum
    ) -> None:
        now = _utcnow()
        stmt = pg_insert(TableState).values(
            zone_id=event["zone_id"],
            camera_id=event["camera_id"],
            state=state,
            state_started_at=now,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[TableState.zone_id],
            set_={
                "camera_id": stmt.excluded.camera_id,
                "state": stmt.excluded.state,
                "state_started_at": stmt.excluded.state_started_at,
            },
        )
        await self._db.execute(stmt)
        # See the matching comment in _upsert_worker_state -- same identity
        # map staleness risk for a Core-level upsert.
        self._db.expire_all()

    # -- customer_sessions helpers (Task 10) --------------------------------------

    async def _find_open_customer_session(self, entity_id: str | None) -> CustomerSession | None:
        if entity_id is None:
            return None
        stmt = (
            select(CustomerSession)
            .where(CustomerSession.entity_id == entity_id)
            .where(CustomerSession.left_at.is_(None))
            .order_by(CustomerSession.started_at.desc())
            .limit(1)
        )
        return (await self._db.execute(stmt)).scalar_one_or_none()

    # -- system_settings helper (Task 10) -----------------------------------------

    async def _current_worker_idle_limit(self) -> int:
        """Reads system_settings.worker_idle_limit (the one -- effectively
        singleton -- settings row; oldest by id if more than one ever
        exists). Falls back to DEFAULT_WORKER_IDLE_LIMIT_SECONDS, logged at
        warning level, if the table has no row yet (fresh install) rather
        than crashing the dispatcher."""
        stmt = select(SystemSetting).order_by(SystemSetting.id).limit(1)
        row = (await self._db.execute(stmt)).scalar_one_or_none()
        if row is None:
            logger.warning(
                "No system_settings row found -- falling back to default "
                "worker_idle_limit=%ss",
                DEFAULT_WORKER_IDLE_LIMIT_SECONDS,
            )
            return DEFAULT_WORKER_IDLE_LIMIT_SECONDS
        return row.worker_idle_limit

    # -- handlers, one per routing-table row --------------------------------------

    async def _handle_customer_seated(self, event: dict[str, Any]) -> None:
        await self._insert_event_log(
            event, role=WorkerRole.CUSTOMER.value, previous_state=None, new_state="SEATED"
        )

        now = _utcnow()
        self._db.add(
            CustomerSession(
                entity_id=event.get("global_id"),
                table_zone_id=event.get("zone_id"),
                camera_id=event.get("camera_id"),
                started_at=now,
                last_seen_at=now,
                status=CustomerSessionStatus.ACTIVE,
            )
        )

    async def _handle_customer_left(self, event: dict[str, Any]) -> None:
        await self._insert_event_log(
            event, role=WorkerRole.CUSTOMER.value, previous_state="SEATED", new_state="LEFT"
        )

        entity_id = event.get("global_id")
        session_row = await self._find_open_customer_session(entity_id)
        if session_row is None:
            # Either a genuinely stray CUSTOMER_LEFT, or (more likely in
            # practice) the dispatcher restarted mid-session and lost track
            # of the CUSTOMER_SEATED row that opened it. Either way there is
            # no real session state to close -- log and move on rather than
            # fabricating one.
            logger.warning(
                "CUSTOMER_LEFT for entity_id=%s has no matching open "
                "customer_sessions row (dispatcher may have restarted "
                "mid-session) -- skipping session close",
                entity_id,
            )
            return

        now = _utcnow()
        session_row.left_at = now
        session_row.last_seen_at = now
        session_row.total_stay_sec = round((now - session_row.started_at).total_seconds())
        session_row.status = CustomerSessionStatus.COMPLETED

    async def _handle_staff_idle(self, event: dict[str, Any]) -> None:
        await self._insert_event_log(
            event,
            role=WorkerRole.WORKER.value,
            previous_state=WorkerActivityStatus.ACTIVE.value,
            new_state=WorkerActivityStatus.IDLE.value,
        )
        await self._upsert_worker_state(event, WorkerActivityStatus.IDLE)
        await self._redis.set(
            f"worker:{event['global_id']}:status", WorkerActivityStatus.IDLE.value
        )

        entity_id = event.get("global_id")
        details = event.get("details") or {}
        idle_duration = details.get("idle_duration_seconds")
        if idle_duration is None or entity_id is None:
            return

        limit = await self._current_worker_idle_limit()
        if idle_duration <= limit:
            return
        if entity_id in self._workers_with_active_idle_alert:
            # Already alerted for this same, still-ongoing idle episode --
            # see the dedup strategy note in __init__.
            return

        self._db.add(
            Alert(
                alert_type="WORKER_IDLE_TOO_LONG",
                entity_id=entity_id,
                camera_id=event.get("camera_id"),
                zone_id=event.get("zone_id"),
                message=(
                    f"Worker {entity_id} has been idle for {idle_duration:.0f}s, "
                    f"exceeding the configured {limit}s idle limit."
                ),
                status=AlertStatusEnum.ACTIVE,
                details={"idle_duration_seconds": idle_duration, "worker_idle_limit": limit},
            )
        )
        self._workers_with_active_idle_alert.add(entity_id)

    async def _handle_worker_active(self, event: dict[str, Any]) -> None:
        await self._insert_event_log(
            event,
            role=WorkerRole.WORKER.value,
            previous_state=WorkerActivityStatus.IDLE.value,
            new_state=WorkerActivityStatus.ACTIVE.value,
        )
        await self._upsert_worker_state(event, WorkerActivityStatus.ACTIVE)
        await self._redis.set(
            f"worker:{event['global_id']}:status", WorkerActivityStatus.ACTIVE.value
        )

        # The worker is active again -- this idle episode is over, so the
        # next STAFF_IDLE for this entity_id is a *new* episode and should
        # be able to raise its own WORKER_IDLE_TOO_LONG alert.
        self._workers_with_active_idle_alert.discard(event.get("global_id"))

    async def _handle_delay_alert(self, event: dict[str, Any]) -> None:
        await self._insert_event_log(
            event, role=None, previous_state=None, new_state=None
        )

        details = dict(event.get("details") or {})
        occupied = details.get("occupied_seconds")
        threshold = details.get("threshold_seconds")
        if occupied is not None and threshold is not None:
            message = (
                f"Table {event.get('zone_id')} has been occupied for "
                f"{occupied:.0f}s, exceeding the {threshold:.0f}s threshold."
            )
        else:
            message = f"Delay alert for table {event.get('zone_id')}."

        self._db.add(
            Alert(
                alert_type=event["event_type"],
                entity_id=event.get("global_id"),
                camera_id=event.get("camera_id"),
                zone_id=event.get("zone_id"),
                message=message,
                status=AlertStatusEnum.ACTIVE,
                details=details,
            )
        )

    async def _handle_zone_transition(self, event: dict[str, Any]) -> None:
        zone_id = event.get("zone_id")
        if zone_id is None:
            # A ZONE_TRANSITION into "no zone" (track left every known zone)
            # has nothing to key a `zone:{camera_id}:{zone_id}:last_seen`
            # entry on -- deliberately a no-op rather than writing a
            # `zone:cam:None:last_seen` key.
            logger.debug(
                "ZONE_TRANSITION for camera=%s has zone_id=None -- skipping Redis write",
                event.get("camera_id"),
            )
            return
        key = f"zone:{event['camera_id']}:{zone_id}:last_seen"
        await self._redis.set(key, _utcnow().isoformat())

    async def _handle_zone_occupancy_change(self, event: dict[str, Any]) -> None:
        details = event.get("details") or {}
        new_count = details.get("new_count", 0)
        key = f"zone:{event['camera_id']}:{event['zone_id']}:count"
        await self._redis.set(key, new_count)

    async def _handle_table_state_changed(self, event: dict[str, Any]) -> None:
        details = event.get("details") or {}
        previous_state = details.get("previous_state")
        new_state = details.get("new_state")

        await self._insert_event_log(
            event, role=None, previous_state=previous_state, new_state=new_state
        )

        state_enum = TableStateEnum(new_state.upper())
        await self._upsert_table_state(event, state_enum)
        await self._redis.set(f"table:{event['zone_id']}:status", state_enum.value)
