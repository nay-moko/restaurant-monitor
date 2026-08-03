# Task 10 — Customer Sessions Tracking + Worker Idle Alert Generation

## 1. Scope recap

Extend `EventDispatcher` (`src/events/event_dispatcher.py`, Task 9) with
two missing pieces of routing logic, using event types `EventEngine`
already produces — no new event types, and `src/events/event_engine.py`,
`src/core/live_pipeline.py`, FastAPI endpoints, WebSocket, and frontend
were **not** touched:

1. `CUSTOMER_SEATED`/`CUSTOMER_LEFT` now also open/close a `customer_sessions`
   row.
2. `STAFF_IDLE` now also raises a `WORKER_IDLE_TOO_LONG` alert once idle
   duration exceeds the admin-configurable `system_settings.worker_idle_limit`.

## 2. Models inspected before writing any code

- [`backend/app/models/customer_session.py`](backend/app/models/customer_session.py) —
  `CustomerSession` (`__tablename__ = "customer_sessions"`):
  `entity_id` (str), `table_zone_id` (str, FK `zones.id`), `camera_id`
  (str, FK `cameras.id`), `started_at` (DateTime, not null),
  `last_seen_at` (DateTime, not null), `left_at` (DateTime, nullable),
  `total_stay_sec` (Integer, nullable), `status`
  (`CustomerSessionStatus.ACTIVE`/`COMPLETED`, default `ACTIVE`).
  No column named `duration` — it's `total_stay_sec`, confirmed at
  [customer_session.py:25](backend/app/models/customer_session.py#L25).
- [`backend/app/models/setting.py`](backend/app/models/setting.py) —
  `SystemSetting` (`__tablename__ = "system_settings"`): `id`,
  `worker_idle_limit` (Integer, **column default `60`**,
  [setting.py:11](backend/app/models/setting.py#L11)), `updated_at`.
  Table is effectively a singleton (no `admin_id`/scoping column at all),
  so it's read as "the first row by `id`, if any".
- [`backend/app/models/alert.py`](backend/app/models/alert.py) —
  `Alert.alert_type` is a free-text `String(50)`, not an enum — confirmed
  the literal string `"WORKER_IDLE_TOO_LONG"` requires no schema change.
- [`backend/app/models/__init__.py`](backend/app/models/__init__.py) —
  confirmed `CustomerSession`, `CustomerSessionStatus`, `SystemSetting` are
  already exported from `app.models` (same import surface Task 9's
  `EventDispatcher` already uses for `Alert`/`EventLog`/etc.).

## 3. Customer session open/close logic

### `_handle_customer_seated` ([event_dispatcher.py](src/events/event_dispatcher.py))
In addition to the pre-existing `events_log` insert, inserts one
`CustomerSession` row: `entity_id=event["global_id"]`,
`table_zone_id=event["zone_id"]`, `camera_id=event["camera_id"]`,
`started_at=last_seen_at=_utcnow()` (the same real-wall-clock helper Task 9
already established — not `EngineEvent.time_seconds`, which is
video-relative), `status=ACTIVE`.

### `_handle_customer_left`
After the pre-existing `events_log` insert, looks up the matching **open**
session: `SELECT * FROM customer_sessions WHERE entity_id = :gid AND
left_at IS NULL ORDER BY started_at DESC LIMIT 1`. If found: sets
`left_at = last_seen_at = now`, `total_stay_sec = round((now -
started_at).total_seconds())`, `status = COMPLETED`. If not found: logs a
`logger.warning(...)` naming the `entity_id` and returns — no row is
fabricated, and the (already-inserted) `events_log` row for the
`CUSTOMER_LEFT` event still lands, matching Task 9's existing behavior of
never dropping the audit-log write.

### "last seen" field
The model has `last_seen_at`. Per the task's instruction to inspect before
implementing: `CUSTOMER_SEATED`/`CUSTOMER_LEFT` are the *only* two event
types this dispatcher ever routes for a customer entity (no
`CUSTOMER_MOVED`/similar exists in `EventEngine`'s 8 rules), so "every
relevant event while the session is open" is exactly these two — both set
`last_seen_at = now` (at open, and again at close). No intermediate update
path was needed or added.

## 4. Worker idle alert generation

### `_current_worker_idle_limit()` (new private helper)
`SELECT * FROM system_settings ORDER BY id LIMIT 1`. If a row exists,
returns `row.worker_idle_limit`. If none exists, logs a `warning` and
returns `DEFAULT_WORKER_IDLE_LIMIT_SECONDS = 60` — a module-level constant
in `event_dispatcher.py` deliberately set to match `SystemSetting.worker_idle_limit`'s
own column default (§2), so "no row yet" and "a row with the column's
default value" behave identically.

### `_handle_staff_idle`
After the pre-existing `events_log` insert + `worker_states` upsert +
Redis `SET`, reads `details["idle_duration_seconds"]` (confirmed present
by Task 6/9, and visible in the real smoke-test output, §7). If present
and greater than the configured limit, and no alert is already tracked as
active for this worker (§4.1), inserts one `Alert` row: `alert_type=
"WORKER_IDLE_TOO_LONG"`, `entity_id`/`camera_id`/`zone_id` from the event,
`status=ACTIVE`, a human-readable `message`, and `details` carrying both
the observed `idle_duration_seconds` and the `worker_idle_limit` that was
compared against (so the alert is self-explanatory without a join).
Threshold comparison is strict `>` ("exceeds"), not `>=`.

### 4.1 Duplicate-alert prevention — decision and why

**Chosen: an in-memory, dispatcher-instance-scoped `set[str]` of
`entity_id`s with an alert already raised for their current idle episode**
(`self._workers_with_active_idle_alert`, populated in `_handle_staff_idle`,
cleared in `_handle_worker_active`), over the alternative of querying for
an existing unresolved `WORKER_IDLE_TOO_LONG` alert before each insert.

Why: it costs one dict lookup instead of an extra `SELECT` round-trip to
Postgres on *every* `STAFF_IDLE` event (which fires repeatedly for a
worker that stays idle, e.g. once per idle-detection cycle upstream), and
it follows the same established in-memory-per-entity-state pattern this
codebase already uses (`CentralIdentityStore`, `EventEngine`'s own
internal dicts — both cited in the task). `WORKER_ACTIVE` is a reliable
"episode ended" signal already routed through this same dispatcher, so
clearing the flag there is correct without needing to inspect `Alert.status`.

Traded off, and accepted: this state does not survive a dispatcher
restart mid-episode, so a restart during an ongoing idle episode could in
theory produce one duplicate alert. This is the same category of
limitation the task already accepts for `CUSTOMER_LEFT`'s "no matching
open session" case, and is documented inline in `EventDispatcher.__init__`.

### Fallback threshold behavior
Documented default: **60 seconds** (`DEFAULT_WORKER_IDLE_LIMIT_SECONDS` in
`event_dispatcher.py`, matching `SystemSetting.worker_idle_limit`'s column
default). A missing `system_settings` row logs a warning and uses this
value rather than raising — proven by
`test_staff_idle_with_no_system_settings_row_falls_back_to_default`.

## 5. Tests — `tests/test_event_dispatcher.py` (extended)

7 new tests added, real Postgres (`restaurant_db`) + real Redis (db 14),
same fixture pattern as Task 9. Two new fixtures:
- `clean_system_settings` — deletes all `system_settings` rows before and
  after each test that uses it, so "no row" vs. "row with a specific
  `worker_idle_limit`" tests are deterministic regardless of what's
  already in the real table.
- `camera_with_zones` teardown extended to also delete
  `customer_sessions` rows by `camera_id` (the model has that FK column).

| Test | Covers |
|---|---|
| `test_customer_seated_creates_customer_session_row` | (a) `CUSTOMER_SEATED` creates a real row, correct `started_at`/`last_seen_at`/`status=ACTIVE`, `left_at`/`total_stay_sec` still `None` |
| `test_customer_left_closes_matching_open_session` | (b) a following `CUSTOMER_LEFT` updates the *same* row (`started_at` unchanged), sets `left_at`, `total_stay_sec >= 0`, `status=COMPLETED` |
| `test_customer_left_with_no_open_session_logs_warning_and_does_not_crash` | (c) no matching open session → `caplog` warning naming the `entity_id`, `dispatch()` still reports success, no session row fabricated, `events_log` row still lands |
| `test_staff_idle_below_limit_creates_no_alert` | (d) idle duration below configured limit → 0 alerts |
| `test_staff_idle_above_limit_creates_exactly_one_worker_idle_alert` | (e) idle duration above configured limit → exactly 1 `WORKER_IDLE_TOO_LONG` alert with correct fields |
| `test_second_staff_idle_for_still_idle_worker_does_not_duplicate_alert` | (f) a second `STAFF_IDLE` for the same still-idle worker → still 1 alert; a `WORKER_ACTIVE` then a third `STAFF_IDLE` crossing the threshold again → a *new*, second alert (episode boundary correctness) |
| `test_staff_idle_with_no_system_settings_row_falls_back_to_default` | (g) empty `system_settings` table → 30s idle (below the 60s default) creates no alert, 70s idle (above it) creates exactly one |

```
python -m pytest tests/test_event_dispatcher.py -v
18 passed in 2.10s
```
(11 pre-existing Task 9 tests + 7 new, all passing, none modified.)

## 6. Regression — full existing suite, honest before/after

```
Before (this task's baseline, = Task 9's final state): 9 failed, 79 passed, 88 total
After  (with Task 10's changes):                       9 failed, 86 passed, 95 total
```

Delta: exactly `+7 passed` (the 7 new tests in `tests/test_event_dispatcher.py`
above), `+0 failed`. The same 9 pre-existing failures remain — byte-identical
set to the ones documented in Task 9's own report (`test_live_pipeline_timing.py`
×3, `test_pipeline_output.py`'s `_update_person_state` test, `test_pose_stride.py`
×1, `test_table_zone_anchoring.py` ×3, `test_tracker.py` ×1) — all unrelated to
this task, all in files this task never touched.

`tests/test_event_dispatcher.py` + `tests/test_event_dispatcher_smoke_e2e.py`
together, isolated:
```
python -m pytest tests/test_event_dispatcher.py tests/test_event_dispatcher_smoke_e2e.py -v
19 passed in 1.08s
```

Post-run verification: a direct query of `customer_sessions` and
`system_settings` after the full suite run shows `0` rows in both — no
Task 10 test data was left behind. (`alerts` shows one pre-existing,
unrelated row — `alert_type="TEST_ALERT"`, `camera_id=None`,
`message="Manual test alert"` — that predates this task and is outside
every fixture's cleanup scope, since Task 9/10 fixtures only ever delete
rows scoped to their own generated `camera_id`.)

## 7. Real end-to-end smoke test — actual proof

`tests/test_event_dispatcher_smoke_e2e.py` extended with a new
`low_worker_idle_limit` fixture (sets `system_settings.worker_idle_limit = 1`
for the duration of the test, cleaned up after — mirrors the existing
pattern of overriding `EventEngine`'s own thresholds via its `config`
argument, just on the dispatcher/Postgres side instead). The existing
5-frame sequence already drives a full `CUSTOMER_SEATED` → `CUSTOMER_LEFT`
cycle for one customer and a `STAFF_IDLE` (`idle_duration_seconds=1.3`) →
`WORKER_ACTIVE` cycle for one worker; with the limit set to `1`, the
`STAFF_IDLE` event now also crosses the configured threshold in the same run.

```
python -m pytest tests/test_event_dispatcher_smoke_e2e.py -v -s
1 passed in 0.85s
```

Actual printed output from the real run:

```
=== Task 9/10 end-to-end smoke test: real rows in restaurant_db ===
-- events_log (6 rows) --
  id=103 type=CUSTOMER_SEATED entity_id=smoke_customer_537df5 role=CUSTOMER zone_id=test9_table_000623b7 prev=None new=SEATED details={'track_id': 1, 'time_seconds': 1.0}
  id=104 type=TABLE_STATE_CHANGED entity_id=None role=None zone_id=test9_table_000623b7 prev=free new=occupied details={'new_state': 'occupied', 'time_seconds': 1.0, 'previous_state': 'free'}
  id=105 type=STAFF_IDLE entity_id=smoke_worker_19ef2f role=WORKER zone_id=test9_service_000623b7 prev=ACTIVE new=IDLE details={'track_id': 2, 'idle_frames': 3, 'time_seconds': 1.3, 'threshold_frames': 3, 'idle_duration_seconds': 1.3}
  id=106 type=CUSTOMER_LEFT entity_id=smoke_customer_537df5 role=CUSTOMER zone_id=test9_table_000623b7 prev=SEATED new=LEFT details={'reason': 'zone_change', 'track_id': 1, 'time_seconds': 2.5, 'duration_seconds': 1.5}
  id=107 type=WORKER_ACTIVE entity_id=smoke_worker_19ef2f role=WORKER zone_id=test9_table_000623b7 prev=IDLE new=ACTIVE details={'track_id': 2, 'idle_frames': 3, 'time_seconds': 2.5, 'idle_duration_seconds': 2.5}
  id=108 type=DELAY_ALERT entity_id=None role=None zone_id=test9_table_000623b7 prev=None new=None details={'time_seconds': 2.5, 'occupied_seconds': 1.5, 'threshold_seconds': 1.0}
-- worker_states (1 rows) --
  entity_id=smoke_worker_19ef2f status=WorkerActivityStatus.ACTIVE zone_id=test9_table_000623b7 last_seen_at=2026-08-02 10:01:36.337612
-- table_states (1 rows) --
  zone_id=test9_table_000623b7 state=TableStateEnum.OCCUPIED state_started_at=2026-08-02 10:01:36.308636
-- alerts (2 rows) --
  id=16 type=WORKER_IDLE_TOO_LONG entity_id=smoke_worker_19ef2f zone_id=test9_service_000623b7 message='Worker smoke_worker_19ef2f has been idle for 1s, exceeding the configured 1s idle limit.'
  id=17 type=DELAY_ALERT entity_id=None zone_id=test9_table_000623b7 message='Table test9_table_000623b7 has been occupied for 2s, exceeding the 1s threshold.'
-- customer_sessions (1 rows) --
  entity_id=smoke_customer_537df5 table_zone_id=test9_table_000623b7 started_at=2026-08-02 10:01:36.297463 last_seen_at=2026-08-02 10:01:36.334768 left_at=2026-08-02 10:01:36.334768 total_stay_sec=0 status=CustomerSessionStatus.COMPLETED
=== Task 9/10 end-to-end smoke test: real keys in Redis (db 14) ===
  worker:smoke_worker_19ef2f:status = 'ACTIVE'
  zone:test9_cam_000623b7:test9_table_000623b7:last_seen = '2026-08-02T10:01:36.340143'
  zone:test9_cam_000623b7:test9_table_000623b7:count = '1'
  table:test9_table_000623b7:status = 'OCCUPIED'
PASSED
```

Note `total_stay_sec=0`: the synthetic frames' `CUSTOMER_SEATED` and
`CUSTOMER_LEFT` are dispatched microseconds apart in a test (real wall-clock
time elapsed between them is a few milliseconds, `round()`s to `0`) — this
is a property of the synthetic-frame smoke test's speed, not a bug; the
unit test `test_customer_left_closes_matching_open_session` only asserts
`total_stay_sec >= 0` for the same reason, and the *formula* itself
(`round((now - started_at).total_seconds())`) is what's under test, not a
specific nonzero value.

## 8. Decisions made unilaterally (per this task's "don't ask mid-task" instruction)

1. **`customer_sessions` "last seen" update is only ever set by
   `CUSTOMER_SEATED` (open) and `CUSTOMER_LEFT` (close)** — no third event
   type touches a customer entity in this dispatcher's 8-rule routing
   table, so there is no intermediate "still here" signal to update it
   from. Documented in §3.
2. **Duplicate-alert prevention via in-memory per-worker set, not a
   pre-insert `SELECT`** — §4.1, chosen for cost (avoids a DB round-trip on
   every repeated `STAFF_IDLE`) and consistency with this codebase's
   existing in-memory-per-entity-state pattern. Accepted limitation:
   doesn't survive a dispatcher restart mid-episode.
3. **Fallback `worker_idle_limit` = 60 seconds**, matching
   `SystemSetting.worker_idle_limit`'s own column default exactly, so "no
   row" and "a row explicitly set to the default" are indistinguishable in
   behavior.
4. **Threshold comparison is strict `>` ("exceeds"), not `>=`.**
5. **`total_stay_sec` computed via `round((now - started_at).total_seconds())`**
   using the real wall-clock time the events were *dispatched* (the same
   `_utcnow()` pattern Task 9 already established for `event_timestamp`/
   `status_started_at`), not `EngineEvent.time_seconds` (video-relative,
   per Task 9's own §7.2 decision — reused here rather than re-litigated).
6. **`CustomerSession.table_zone_id`/`camera_id` are taken directly from
   the `CUSTOMER_SEATED` event's `zone_id`/`camera_id`** (both are
   non-nullable FK columns on the model) — if `EventEngine` ever emitted a
   `CUSTOMER_SEATED` with a `None` `zone_id`, the resulting `IntegrityError`
   surfaces as a normal per-event `dispatch()` failure (Task 9's SAVEPOINT
   isolation already handles this), not a special case added here.

## 9. Files touched

- `src/events/event_dispatcher.py` — `_handle_customer_seated`,
  `_handle_customer_left`, `_handle_staff_idle`, `_handle_worker_active`
  extended; new `_find_open_customer_session`, `_current_worker_idle_limit`
  helpers; new `DEFAULT_WORKER_IDLE_LIMIT_SECONDS` constant; new
  `self._workers_with_active_idle_alert` instance state; `CustomerSession`,
  `CustomerSessionStatus`, `SystemSetting`, `select` added to imports.
  Module docstring updated to describe the Task 10 additions.
- `tests/test_event_dispatcher.py` — `CustomerSession`,
  `CustomerSessionStatus`, `SystemSetting` added to imports; new
  `clean_system_settings` fixture; `camera_with_zones` teardown extended
  to clean up `customer_sessions`; 7 new tests (§5).
- `tests/test_event_dispatcher_smoke_e2e.py` — `CustomerSession`,
  `SystemSetting`, `delete` added to imports; new `low_worker_idle_limit`
  fixture; existing test extended to query/print/assert on
  `customer_sessions` and the new `WORKER_IDLE_TOO_LONG` alert (§7).
- `docs/TASK10_REPORT.md` — this file.

Nothing in `src/events/event_engine.py`, `src/core/live_pipeline.py`,
FastAPI endpoints, WebSocket, or frontend was touched. The separate,
still-open `ZONE_TRANSITION`/`WORKER_ENTERED_ZONE`/etc. history-persistence
gap noted in this task's brief was left untouched, as instructed.
