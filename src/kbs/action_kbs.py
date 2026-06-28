"""
action_kbs.py
-------------
Promotes Unknown persons to Customer or Worker based on
LSTM action labels + zone + pose-frame counts.

Pose-frames are sampled at 3fps (not raw video frames).
Re-ID-dependent rules are guarded by re_id_ready flag.
"""

from experta import KnowledgeEngine, Fact, Field, Rule, AS, MATCH, NOT,TEST


# ---------------------------------------------------------------------------
# Facts
# ---------------------------------------------------------------------------

class PersonFact(Fact):
    """
    One fact per tracked person visible to this engine.

    Fields
    ------
    track_id        : int   - DeepSORT track id (camera-local)
    global_id       : str   - Re-ID global identity, e.g. "global_7" (None if unknown)
    role            : str   - "unknown" | "customer" | "worker"
    action          : str   - latest LSTM label: "sitting"|"standing"|"walking"|"serving"
    zone_type       : str   - zone the person's bbox centroid falls in
    pose_frame_count: int   - consecutive pose-frames with the current action in current zone
    appearance_count: int   - how many times this global_id entered a walk zone (Re-ID)
    re_id_ready     : bool  - True once Re-ID is operational
    """
    track_id         = Field(int,  mandatory=True)
    global_id        = Field(object, default=None)   # str or None
    role             = Field(str,  default="unknown")
    action           = Field(str,  default="unknown")
    zone_type        = Field(str,  default="unknown")
    pose_frame_count = Field(int,  default=0)
    appearance_count = Field(int,  default=0)
    re_id_ready      = Field(bool, default=False)


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class ActionKBS(KnowledgeEngine):
    """
    Classifies Unknown persons into Customer or Worker.
    Call reset() + declare all PersonFacts + run() each inference cycle.
    Read results via self.facts after run().
    """

    # -- Promote to Customer -------------------------------------------------
    # Rule: sitting in a table zone for more than 6 consecutive pose-frames

    @Rule(
        AS.person << PersonFact(
            role="unknown",
            action="sitting",
            zone_type="table",
            pose_frame_count=MATCH.count,
        ),
        TEST(lambda count: count > 3),
        salience=10,
    )
    def promote_to_customer(self, person, count):
        self.modify(person, role="customer")

    # -- Promote to Worker via serving (Re-ID NOT required) ------------------
    # Rule: serving action for more than 6 consecutive pose-frames (any zone)

    @Rule(
        AS.person << PersonFact(
            role="unknown",
            action="serving",
            pose_frame_count=MATCH.count,
        ),
        TEST(lambda count: count > 3),
        salience=10,
    )
    def promote_to_worker_via_serving(self, person, count):
        self.modify(person, role="worker")

    # -- Promote to Worker via walking (Re-ID required) ----------------------
    # Rule: appeared in a walk zone more than 2 times across cameras
    # Guarded by re_id_ready — skipped until Re-ID is implemented.

    @Rule(
        AS.person << PersonFact(
            role="unknown",
            action="walking",
            zone_type="walk",
            appearance_count=MATCH.appearances,
            re_id_ready=True,
        ),
        TEST(lambda appearances: appearances > 2),
        salience=10,
    )
    def promote_to_worker_via_walking(self, person, appearances):
        self.modify(person, role="worker")

    # -- Already classified: skip -------------------------------------------
    # Persons already promoted are not processed by this engine.
    # (live_pipeline routes them to worker_kbs / table_kbs instead)