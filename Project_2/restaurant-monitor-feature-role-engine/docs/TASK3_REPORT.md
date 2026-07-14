# Task 3 Report — Wire config.json's process_fps to actual pose_stride

## The bug

`config/config.json` declares `pipeline.process_fps: 2`, but nothing in the codebase read it.
`src/run_live.py`'s `main()` hardcoded `pose_stride = 1`, so pose/action inference ran on
every single frame regardless of the video's native FPS or the configured processing rate —
the config value had zero effect on runtime behavior.

## Files/functions changed — `src/run_live.py`

- **[run_live.py:39-52](src/run_live.py#L39-L52)** — new function `resolve_process_fps(config: dict) -> float`.
  Reads `config["pipeline"]["process_fps"]` from the same config dict `LivePipeline.__init__`
  already loads and exposes as `pipeline.config` ([live_pipeline.py:61](src/core/live_pipeline.py#L61))
  — no new config-loading path was added. Raises `ValueError` naming the exact key
  (`'pipeline.process_fps'`) and the offending value if it is missing, non-numeric (including
  explicitly rejecting `bool`, since `isinstance(True, int)` is `True` in Python and a JSON
  `true`/`false` is not a valid FPS), zero, or negative.
- **[run_live.py:55-72](src/run_live.py#L55-L72)** — new function
  `compute_pose_stride(actual_fps: float | None, process_fps: float) -> int`. Implements
  `max(1, round(actual_fps / process_fps))` when `actual_fps` is a positive number. Falls back
  to `1` with a printed `[WARNING]` line when `actual_fps` is falsy/non-positive — reusing the
  exact same truthiness/positivity check (`actual_fps and actual_fps > 0`) already used at
  [run_live.py:161](src/run_live.py#L161) for the `--start-sec` frame-seeking fallback, per the
  task's instruction to match that existing fallback condition.
- **[run_live.py:141-142](src/run_live.py#L141-L142)** — `main()` now calls
  `process_fps = resolve_process_fps(pipeline.config)` immediately after constructing
  `pipeline`, so a bad config value fails at startup before any video I/O happens.
- **[run_live.py:156-159](src/run_live.py#L156-L159)** — the hardcoded `pose_stride = 1` line
  (previously a comment-only justification for always running every frame) is replaced with
  `pose_stride = compute_pose_stride(fps, process_fps)`, using the `fps` already read from
  `capture.get(cv2.CAP_PROP_FPS)` on the line above.
- **Downstream usage unchanged**: [run_live.py:186](src/run_live.py#L186) still passes
  `pose_stride=pose_stride` into `pipeline.process_frame(...)` exactly as before — only how the
  value is computed changed, not how it's consumed.

## Why this is correct

- `process_fps` is read from the one config object the codebase already loads and passes
  around (`pipeline.config`), so there's a single source of truth for the value — consistent
  with how `detector` and `tracker` config sections are already consumed in
  `LivePipeline.__init__` ([live_pipeline.py:64](src/core/live_pipeline.py#L64),
  [live_pipeline.py:75](src/core/live_pipeline.py#L75)).
- Raising `ValueError` on a missing/invalid `process_fps` (rather than silently defaulting to,
  say, `2`) means a typo'd or deleted config key is caught immediately at startup instead of
  quietly reverting to old always-every-frame behavior — exactly the failure mode this task
  exists to close.
- Computing `pose_stride` from the *actual* per-capture FPS (`capture.get(cv2.CAP_PROP_FPS)`)
  rather than a fixed number is what makes the configured `process_fps` target rate hold across
  cameras with different native FPS — `data/metadata/videos/videos_index.json` documents
  cameras at both 15.001 and 7.0 native FPS; a fixed stride would hit ~2 fps of pose inference
  on one and a very different rate on the other. `max(1, round(...))` guarantees the stride
  never drops below 1 frame (can't skip a fraction of a frame) and rounds rather than
  truncates, so the achieved rate is the closest achievable approximation of `process_fps`.
- The FPS-unavailable fallback mirrors the codebase's own existing precedent for the same
  failure mode (`fps` falsy/non-positive) rather than inventing new fallback semantics, and
  prints a `[WARNING]` so a silently-degraded capture source (stride defaults to processing
  every frame) is visible in the run's console output rather than hidden.

## Test

Added `tests/test_pose_stride.py` (13 cases):

**(a) pose_stride computed correctly:**
- `test_pose_stride_when_native_fps_higher_than_process_fps` — 15.001 fps / process_fps=2 → 8.
- `test_pose_stride_when_native_fps_lower_than_process_fps` — 1.0 fps / process_fps=2 → 1
  (floored, since `round(0.5)` is 0 under Python's banker's rounding and `max(1, 0) = 1`).
- `test_pose_stride_matches_videos_index_example_fps` — 7.0 fps / process_fps=2 → 4, using the
  exact native FPS value documented in `videos_index.json`.
- `test_pose_stride_falls_back_visibly_when_fps_unavailable` — `None`, `0`, and `-5` all fall
  back to stride `1` and each prints a `WARNING` (asserted via `capsys`).

**(b) missing/invalid `process_fps` raises a clear error:**
- Parametrized over 7 invalid configs: no `"pipeline"` key at all, `"pipeline": {}` (missing
  key), `0`, `-2`, `"2"` (string), `None`, and `True` (bool) — each asserted to raise
  `ValueError` matching `"process_fps"` in the message.
- `test_resolve_process_fps_accepts_valid_config` — confirms a valid config (`process_fps: 2`)
  returns `2.0` without raising.

**(c) hardcoded stride removed / downstream unchanged:**
- `test_hardcoded_pose_stride_removed_and_still_passed_downstream` — inspects
  `inspect.getsource(main)` and asserts the literal `"pose_stride = 1"` is gone, that
  `compute_pose_stride(` is now called, and that `pose_stride=pose_stride` still appears
  (proving the downstream call to `process_frame()` is untouched).

### Test result
```
python -m pytest tests/test_pose_stride.py -v
```
```
13 passed in 9.03s
```

### Full suite regression check
```
python -m pytest tests/ -v
```
```
31 passed, 1 failed in 9.26s
```
The 1 failure is the same pre-existing, unrelated `tests/test_tracker.py::test_tracker_update`
failure documented in `docs/TASK1_REPORT.md` and `docs/TASK2_REPORT.md` (list-vs-dict detection
format mismatch between the test and `src/ai_models/tracker.py`, predating this session).
Untouched by this change and out of scope here.

## Decisions made unilaterally

1. **Validation and stride computation extracted as module-level functions
   (`resolve_process_fps`, `compute_pose_stride`) rather than left inline in `main()`.** The
   task requires unit tests for both the FPS-config validation and the stride arithmetic;
   `main()` opens a real video capture and constructs a full `LivePipeline`, which is not
   something a fast unit test should have to do. Pulling the two pieces of logic into pure,
   directly-importable functions was the minimal change that makes them independently
   testable without altering `main()`'s control flow or observable behavior.
2. **`bool` explicitly rejected as a valid `process_fps`.** Python's `isinstance(True, int)` is
   `True`, so without an explicit exclusion a config value of `true`/`false` (a plausible typo
   for a numeric field in hand-edited JSON) would silently pass validation and produce a
   nonsensical stride. Excluding `bool` keeps the validation aligned with the task's intent
   ("not a positive number").
3. **Fallback-condition reuse.** The task pointed at "the same fallback condition already
   handled elsewhere in run_live.py for frame_index from --start-sec" — I used that exact
   `actual_fps and actual_fps > 0` check (mirroring [run_live.py:161](src/run_live.py#L161))
   rather than writing new fallback semantics (e.g. treating `NaN` or very small FPS
   differently), keeping the two fallback code paths in this file consistent with each other.
4. **Warning uses `print()`, matching existing style** — consistent with the same decision
   made in Task 2 for the `[TableKBS][WARNING]` log; there is still no `logging` module
   configured anywhere in this codebase, so introducing one here would be out of scope.

## Out of scope (explicitly not touched)
Event Engine, data-contract layer, backend, frontend, and the pre-existing `test_tracker.py`
failure.
