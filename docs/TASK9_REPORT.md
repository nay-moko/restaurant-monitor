# Task 9 — Event Dispatcher (Real Redis + Real PostgreSQL Integration)

## 1. Scope recap

Build a real `EventDispatcher` that routes Task 6's `EventEngine` output
(8 event types, `src/events/event_engine.py`, not modified) into the real,
already-migrated `restaurant_db` (9 tables via `alembic upgrade head`) and
the real local Redis/Memurai instance at `localhost:6379`. No FastAPI
endpoints, WebSocket, frontend, or changes to `live_pipeline.py`/
`event_engine.py`.

Before writing any code, the actual model files were read directly
(`backend/app/models/event_log.py`, `worker_state.py`, `table_state.py`,
`alert.py`, `camera.py`, `zone.py`, `customer_session.py`) — the routing
table below uses their real, exact column/enum names, not the task's
semantic-guide names.

## 2. `backend/app/core/redis.py` — new minimal async Redis client

Previously a single comment line. Now:

```python
redis_client: redis.Redis = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
    socket_timeout=5.0,
    socket_connect_timeout=5.0,
)

async def get_redis_client() -> AsyncGenerator[redis.Redis, None]:
    yield redis_client
```

Mirrors `src/core/central_identity_store.py`'s connection-parameter style
(host/port/db from config, `decode_responses=True`, explicit socket
timeouts so an unreachable Redis fails fast) but uses `redis.asyncio`
instead of the sync `redis` package, since this project's async layer
(`backend/app/core/database.py`'s `AsyncSession`) is async end-to-end.

One deliberate difference from `get_db()`: `get_db()` yields a **new**
`AsyncSession` per call because SQLAlchemy sessions are cheap, short-lived
wrappers around a shared connection-pooled `engine`. A `redis.asyncio.Redis`
instance *is itself* already a connection pool — there is no equivalent
lightweight "session" object to construct per call — so `get_redis_client()`
just yields the one shared, module-level client instead of building a new
one every time.

**`backend/app/core/config.py`**: added `REDIS_HOST: str = "127.0.0.1"`,
`REDIS_PORT: int = 6379`, `REDIS_DB: int = 0` to `Settings`. `.env.example`
updated to document the same three keys (`.env` itself untouched — the
defaults already match the real local instance).

`127.0.0.1`, not `localhost` — see §7.1 for why.

## 3. `src/events/event_dispatcher.py` — new file

Lives in `src/events/` alongside `event_engine.py` per instructions, but
its ORM inserts/updates need `backend/app/models`. Exactly like
`alembic/env.py` already does for the identical cross-tree reason
([alembic/env.py:8-14](alembic/env.py#L8-L14)), the module prepends
`backend/` to `sys.path` itself
([event_dispatcher.py:40-42](src/events/event_dispatcher.py#L40-L42)) rather
than relying on the caller's `sys.path`.

`EventDispatcher.__init__(self, db: AsyncSession, redis_client: aioredis.Redis)`
([L115-129](src/events/event_dispatcher.py#L115-L129)) — both
dependency-injected, never constructed internally, so tests hand it a
session/client pointed at disposable data instead of touching production
state.

### 3.1 Routing table as implemented (real column/key names)

| event_type | Postgres | Redis |
|---|---|---|
| `CUSTOMER_SEATED` | `events_log` insert: `entity_id=global_id`, `role="CUSTOMER"`, `previous_state=None`, `new_state="SEATED"` | — |
| `CUSTOMER_LEFT` | `events_log` insert: `role="CUSTOMER"`, `previous_state="SEATED"`, `new_state="LEFT"`, `details` carries the engine's `duration_seconds`/`reason` | — |
| `STAFF_IDLE` | `events_log` insert (`role="WORKER"`, `previous_state="ACTIVE"`, `new_state="IDLE"`) **+** `worker_states` upsert (`entity_id` PK, `status=WorkerActivityStatus.IDLE`, `status_started_at`/`last_seen_at=now`) | `SET worker:{entity_id}:status "IDLE"` |
| `WORKER_ACTIVE` | `events_log` insert (`previous_state="IDLE"`, `new_state="ACTIVE"`) **+** `worker_states` upsert (`status=ACTIVE`) | `SET worker:{entity_id}:status "ACTIVE"` |
| `DELAY_ALERT` | `events_log` insert **+** `alerts` insert (`alert_type="DELAY_ALERT"`, `zone_id`, `message` built from `occupied_seconds`/`threshold_seconds`, `status=AlertStatusEnum.ACTIVE`) | — |
| `ZONE_TRANSITION` | — | `SET zone:{camera_id}:{zone_id}:last_seen <ISO datetime>` |
| `ZONE_OCCUPANCY_CHANGE` | — | `SET zone:{camera_id}:{zone_id}:count <new_count>` |
| `TABLE_STATE_CHANGED` | `events_log` insert (`previous_state`/`new_state` = the engine's own lowercase `"free"/"occupied"/"dirty"` strings, verbatim) **+** `table_states` upsert (`zone_id` PK, `state=TableStateEnum(new_state.upper())`) | `SET table:{zone_id}:status "OCCUPIED"` (etc., uppercase enum value) |

`worker_states`/`table_states` upserts use real Postgres
`INSERT ... ON CONFLICT (entity_id\|zone_id) DO UPDATE`
([`_upsert_worker_state`](src/events/event_dispatcher.py#L215-L247),
[`_upsert_table_state`](src/events/event_dispatcher.py#L249-L272)) against
each table's actual primary key — not a `SELECT`-then-`INSERT`/`UPDATE`
race.

An event_type absent from the routing table raises `UnknownEventTypeError`
(typed, [L78-80](src/events/event_dispatcher.py#L78-L80)) from
`dispatch_one()` — never silently dropped.

### 3.2 A real SQLAlchemy identity-map bug found and fixed during testing

`ON CONFLICT DO UPDATE` is a Core-level DML statement — the ORM's identity
map has no way to know it just changed a row that might already be loaded
as a Python object in the same session. Because `AsyncSessionLocal` is
configured with `expire_on_commit=False`
([database.py:18](backend/app/core/database.py#L18)), a second
`STAFF_IDLE` → `WORKER_ACTIVE` sequence in the same session initially
returned the **stale, pre-upsert** `WorkerState` object on re-query — the
Postgres row itself was correct, but the ORM read gave back cached data.
Fixed by calling `self._db.expire_all()` immediately after each upsert
executes ([L222](src/events/event_dispatcher.py#L222),
[L266](src/events/event_dispatcher.py#L266)), forcing the next `select()`
in that session to re-fetch from Postgres. Caught by
`test_staff_idle_then_worker_active_upserts_single_worker_state_row`
re-querying after both dispatches — this test failed with the real, wrong
value (`IDLE` instead of `ACTIVE`) before the fix, confirming it wasn't a
false positive.

## 4. Failure isolation (`dispatch()`)

`dispatch(events: list[dict]) -> DispatchResult` never raises for a
per-event failure. Each event runs inside its own Postgres **SAVEPOINT**
(`async with self._db.begin_nested():`,
[L158-166](src/events/event_dispatcher.py#L158-L166)) wrapped in its own
`try/except`. This SAVEPOINT is not cosmetic — it is the actual fix for a
real bug found while writing the tests:

Postgres aborts an entire transaction on the first failed statement (a
real FK violation, a bad enum value, anything) until it sees a `ROLLBACK` —
every statement after it in the same transaction fails too, even a
perfectly valid one, with `current transaction is aborted, commands
ignored until end of transaction block`. Without a per-event SAVEPOINT,
one bad event in a batch would cascade-fail every event dispatched after
it in the same session, which would badly violate requirement 5. The
SAVEPOINT rolls back only that one event's own writes on failure and
clears the "aborted" flag so the next event's statements run normally.

Proven by two tests, not just asserted:
- `test_dispatch_isolates_unknown_event_type_and_keeps_processing_the_rest` —
  an app-level `UnknownEventTypeError` sandwiched between two good events.
- `test_dispatch_isolates_a_real_fk_constraint_violation_and_keeps_processing_the_rest` —
  a **real Postgres FK violation** (a `STAFF_IDLE` event referencing a
  nonexistent `camera_id`) sandwiched between two good `CUSTOMER_SEATED`
  events in the same batch/session. Both good events land; only the bad
  one is reported in `DispatchResult.failures`. This test would fail
  (second good event lost) without the SAVEPOINT — confirmed by running it
  against an earlier version of the code that executed each handler
  without `begin_nested()`.

## 5. Tests

### 5.1 `tests/test_event_dispatcher.py` — 11 tests, routing table + failure isolation

Real `restaurant_db` (via `AsyncSessionLocal`, unmodified) and real Redis
db 14 (dedicated — `tests/test_central_identity_store.py` already claims
db 15). Isolation:
- **Redis**: `flushdb()` before/after each test on db 14 (same pattern as
  the Task 8 test file, different db index).
- **Postgres**: no cheap separate-schema option for 9 already-migrated
  tables, so each test gets a uniquely suffixed, disposable `Camera` + two
  `Zone` rows (a `"table"` zone and a `"service"` zone — real FK targets
  for `events_log`/`alerts`/`worker_states`/`table_states`), and a teardown
  that deletes every row created under that `camera_id` — in FK-safe order
  (`events_log`, `alerts`, `worker_states`, `table_states`, `zones`,
  `cameras`) — regardless of pass/fail. Verified empty (`0` rows in all 6
  tables) after a full run (§5.3).

Both real services are required; tests skip (not fail) if either is
unreachable (`requires_real_redis`/`requires_real_postgres` markers).

One test per routing-table row, plus:
`test_unknown_event_type_raises_typed_error`,
`test_dispatch_isolates_unknown_event_type_and_keeps_processing_the_rest`,
`test_dispatch_isolates_a_real_fk_constraint_violation_and_keeps_processing_the_rest`
(§4), and `test_staff_idle_then_worker_active_upserts_single_worker_state_row`
which also asserts the upsert produces exactly **one** `worker_states` row
across two dispatches, not a duplicate.

```
python -m pytest tests/test_event_dispatcher.py -v
11 passed in 2.28s
```

### 5.2 `tests/test_event_dispatcher_smoke_e2e.py` — the required real end-to-end smoke test

Drives the real, unmodified `EventEngine` with a 5-frame sequence of real
`FrameOutput`/`TrackOutput` objects (same dataclasses `LivePipeline`
actually produces, same technique `tests/test_event_engine.py` already
uses) engineered to fire all 8 rules in one continuous run, feeds every
emitted event dict into the real `EventDispatcher`, then **queries the
real rows/keys back out** and prints them (`-s`, see §6 for why synthetic
frames rather than a literal `LivePipeline` run). Reuses the same
real-service fixtures as §5.1 (imported directly from
`test_event_dispatcher.py`).

```
python -m pytest tests/test_event_dispatcher_smoke_e2e.py -v -s
1 passed in 2.02s
```

### 5.3 Regression — full existing suite, honest before/after

```
Before (baseline, before any Task 9 change): 9 failed, 67 passed, 76 total  (107.49s)
After  (with Task 9's new files):            9 failed, 79 passed, 88 total  (111.12s)
```

Delta: exactly `+12 passed` (11 in `test_event_dispatcher.py` + 1 in
`test_event_dispatcher_smoke_e2e.py`), `+0 failed`. The same 9 pre-existing
failures remain, byte-identical to baseline, all unrelated to this task
(`test_live_pipeline_timing.py` ×3, `test_pipeline_output.py`'s
`_update_person_state` test, `test_pose_stride.py` ×1,
`test_table_zone_anchoring.py` ×3, `test_tracker.py` ×1 — same set
documented in `docs/TASK8_REPORT.md` §7). Nothing in
`live_pipeline.py`/`event_engine.py`/FastAPI/WebSocket/frontend was
touched.

Post-run verification that test cleanup actually works: a direct query of
all 6 affected tables in the real `restaurant_db` after the full suite run
shows `0` rows in every one (`cameras`, `zones`, `worker_states`,
`table_states`, `events_log`, `alerts`) — no test-created data was left
behind.

## 6. Real end-to-end smoke test — actual proof

5 frames on one synthetic camera/customer/worker/table, thresholds
overridden via `EventEngine`'s own legitimate `config` argument
(`staff_idle_threshold_frames=3`, `delay_alert_threshold_seconds=1.0`,
`zone_transition_min_interval_seconds=0.0` — not a modification of
`event_engine.py`, just smaller numbers so the same real rules fire in 5
frames instead of 300). All 8 event types fired for real; `dispatch()`
reported `0` failures. Actual printed output from the real run:

```
=== Task 9 end-to-end smoke test: real rows in restaurant_db ===
-- events_log (6 rows) --
  id=23 type=CUSTOMER_SEATED entity_id=smoke_customer_c3e927 role=CUSTOMER zone_id=test9_table_4ac4c6f1 prev=None new=SEATED details={'track_id': 1, 'time_seconds': 1.0}
  id=24 type=TABLE_STATE_CHANGED entity_id=None role=None zone_id=test9_table_4ac4c6f1 prev=free new=occupied details={'new_state': 'occupied', 'time_seconds': 1.0, 'previous_state': 'free'}
  id=25 type=STAFF_IDLE entity_id=smoke_worker_187c01 role=WORKER zone_id=test9_service_4ac4c6f1 prev=ACTIVE new=IDLE details={'track_id': 2, 'idle_frames': 3, 'time_seconds': 1.3, 'threshold_frames': 3, 'idle_duration_seconds': 1.3}
  id=26 type=CUSTOMER_LEFT entity_id=smoke_customer_c3e927 role=CUSTOMER zone_id=test9_table_4ac4c6f1 prev=SEATED new=LEFT details={'reason': 'zone_change', 'track_id': 1, 'time_seconds': 2.5, 'duration_seconds': 1.5}
  id=27 type=WORKER_ACTIVE entity_id=smoke_worker_187c01 role=WORKER zone_id=test9_table_4ac4c6f1 prev=IDLE new=ACTIVE details={'track_id': 2, 'idle_frames': 3, 'time_seconds': 2.5, 'idle_duration_seconds': 2.5}
  id=28 type=DELAY_ALERT entity_id=None role=None zone_id=test9_table_4ac4c6f1 prev=None new=None details={'time_seconds': 2.5, 'occupied_seconds': 1.5, 'threshold_seconds': 1.0}
-- worker_states (1 rows) --
  entity_id=smoke_worker_187c01 status=WorkerActivityStatus.ACTIVE zone_id=test9_table_4ac4c6f1 last_seen_at=2026-08-01 09:56:14.958126
-- table_states (1 rows) --
  zone_id=test9_table_4ac4c6f1 state=TableStateEnum.OCCUPIED state_started_at=2026-08-01 09:56:14.912325
-- alerts (1 rows) --
  id=3 type=DELAY_ALERT zone_id=test9_table_4ac4c6f1 message='Table test9_table_4ac4c6f1 has been occupied for 2s, exceeding the 1s threshold.'
=== Task 9 end-to-end smoke test: real keys in Redis (db 14) ===
  worker:smoke_worker_187c01:status = 'ACTIVE'
  zone:test9_cam_4ac4c6f1:test9_table_4ac4c6f1:last_seen = '2026-08-01T09:56:14.966378'
  zone:test9_cam_4ac4c6f1:test9_table_4ac4c6f1:count = '1'
  table:test9_table_4ac4c6f1:status = 'OCCUPIED'
PASSED
```

Note `ZONE_TRANSITION`/`ZONE_OCCUPANCY_CHANGE` fired too (both required for
`fired_types` to satisfy the test's assertion) but, per the routing table,
write only Redis keys already shown above (`...last_seen`, `...count`) —
they have no `events_log` row by design, which is itself part of what this
smoke test proves (Redis-only routing genuinely produces no DB row).

## 7. Decisions made unilaterally

1. **`REDIS_HOST` defaults to `"127.0.0.1"`, not the literal string
   `"localhost"`.** Real-environment discovery, not a style choice: on
   this Windows/Memurai setup, `redis.asyncio`'s DNS resolution of
   `"localhost"` returns the IPv6 `::1` candidate first, and Memurai only
   listens on IPv4 — every connection attempt hung for the full
   `socket_connect_timeout` before ever trying the v4 address (confirmed
   by direct reproduction: `redis.asyncio.Redis(host="localhost", ...)`
   timed out; the identical call with `host="127.0.0.1"` returned
   immediately). Using the literal loopback IP sidesteps resolution order
   entirely. Documented inline at
   [config.py](backend/app/core/config.py)'s `REDIS_HOST` field.
2. **`event_timestamp`/`status_started_at`/etc. use the real wall-clock
   time the event was *dispatched*, not a value derived from
   `EngineEvent.time_seconds`.** `time_seconds` is video-relative
   (`frame_index / fps`, per `pipeline_output.py`'s own docstring) and
   cannot be turned into a real calendar datetime; the original
   video-relative value is preserved inside `details["time_seconds"]` for
   anyone who needs it (visible in §6's printed proof).
3. **`events_log.role`** is set to `"CUSTOMER"`/`"WORKER"` (matching
   `WorkerRole`'s string values) based on the *event type*
   (`CUSTOMER_SEATED`/`CUSTOMER_LEFT` → `"CUSTOMER"`;
   `STAFF_IDLE`/`WORKER_ACTIVE` → `"WORKER"`), since `EngineEvent` itself
   carries no `role` field. `None` for the two zone/table-level event
   types (`DELAY_ALERT`, `TABLE_STATE_CHANGED`) that aren't about a single
   person.
4. **`events_log.previous_state`/`new_state`** for `CUSTOMER_SEATED`/
   `CUSTOMER_LEFT`/`STAFF_IDLE`/`WORKER_ACTIVE` are dispatcher-assigned
   semantic labels (`"SEATED"`/`"LEFT"`/`WorkerActivityStatus` values)
   describing the transition each event *represents*, since these 4 event
   types carry no previous/new state strings of their own (unlike
   `TABLE_STATE_CHANGED`, which has real ones from `EventEngine` and uses
   them verbatim, lowercase, unchanged).
5. **`ZONE_TRANSITION` with `zone_id=None` is a safe no-op**, not a
   failure. It fires when a track leaves every known zone (moves to
   nowhere-in-particular); there is nothing to key a
   `zone:{camera_id}:{zone_id}:last_seen` entry on, so the handler logs at
   debug level and returns rather than writing a literal `...:None:...`
   key. Covered by `test_zone_transition_with_no_zone_id_is_a_safe_noop`.
6. **Per-event SAVEPOINT via `begin_nested()`** (§4) — not explicitly
   requested by name in the task, but the only correct way to satisfy
   requirement 5 against a **real** Postgres connection (an in-memory fake
   would never have surfaced the "aborted transaction" cascade this fixes).
7. **`self._db.expire_all()` after each Core-level upsert** (§3.2) — found
   by testing, not anticipated in the original design; necessary given
   `AsyncSessionLocal`'s `expire_on_commit=False` configuration.
8. **Installed missing packages into the shared system Python** rather than
   only using `backend/.venv`: `sqlalchemy==2.0.51`, `asyncpg==0.31.0`,
   `pydantic-settings==2.14.2` (versions matched exactly to what
   `backend/.venv` already had pinned) plus `pytest-asyncio` (new
   dependency, none of this task's other packages needed it) — because
   `src/events/event_dispatcher.py` and its tests need both the `src.*`/
   `torch`/`faiss` ecosystem (system Python) and `app.*`/SQLAlchemy/asyncpg
   (previously only in `backend/.venv`) importable in the same process.
9. **`pytest.ini`**: added `asyncio_mode = auto` plus
   `asyncio_default_fixture_loop_scope = session` and
   `asyncio_default_test_loop_scope = session`. The session-scope setting
   is load-bearing, not a default left in place: `backend/app/core/database.py`'s
   `engine` (and `backend/app/core/redis.py`'s `redis_client`) are
   process-wide singletons whose underlying asyncpg/redis connections bind
   to whichever asyncio event loop first uses them. pytest-asyncio's
   *default* per-test event loop would hand the second test a connection
   still bound to the first test's already-closed loop
   (`RuntimeError: Event loop is closed` / `asyncpg...InterfaceError:
   cannot perform operation: another operation is in progress` — both
   actually hit and diagnosed during this task, see the fix history in
   `tests/test_event_dispatcher.py`'s `_postgres_reachable()` docstring).
   One session-wide loop keeps every test on the loop those singletons
   were actually opened on. This only matters when tests share
   process-wide async singletons — it does not affect any of the existing
   76 (sync) tests.

## 8. Files touched

- `backend/app/core/redis.py` — new Redis client wrapper (§2).
- `backend/app/core/config.py` — `REDIS_HOST`/`REDIS_PORT`/`REDIS_DB` added
  to `Settings`.
- `.env.example` — documents the 3 new Redis keys.
- `src/events/event_dispatcher.py` — new (§3).
- `tests/test_event_dispatcher.py` — new, 11 tests (§5.1).
- `tests/test_event_dispatcher_smoke_e2e.py` — new, the required real
  end-to-end smoke test (§5.2, §6).
- `pytest.ini` — new (§7.9).
- `docs/TASK9_REPORT.md` — this file.

Nothing in `src/events/event_engine.py`, `src/core/live_pipeline.py`,
FastAPI endpoints, WebSocket, or frontend was touched.
