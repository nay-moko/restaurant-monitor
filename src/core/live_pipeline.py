from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from src.ai_models.detector import PersonDetector
from src.ai_models.tracker import RestaurantTracker
from src.zone_management.zone_manager import ZoneManager


from ultralytics import YOLO

class LivePipeline:
    KEYPOINT_NAMES = [
        "nose", "left_eye", "right_eye", "left_ear", "right_ear",
        "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
        "left_wrist", "right_wrist", "left_hip", "right_hip",
        "left_knee", "right_knee", "left_ankle", "right_ankle"
    ]

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
        import pickle, torch
        from src.core.classifiers import PoseLSTM  # we'll define this

        model_path = self.project_dir / "models/pose_lstm.pth"
        le_path    = self.project_dir / "models/label_encoder.pkl"

        self.action_model = PoseLSTM()
        self.action_model.load_state_dict(torch.load(model_path, map_location="cpu"))
        self.action_model.eval()

        with open(le_path, "rb") as f:
            self.label_encoder = pickle.load(f)

        self._kp_buffer: dict[int, list[dict]] = {}  # track_id -> list of (frame_id, kp_dict)
        self._action_labels: dict[int, str] = {}     # track_id -> latest label
        self._pose_samples: list[dict] = []
        self.zone_manager = ZoneManager()

    def process_frame(self, frame, camera_id, video_id, frame_index, time_seconds, pose_stride=None):
        detections, keypoints_list = self.detector.detect_with_pose(frame)
        tracked_objects = self.tracker.update(detections, frame=frame)
        tracked_objects = self.enrich_tracks_with_zones(camera_id, tracked_objects)
        person_crops = self.crop_persons(frame, tracked_objects)

        if pose_stride is None or frame_index % pose_stride == 0:
            self._extract_pose_from_detections(frame, video_id, frame_index, detections, keypoints_list, tracked_objects)

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
            # cv2.putText(
            #     frame,
            #     label,
            #     (int(x), max(20, int(y) - 10)),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.5,
            #     (0, 255, 0),
            #     1,
            # )

    def draw_tracks(self, frame, tracked_objects: list[dict[str, Any]]) -> None:
        for obj in tracked_objects:
            box = obj.get("box", [0, 0, 0, 0])
            x1, y1, x2, y2 = map(int, box)
            track_id = obj.get("track_id", "?")
            zone = obj.get("zone", {})
            zone_id = zone.get("zone_id", "unknown")
            zone_type = zone.get("zone_type", "unknown")

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 128, 255), 2)
            # cv2.putText(
            #     frame,
            #     f"ID {track_id} | {zone_id}",
            #     (x1, max(20, y1 - 10)),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.6,
            #     (0, 128, 255),
            #     2,
            # )
            action = self._action_labels.get(track_id, "...")
            # # Line 1: ID and zone
            # cv2.putText(frame, f"ID {track_id} | {zone_id}", (x1, max(20, y1 - 25)),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 128, 255), 1)

            # Line 2: action
            action = self._action_labels.get(track_id, "...")
            cv2.putText(frame, action, (x1, max(35, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 100), 2)

    def _extract_pose_from_detections(self, frame, video_id, frame_index, detections, keypoints_list, tracked_objects):
        h, w = frame.shape[:2]

        for det, kpts in zip(detections, keypoints_list):
            if kpts is None:
                continue

            track_id = self._match_to_track(det["box"], tracked_objects)
            if track_id is None:
                continue

            kp_dict = {
                self.KEYPOINT_NAMES[j]: {
                    "x":    round(float(kpts[j][0] / w), 4),
                    "y":    round(float(kpts[j][1] / h), 4),
                    "conf": round(float(kpts[j][2]),     4),
                }
                for j in range(17)
            }

            self._predict_action(track_id, frame_index, kp_dict)

            self._pose_samples.append({
                "vid_id":            video_id,
                "frame_id":          frame_index,
                "tracked_person_id": track_id,
                "keypoints":         kp_dict,
                "label":             ""
            })
    def _match_to_track(self, pose_box, tracked_objects) -> int | None:
        best_iou, best_id = 0.0, None
        px1, py1, px2, py2 = pose_box

        for obj in tracked_objects:
            tx1, ty1, tx2, ty2 = obj["box"]
            ix1, iy1 = max(px1, tx1), max(py1, ty1)
            ix2, iy2 = min(px2, tx2), min(py2, ty2)
            inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
            if inter == 0:
                continue
            union = (px2-px1)*(py2-py1) + (tx2-tx1)*(ty2-ty1) - inter
            iou = inter / union if union > 0 else 0
            if iou > best_iou:
                best_iou, best_id = iou, obj["track_id"]

        return best_id if best_iou > 0.4 else None
    def _predict_action(self, track_id: int, frame_id: int, kp_dict: dict) -> None:
        import torch, numpy as np
        buf = self._kp_buffer.setdefault(track_id, [])
        buf.append((frame_id, kp_dict))

        # Keep only recent frames (drop if gap too large)
        while len(buf) > 1 and buf[-1][0] - buf[-2][0] >= 10:
            buf.pop(0)

        if len(buf) > 6:
            buf.pop(0)

        if len(buf) < 6:
            return

        def normalize_kp(kp_dict):
            lh = kp_dict.get('left_hip',  {'x': 0, 'y': 0, 'conf': 0})
            rh = kp_dict.get('right_hip', {'x': 0, 'y': 0, 'conf': 0})
            ls = kp_dict.get('left_shoulder',  {'x': 0, 'y': 0, 'conf': 0})
            rs = kp_dict.get('right_shoulder', {'x': 0, 'y': 0, 'conf': 0})
            cx = (lh['x'] + rh['x']) / 2
            cy = (lh['y'] + rh['y']) / 2
            shoulder_y = (ls['y'] + rs['y']) / 2
            torso_h = abs(cy - shoulder_y)
            scale = torso_h if torso_h > 1e-5 else 1.0
            return {
                name: {'x': (kp['x'] - cx) / scale, 'y': (kp['y'] - cy) / scale, 'conf': kp['conf']}
                for name, kp in kp_dict.items()
            }

        def flatten(kp):
            kp = normalize_kp(kp)
            return [v for pt in kp.values() for v in [pt['x'], pt['y'], pt['conf']]]

        x = np.array([flatten(buf[i][1]) for i in range(6)], dtype=np.float32)
        x = torch.tensor(x).unsqueeze(0)  # (1, 6, 51)

        with torch.no_grad():
            pred = self.action_model(x).argmax(1).item()

        self._action_labels[track_id] = self.label_encoder.classes_[pred]
        
    def save_pose_dataset(self, output_path: str):
        import os
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        existing = []
        if os.path.exists(output_path):
            with open(output_path, "r") as f:
                existing = json.load(f)
        
        combined = existing + self._pose_samples
        with open(output_path, "w") as f:
            json.dump(combined, f, indent=2)
        
        print(f"Saved {len(self._pose_samples)} new samples (total: {len(combined)}) → {output_path}")