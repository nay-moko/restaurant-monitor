"""
worker_kbs.py
-------------
Determines the operational state of classified Workers.
Operates globally across cameras (requires Re-ID for cross-camera idle detection).

Worker states
-------------
serving : doing serving action near a table zone
working : doing serving anywhere OR walking in a customer-facing camera
idle    : sitting or standing for more than 20 consecutive pose-frames

Priority (salience): serving > working > idle
"""

from experta import KnowledgeEngine, Fact, Field, Rule, AS, MATCH, TEST


# ---------------------------------------------------------------------------
# Facts
# ---------------------------------------------------------------------------

class WorkerFact(Fact):
    """
    One fact per confirmed Worker, aggregated across cameras via global_id.

    Fields
    ------
    global_id        : str  - Re-ID global identity (required)
    action           : str  - latest LSTM label
    zone_type        : str  - zone type at current camera
    camera_type      : str  - "customer_facing" | "kitchen" | "other"
    pose_frame_count : int  - consecutive pose-frames in current action+zone
    state            : str  - output: "serving"|"working"|"idle"|"unknown"
    re_id_ready      : bool - True once Re-ID is operational
    """
    global_id        = Field(str,  mandatory=True)
    action           = Field(str,  default="unknown")
    zone_type        = Field(str,  default="unknown")
    camera_type      = Field(str,  default="other")
    pose_frame_count = Field(int,  default=0)
    state            = Field(str,  default="unknown")
    re_id_ready      = Field(bool, default=False)


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class WorkerKBS(KnowledgeEngine):
    """
    Classifies Worker state each inference cycle.
    Call reset() + declare WorkerFacts + run() per cycle.
    """

    # -- Serving state -------------------------------------------------------
    # Serving action near a table zone → state = serving
    # Highest priority: a worker actively handing food trumps all other states.

    @Rule(
        AS.worker << WorkerFact(
            action="serving",
            zone_type="table",
            state=MATCH.current_state,
        ),
        TEST(lambda current_state: current_state != "serving"),
        salience=30,
    )
    def set_state_serving(self, worker, current_state):
        self.modify(worker, state="serving")

    # -- Working state (serving action, non-table zone) ----------------------
    # Serving anywhere outside a table zone still counts as working.

    @Rule(
        AS.worker << WorkerFact(
            action="serving",
            state=MATCH.current_state,
        ),
        TEST(lambda current_state: current_state != "working"),
        salience=20,
    )
    def set_state_working_via_serving(self, worker, current_state):
        self.modify(worker, state="working")

    # -- Working state (walking in customer-facing camera) -------------------

    @Rule(
        AS.worker << WorkerFact(
            action="walking",
            camera_type="customer_facing",
            state=MATCH.current_state,
        ),
        TEST(lambda current_state: current_state != "working"),
        salience=20,
    )
    def set_state_working_via_walking(self, worker, current_state):
        self.modify(worker, state="working")

    # -- Idle state ----------------------------------------------------------
    # sitting or standing for more than 20 consecutive pose-frames.
    # Applied globally (re_id_ready guard — idle across cameras needs Re-ID).

    @Rule(
        AS.worker << WorkerFact(
            action=MATCH.action,
            pose_frame_count=MATCH.count,
            state=MATCH.current_state,
            re_id_ready=True,
        ),
        TEST(lambda action, count, current_state: action in ("sitting", "standing") and count > 20 and current_state != "idle"),
        salience=10,
    )
    def set_state_idle(self, worker, **kwargs):
        self.modify(worker, state="idle")

    @Rule(
        AS.worker << WorkerFact(
            action=MATCH.action,
            pose_frame_count=MATCH.count,
            state=MATCH.current_state,
            re_id_ready=False,
        ),
        TEST(lambda action, count, current_state: action in ("sitting", "standing") and count > 20 and current_state != "idle"),
        salience=5,
    )
    def set_state_idle_local(self, worker, **kwargs):
        self.modify(worker, state="idle")