# Task 4 Report — Unified Data Contract (TrackOutput / FrameOutput) + JSON Export

## The problem

`LivePipeline.process_frame()` returned a raw, loosely-shaped `dict`. No formal contract
existed for what a frame's output must contain, and no serialization path existed to turn it
into exportable JSON. Every future consumer (Event Engine, a future Redis publisher, tests)
had no stable shape to depend on.

## Inspection performed before writing any code

Read `process_frame()`, `_run_kbs()`, `enrich_tracks_with_zones()`, `get_tables_current_state()`,
`_update_person_state()`, `src/ai_models/detector.py`, `src/ai_models/tracker.py`, and
`src/zone_management/zone_manager.py`'s `get_bbox_zone()`/`_zone_result()`/`_unknown_zone()`
directly in the current (post Tasks 1/2/3/5) codebase, plus `docs/ARCHITECTURE.md` and
`docs/EVENT_ENGINE.md` for what the *planned* Event Engine expects to consume from this
snapshot. Confirmed the exact current shapes:
- `tracked_objects[i]` (post-tracker): `track_id: int`, `box: list[float]` (4 floats),
  `conf: float`, `class_id: int`, `class_name: str`.
- Post `enrich_tracks_with_zones`, each track additionally has: `zone: dict` (from
  `ZoneManager.get_bbox_zone()` — `zone_id`, `zone_type`, `zone_name`, `intersection_pct`,
  `box`, `matched: bool`, `method`; unmatched zones use the sentinel `"unknown"`/`"Unknown"`,
  never `None`, and omit `matched` entirely), `zone_type_normalized: str` (the
  `ZONE_TYPE_MAP`-bucketed value: `"table"`/`"walk"`/`"staff"`/`"unknown"`), `zone_name: str`,
  `zone_point: list[int]`.
- Per-track role/identity state lives in `LivePipeline` instance dicts, not on the track dict
  itself: `self._person_roles[track_id]`, `self._global_ids[track_id]`,
  `self._action_labels[track_id]` (key absent, not `"unknown"`, until the pose buffer fills to
  3 frames — a genuine "not yet predicted" state, confirmed live in the smoke test below).
- `get_tables_current_state(camera_id)` (Task 2) returns `dict[zone_id, state]` for that
  camera's configured `"table"`/`"table_area"` zones, defaulting to `"empty"`.
- `docs/EVENT_ENGINE.md`'s Level-1 raw-event table explicitly names `box`, `zone_id`,
  `zone_type`, `global_id`, `role`, `confidence`, and `action` as the fields its planned
  extractor needs from this snapshot — direct confirmation that the task's required floor plus
  `action` (which I added as a bonus field, see below) is exactly what's meaningful downstream.

## Final shape of both dataclasses

`src/core/pipeline_output.py`:

```python
@dataclass
class TrackOutput:
    track_id: int
    global_id: str
    bbox: list[float]
    zone_id: str | None
    zone_type: str | None
    role: str
    confidence: float | None
    action: str | None = None
    zone_name: str | None = None

@dataclass
class FrameOutput:
    camera_id: str
    video_id: str
    frame_index: int
    time_seconds: float
    tracks: list[TrackOutput]
    table_states: dict[str, str]
```

### Field-by-field rationale

**TrackOutput** — the 7 required fields plus 2 bonus fields:
- `track_id`, `global_id`, `bbox`, `role` — direct pass-through of what the pipeline already
  computes per track (`obj["track_id"]`, `self._global_ids.get(...)`, `obj["box"]` cast to
  `float`, `self._person_roles.get(...)`).
- `confidence` — sourced from `obj.get("conf")` (the tracker's forwarded detector confidence,
  per the task's explicit "detector confidence if available" spec — **not** RoleEngine's
  role-confidence score, which is a different, separate signal; see "considered and excluded"
  below).
- `zone_id` / `zone_type` — **deliberately handled differently from each other** (a judgment
  call, documented at [live_pipeline.py:266-289](src/core/live_pipeline.py#L266-L289)):
  `zone_id` becomes `None` when `zone.get("matched")` is falsy, because `"unknown"` there is
  purely a not-found sentinel with no identity value. `zone_type` uses
  `zone_type_normalized` and is **kept as the string `"unknown"`** even when unmatched, because
  it's a real, meaningful category throughout the rest of the pipeline (`ZONE_TYPE_MAP`,
  `RoleEngine`, `TableKBS` all treat `"unknown"` zone_type as a legitimate observation, not an
  absence). The normalized bucket (`table`/`walk`/`staff`/`unknown`) was used rather than the
  raw, more granular `zone.zone_type` (e.g. `"table_area"`, `"service_path"`, `"buffet"`)
  because the normalized value is what every other decision-making component in this codebase
  (RoleEngine's `ObservationFact.zone_type`, `TableKBS`'s anchoring from Task 2) actually keys
  off — it's the canonical categorization, not the raw taxonomy.
- `action` (bonus) — from `self._action_labels.get(track_id)` (no default → genuinely `None`
  when no prediction exists yet, not the `"unknown"` placeholder `draw_tracks()` uses for
  display). Included because `docs/EVENT_ENGINE.md` explicitly names `ActionObserved` as a
  Level-1 raw event sourced from this exact field, and because it's a real, meaningful,
  already-computed per-track signal (confirmed live: `None` for the first two frames of the
  real smoke test while the 3-frame pose buffer fills, then `"sitting"` once a prediction
  exists).
- `zone_name` (bonus) — human-readable zone label (`"Table 3"`, not just an id), useful for
  Event Engine narrative/logging and any future UI; `None` under the same "matched" rule as
  `zone_id`.

**FrameOutput** — the 5 required fields plus `video_id`:
- `camera_id`, `frame_index`, `tracks`, `table_states` — direct requirements.
- `time_seconds` — the exact video-relative value passed into `process_frame()` (Task 1's
  fix), passed straight through to `_build_frame_output()` with **no re-derivation** — verified
  by a dedicated test (see below).
- `video_id` (bonus) — already present in the current raw dict return and dropped nowhere else
  in the codebase; kept since there was no reason to lose it.

### Fields deliberately excluded, with reasons

- **Raw `detections`** (pre-tracking YOLO output): excluded. `tracks` (post-tracker,
  post-enrichment) is the identity-bearing, zone-aware superset of this information; raw
  per-frame boxes with no track identity aren't a stable contract object a downstream Event
  Engine would key state machines off.
- **`person_crops`**: excluded. These are `numpy.ndarray` image crops — not JSON-serializable,
  and a debug/ReID-pipeline-internal artifact rather than a structured fact.
- **RoleEngine's per-decision confidence score**: considered, not included. `docs/EVENT_ENGINE.md`
  lists a `confidence` field under `RoleAssigned` sourced from `RoleEngine.get_decisions()`, but
  that value is a `KnowledgeEngine` sim scoring artifact used *by* the decision loop
  ([live_pipeline.py:643-660](src/core/live_pipeline.py#L643-L660), pre-fix line numbers)
  and is **not retained anywhere in `LivePipeline`'s persistent per-track state** after that
  loop runs — only the resulting `role` string is kept in `self._person_roles`. Surfacing it
  would require adding new persistent state, which is populating the contract from data the
  pipeline doesn't currently retain — out of this task's scope per its own instruction not to
  invent fields the pipeline doesn't produce. The task's `confidence` field is explicitly
  specified as detector confidence, which resolved this ambiguity directly from the task text.

## Files/functions changed

- **New file `src/core/pipeline_output.py`** — `TrackOutput`, `FrameOutput`,
  `frame_output_to_json()` ([pipeline_output.py:21-63](src/core/pipeline_output.py#L21-L63)).
- **`src/core/live_pipeline.py`**:
  - [live_pipeline.py:21](src/core/live_pipeline.py#L21) — import added.
  - [live_pipeline.py:155-172](src/core/live_pipeline.py#L155-L172) — `process_frame()` now
    builds a `FrameOutput` via `_build_frame_output()` and adds it to the returned dict under
    the new key `"frame_output"`.
  - [live_pipeline.py:266-304](src/core/live_pipeline.py#L266-L304) — two new methods:
    `_build_track_output(obj)` and `_build_frame_output(...)`.
- No other file touched.

## Return-type integration decision (point 2)

**Chosen: additive.** `process_frame()`'s return type is unchanged — still the same `dict`
with the same keys as before — with one new key, `"frame_output"`, holding the `FrameOutput`
instance.

**Why**: grepped every call site of `process_frame(` across the repo (excluding docs/generated
output files). There is exactly **one** real caller: `src/run_live.py:182`
(`event = pipeline.process_frame(...)`), which immediately does dict-key access
(`event["tracked_objects"]`, `event["person_crops"]`). `src/run_all_cameras.py` never calls
`process_frame()` directly — it only launches `run_live.py` as a subprocess (Task 5). Replacing
the dict return with a bare `FrameOutput` instance would break `run_live.py`'s existing
`event[...]` indexing immediately (dataclasses don't support `__getitem__` by default), for a
sole caller that doesn't even need the new contract yet. Adding the new contract as an extra
dict key is strictly backward-compatible — `run_live.py` needed zero changes and still works
exactly as before — while making `FrameOutput` fully available to whichever caller wants it
next (Event Engine, a future test, etc.), satisfying the task's explicit fallback instruction
for this exact situation.

## Tests

`tests/test_pipeline_output.py` (4 tests):

**(a)** `test_frame_output_round_trips_through_json_without_data_loss` — constructs a
`FrameOutput` with two `TrackOutput`s (one fully populated, one with `None` fields) using
realistic sample data, serializes via `frame_output_to_json`, decodes via `json.loads`, and
asserts every field matches byte-for-byte, including that `None` values survive as JSON `null`.

**(b)** `test_process_frame_produces_frame_output_reflecting_real_pipeline_state` — calls the
real, modified `process_frame()` end-to-end (real `enrich_tracks_with_zones()`, real
`ZoneManager.get_bbox_zone()` geometry matching, real `RoleEngine`, real `TableKBS`, real
`_build_frame_output()`) on a `LivePipeline` built via `object.__new__()`. Only the ML
perception layer (`detector`, `tracker` — already covered by their own tests) is replaced with
lightweight stubs returning realistic, pre-shaped data; `ZoneManager` itself is real (also
built via `object.__new__()`, bypassing only its disk-reading `__init__`, since
`get_bbox_zone()` depends solely on class-level constants + `self.zones_config`). Asserts the
resulting `FrameOutput.tracks[0]` has a real geometrically-matched `zone_id`/`zone_type`/
`zone_name` (not a hardcoded placeholder) and that `table_states` reflects a real `TableKBS`
run, plus that the raw dict return is unchanged (`event["tables_current_state"] ==
frame_output.table_states`).

**(c)** `test_frame_output_time_seconds_is_video_relative_not_wall_clock` — passes a
`time_seconds` value (`999999.25`) deliberately impossible to confuse with any real wall-clock
`time.time()` value, and asserts `FrameOutput.time_seconds` equals it exactly.
`test_process_frame_raises_on_none_time_seconds_via_update_person_state` additionally confirms
this task didn't reintroduce a bypass around Task 1's `ValueError`-on-`None` guard.

### Test results
```
python -m pytest tests/test_pipeline_output.py -v
```
```
tests/test_pipeline_output.py::test_frame_output_round_trips_through_json_without_data_loss PASSED
tests/test_pipeline_output.py::test_process_frame_produces_frame_output_reflecting_real_pipeline_state PASSED
tests/test_pipeline_output.py::test_frame_output_time_seconds_is_video_relative_not_wall_clock PASSED
tests/test_pipeline_output.py::test_process_frame_raises_on_none_time_seconds_via_update_person_state PASSED
4 passed in 3.92s
```

### Full suite regression check
```
python -m pytest tests/ -v
```
```
40 passed, 1 failed in 6.82s
```
The 1 failure is the same pre-existing, unrelated `tests/test_tracker.py::test_tracker_update`
failure documented in Tasks 1, 2, 3, and 5 (list-vs-dict detection format mismatch, predating
this session). Untouched.

## Real end-to-end smoke test

Ran the actual `LivePipeline` (real YOLO detector, real DeepSort tracker, real `ZoneManager`,
real `RoleEngine`, real `TableKBS` — no stubs) against 5 real frames of `camera_01`'s real
recorded video (`data/raw_videos/camera_01/video_001.mp4`), calling `process_frame()` and
`frame_output_to_json()` exactly as a real caller would, following the verification standard
set in Task 5.

**Result: passed.** Highlights confirming genuinely real (not placeholder) data:
- `time_seconds` correctly derived from `frame_index / real_fps` (real fps = 15.00065),
  matching Task 1's contract — e.g. frame 4 → `0.26666 s`.
- `action` was `None` for frames 0–1 (the 3-frame pose buffer hadn't filled yet) and became the
  real predicted label `"sitting"` from frame 2 onward — direct live confirmation of the
  documented "genuinely not-yet-predicted vs. real value" semantics for that field.
- `zone_id`/`zone_type` reflected a real geometric match (`cam01_service_auto` / `"walk"`) for
  both tracked people in these frames — this video's opening frames show people in a walk zone,
  not seated at a table, so no `"table"` zone_type appeared in this particular 5-frame window;
  that's the real content of the video, not a limitation of the contract.
- `table_states` correctly showed both `cam01_table_1` and `cam01_table_2` as `"empty"` with
  zero customer history — direct re-confirmation, now flowing through the new typed contract,
  of Task 2's zone-anchoring fix.
- Every frame's `FrameOutput` serialized to valid JSON (773–888 chars) and round-tripped
  through `json.loads` correctly.

**Minor observation, not fixed (documented per Task 5's precedent rather than silently
ignored):** a `sklearn.exceptions.InconsistentVersionWarning` fires on `LivePipeline.__init__`
(`models/label_encoder.pkl` was pickled with scikit-learn 1.7.2; the installed version from
Task 5 is 1.9.0). It is non-blocking — the encoder still unpickles and produces correct action
labels (confirmed: `"sitting"` predictions are correct) — so no action was taken; flagged here
for visibility since it's the kind of thing that could silently break on a future sklearn
major-version bump.

## Decisions made unilaterally

1. **Additive dict-key integration** rather than changing `process_frame()`'s return type —
   detailed above, driven directly by there being exactly one real call site.
2. **`zone_id` nulled on no-match, `zone_type` kept as `"unknown"` string on no-match** — an
   intentional asymmetry between an identifier field (where absence should be `None`) and a
   categorical field (where `"unknown"` is a real, meaningful value elsewhere in this codebase).
3. **`zone_type_normalized` used over the raw, more granular zone type** for the `zone_type`
   field — matches what every other decision-making component in the pipeline already keys off.
4. **`action` and `zone_name` added as bonus fields** — directly justified by
   `docs/EVENT_ENGINE.md`'s own stated Level-1 event requirements, not invented.
5. **RoleEngine's per-decision confidence score excluded** — not retained in any persistent
   per-track state today; adding it would mean inventing new state-tracking beyond this task's
   contract-definition scope.
6. **Raw `detections` and `person_crops` excluded from `FrameOutput`** — redundant with
   `tracks`, and not JSON-serializable, respectively.
7. **Test stub for `ZoneManager` uses the real class** (`object.__new__(ZoneManager)` +
   `.zones_config` set directly) rather than a fake, so zone-matching geometry is genuinely
   exercised in test (b), not mocked away.
8. **Test's stub detection bbox sized just under `ReIDGallery.MIN_CROP_WIDTH`** so `_run_kbs()`
   takes its real "crop too small, skip ReID" branch — avoids needing to load the real OSNet
   embedding model in a unit test while still exercising genuine pipeline logic rather than
   mocking that branch away.

## Out of scope (explicitly not touched)
Event Engine, KPI Engine, backend, frontend, any network/Redis publishing code, and the
pre-existing `test_tracker.py` failure.
