# Task 8 — Cross-Process Identity Sync (Central Identity Store)

## 1. Problem recap

Since Task 5, each camera runs as a fully independent OS subprocess
(`src/run_all_cameras.py` launches one `run_live.py` per enabled camera via
`subprocess.Popen`). Each subprocess builds its own in-process
`LivePipeline`, with its own in-memory `ReIDGallery` (permanent workers) and
`SessionGallery` (session-level people). Neither gallery is visible to any
other camera's process, so the same physical person seen first by
camera_01's process and later by camera_02's process previously got two
unrelated `global_id`s.

This task adds a Redis-backed `CentralIdentityStore` that all camera
processes share, and wires it into `LivePipeline` as a new middle tier
between the existing permanent worker gallery and the existing local
session gallery.

## 2. Design

### 2.1 `src/core/central_identity_store.py` (new file)

`CentralIdentityStore` — a small class with one real entry point,
`resolve_identity(embedding) -> global_id`, plus `remove(global_id)` and
`ping()`. All state lives in Redis, not in the class instance, so any
number of camera processes can each hold their own `CentralIdentityStore`
object pointed at the same Redis server and see each other's identities.

Storage layout (Redis, single db):
- `central_identity_store:embeddings` — a hash, `global_id -> JSON list of
  512 floats`.
- `central_identity_store:counter` — an `INCR` counter used to mint new
  `global_id`s as `central_<n>`.
- `central_identity_store:lock` — a `redis.lock()` distributed lock guarding
  the whole match-then-register sequence of every `resolve_identity()`
  call.

`resolve_identity()`:
1. Acquire the lock (`blocking=True`, `blocking_timeout=10s`,
   auto-expires after `timeout=10s` if the holding process dies).
2. `HGETALL` all stored identities, compute cosine similarity between the
   query embedding and every stored one (embeddings are L2-normalized
   defensively inside the store, not just trusted from the caller).
3. If the best match clears `threshold` **and** beats the runner-up by
   `ReIDGallery.MIN_MATCH_MARGIN` (imported directly from
   `src/kbs/reid_gallery.py` — line 56 — rather than re-declared, so the two
   stay in sync by construction), refresh that identity's stored embedding
   with the new observation and return its `global_id`.
4. Otherwise, `INCR` the counter, `HSET` the new embedding, return the new
   `global_id`.
5. Release the lock in a `finally` block.

Every public method (`resolve_identity`, `remove`, `ping`) wraps all
`redis.exceptions.RedisError` subclasses (including lock timeouts and
connection/timeout errors) in `CentralIdentityStoreError` and re-raises —
nothing is swallowed. Constructing the store (`__init__`) never touches the
network, because `redis.Redis(...)` connects lazily — verified explicitly
in `test_construction_does_not_raise_when_redis_unreachable`.

### 2.2 Threshold and margin — why 0.65 and reused margin

Task instructions require reusing `SessionGallery`'s threshold (0.65), not
`ReIDGallery`'s stricter permanent-gallery threshold (0.72), because the
central store takes over `SessionGallery`'s role for not-yet-confirmed
people — misclassifying a session-level person is cheap to correct
(promotion to the permanent gallery is a one-way, higher-bar decision made
separately by `RoleEngine`), so the store should err toward matching rather
than fragmenting one real person into many `global_id`s across cameras.
`SessionGallery.threshold` is only an instance-default constructor
parameter (`src/kbs/reid_gallery.py:179`), not a class constant, so it is
hardcoded as `CentralIdentityStore.THRESHOLD = 0.65` with a comment
pointing at that line, rather than instantiating a whole `SessionGallery`
just to read a default. The margin constant (`0.05`) *is* a class constant
(`ReIDGallery.MIN_MATCH_MARGIN`) and is imported directly, so it cannot
drift out of sync with the rest of the codebase.

### 2.3 Locking strategy — why a single global lock

A single `central_identity_store:lock` guards *all* identities, not one
lock per candidate/bucket. Rationale: the store's data volume is bounded by
"people currently active in the restaurant across all cameras," which is
small (tens, not thousands); a single lock is the simplest correct design
for the race the task calls out (two processes registering the same person
twice), and sharding/per-person locks would be premature optimization for
a scale this store doesn't operate at. The lock has its own `timeout`
(auto-release if a process dies mid-op, so one crashed process can't wedge
every other camera forever) and the caller is protected either way:
`resolve_identity()` raises `CentralIdentityStoreError` if the lock can't
be acquired within `blocking_timeout`, which `LivePipeline` catches and
falls back to tier 3.

### 2.4 `src/core/live_pipeline.py` — wiring

- `__init__` ([live_pipeline.py:20-23](src/core/live_pipeline.py#L20-L23),
  import; [live_pipeline.py:106-123](src/core/live_pipeline.py#L106-L123),
  construction): reads an optional `config["redis"]` section
  (`host`/`port`/`db`, defaulting to `localhost`/`6379`/`0`), backward
  compatible with every existing `config.json` (none currently has a
  `redis` key — verified against `config/config.json`). Construction is
  unconditional and cannot fail on an unreachable Redis (see 2.1).

- `_run_kbs()` Re-ID pre-check, restructured into three tiers
  ([live_pipeline.py:541-577](src/core/live_pipeline.py#L541-L577)):
  1. Permanent Worker Gallery (`self.reid_gallery._match`) — unchanged,
     first.
  2. `self.central_identity_store.resolve_identity(embedding)` — new
     primary path. Wrapped in `try/except CentralIdentityStoreError`;
     on failure, logs a clear message
     (`"[ReID] central identity store unavailable (...); falling back to
     local session gallery for track {tid}"`) and falls through.
  3. `self.session_gallery` — retained exactly as it existed before this
     task (same `match`/`update_seen`/`register` calls), now reached only
     when tier 2 raised or returned no id.

- Promotion logic ([live_pipeline.py:636-667](src/core/live_pipeline.py#L636-L667)):
  a person confirmed as `worker` by `RoleEngine` is promoted from whichever
  tier issued their id — `session_`-prefixed ids are removed from
  `SessionGallery` (unchanged behavior), `central_`-prefixed ids are removed
  from the central store via `remove()`, itself wrapped in
  `try/except CentralIdentityStoreError` so a Redis failure *during*
  promotion also can't crash the pipeline — it just leaves a harmless
  orphaned entry in Redis (logged as a warning) since tier 1 always takes
  precedence for that person on their next sighting anyway.

## 3. Fallback behavior — how it was verified

Requirement: Redis unreachable must not crash construction or any frame,
and must be caught at the point of use.

- **Construction**: `test_construction_does_not_raise_when_redis_unreachable`
  constructs `CentralIdentityStore(host="localhost", port=1, ...)` (port 1
  refuses connections) and asserts no exception — confirms `redis.Redis()`'s
  lazy-connect behavior is actually relied upon correctly, not just assumed.
- **Point of use / typed error**:
  `test_resolve_identity_raises_typed_error_when_redis_unreachable` calls
  `resolve_identity()` against the same unreachable target and asserts it
  raises `CentralIdentityStoreError` specifically (not a bare
  `redis.exceptions.*`).
- **Real call chain, no crash, correct fallback tier**:
  `test_pipeline_falls_back_to_session_gallery_when_redis_unreachable` builds
  a `LivePipeline` (via the same `object.__new__` + minimal-state pattern
  already established in `tests/test_pipeline_output.py`, extended with a
  `central_identity_store` pointed at the unreachable port) and drives the
  **real** `process_frame() → _run_kbs()` chain. Assertions: the call
  returns normally (no exception reaches the caller), the log output
  contains the expected fallback message, and — critically — the track's
  assigned `global_id` actually starts with `session_` (proof tier 3 ran,
  not just "nothing crashed"). A second test,
  `test_pipeline_process_frame_twice_stays_on_fallback_without_crashing`,
  drives a second frame on the same track to also exercise the "already
  resolved, just touch" branch under the same failure condition.

## 4. Tests written (`tests/test_central_identity_store.py`)

All 7 pass:

| Test | Covers |
|---|---|
| `test_dissimilar_embeddings_get_different_global_ids` | (a) two orthogonal (cosine=0) embeddings → two distinct `global_id`s, real Redis |
| `test_near_identical_embeddings_get_same_global_id` | (b) two embeddings with cosine≈0.9998 → same `global_id`, real Redis |
| `test_lock_prevents_duplicate_ids_for_concurrent_registrations` | (c) 8 real OS threads, released simultaneously via a `threading.Barrier`, hitting a real local Redis instance with the same embedding → all 8 converge on exactly one `global_id`; the store's hash has exactly 1 entry afterward |
| `test_resolve_identity_raises_typed_error_when_redis_unreachable` | typed-error contract |
| `test_construction_does_not_raise_when_redis_unreachable` | construction never touches the network |
| `test_pipeline_falls_back_to_session_gallery_when_redis_unreachable` | (d) real `process_frame()`/`_run_kbs()` chain, no crash, verified fallback tier |
| `test_pipeline_process_frame_twice_stays_on_fallback_without_crashing` | (d) fallback stays stable across repeated frames on the same track |

(a)-(c) use a dedicated Redis db (15), flushed before/after each test, and
are skipped automatically (`requires_real_redis`) if no Redis instance is
reachable — none of them mock Redis.

```
python -m pytest tests/test_central_identity_store.py -v
======= 7 passed in 63.38s =======
```

## 5. Regression suite

Ran the full suite before touching any code, to establish a baseline, and
again after:

```
Before (baseline, on this branch prior to any Task 8 change): 11 failed, 30 passed
After  (with Task 8's changes + 7 new tests):                 11 failed, 37 passed
```

The same 11 pre-existing failures appear identically before and after
(`test_live_pipeline_timing.py` x3, `test_pipeline_output.py` x3,
`test_pose_stride.py` x1, `test_table_zone_anchoring.py` x3,
`test_tracker.py` x1). These test files reference methods/attributes that
do not exist in the current `src/core/live_pipeline.py` on this branch
(e.g. `_update_person_state`, `frame_output`, `person_state`) and a
`TypeError` in `src/ai_models/tracker.py` unrelated to Re-ID — all
pre-existing and out of this task's scope (table-state/tracker/output-format
logic explicitly excluded). No new failures were introduced; the delta is
exactly +7 passing (the new test file).

## 6. Smoke test

### 6.1 Real 2-process orchestrator run

Launched `src/run_all_cameras.py` for real, with a temporary 2-camera
config (`camera_01`, `camera_02` — the only two cameras in
`config/camera_config.json` sharing the same `"Winter_section"` location),
against the real recorded videos in `data/raw_videos/`, `--max-frames 60`,
with a real local Redis instance already running on `localhost:6379`
(confirmed reachable beforehand). Each camera ran as a genuinely separate
OS process (own PID, own `logs_smoke/<camera_id>.log`, own loaded copy of
every model). Redis db 0 was flushed before the run for a clean slate.

*(Aside, unrelated to Task 8: `run_all_cameras.py`'s own `main()` prints
Arabic text and crashes with `UnicodeEncodeError` under this Windows
console's default `cp1252` stdout encoding before it even reaches
`launch_all()`. This is a pre-existing bug in that file, not touched by
this task per the out-of-scope instructions. Worked around for this smoke
test only by launching with `PYTHONIOENCODING=utf-8` in the environment —
no source change.)*

Result: **the central store was exercised for real by both processes.**
Grepping both logs for `[ReID]` lines shows both cameras independently
resolving tracks through tier 2 (`resolved via central identity store →
central_N`) and promoting confirmed workers out of it. One id,
`central_6`, appears in **both** logs:

- `logs_smoke/camera_02.log:40` — registered fresh: `track 5 resolved via
  central identity store → central_6` (camera_02's 2nd processed frame).
- `logs_smoke/camera_01.log:336` — matched, not re-registered: `track 11
  resolved via central identity store → central_6` (camera_01's 48th
  processed frame).
- `logs_smoke/camera_02.log:546` — later promoted: `Promoted central_6 to
  permanent worker → worker_4e17c113`.

This is a genuine cross-process id reuse mechanically. **However, I cannot
honestly claim this proves the *same real physical person* crossed both
cameras**: `camera_01/video_001.mp4` and `camera_02/video_001.mp4` are two
separate hour-long recordings with no confirmed shared wall-clock start
time in `videos_index.json`, and comparing only 60 frames (≈4s) from each
gives no visual confirmation either way. Per the task's instruction to be
honest about what remains unverified, I do not present this single
cross-camera match as proof by itself — see 6.2 for the unambiguous
verification instead.

### 6.2 Rigorous verification: two separate OS processes, real inference, ground-truth-known input

To get an unambiguous result (not dependent on whether the two video files
happen to overlap in real time), I ran two **completely independent**
`python` process invocations (not threads, not the same interpreter),
each loading its own real OSNet model from scratch and calling the real
`CentralIdentityStore` against a dedicated Redis db (14, flushed before):

1. Extracted one real person crop from `camera_01/video_001.mp4` frame 800
   via the real `PersonDetector` and saved it to disk as a JPEG.
2. **Process A** (`python resolve_from_crop.py verify_crop.jpg PROC_A`):
   loads `ReIDGallery` fresh, extracts a real embedding from the saved
   crop, calls `CentralIdentityStore.resolve_identity()` → `central_1`.
3. **Process B**, launched separately afterward (own PID, own fresh model
   load, no shared Python state with Process A): same crop → `central_1`.
4. Redis hash size after both: **1** (no duplicate registered).

```
=== Process A === RESULT:PROC_A:central_1
=== Process B === RESULT:PROC_B:central_1
hash entries: 1
```

This is the unambiguous proof: two genuinely separate OS processes, each
doing real OSNet inference independently, converge on the exact same
shared `global_id` for the same person via Redis, with no duplicate
registration.

### 6.3 An honest finding surfaced during verification (not a Task 8 bug)

While building an additional negative-control check (feed the store a
crop of a visually distinct second person and confirm a *different*
`global_id`), I found that a crop of a clearly different person (different
face, different clothing, from `camera_02/video_001.mp4`) also matched
`central_1`. Debugging this directly (computing cosine similarity between
the two real 512-d embeddings in isolation) showed the underlying OSNet
model itself — loaded from **generic ImageNet-pretrained weights**, because
no fine-tuned `models/reid/osnet_x0_25.pth` exists on disk (confirmed via
the model's own load warning: `No file found at "models\reid\osnet_x0_25.pth"`
→ falls back to `osnet_x0_25_imagenet.pth`) — returns cosine similarity
≈**0.72** between these two different people. That is at or above *both*
`SessionGallery`'s existing 0.65 threshold and `ReIDGallery`'s existing,
stricter 0.72 permanent-worker threshold.

This is a **pre-existing characteristic of the ReID model weights already
used everywhere in this codebase** (`ReIDGallery`, `SessionGallery`, and
now `CentralIdentityStore` all share the same `_extract()`/model), not
something introduced by this task's threshold or margin logic — the store
was built, per the task's own instruction, to reuse the *exact* thresholds
already validated (or not) elsewhere in the codebase, and it does so
faithfully. Retraining/fine-tuning the ReID model or re-tuning thresholds
network-wide is out of this task's scope (and would affect
`ReIDGallery`/`SessionGallery` identically, not just the new store), so I
did not attempt it. **Flagging this explicitly**: the 6.1 cross-camera
`central_6` match should be read in light of this — it is plausible but not
provably a true same-person match, and the false-positive rate of the
underlying model at this threshold, on this dataset, is a pre-existing
open question worth a dedicated follow-up task, not something Task 8's
scope covers or should silently paper over.

## 7. Decisions made unilaterally (ambiguity in the task)

1. **`global_id` prefix**: new central-store ids are `central_<n>`
   (sequential, via Redis `INCR`) — distinguishable from `worker_*` and
   `session_*` at a glance in logs/tests, and needed because the promotion
   code path (`_run_kbs`) has to recognize which store issued an id to know
   where to call `.remove()`.
2. **Embedding refresh on match**: `resolve_identity()` overwrites the
   stored embedding with the newly observed one on every match (mirrors
   `SessionGallery.update_seen`'s drift-tracking behavior) rather than
   keeping the original registration vector frozen forever.
3. **No TTL/purge in the central store**: unlike `SessionGallery`
   (`purge_old()`, 30 min TTL), the central store never expires entries.
   The task described it as taking over `SessionGallery`'s *role*, not
   its TTL mechanics, and adding one wasn't required by any of the four
   verification scenarios; flagging it here as a known limitation (the
   store will grow unboundedly over a long-running deployment) rather than
   building an unrequested feature.
4. **Single global lock, not per-bucket**: see §2.3.
5. **`redis` version pin**: pinned to `8.0.1`, the version already resolved
   in this dev environment (`pip show redis`), following the same
   precedent `requirements.txt`'s header already documents for `gdown`,
   `tensorboard`, and `scikit-learn`.
6. **Smoke-test camera pair**: used `camera_01`+`camera_02` (both
   `"Winter_section"`) since they're the only same-location pair with
   recorded video in `data/raw_videos/`, and reported honestly (§6.1) that
   this alone doesn't prove same-person convergence — hence §6.2's
   separate, unambiguous check.

## 8. Files changed

- `src/core/central_identity_store.py` — **new**, `CentralIdentityStore` +
  `CentralIdentityStoreError`.
- `src/core/live_pipeline.py` — import ([L23](src/core/live_pipeline.py#L23)),
  `CentralIdentityStore` construction in `__init__`
  ([L106-L124](src/core/live_pipeline.py#L106-L124)), 3-tier Re-ID
  restructure in `_run_kbs`
  ([L541-L577](src/core/live_pipeline.py#L541-L577)), promotion logic
  update ([L636-L667](src/core/live_pipeline.py#L636-L667)).
- `requirements.txt` — added `redis==8.0.1` + header note.
- `src/core/central_state.py` — header comment only, noting supersession;
  no code removed, per the working constraint.
- `tests/test_central_identity_store.py` — **new**, 7 tests (§4).
- `docs/TASK8_REPORT.md` — this file.

Nothing in the Event Engine, KPI Engine, backend, frontend, or table-state
logic was touched.
