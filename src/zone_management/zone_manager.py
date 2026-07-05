import json
from pathlib import Path
from typing import Any

from shapely.geometry import Point, Polygon, box as shapely_box


class ZoneManager:
    ZONE_TYPE_MAP: dict[str, str] = {
        "table_area"           : "table",   # broad container: "is this person in the table section at all"
        "table"                : "table",   # single table (leaf, nested inside a table_area): "which exact table"
        "service_path"         : "walk",
        "hallway"              : "walk",
        "corridor"             : "walk",
        "open_area"            : "walk",
        "mixed_area"           : "walk",
        "entrance"             : "walk",
        "bathroom_entrance"    : "walk",
        "prayer_room_entrance" : "walk",
        "staff_area"           : "work",
        "buffet"               : "work",
        "cashier"              : "work",
    }

    # COCO keypoint indices for lower body: hips, knees, ankles
    LOWER_BODY_KP_INDICES = (11, 12, 13, 14, 15, 16)
    # COCO keypoint indices for hands: left_wrist, right_wrist
    HAND_KP_INDICES = (9, 10)
    KP_CONF_THRESHOLD = 0.25

    def __init__(self, zones_config_path: str = "config/zones_config.json"):
        self.project_dir = Path.cwd()
        self.zones_config_path = self.project_dir / zones_config_path

        if not self.zones_config_path.exists():
            raise FileNotFoundError(
                f"zones_config.json not found: {self.zones_config_path}"
            )

        with open(self.zones_config_path, "r", encoding="utf-8") as f:
            self.zones_config = json.load(f)

    def get_bbox_zone(
        self,
        camera_id: str,
        box: list[int | float],
        keypoints=None,
    ) -> dict[str, Any]:
        camera_zones = self.zones_config.get(camera_id)
        if camera_zones is None:
            return self._unknown_zone(reason="camera_not_found", box=box)

        zones = camera_zones.get("zones", [])
        if not zones:
            return self._unknown_zone(reason="no_zones", box=box)

        # -- Step 1: skeleton check -------------------------------------
        # If any visible lower-body keypoint (hip/knee/ankle) falls inside
        # a walk zone, instantly assign that walk zone (skip intersection logic).
        walk_zone_hit = self._check_lower_body_in_walk_zone(zones, keypoints)
        if walk_zone_hit is not None:
            print(f"[ZoneManager] cam={camera_id} box={box} → WALK zone_id={walk_zone_hit.get('zone_id')} (method=skeleton)")
            return self._zone_result(walk_zone_hit, 100.0, box, method="skeleton")

        # -- Step 2: intersection-percentage fallback ---------------------
        x1, y1, x2, y2 = box

        # Skip the top 10% of the bbox to avoid false overlaps with
        # work/walk zones caused by camera angle.
        y1_trimmed = y1 + 0.10 * (y2 - y1)
        bbox_poly = shapely_box(x1, y1_trimmed, x2, y2)
        bbox_area = bbox_poly.area

        if bbox_area == 0:
            return self._unknown_zone(reason="empty_bbox", box=box)

        work_pct = 0.0
        table_area_pct = 0.0
        work_zone = None
        table_area_zone = None

        # bbox center point — used only as a FALLBACK for table matching,
        # when hand keypoints aren't available/confident enough (see below).
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0
        center_point = Point(cx, cy)

        # Specific-table matching: prefer HANDS over bbox center.
        # A person's hands (wrists) are what actually interacts with a
        # table — reaching for a cup, resting hands on the surface — so a
        # visible wrist inside a table polygon is a much more direct signal
        # of "at this table" than bbox center, and is also more stable than
        # %-intersection (which flickered between adjacent tables on tiny
        # bbox jitter and stalled pose_frame_count).
        table_specific_zone, table_match_method = self._find_table_by_hands(zones, keypoints)
        if table_specific_zone is None:
            table_specific_zone = self._find_table_by_center(zones, center_point)
            table_match_method = "center_point"

        for zone in zones:
            points = zone.get("points", [])
            if len(points) < 3:
                continue

            polygon = Polygon(points)
            if not polygon.is_valid:
                continue

            inter_area = bbox_poly.intersection(polygon).area
            pct = (inter_area / bbox_area) * 100

            raw_zone_type = zone.get("zone_type")
            zone_type = self.ZONE_TYPE_MAP.get(raw_zone_type, "unknown")

            if zone_type in ("work", "walk") and pct > work_pct:
                work_pct = pct
                work_zone = zone
            elif zone_type == "table" and raw_zone_type == "table_area" and pct > table_area_pct:
                # broader term: the general table section — tells us the person IS at a table
                table_area_pct = pct
                table_area_zone = zone

        if work_pct >= 30 and work_zone is not None:
            print(f"[ZoneManager] cam={camera_id} box={box} → WORK zone_id={work_zone.get('zone_id')} pct={work_pct:.1f}")
            return self._zone_result(work_zone, work_pct, box, method="intersection")

        # A specific single table always wins over its broader container —
        # it's strictly more useful information (exact table > general area).
        if table_specific_zone is not None:
            print(f"[ZoneManager] cam={camera_id} box={box} → TABLE(specific) zone_id={table_specific_zone.get('zone_id')} parent={table_specific_zone.get('parent_zone_id')} method={table_match_method}")
            return self._zone_result(table_specific_zone, 100.0, box, method=table_match_method)

        if table_area_zone is not None:
            print(f"[ZoneManager] cam={camera_id} box={box} → TABLE(area only, no specific table matched) zone_id={table_area_zone.get('zone_id')} pct={table_area_pct:.1f}")
            return self._zone_result(table_area_zone, table_area_pct, box, method="intersection")

        print(f"[ZoneManager] cam={camera_id} box={box} → UNKNOWN (no sufficient intersection)")
        return self._unknown_zone(reason="no_sufficient_intersection", box=box)

    def _find_table_by_hands(self, zones, keypoints) -> tuple[dict[str, Any] | None, str]:
        """Check wrist keypoints against 'table' leaf zones.

        Returns (zone, method) — method is 'hands' if a wrist match was
        found, else (None, 'hands') to signal the caller should fall back
        to bbox-center matching.
        """
        if keypoints is None:
            return None, "hands"

        table_zones = [
            zone for zone in zones
            if zone.get("zone_type") == "table" and len(zone.get("points", [])) >= 3
        ]
        if not table_zones:
            return None, "hands"

        for idx in self.HAND_KP_INDICES:
            if idx >= len(keypoints):
                continue

            x, y, conf = keypoints[idx]
            if conf < self.KP_CONF_THRESHOLD:
                continue

            point = Point(float(x), float(y))

            best_zone, best_area = None, None
            for zone in table_zones:
                polygon = Polygon(zone["points"])
                if polygon.is_valid and polygon.contains(point):
                    if best_area is None or polygon.area < best_area:
                        best_area = polygon.area
                        best_zone = zone

            if best_zone is not None:
                return best_zone, "hands"

        return None, "hands"

    def _find_table_by_center(self, zones, center_point: Point) -> dict[str, Any] | None:
        """Return the leaf 'table' zone whose polygon contains the bbox center point.

        If the center falls inside more than one table polygon (shouldn't
        normally happen with well-drawn zones, but can with overlapping
        annotations), pick the one with the smallest area — the most
        specific/tightest match.
        """
        best_zone = None
        best_area = None
        for zone in zones:
            if zone.get("zone_type") != "table":
                continue
            points = zone.get("points", [])
            if len(points) < 3:
                continue
            polygon = Polygon(points)
            if not polygon.is_valid or not polygon.contains(center_point):
                continue
            if best_area is None or polygon.area < best_area:
                best_area = polygon.area
                best_zone = zone
        return best_zone

    def _check_lower_body_in_walk_zone(self, zones, keypoints) -> dict[str, Any] | None:
        if keypoints is None:
            return None

        walk_zones = [
            zone for zone in zones
            if self.ZONE_TYPE_MAP.get(zone.get("zone_type"), "unknown") == "walk"
            and len(zone.get("points", [])) >= 3
        ]
        if not walk_zones:
            return None

        for idx in self.LOWER_BODY_KP_INDICES:
            if idx >= len(keypoints):
                continue

            x, y, conf = keypoints[idx]
            if conf < self.KP_CONF_THRESHOLD:
                continue

            point = Point(float(x), float(y))

            for zone in walk_zones:
                polygon = Polygon(zone["points"])
                if polygon.is_valid and polygon.contains(point):
                    return zone

        return None

    def enrich_detection(self, camera_id: str, detection: dict[str, Any]) -> dict[str, Any]:
        box = detection.get("box")

        if box is None:
            detection["zone"] = self._unknown_zone(reason="missing_box")
            return detection

        keypoints = detection.get("keypoints")
        detection["zone"] = self.get_bbox_zone(camera_id, box, keypoints=keypoints)
        return detection

    def enrich_frame_result(self, frame_result: dict[str, Any]) -> dict[str, Any]:
        camera_id = frame_result.get("camera_id")
        detections = frame_result.get("detections", [])

        enriched_detections = []

        for detection in detections:
            enriched_detections.append(
                self.enrich_detection(camera_id, detection)
            )

        frame_result["detections"] = enriched_detections
        return frame_result

    def _zone_result(
        self,
        zone: dict[str, Any],
        pct: float,
        box: list[int | float] | None = None,
        method: str = "intersection",
    ) -> dict[str, Any]:
        return {
            "zone_id": zone.get("zone_id"),
            "zone_type": zone.get("zone_type"),
            "zone_name": zone.get("zone_name"),
            "intersection_pct": round(pct, 2),
            "box": box,
            "matched": True,
            "method": method,
        }

    def _unknown_zone(
        self,
        reason: str,
        box: list[int | float] | None = None
    ) -> dict[str, Any]:
        return {
            "zone_id": "unknown",
            "zone_type": "unknown",
            "zone_name": "Unknown",
            "intersection_pct": 0.0,
            "box": box,
            "matched": False,
            "reason": reason
        }