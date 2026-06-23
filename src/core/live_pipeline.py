from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from src.ai_models.detector import PersonDetector
from src.ai_models.tracker import RestaurantTracker
from src.zone_management.zone_manager import ZoneManager


class LivePipeline:
    def __init__(self, config_path: str = "config/config.json"):
        self.project_dir = Path.cwd()
        self.config_path = self.project_dir / config_path

        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
         
         # it will bring the config from the json file and if it didnt find a value-
         #-in a vaariable in the json then it will bring it from the constructor
        detector_config = self.config["detector"]
        self.detector = PersonDetector(
            model_name=detector_config.get("model"),
            conf_threshold=detector_config.get("conf_threshold"),
            imgsz=detector_config.get("imgsz"),
            min_box_width=detector_config.get("min_box_width"),
            min_box_height=detector_config.get("min_box_height"),
            device=detector_config.get("device"),
                                     )
        tracker_config = self.config.get("tracker", {})
        self.tracker = RestaurantTracker(
         max_age=tracker_config.get("max_age"),
         n_init=tracker_config.get("n_init"),
         nms_max_overlap=tracker_config.get("nms_max_overlap")
)
        self.zone_manager = ZoneManager()

    def process_frame(self,frame,camera_id: str,video_id: str,frame_index: int,time_seconds: float | None,) -> dict[str, Any]:
        detections = self.detector.detect(frame)
        tracked_objects = self.tracker.update(detections, frame=frame)
        tracked_objects = self.enrich_tracks_with_zones(camera_id, tracked_objects)
        person_crops = self.crop_persons(frame, tracked_objects)

        return {
            "camera_id": camera_id,
            "video_id": video_id,
            "frame_index": frame_index,
            "time_seconds": time_seconds,
            "detections": detections,
            "tracked_objects": tracked_objects,
            "person_crops": person_crops,
        }

    def enrich_tracks_with_zones(self,camera_id: str,tracked_objects: list[dict[str, Any]],) -> list[dict[str, Any]]:
        enriched_tracks: list[dict[str, Any]] = []

        for obj in tracked_objects:
            zone = self.zone_manager.get_bbox_zone(
                camera_id=camera_id,
                box=obj.get("box", [0, 0, 0, 0]),
                                                   )
            enriched_obj = dict(obj)
            enriched_obj["zone"] = zone
            enriched_tracks.append(enriched_obj)

        return enriched_tracks

    def crop_persons(self, frame, tracked_objects: list[dict[str, Any]]) -> list[dict[str, Any]]:
     crops: list[dict[str, Any]] = []
     
    # جلب أبعاد الفريم مرة واحدة خارج الحلقة لتوفير الجهد المعالج
     height, width = frame.shape[:2]

     for obj in tracked_objects:
        box = obj.get("box", [0, 0, 0, 0])
        x1, y1, x2, y2 = [int(value) for value in box]

        # 💡 تصحيح فحص الحدود الاحترافي (بين صفر وعرض/ارتفاع الصورة بالكامل)
        x1 = max(0, min(width, x1))
        x2 = max(0, min(width, x2))
        y1 = max(0, min(height, y1))
        y2 = max(0, min(height, y2))

        # أخذ لقطة مرجعية سريعة بدون حجز ذاكرة إضافية أولاً
        crop = frame[y1:y2, x1:x2]
        
        # حماية من الصناديق الفارغة أو المنهارة
        if crop.size == 0 or x1 >= x2 or y1 >= y2:
            continue

        crops.append(
            {
                "track_id": obj.get("track_id"),
                "zone": obj.get("zone", {}),
                "box": [x1, y1, x2, y2],
                # 💎 نقوم بعمل نسخة حقيقية فقط هنا بعد التأكد من سلامة اللقطة
                "crop": crop.copy(), 
            }
        )

     return crops

    def draw_zones(self, frame, camera_id: str) -> None:
        camera_zones = self.zone_manager.zones_config.get(camera_id, {}).get("zones", [])

        for zone in camera_zones:
            points = zone.get("points", [])
            if len(points) < 3:
                continue

            polygon = np.array(points, dtype=np.int32)
            cv2.polylines(frame, [polygon], isClosed=True, color=(0, 255, 0), thickness=2)

            label = f"{zone.get('zone_id', 'zone')} | {zone.get('zone_type', 'unknown')}"
            x, y = polygon[0]
            cv2.putText(
                frame,
                label,
                (int(x), max(20, int(y) - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
            )

    def draw_tracks(self, frame, tracked_objects: list[dict[str, Any]]) -> None:
        for obj in tracked_objects:
            box = obj.get("box", [0, 0, 0, 0])
            x1, y1, x2, y2 = map(int, box)
            track_id = obj.get("track_id", "?")
            zone = obj.get("zone", {})
            zone_id = zone.get("zone_id", "unknown")
            zone_type = zone.get("zone_type", "unknown")

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 128, 255), 2)
            cv2.putText(
                frame,
                f"ID {track_id} | {zone_id}",
                (x1, max(20, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 128, 255),
                2,
            )

            cv2.putText(
                frame,
                zone_type,
                (x1, min(frame.shape[0] - 10, y2 + 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 215, 0),
                1,
            )