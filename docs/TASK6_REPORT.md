# Task 6 — Event Engine (Level 1: Semantic Event Detection)

## 1. Scope recap

Pure logic layer: `EventEngine.process_frame(frame_output: FrameOutput) ->
list[dict]`. Consumes Task 4's `FrameOutput` contract
(`src/core/pipeline_output.py`), reasons about *change between the current
and previous frame* per track/table/zone, and returns semantic events. No
Redis, no `sqlalchemy`, no network/DB code, no changes to
`src/core/live_pipeline.py`, `WorkerKBS`, the Event Dispatcher, backend, or
frontend.

`docs/EVENT_ENGINE.md` (pre-existing in this repo) describes a much larger
future architecture — a three-level (`RawEvent` → semantic state machines →
business events) pipeline backed by Redis/Postgres/`asyncio.Queue`. That
document is explicitly **not** what this task builds: this task's own
instructions specify a single flat set of 7 rules, forbid Redis/DB
dependencies, and use different event names/semantics than that doc's
Level 2 (e.g. this task's `CUSTOMER_SEATED` fires immediately on a
zone-type transition into a table; that doc's `CustomerSeated` requires a
20s continuous dwell). I followed **this task's explicit instructions**,
since they were given directly, are self-contained, and say "exact rules."
`docs/EVENT_ENGINE.md` is aspirational for a later task, not something I
reconciled against.

## 2. `EngineEvent` — final shape

```python
@dataclass
class EngineEvent:
    event_type: str
    camera_id: str
    time_seconds: float
    track_id: int | None = None
    global_id: str | None = None
    zone_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)
```

(`src/events/event_engine.py:34-48`.) `track_id`/`global_id`/`zone_id` are
the common identifying fields most event types use (`None` when not
applicable — `ZONE_OCCUPANCY_CHANGE` and `DELAY_ALERT` are table/zone-level,
not per-track, so they leave `track_id`/`global_id` as `None`).
Event-type-specific data (durations, counts, thresholds) lives in
`details`. `engine_event_to_dict()` (line 51) is a thin
`dataclasses.asdict()` wrapper; `EventEngine.process_frame()` (line 128)
returns `[engine_event_to_dict(e) for e in events]` — a plain
`list[dict]`, matching the required public signature exactly.

## 3. Internal state

- `self._track_states: dict[str, dict]` — keyed `f"{camera_id}:{track_id}"`,
  never `track_id` alone (line 106-109). Per track:
  `zone_id`/`zone_type`/`role` (last-seen snapshot), `idle_counter`,
  `is_idle`, `seated_since`, `zone_entered_time`,
  `last_zone_transition_time`.
- `self._camera_track_ids_seen: dict[str, set[int]]` (line 111-113) — the
  previous frame's track_id set per camera, diffed against the current
  frame's set to detect tracks that vanished entirely (rule 2's second
  trigger) without rescanning the whole `_track_states` dict every frame.
- `self._zone_occupancy_counts: dict[str, dict[str, int]]` (line 115-117)
  — previous frame's per-zone person count, per camera (rule 7).
- `self._camera_seen_before: set[str]` (line 119-125) — which cameras have
  had at least one frame processed, to bootstrap zone-occupancy counts
  silently on a camera's genuine first frame (see §7.2).
- `self._table_occupancy: dict[str, dict]` (line 118-127) — keyed
  `f"{camera_id}:{zone_id}"`; `{"occupied_since": float|None,
  "delay_alert_fired": bool}`. **This is the documented in-memory
  substitute for rule 5's future Redis-backed value** (see §5).
- On first sighting of a `track_id` (`prev is None`, line 152-154): store
  its state, `continue` immediately — no rule below it in the loop runs, so
  every one of the 7 rules correctly emits nothing on first sighting.

## 4. Rule-by-rule implementation

| Rule | Location | Notes |
|---|---|---|
| 1. `CUSTOMER_SEATED` | `event_engine.py:166-180` | `role=="customer" and zone_changed and zone_type=="table"`. Also opens that table's `occupied_since` clock (only if not already open — see §5). |
| 2. `CUSTOMER_LEFT` | `:181-192` (still-present case), `:253-268` (disappearance case) | Still-present: fires when `seated_since is not None and zone_type != "table"`, duration = `now - seated_since`. Disappearance: diffs `_camera_track_ids_seen` against the current frame's track_id set; for any vanished id that had `seated_since` set, fires with `reason: "track_disappeared"` and the *current* frame's `time_seconds` as the departure instant (no grace/debounce period — the task's wording is "no longer appears... at all," unqualified). The track's state entry is deleted after handling, bounding memory growth. |
| 3. `STAFF_IDLE` | `:194-224` | Per-track `idle_counter` increments on every frame with `role=="worker"` and `zone_changed == False`; fires once via `idle_counter == threshold and not is_idle` (equality, not `>=`, so it can only be true on the exact crossing frame), sets `is_idle = True` so it can't refire until a zone change resets it. |
| 4. `WORKER_ACTIVE` | `:196-208` | On a zone change for a track with `is_idle == True`: fires with `idle_frames` and `idle_duration_seconds` (`now - zone_entered_time`), then resets `is_idle = False`, `idle_counter = 0`, `zone_entered_time = now`. |
| 5. `DELAY_ALERT` | `:176-180` (open), `:227-234` (service reset), `:294-317` (check) | See §5. |
| 6. `ZONE_TRANSITION` | `:237-246` | Fires on any `zone_changed`, gated by `last_zone_transition_time`: suppressed if `< 2.0s` (configurable) since the *last emitted* `ZONE_TRANSITION` for that track — not since the last raw zone change. Zone bookkeeping (`prev["zone_id"] = ...`) still updates every frame regardless of suppression, so `from_zone_id` on the next emitted transition is always the true previous zone, not a stale one. |
| 7. `ZONE_OCCUPANCY_CHANGE` | `:270-292` | Per-zone counts recomputed from scratch each frame (only tracks with non-`None` `zone_id`); diffed against the previous frame's counts per camera; one event per changed zone with `old_count`/`new_count`. No debounce — the task specifies none for this rule (contrast with rule 6, which explicitly asks for one). |

## 5. `DELAY_ALERT` — design and the in-memory Redis substitute

Rule 5 explicitly ties `occupied_since` to `CUSTOMER_SEATED`: *"stored
'occupied since' timestamp (set when CUSTOMER_SEATED fired)."* Implemented
literally:

- **Open**: when `CUSTOMER_SEATED` fires for `zone_id`, `self._table_occupancy["{camera}:{zone_id}"]["occupied_since"]`
  is set to `now` **only if it isn't already set** — a second customer
  joining an already-occupied table doesn't push the clock forward
  (`event_engine.py:176-180`).
- **Service-event reset** (the literal "without an intervening service
  event" clause): a `role=="worker"` track with `action=="serving"` at
  that same `zone_id` resets `occupied_since = now` and
  `delay_alert_fired = False` (`:227-234`). `action=="serving"` is a real,
  directly-observable `TrackOutput` field (confirmed against
  `models/label_encoder.pkl`'s classes: `['serving', 'sitting', 'standing',
  'walking']`) — not a recomputation of `TableKBS`'s own served-flag logic,
  just consuming an already-computed per-track fact.
- **Vacancy reset**: consumes `FrameOutput.table_states[zone_id] ==
  "free"` directly (`:294-303`) — this is the task's explicitly-named
  "consume `TableKBS`'s already-computed output" field, used here as the
  authoritative "is this table actually empty" signal, rather than the
  Event Engine re-deriving vacancy itself from customer-departure
  bookkeeping.
- **Fire-once-per-crossing check**: `:305-317`, same pattern as
  `STAFF_IDLE`.

`self._table_occupancy` **is** the in-memory substitute called for by the
task — commented as such at its declaration (`event_engine.py:118-127`).
In the eventual multi-process architecture this timestamp would need to
live in Redis (exactly like Task 8's `CentralIdentityStore`, or
`docs/EVENT_ENGINE.md`'s `TableStateMachine`) so every camera process
observing the same table agrees on one clock; for this task's single-process,
Redis-free scope, a plain dict is the documented, honest substitute.

**Known consequence of the literal design** (documented, not a bug): if a
table is genuinely occupied per `table_states` but no track at that zone
was ever classified `role=="customer"` (e.g. RoleEngine hasn't confirmed a
role yet), `occupied_since` is never opened and `DELAY_ALERT` correctly
never fires for that occupancy — covered by
`test_delay_alert_does_not_fire_without_any_customer_seated_event`.

## 6. Config values used vs. defaulted

`config/config.json` has no `"events"` section (confirmed by reading the
full file). All three thresholds therefore use their documented class
defaults, read via `config.get("events", {}).get(<key>, <default>)` so a
future `config.json` addition is picked up automatically without a code
change:

| Threshold | Key (if added later) | Default used |
|---|---|---|
| `STAFF_IDLE` frame count | `events.staff_idle_threshold_frames` | `300` frames |
| `DELAY_ALERT` seconds | `events.delay_alert_threshold_seconds` | `900.0` seconds |
| `ZONE_TRANSITION` downsample interval | `events.zone_transition_min_interval_seconds` | `2.0` seconds |

(The task only explicitly ties `STAFF_IDLE`/`DELAY_ALERT` to config; I
extended the same pattern to the `ZONE_TRANSITION` interval too, for
consistency and testability, rather than hardcoding it as a true constant.)

## 7. Decisions made unilaterally (ambiguity in the task)

1. **Table/zone state keys use `f"{camera_id}:{zone_id}"`**, not bare
   `zone_id`. The task only *requires* this for the per-track dict, but
   zone_ids observed elsewhere in this codebase already look
   camera-prefixed (e.g. `"camera_01_table_3"` in
   `tests/test_pipeline_output.py`) — prefixing again is redundant but
   harmless, and applying the same "never trust a bare id across cameras"
   principle uniformly is more defensive than assuming that naming
   convention holds everywhere.
2. **`ZONE_OCCUPANCY_CHANGE` bootstraps silently on a camera's true first
   frame** (`self._camera_seen_before`, §3): the task states this exception
   explicitly only for the per-track "first sighting" case, but a
   phantom-0-to-N comparison on a camera's very first frame is the same
   kind of non-event, so I applied the identical exception here. Covered by
   `test_zone_occupancy_change_silent_on_first_frame_then_fires_on_real_change`.
3. **`DELAY_ALERT`'s "intervening service event"** is implemented as
   `role=="worker" and action=="serving"` at the table's zone_id — the
   most direct, already-computed `FrameOutput` signal available; not a
   recomputation of `TableKBS`'s own serving-detection heuristic (which
   additionally requires sustained frame counts and `zone_specificity`, a
   field this task's `TrackOutput` doesn't carry).
4. **No cross-table move fires `CUSTOMER_LEFT`**: a customer whose
   `zone_id` changes directly from table A to table B in one frame fires
   `CUSTOMER_SEATED` for B (new zone, `zone_type=="table"`) but not
   `CUSTOMER_LEFT` for A, because rule 2's literal trigger
   ("current zone_id is no longer *a* table zone") is false — the new zone
   is still a table. `seated_since` is simply overwritten to restart the
   clock at B. A direct consequence of implementing both rules literally
   and independently, not a bug; flagged here rather than silently
   "fixed" with unrequested extra logic.
5. **`WORKER_ACTIVE`/`STAFF_IDLE` idle duration reported in both frames and
   seconds** (`idle_frames` and `idle_duration_seconds` in `details`) since
   rule 3's counter is explicitly frame-based but rule 4 just says "include
   the idle duration" without specifying units — reporting both avoids
   guessing which one a downstream consumer wants.
6. **Vanished tracks' state is deleted after handling** (not just marked
   closed) — track_ids are not expected to be reused by DeepSort within a
   camera's process lifetime, so this bounds `_track_states`' memory growth
   without needing a TTL/purge mechanism (paralleling a note in Task 8's
   report about the same general class of concern).

## 8. Tests (`tests/test_event_engine.py`)

23 tests, all passing, covering every rule's trigger and non-trigger paths
plus the cross-cutting requirements:

```
python -m pytest tests/test_event_engine.py -v
======= 23 passed in 0.08s =======
```

Highlights: `test_first_sighting_generates_no_event`,
`test_multi_camera_same_numeric_track_id_is_independent_first_sighting`
(proves camera-id-scoped keying), `test_staff_idle_fires_exactly_once_at_threshold`
(asserts silence before, exactly-one at, and silence after the threshold
frame), `test_delay_alert_resets_on_serving_action_then_can_refire`,
`test_zone_transition_fires_and_is_downsampled_within_interval` (asserts
suppression *and* that `from_zone_id` still reflects the true latest zone
after a suppressed frame).

## 9. Regression suite

```
Before (baseline, before any Task 6 change): 11 failed, 37 passed
After  (with Task 6's new module + 23 tests): 11 failed, 60 passed
```

The same 11 pre-existing failures as documented in `docs/TASK8_REPORT.md`
§5 appear identically before and after — unrelated to this task (stale
tests referencing methods that don't exist on the current
`live_pipeline.py`, plus one `TypeError` in `src/ai_models/tracker.py`).
No regressions; delta is exactly +23 passing.

## 10. Smoke test — real pipeline inference, externally mapped into `FrameOutput`

`LivePipeline.process_frame()` does **not** currently construct or return a
`FrameOutput` — `pipeline_output.py`'s `TrackOutput`/`FrameOutput` exist as
a contract but aren't wired into `live_pipeline.py` yet (this is exactly
why `tests/test_pipeline_output.py`'s two integration tests are among the
11 pre-existing failures). Wiring that up is explicitly out of this task's
scope (`live_pipeline.py` must not be touched at all).

So per the task's own fallback instruction, I did the following instead:
ran the real, **unmodified** `LivePipeline` (real YOLO-pose detector, real
DeepSort tracker, real OSNet Re-ID, real RoleEngine/TableKBS) against 450
real frames (~30s at 15fps) of `data/raw_videos/camera_01/video_001.mp4`,
and in a separate, external script (not a change to `live_pipeline.py`)
mapped each frame's real `process_frame()` return dict plus the pipeline's
own already-computed `_person_roles`/`_global_ids`/`_action_labels`/
`get_tables_current_state()` into real `TrackOutput`/`FrameOutput` objects
— the exact same field mapping `tests/test_pipeline_output.py`'s existing
stub-pipeline test already establishes as the intended contract. This
sequence of genuine `FrameOutput`s was fed straight into `EventEngine`.

**Result: 116 real events.**

```
By type: {'ZONE_OCCUPANCY_CHANGE': 115, 'STAFF_IDLE': 1}
```

- One genuine `STAFF_IDLE`, for a real confirmed worker
  (`global_id=worker_09985e1e`) at zone `cam01_service_auto`:
  `{"idle_frames": 300, "idle_duration_seconds": 19.999, "threshold_frames": 300}`
  — fired on the exact frame the real idle counter reached the real
  default threshold (300), not before.
- 115 `ZONE_OCCUPANCY_CHANGE` events, almost all at zone
  `cam01_service_auto`, with counts flapping rapidly (0↔1↔2↔3) frame to
  frame. This reflects genuine DeepSort tracker/zone-matching noise in the
  real video (track ids appearing/disappearing across a service-path zone
  near the camera) — **honestly reported, not filtered**: rule 7 has no
  debounce in the task's specification (unlike rule 6, which explicitly
  gets one), so this bursty-but-correct output is a faithful, literal
  implementation, not a defect. Worth flagging as a candidate for a
  debounce in a future task if this output is too noisy for a real
  consumer — not added here since it wasn't asked for.

**What did not fire in this window, and why (honestly, not swept under
the rug)**: `CUSTOMER_SEATED`/`CUSTOMER_LEFT`/`WORKER_ACTIVE`/
`ZONE_TRANSITION`/`DELAY_ALERT` did not fire in these particular 450
frames. No track in this specific camera/time window was ever classified
`role=="customer"` while transitioning into a table zone (so neither
`CUSTOMER_SEATED`, `CUSTOMER_LEFT`, nor `DELAY_ALERT`, which depends on
`CUSTOMER_SEATED`, had anything to react to); the one `STAFF_IDLE` streak
completed near the end of the 30s window with no further zone change
observed before the window ended, so its `WORKER_ACTIVE` close never
occurred within the tested range; and zero `ZONE_TRANSITION`s despite the
occupancy flapping suggests that flapping is driven by track ids
appearing/disappearing (churn) rather than any single persistent track's
own `zone_id` value oscillating — `ZONE_TRANSITION` only fires for a track
present across two consecutive frames whose zone actually changed, so
track churn alone doesn't trigger it. This is a genuinely different,
narrower real-data outcome than the synthetic tests (which deliberately
construct sequences to hit every rule) — reported as-is rather than
extending the smoke run further to force every rule to fire, since a
longer run past this point starts becoming its own separate
exercise rather than a "short sequence" smoke test.

## 11. Files added

- `src/events/__init__.py` — new, empty (package marker).
- `src/events/event_engine.py` — new, `EngineEvent` + `EventEngine`.
- `tests/test_event_engine.py` — new, 23 tests.
- `docs/TASK6_REPORT.md` — this file.

Nothing else was modified. `src/core/live_pipeline.py`, `WorkerKBS`, the
Event Dispatcher, backend, and frontend were not touched.

## 12. Addendum — Rule 8: `TABLE_STATE_CHANGED`

### 12.1 The gap

`FrameOutput.table_states` was only consumed indirectly, as a side input
to `DELAY_ALERT`'s vacancy check (§5). No rule compared the current
frame's `table_states` to the previous frame's independent of any tracked
person, so a `TableKBS`-computed transition like `"occupied" -> "dirty"`
(customers already gone, no single track's movement to hang an event off
of) produced nothing, even though `TableKBS` had already computed it
correctly. This addendum adds an 8th rule, `TABLE_STATE_CHANGED`, to close
that gap — same architecture as the other 7 (persisted previous-frame
snapshot, diff, emit only on an actual change, no event on first
sighting), and still zero Redis/DB dependency, `live_pipeline.py`
untouched.

### 12.2 Implementation

- New state dict, `self._table_states_prev: dict[str, str]`, keyed
  `f"{camera_id}:{zone_id}"` (same camera-scoping convention as every
  other rule in this engine) — declared at
  `src/events/event_engine.py:126-132`, deliberately separate from
  `self._table_occupancy` (rule 5): rule 8 is a direct `table_states` diff,
  independent of rule 5's `CUSTOMER_SEATED`-driven occupancy clock, so the
  two must not share bookkeeping.
- Logic block at `src/events/event_engine.py:302-330`, placed right after
  rule 7 (`ZONE_OCCUPANCY_CHANGE`) and before rule 5's remaining
  `table_states` loop — iterates `frame_output.table_states.items()`
  directly:
  - No prior stored value for that `f"{camera_id}:{zone_id}"` key → store
    the current state, emit nothing (first-sighting rule, `:312-316`).
  - Prior value exists and differs from the current state → emit
    `TABLE_STATE_CHANGED` with `zone_id` set, `track_id`/`global_id` left
    `None` (table-level, not per-track — same convention as
    `ZONE_OCCUPANCY_CHANGE`/`DELAY_ALERT`), and
    `details={"previous_state": ..., "new_state": ..., "time_seconds": ...}`
    (`:318-327`).
  - The stored value is updated to the current state every time this zone
    is seen, whether or not an event fired (`:330`).
- Does not read or duplicate `TableKBS`'s internal logic — only compares
  the already-computed state string `FrameOutput.table_states` already
  carries, exactly as `DELAY_ALERT`'s existing vacancy check already does.
- Module docstring (`event_engine.py:14-17`) updated from "7 event rules"
  to "8", listing `TABLE_STATE_CHANGED`.

### 12.3 Decision made unilaterally

The task's example `details` shape (`{"previous_state": ..., "new_state":
..., "time_seconds": ...}`) duplicates `time_seconds` inside `details`
even though it's already a top-level `EngineEvent` field. Implemented
exactly as specified rather than "cleaning it up" by dropping the
duplicate — the task's wording was explicit about this shape, and a
downstream consumer reading only `details` (e.g. a payload logged/forwarded
without the outer envelope) would otherwise lose it.

### 12.4 Tests

5 new tests added to the existing `tests/test_event_engine.py` (not a new
file, per instructions):

- `test_table_state_changed_first_sighting_emits_nothing`
- `test_table_state_changed_fires_with_correct_previous_and_new_state`
  (asserts both an initial `free -> occupied` transition and a follow-up
  real `occupied -> dirty` transition, each with correct
  `previous_state`/`new_state`)
- `test_table_state_changed_does_not_fire_when_state_unchanged`
- `test_table_state_changed_fires_independent_of_any_tracked_person`
  (zero tracks in either frame — proves the event is derived purely from
  `table_states`, not from any tracked person's movement)
- `test_table_state_changed_is_scoped_per_camera` (two cameras' same-named
  zone_id `"t1"` are independent first sightings — proves the
  `f"{camera_id}:{zone_id}"` keying convention)

```
python -m pytest tests/test_event_engine.py -v
======= 28 passed in 0.24s =======
```

(23 previously-existing + 5 new, all passing.)

### 12.5 Regression suite (post-addendum)

```
Before addendum (== Task 6's "after" baseline, §9): 11 failed, 60 passed
After addendum:                                      11 failed, 65 passed
```

Same 11 pre-existing failures, unchanged. Delta is exactly +5 passing (the
new rule-8 tests). No regressions.

### 12.6 Files touched by this addendum

- `src/events/event_engine.py` — added `self._table_states_prev` (init)
  and the `TABLE_STATE_CHANGED` rule block; updated module docstring's
  rule count/list.
- `tests/test_event_engine.py` — added the 5 tests in §12.4.
- `docs/TASK6_REPORT.md` — this section, appended; no existing section
  rewritten or removed.

### 12.7 Renaming note (acknowledged, not actioned in this session)

Per this addendum's instructions, the work previously labeled "Task 8"
(`docs/TASK8_REPORT.md`, cross-process identity sync via
`central_identity_store.py`) should be referred to as **Task 7** in all
future communication and new report files, reflecting actual execution
order (this Event Engine work ran before the identity-sync work).
`docs/TASK8_REPORT.md` itself was **not** renamed or moved in this
session, as instructed — that rename is a separate, simple file operation
to be handled explicitly if/when requested.
