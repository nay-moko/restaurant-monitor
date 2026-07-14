# Task 5 Report — Automated Multi-Process Camera Orchestration

## The problem

Running the pipeline for multiple cameras meant manually opening one terminal per camera and
running `python src/run_live.py --camera-id camera_01`, `--camera-id camera_02`, etc. This
happened to produce separate OS processes only by accident of the operator's workflow — there
was no code managing discovery, crash isolation, unified logging, or shutdown.

## Design

### New file: `src/run_all_cameras.py`

**Naming**: `run_all_cameras.py`, matching the task's own suggestion. It follows the existing
`run_*.py` entry-point convention set by `src/run_live.py`, and the name immediately
communicates the scope difference — "all cameras" (supervisor) vs. `run_live.py`'s "one
camera, one process" (worker) — without needing a README to explain it.

**Module layout**:
- `load_enabled_cameras(camera_config_path)` ([run_all_cameras.py:51](src/run_all_cameras.py#L51))
  — reads `config/camera_config.json`, returns only `"enabled": true` entries.
- `load_camera_video_source(camera_id, videos_index_path)` ([run_all_cameras.py:68](src/run_all_cameras.py#L68))
  — looks up `(path, video_id)` for a camera in `data/metadata/videos/videos_index.json`;
  returns `None` if the camera has no video record (see "Camera → video source mapping" below).
- `build_camera_command(...)` ([run_all_cameras.py:87](src/run_all_cameras.py#L87)) — pure
  function building the `argv` for one camera's `run_live.py` invocation.
- `CameraProcess` ([run_all_cameras.py:112](src/run_all_cameras.py#L112)) — small container
  holding one camera's `Popen`, its log path, and its open log file handle.
- `CameraOrchestrator` ([run_all_cameras.py:123](src/run_all_cameras.py#L123)) — the
  supervisor. Key methods: `launch_all()`/`launch_camera()` (discovery + launch),
  `poll_once()`/`supervise()` (crash detection loop), `shutdown()` (termination),
  `install_signal_handlers()`/`_handle_signal()` (SIGINT/SIGTERM wiring).
- `main()` ([run_all_cameras.py:333](src/run_all_cameras.py#L333)) — CLI entry point:
  `install_signal_handlers()` → `launch_all()` → `supervise()`.

### Why `subprocess.Popen`, one call per camera

Each `launch_camera()` call does exactly one `subprocess.Popen([python_executable, script_path,
"--camera-id", ..., "--video-id", ..., "--source", ...], ...)` ([run_all_cameras.py:198-200](src/run_all_cameras.py#L198-L200)
after the fix described below). No `multiprocessing`, no worker pool — each camera gets a
genuinely separate OS process with its own interpreter, matching the pre-existing manual
behavior exactly, per the task's explicit requirement.

### Camera → video source mapping (unilateral decision)

`config/camera_config.json` has no video path field — only `type`/`location`/`enabled`/
`description`. The task's illustrative command (`run_live.py --camera_id camera_01`, no
`--source`) would default every camera to `--source 0` (webcam), which is nonsensical for
concurrently supervising 15 processes against pre-recorded video (established in
`docs/TASK1_REPORT.md`: this pipeline processes video, not a live feed). Instead, for each
enabled camera the orchestrator looks up its recorded source in
`data/metadata/videos/videos_index.json` (already the codebase's existing per-camera video
manifest) and passes it explicitly via `--source`.

Checked against the real project data: `camera_config.json` has 15 `enabled: true` cameras,
but `videos_index.json` only has records for 9 of them. For the other 6
(`camera_05/08/09/10/12/14`), `launch_camera()` logs a `[orchestrator][WARNING]` naming the
camera_id and skips launching it — not a crash, not a silent no-op, and not a nonsensical
webcam fallback ([run_all_cameras.py:170-176](src/run_all_cameras.py#L170-L176)). Verified
directly against the real config:
```
camera_05 -> None   camera_08 -> None   camera_09 -> None
camera_10 -> None   camera_12 -> None   camera_14 -> None
camera_01/02/04/06/07/11/13/15/16 -> (real path, real video_id)
```

### Crash isolation

This falls directly out of using independent `Popen` objects: `poll_once()`
([run_all_cameras.py:218](src/run_all_cameras.py#L218)) iterates every tracked camera's *own*
`Popen.poll()` independently — one camera's exit code has no code path that touches any other
camera's `Popen` object. No restart logic exists anywhere in this module (verified by
inspection and by the fact `launch_camera()` is only ever called from `launch_all()`, once,
at startup).

### No restart

Deliberately absent. `poll_once()` marks a camera `exit_logged = True` once and only logs its
exit (camera_id + exit code, `INFO` for code 0 / `ERROR` otherwise); nothing re-invokes
`launch_camera()` for it. This was checked for scope-creep risk and left out exactly as
instructed.

### Unified logging

`launch_camera()` opens `logs/<camera_id>.log` in append mode and passes it directly as
`stdout=log_file, stderr=subprocess.STDOUT` to `Popen` ([run_all_cameras.py:196-201](src/run_all_cameras.py#L196-L201)
post-fix). This was a deliberate simplification over an earlier draft that used a background
reader-thread to prefix every line with `[camera_id]`: direct OS-level redirection gives a
**stronger** attribution guarantee (each camera's fd points at its own file — no possibility of
a thread race writing one camera's line into another's file) with less code and no
thread-lifecycle bugs to get wrong. The task's requirement explicitly allows either
"prefixed or otherwise clearly attributable" — separate files, one per camera_id, satisfy the
"otherwise" clause directly.

### Clean shutdown

`install_signal_handlers()` ([run_all_cameras.py:299](src/run_all_cameras.py#L299)) registers
`SIGINT` (and `SIGTERM`, best-effort — wrapped in `try/except` since it isn't independently
catchable on every platform) to call `_handle_signal()`, which only sets a
`threading.Event` — it does no I/O itself, keeping the handler minimal. `supervise()`
([run_all_cameras.py:255](src/run_all_cameras.py#L255)) polls in a loop and, in its `finally`
block, always calls `shutdown()` ([run_all_cameras.py:273](src/run_all_cameras.py#L273)),
which `terminate()`s every still-running child, waits up to a timeout, escalates to `.kill()`
for stragglers, and closes their log file handles. `install_signal_handlers()` is separated
from `supervise()` specifically so `supervise()` contains zero `signal`-module calls — `main()`
is the only caller of `install_signal_handlers()`, keeping `signal.signal()`'s main-thread-only
restriction from leaking into anything test code needs to drive from a background thread.

## Pre-existing bugs found (not introduced by this task)

Verifying this orchestrator against the *real* `run_live.py` and real cameras (rather than
stopping at the fake-worker unit tests) surfaced two genuine, pre-existing gaps unrelated to
orchestration logic:

1. **`run_live.py`'s own `sys.path` setup is broken for direct script invocation.**
   `sys.path.append(str(Path(__file__).resolve().parents[2]))` at
   [run_live.py:12](src/run_live.py#L12) climbs two directories from `src/run_live.py`,
   landing one level *above* the project root, not at it. Running `python src/run_live.py
   --help` directly from the project root — the exact manual workflow this task describes —
   fails immediately with `ModuleNotFoundError: No module named 'src'`. This is **not** a bug
   in `run_live.py`'s processing logic (which I was told not to touch), so I did not edit that
   file. Instead, since correctly launching a child process is an orchestration responsibility,
   `launch_camera()` now sets `cwd=PROJECT_ROOT` and `PYTHONPATH` (prepended, existing value
   preserved) on the child's environment before spawning it
   ([run_all_cameras.py:186-201](src/run_all_cameras.py#L186-L201)), which makes `import
   src...` resolve regardless of `run_live.py`'s own faulty `sys.path` line. Verified: before
   this fix, a live 2-camera run failed both cameras with `ModuleNotFoundError: No module named
   'src'`; after it, both ran the real pipeline successfully.
2. **`models/label_encoder.pkl` requires `scikit-learn` to unpickle, but nothing imports
   `sklearn` by name anywhere in `src/`.** `LivePipeline.__init__`'s `pickle.load()`
   ([live_pipeline.py:91](src/core/live_pipeline.py#L91)) needs the class the pickle was
   serialized from (`sklearn.preprocessing.LabelEncoder`) importable, even with zero `import
   sklearn` statements in the codebase — Task 1's static-import-grepping approach couldn't have
   caught this. Installed `scikit-learn==1.9.0` (plus its own transitive deps `joblib`,
   `threadpoolctl`, `narwhals`) and added them to `requirements.txt` with an explanatory
   comment, following the same precedent Task 1 set for `gdown`/`tensorboard`/`setuptools`
   (undeclared-but-required dependencies discovered by actually running the code, not just
   reading it).

Both are documented here rather than silently folded into "the fix," since neither is part of
the orchestration layer itself — they were blockers to *verifying* it end-to-end for real.

## How crash isolation was verified (not assumed)

`tests/test_run_all_cameras.py::test_one_crashing_camera_does_not_affect_others`:
- Launches two **real, separate OS subprocesses** via `tests/fixtures/fake_camera_worker.py`
  (a lightweight stand-in for `run_live.py` — same CLI shape, no ML pipeline, so tests run in
  milliseconds instead of minutes and don't need real video files).
- One camera (`camera_crash`) is configured via the `FAKE_CAMERA_CRASH_IDS` environment
  variable to raise an unhandled `RuntimeError` and exit non-zero after 0.3s; the other
  (`camera_survivor`) runs for 5s.
- The test polls until `camera_crash`'s `Popen.poll()` actually returns non-zero (confirmed via
  the OS, not assumed), then — the critical assertion — checks `camera_survivor`'s
  `Popen.poll()` **is still `None`** (still genuinely running), proving the crash had no effect.
- Also verified live against the real pipeline: launching two real cameras and letting them run
  to natural completion produced independent `exit_code=0` log lines for each, with no
  cross-effect.

## How logging separation works

`tests/test_run_all_cameras.py::test_each_camera_output_goes_to_its_own_log_file` launches two
cameras, lets both finish, then reads both `logs/<camera_id>.log` files directly and asserts
`camera_a`'s log contains `camera_id=camera_a` but *not* `camera_id=camera_b`, and vice versa.
Also verified live: a real 2-camera run produced `camera_01.log` (263 lines) and `camera_02.log`
(692 lines) each containing that camera's own `Frame N/20 done` / `LIVE DATABASE STATE` output
exclusively.

## How clean shutdown was implemented and verified

Three layers of verification, because the most "obvious" way to test this — send a real OS
signal from outside the process — turned out to be unreliable in this sandboxed Windows
environment (documented honestly below rather than glossed over):

1. **Automated test** (`test_signal_triggers_termination_of_all_children_no_orphans`): launches
   two real long-running (30s) subprocesses, runs `supervise()` in a background thread (safe,
   since `supervise()` itself makes no `signal` calls), then invokes `_handle_signal(signal.SIGINT,
   None)` directly — the exact `(signum, frame)` calling convention the interpreter itself uses
   when it delivers a real signal to a registered handler. Asserts the `supervise()` thread
   returns and that **every** tracked `Popen.poll()` is non-`None` afterward (genuine OS-level
   confirmation, not an in-memory flag).
2. **Dedicated orphan-tree check** (ad hoc, described in the session, not committed as a test):
   this Python 3.13 Windows venv's `.venv/Scripts/python.exe` turned out to be a small (255KB)
   launcher stub that spawns the real interpreter as a *child* process — confirmed via a live
   process tree during manual verification (`run_all_cameras.py` PID → real interpreter PID →
   per-camera stub PID → per-camera real interpreter PID, each pair sharing an identical
   command line). This raised a legitimate question: does `Popen.terminate()` on the
   orchestrator's tracked (stub) PID also kill the real interpreter child, or orphan it? A
   standalone script launched a real subprocess the same way `CameraOrchestrator` does, called
   `.terminate()` on the tracked PID, and enumerated the OS process list before/after via WMI
   (`Get-CimInstance Win32_Process`). Result: **no orphan** — `terminate()` on the tracked PID
   cleans up the entire tree. (Python's Windows venv launcher is specifically designed not to
   leak its child on termination.)
3. **Attempted live end-to-end signal delivery, honestly reported as inconclusive by tooling,
   not by design**: I tried sending a real `SIGINT` from the Bash tool (Git Bash/MSYS) to a
   backgrounded real orchestrator process using `kill -INT $!`. This did not work — `$!` in
   Git Bash returns an **MSYS-internal PID**, not the real Windows PID (confirmed: `$!` reported
   `206` while `tasklist`/`Get-CimInstance` showed the real PIDs in the thousands), so the
   signal never reached anything. This is a tooling/environment boundary (MSYS PID-space vs.
   Win32 PID-space), not a defect in the orchestrator, and it's exactly the kind of
   cross-platform signal-delivery fragility that motivated verification method (1) instead of
   relying on real OS signal delivery as the primary test. Leftover processes from this
   experiment (6 python.exe processes, ~1.4GB combined) were confirmed still healthy — i.e.
   never actually signaled at all — and were cleaned up via `taskkill /F /T` after explicit user
   approval, since an ad hoc `taskkill` targeting a PID identified only from a fresh process
   listing was correctly flagged by the permission system as unverifiable without that
   confirmation.

Net result across all three: shutdown behavior is verified to actually terminate every child,
including the Windows-specific launcher-stub/real-interpreter relationship, with no orphans in
any of the scenarios tested.

## Test results

### New tests: `tests/test_run_all_cameras.py` (5 tests)
```
tests/test_run_all_cameras.py::test_load_enabled_cameras_excludes_disabled PASSED
tests/test_run_all_cameras.py::test_orchestrator_only_launches_enabled_cameras PASSED
tests/test_run_all_cameras.py::test_one_crashing_camera_does_not_affect_others PASSED
tests/test_run_all_cameras.py::test_each_camera_output_goes_to_its_own_log_file PASSED
tests/test_run_all_cameras.py::test_signal_triggers_termination_of_all_children_no_orphans PASSED
5 passed in 1.70s
```
No `python.exe` processes remained after any test run (checked via `tasklist` before/after).

### Live, real-pipeline smoke tests (manual, not part of the pytest suite)
- 2 real cameras (`camera_01`, `camera_02`), real video files, `--max-frames 20`: both exited
  with code 0, both produced correct, fully-attributed per-camera logs with real
  `Frame N/20 done` / role-engine / table-state output.
- Definitive orphan-tree check (described above): confirmed no orphan under `terminate()`.

### Full suite regression check
```
python -m pytest tests/ -v
```
```
36 passed, 1 failed in 15.56s
```
The 1 failure is the same pre-existing, unrelated `tests/test_tracker.py::test_tracker_update`
failure documented in Tasks 1–3 (list-vs-dict detection format mismatch between the test and
`src/ai_models/tracker.py`, predating this session). Untouched by this change.

## Decisions made unilaterally

1. **Script name**: `run_all_cameras.py` — matches the `run_*.py` convention, self-descriptive
   scope difference from `run_live.py`.
2. **Camera → video source resolution via `videos_index.json`**, with enabled-but-unindexed
   cameras skipped and warned rather than defaulted to a webcam — detailed above.
3. **`cwd`/`PYTHONPATH` fix for child processes**: worked around a pre-existing `run_live.py`
   `sys.path` bug at the launch layer rather than touching `run_live.py` itself, since the task
   explicitly forbade modifying that file's logic but launching children correctly is squarely
   the orchestrator's job.
4. **`scikit-learn` added to `requirements.txt`**: a genuine, previously-undetected runtime
   dependency (needed to unpickle `label_encoder.pkl`) found only by actually running the real
   pipeline end-to-end while verifying this task — not an orchestration-layer change, but
   necessary to get real (not just simulated) verification evidence.
5. **Log redirection via direct `stdout=file` rather than a per-line-prefixing reader thread**:
   simpler, avoids thread-lifecycle complexity, and gives an equal-or-stronger attribution
   guarantee (separate OS file descriptors can't interleave) — satisfies the task's "or
   otherwise clearly attributable" clause directly.
6. **Shutdown handler tested via direct invocation of the registered callback, not real
   cross-process signal delivery**: chosen deliberately after confirming Git Bash's PID-space
   mismatch makes real signal delivery to an arbitrary background Windows process unreliable
   from this tool — calling `handler(signum, frame)` directly is the standard, portable way to
   unit-test a signal handler, and I additionally ran a dedicated orphan-tree check (not just
   `poll()` on the immediate child) once the venv's launcher-stub behavior came to light during
   manual verification, to close the one real gap that direct-invocation testing alone
   wouldn't have caught.
7. **No retry/restart logic added anywhere**, per explicit instruction.

## Out of scope (explicitly not touched)
Event Engine, data-contract layer, KPI Engine, backend, frontend, `run_live.py`'s per-camera
processing logic (only its child-launch environment was adjusted, from the orchestrator side),
and the pre-existing `test_tracker.py` failure.
