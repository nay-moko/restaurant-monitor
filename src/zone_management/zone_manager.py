import json
from pathlib import Path
from typing import Any


class ZoneManager:
    def __init__(self, zones_config_path: str = "config/zones_config.json"):
        self.project_dir = Path.cwd()
        self.zones_config_path = self.project_dir / zones_config_path

        if not self.zones_config_path.exists():
            raise FileNotFoundError(
                f"zones_config.json not found: {self.zones_config_path}"
            )

        with open(self.zones_config_path, "r", encoding="utf-8") as f:
            self.zones_config = json.load(f)

    def get_bbox_zone(self, camera_id: str, box: list[int | float]) -> dict[str, Any]:
        x1, y1, x2, y2 = box

        bottom_center_x = (x1 + x2) / 2
        bottom_center_y = y2

        return self.get_point_zone(
            camera_id=camera_id,
            point=[bottom_center_x, bottom_center_y]
        )

    def get_point_zone(self, camera_id: str, point: list[int | float]) -> dict[str, Any]:
        camera_zones = self.zones_config.get(camera_id)

        if camera_zones is None:
            return self._unknown_zone(reason="camera_not_found", point=point)

        zones = camera_zones.get("zones", [])

        for zone in zones:
            polygon = zone.get("points", [])

            if self._point_in_polygon(point, polygon):
                return {
                    "zone_id": zone.get("zone_id"),
                    "zone_type": zone.get("zone_type"),
                    "zone_name": zone.get("zone_name"),
                    "point": [round(point[0], 2), round(point[1], 2)],
                    "matched": True
                }

        return self._unknown_zone(reason="point_outside_all_zones", point=point)

    def enrich_detection(self, camera_id: str, detection: dict[str, Any]) -> dict[str, Any]:
        box = detection.get("box")

        if box is None:
            detection["zone"] = self._unknown_zone(reason="missing_box")
            return detection

        detection["zone"] = self.get_bbox_zone(camera_id, box)
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

    def _unknown_zone(
        self,
        reason: str,
        point: list[int | float] | None = None
    ) -> dict[str, Any]:
        return {
            "zone_id": "unknown",
            "zone_type": "unknown",
            "zone_name": "Unknown",
            "point": point,
            "matched": False,
            "reason": reason
        }

    def _point_in_polygon(
        self,
        point: list[int | float],
        polygon: list[list[int | float]]
    ) -> bool:
        if len(polygon) < 3:
            return False

        x, y = point
        inside = False
        j = len(polygon) - 1

        for i in range(len(polygon)):
            xi, yi = polygon[i]
            xj, yj = polygon[j]

            intersects = (
                (yi > y) != (yj > y)
                and x < (xj - xi) * (y - yi) / ((yj - yi) + 1e-9) + xi
            )

            if intersects:
                inside = not inside

            j = i

        return inside