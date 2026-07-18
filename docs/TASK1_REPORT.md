# Task 1 Report — Environment Setup + Video-Relative Timing Fix

## Part A — Environment Setup

### What was done
- Reused the pre-existing `.venv/` at the project root (Python 3.13.7, created via
  `python -m venv .venv`). Confirmed it was empty except for `pip` before installing anything into it.
- Installed every package actually required by `src/`, `storage/`, and `api/` into `.venv`
  (never into the global interpreter), determined by grepping every `import` / `from ... import`
  statement across those directories rather than trusting the old `requirements.txt`.
- Pinned the full resolved environment (direct + transitive) into `requirements.txt` via
  `pip freeze`, so `pip install -r requirements.txt` reproduces a byte-identical environment
  for any teammate.
- Confirmed `.gitignore` already excludes `.venv/` (line 4) — no change needed there.
- Ran an import check covering every major library (`cv2`, `numpy`, `pandas`, `shapely`,
  `torch`, `torchvision`, `ultralytics`, `deep_sort_realtime`, `experta`, `faiss`, `torchreid`,
  `sqlalchemy`, `aiosqlite`, `asyncpg`, `pytest`) — all succeeded.

### Old vs. new `requirements.txt`
The old file listed 5 unpinned packages (`ultralytics`, `opencv-python`, `numpy`, `pandas`,
`deep-sort-realtime`) and was missing everything else the codebase actually imports:
`torch`, `torchvision`, `shapely` (`src/zone_management/zone_manager.py`), `experta`
(`src/kbs/role_engine.py`, `src/kbs/table_kbs.py`), `faiss` + `torchreid`
(`src/kbs/reid_gallery.py`), and the async storage stack `sqlalchemy` + `aiosqlite` + `asyncpg`
(`storage/database.py`). The new `requirements.txt` is a full pinned freeze of the resolved
environment.

### Decisions made unilaterally (flagged per your instructions)

1. **`requirements.txt` is a full `pip freeze`, not just direct dependencies.** You asked for
   pinned versions "so every teammate ... gets the exact same environment" — a full freeze
   (including transitive pins) guarantees that more strongly than pinning only the ~13 direct
   imports and letting pip re-resolve transitives on each install. Trade-off noted: it's a
   longer file and needs periodic regeneration if a direct dependency is bumped.

2. **Three undeclared transitive dependencies had to be added that don't appear in any `import`
   statement in `src/`/`storage/`/`api/`:**
   - `gdown` — `torchreid`'s package `__init__` unconditionally imports it
     (`torchreid/reid/data/datasets/image/university1652.py`), even though nothing in this repo
     uses that code path. Without it, the bare `import torchreid` in
     [reid_gallery.py:25](src/kbs/reid_gallery.py#L25) fails.
   - `tensorboard` — `torchreid`'s training `Engine` class does `from torch.utils.tensorboard
     import SummaryWriter` at import time. Same failure mode as above.
   - `setuptools<81` (pinned to 80.10.2) — `deep-sort-realtime`'s PyTorch embedder does a bare
     `import pkg_resources` at runtime (`update()` → `DeepSort.__init__` →
     `embedder_pytorch.py`). `pip install deep-sort-realtime` alone resolves the latest
     `setuptools` (83.0.0), which dropped `pkg_resources` entirely, so
     `RestaurantTracker()` (used by `src/ai_models/tracker.py` and exercised in
     `tests/test_tracker.py`) crashed at construction until this was pinned down.

   I judged these were in scope: the task said to "add every dependency currently required by
   the existing codebase," and without these three, the codebase does not import at all — that's
   a stronger requirement than "appears in a `import` line."

3. **`faiss-cpu` and `torchreid` on Python 3.13/Windows**: both are somewhat fragile packages
   (faiss historically lacked Windows wheels; torchreid is unmaintained since ~2021). Both
   installed and imported cleanly against Python 3.13.7 here, so no substitution was needed —
   flagging only because this was a real risk I checked rather than assumed.

### Verification
```
python -c "import cv2, numpy, pandas, shapely, torch, torchvision, ultralytics, \
  deep_sort_realtime, experta, faiss, torchreid, sqlalchemy, aiosqlite, asyncpg, pytest"
```
→ `ALL IMPORTS OK` (one benign warning: torchreid falls back to a pure-Python ranking metric
because Cython isn't available — unrelated to this task, not an error).

## Part B — Video-Relative Timing Fix

### Call chain traced
`src/run_live.py` (`main()`) already computes `time_seconds = frame_index / fps` per frame
([run_live.py:142](src/run_live.py#L142)) and was already passing it into
`pipeline.process_frame(..., time_seconds=time_seconds)`
([run_live.py:150](src/run_live.py#L150)). The break in the chain was inside
`src/core/live_pipeline.py`: `process_frame()` accepted `time_seconds` but only put it in the
returned event dict — it never forwarded it to `_run_kbs()`, which never forwarded it to
`_update_person_state()`. That method fell back to `datetime.now()` and an internal
`_internal_frames_count` × hardcoded 2fps assumption instead.

### Files/functions changed — `src/core/live_pipeline.py`
- **[live_pipeline.py:152](src/core/live_pipeline.py#L152)** — `process_frame()` now calls
  `self._run_kbs(tracked_objects, person_crops, time_seconds)` instead of dropping
  `time_seconds` on the floor.
- **[live_pipeline.py:491](src/core/live_pipeline.py#L491)** — `_run_kbs()` signature gained a
  required `time_seconds: float` parameter.
- **[live_pipeline.py:668-673](src/core/live_pipeline.py#L668-L673)** — the call to
  `_update_person_state()` inside `_run_kbs()` now passes `time_seconds=time_seconds`.
- **[live_pipeline.py:309-350](src/core/live_pipeline.py#L309-L350)** — `_update_person_state()`
  rewritten:
  - Signature: `_update_person_state(self, global_id, local_id, zone_type, time_seconds: float)`
    — no default value.
  - Raises `ValueError` immediately if `time_seconds is None`, with a message naming the
    expected source (`frame_index / video_fps`).
  - "Entrance date" is now `str(timedelta(seconds=int(time_seconds)))` — a video-relative
    elapsed-time string — computed on first sighting of a `global_id` and again whenever
    `current_location` changes (zone transition), instead of `datetime.now().strftime(...)`.
  - A new field `_entrance_time_seconds` stores the raw `time_seconds` value at the most recent
    entrance/zone-change; it's the video-time analog of what "Entrance date" used to freeze in
    wall-clock form, and is what "Duration" is diffed against.
  - "Duration" for a person who stayed in the same zone is now
    `str(timedelta(seconds=int(time_seconds - person_record["_entrance_time_seconds"])))` —
    a direct video-time difference — instead of `frames_count / 2.0`.
  - `_internal_frames_count` is fully removed (not left dead): no writes, no reads, no field in
    the stored records.

### Why this is correct
- `time_seconds` is derived once, upstream in `run_live.py`, from the *actual* video FPS
  (`capture.get(cv2.CAP_PROP_FPS)`), not assumed. Every downstream consumer now shares that one
  source of truth instead of re-deriving time from wall-clock reads or a hardcoded rate.
- Duration is now a pure function of two `time_seconds` samples, so it's correct regardless of
  processing speed, frame drops, `pose_stride`, or `--max-frames` limits — none of which
  correspond 1:1 with video time.
- Making `time_seconds` a required, `None`-checked parameter means any future caller that
  forgets to thread it through fails loudly at the call site instead of silently reintroducing
  wall-clock time or a frame-count guess.

### Decision made unilaterally
`_run_kbs()` was the only call site between `process_frame()` and `_update_person_state()`, so
"thread it through the call chain" had one unambiguous path — no alternate routing was
possible or needed. The one real judgment call was the **Duration string format**: the
pre-existing code used `str(timedelta(...))`, which Python renders unpadded for single-digit
hours (e.g. `"0:00:25"`, not `"00:00:25"`). I preserved that exact format (rather than
hand-padding to `"00:00:25"`) to keep the fix minimal and behavior-compatible with whatever
already consumes the `Duration` field, since reformatting it was not requested.

## Test

Added `tests/test_live_pipeline_timing.py` with 3 cases:

1. `test_duration_computed_from_time_seconds_difference` — drives `_update_person_state()`
   through same-zone updates (asserts `Duration` equals the exact `time_seconds` delta, e.g.
   25s apart → `"0:00:25"`) and a zone change (asserts entrance/duration reset to the new
   `time_seconds`).
2. `test_no_datetime_now_used_in_update_person_state` — inspects the live source of
   `_update_person_state` via `inspect.getsource()` and asserts neither `"datetime.now"` nor
   `"_internal_frames_count"` appear.
3. `test_update_person_state_raises_on_none_time_seconds` — asserts `ValueError` when
   `time_seconds=None`.

Tests construct `LivePipeline` via `object.__new__()` rather than the real `__init__()`
(which loads YOLO/pose-LSTM/ReID models) — scoped to the method under test rather than a full
pipeline integration test, since Part A dependency installation, not model loading, was what
this task needed verified end-to-end.

### Result
```
python -m pytest tests/test_live_pipeline_timing.py -v
```
```
tests/test_live_pipeline_timing.py::test_duration_computed_from_time_seconds_difference PASSED
tests/test_live_pipeline_timing.py::test_no_datetime_now_used_in_update_person_state PASSED
tests/test_live_pipeline_timing.py::test_update_person_state_raises_on_none_time_seconds PASSED
3 passed in 6.59s
```

Also ran the full `tests/` suite as a regression check: 15 passed, 1 pre-existing failure
(`tests/test_tracker.py::test_tracker_update`) unrelated to this task — it feeds
`RestaurantTracker.update()` a list-format detection (`[100, 100, 200, 300, 0.9, 0]`) while
`src/ai_models/tracker.py` expects dict-format detections (`det["box"]`), a test/code data-shape
mismatch that predates this session. Left untouched per the explicit scope boundary in this
task (Event Engine / KPI Engine / backend / frontend / unrelated fixes are out of scope).

## Out of scope (explicitly not touched)
Event Engine, KPI Engine, backend, frontend, and the pre-existing `test_tracker.py` failure
described above.
