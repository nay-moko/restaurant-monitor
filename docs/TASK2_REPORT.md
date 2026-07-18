# Task 2 Report — Table Zone Anchoring Gap

## The bug

Inside `LivePipeline._run_kbs()`, the set of `zone_id`s handed to `TableKBS` was built
exclusively from *historical activity* dictionaries (`zone_customer_counts`,
`self._table_customer_counts`, `self._table_was_served`). A table zone that is genuinely
configured in `config/zones_config.json` but has had zero customers/serving events since the
process started never got a `TableFact` declared, so it never appeared in
`self._table_states` — it silently vanished from the output instead of correctly reporting
`"free"`.

## Files/functions changed — `src/core/live_pipeline.py`

- **[live_pipeline.py:152](src/core/live_pipeline.py#L152)** — `process_frame()` now calls
  `self._run_kbs(tracked_objects, person_crops, time_seconds, camera_id)`, passing `camera_id`
  through (previously only `tracked_objects`, `person_crops`, `time_seconds` were passed).
- **[live_pipeline.py:491-497](src/core/live_pipeline.py#L491-L497)** — `_run_kbs()` signature
  gained a required `camera_id: str` parameter, needed to look up that camera's configured
  zones.
- **[live_pipeline.py:712-741](src/core/live_pipeline.py#L712-L741)** — the `all_zone_ids`
  computation was rewritten:
  - `configured_table_zone_ids`: pulled from
    `self.zone_manager.zones_config.get(camera_id, {}).get("zones", [])`, filtered to
    `zone.get("zone_type") == "table"` specifically (excludes the broader `"table_area"`
    container zone_type).
  - `historical_zone_ids`: the same three historical sets as before
    (`zone_customer_counts`, `self._table_customer_counts`, `self._table_was_served`),
    unchanged.
  - `unconfigured_zone_ids = historical_zone_ids - configured_table_zone_ids`: any zone_id
    with history that isn't a currently-configured table zone. For each, a
    `[TableKBS][WARNING]` line is printed naming both `camera_id` and `zone_id`, flagging a
    data-consistency problem (stale config, renamed zone, etc.) instead of silently
    swallowing or crashing on it.
  - `all_zone_ids = configured_table_zone_ids | historical_zone_ids` — the union, so nothing
    in either set is dropped.
- Everything downstream of this block (`self.table_kbs.reset()` / `.declare()` / `.run()` /
  building `self._table_states`) is unchanged — it already iterated `all_zone_ids` generically.

## Why this is correct

- `TableFact.state` defaults to `"free"` in `src/kbs/table_kbs.py` ([table_kbs.py:43](src/kbs/table_kbs.py#L43)),
  and the `set_state_free` rule only fires when `customer_count=0`, `was_served=False`, and the
  fact's current state is *not already* `"free"` ([table_kbs.py:60-70](src/kbs/table_kbs.py#L60-L70)).
  So a configured table zone declared with no history (`customer_count=0`, `was_served=False`)
  correctly resolves to `"free"` purely from the `TableFact` default — no rule needs to fire.
- Using `zone_type == "table"` (not `"table_area"`) matches how the rest of the pipeline
  already distinguishes the two: `ZONE_TYPE_MAP` ([live_pipeline.py:24-38](src/core/live_pipeline.py#L24-L38))
  normalizes both `"table_area"` and `"table"` to the same `"table"` bucket for per-track zone
  classification, but `"table_area"` is a broad container zone (can overlap several individual
  tables), so anchoring the `TableKBS` universe on it would either double-count or misattribute
  customer/serving state to the wrong physical table. The specific leaf `"table"` zones are
  the actual unit `TableFact` reasons about.
- The union with `historical_zone_ids` (rather than replacing it) means a zone_id that
  accumulated real activity is never dropped just because it's momentarily missing from
  config — it's surfaced with a warning instead, per the requirement not to silently lose
  data.

## Test

Added `tests/test_table_zone_anchoring.py` with 3 cases, all calling the real `_run_kbs()` on
a `LivePipeline` built via `object.__new__()` (bypassing the heavy `__init__`, same pattern as
Task 1's test) with a stub `zone_manager.zones_config`:

1. `test_configured_table_with_no_history_defaults_to_free` — a configured `"table"` zone
   with zero history resolves to `"free"` and is present in `_table_states`; a sibling
   `"table_area"` zone in the same config is confirmed absent (proves the leaf-type filter).
2. `test_table_with_history_still_gets_occupied_and_dirty_state` — regression check: one
   zone gets a real tracked customer (drives `customer_count > 0` → `"occupied"`), another
   has a persisted `was_served=True` flag with no current customers → `"dirty"`. Confirms the
   fix didn't change existing state-derivation behavior.
3. `test_unconfigured_zone_with_history_logs_warning_and_is_kept` — a `zone_id` with history
   (`was_served=True`) absent from the configured zones: asserts the printed output contains
   `"WARNING"`, the `camera_id`, and the `zone_id` (via `capsys`), and that the zone still
   ends up in `_table_states` (as `"dirty"`) rather than being dropped.

### Test result
```
python -m pytest tests/test_table_zone_anchoring.py -v
```
```
tests/test_table_zone_anchoring.py::test_configured_table_with_no_history_defaults_to_free PASSED
tests/test_table_zone_anchoring.py::test_table_with_history_still_gets_occupied_and_dirty_state PASSED
tests/test_table_zone_anchoring.py::test_unconfigured_zone_with_history_logs_warning_and_is_kept PASSED
3 passed in 7.32s
```

### Full suite regression check
```
python -m pytest tests/ -v
```
```
18 passed, 1 failed in 8.39s
```
The 1 failure is the same pre-existing, unrelated `tests/test_tracker.py::test_tracker_update`
failure already documented in `docs/TASK1_REPORT.md` (a list-vs-dict detection format mismatch
between the test and `src/ai_models/tracker.py`, predating this session). It is untouched by
this change and out of scope here.

## Decisions made unilaterally

1. **Threading `camera_id` into `_run_kbs()`.** The task didn't say how to get `camera_id`
   into the zone-anchoring logic, only that it should be anchored on "the camera's actual
   configured table zones." `process_frame()` already has `camera_id` in scope and is the only
   caller of `_run_kbs()`, so adding it as a fourth parameter was the direct, minimal-blast-radius
   option — no alternate routing existed.
2. **Warning uses `print()`, matching existing style.** The rest of `_run_kbs()` and
   `run_live.py` use tagged `print()` statements for diagnostics (`[ReID] ...`,
   `[RoleEngine] ...`, `[ERROR] ...`) rather than the `logging` module — there is no logger
   configured anywhere in this codebase yet. I followed that existing convention
   (`[TableKBS][WARNING] camera_id=... zone_id=...`) rather than introducing a new logging
   framework, which would be out of scope for this fix.
3. **Test uses a stub `zone_manager` object, not the real `ZoneManager` class.** The real
   `ZoneManager.__init__` reads `config/zones_config.json` from disk; a minimal stub exposing
   just `.zones_config` (the only attribute `_run_kbs()` touches) keeps the test independent of
   the repo's actual zone config and fast, consistent with how Task 1's test avoided
   `LivePipeline.__init__()` entirely.
4. **Role-engine coupling in the "occupied" test case.** To exercise `customer_count > 0`
   for real (rather than just pre-seeding history dicts, which the code deliberately does
   *not* use for `TableFact.customer_count` — only for zone-universe membership), the test
   needs a tracked object whose role resolves to `"customer"` after `RoleEngine` runs. I
   verified empirically that pre-setting `self._person_roles[tid] = "customer"` before the
   call is preserved through a single `RoleEngine` cycle (its decision only overwrites
   `self._person_roles[tid]` when it computes something other than `"unknown"`, and with only
   one weak-evidence cycle it echoes back the `previous_role` it was given). This keeps the
   test aligned with real pipeline data flow rather than hand-writing `TableFact`s directly,
   which would bypass the exact code path being fixed.

## Out of scope (explicitly not touched)
Event Engine, KPI Engine, backend, frontend, the data-contract layer, and the pre-existing
`test_tracker.py` failure.
