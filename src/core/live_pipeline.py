from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import torch

from src.ai_models.detector import PersonDetector
from src.ai_models.tracker import RestaurantTracker
from src.zone_management.zone_manager import ZoneManager
from src.kbs.action_kbs import ActionKBS, PersonFact
from src.kbs.worker_kbs import WorkerKBS, WorkerFact
from src.kbs.table_kbs import TableKBS, TableFact
from src.kbs.reid_gallery import ReIDGallery
from src.core.classifiers import PoseLSTM


class LivePipeline:
    ZONE_TYPE_MAP: dict[str, str] = {
        "table_area"           : "table",
        "service_path"         : "walk",
        "hallway"              : "walk",
        "corridor"             : "walk",
        "open_area"            : "walk",
        "mixed_area"           : "walk",
        "entrance"             : "walk",
        "bathroom_entrance"    : "walk",
        "prayer_room_entrance" : "walk",
        "staff_area"           : "staff",
        "buffet"               : "staff",
        "cashier"              : "staff",
    }

    KEYPOINT_NAMES = [
        "nose", "left_eye", "right_eye", "left_ear", "right_ear",
        "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
        "left_wrist", "right_wrist", "left_hip", "right_hip",
        "left_knee", "right_knee", "left_ankle", "right_ankle"
    ]

    ROLE_COLORS = {
        "unknown":  (255, 255, 255),  # white
        "customer": (255, 100,   0),  # blue  (BGR)
        "worker":   (  0, 140, 255),  # orange (BGR)
    }

    def __init__(self, config_path: str = "config/config.json"):
        self.project_dir = Path.cwd()
        self.config_path = self.project_dir / config_path

        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        # -- Detector -------------------------------------------------------
        detector_config = self.config["detector"]
        self.detector = PersonDetector(
            model_name=detector_config.get("model"),
            conf_threshold=detector_config.get("conf_threshold"),
            imgsz=detector_config.get("imgsz"),
            min_box_width=detector_config.get("min_box_width"),
            min_box_height=detector_config.get("min_box_height"),
            device=detector_config.get("device"),
        )

        # -- Tracker --------------------------------------------------------
        tracker_config = self.config.get("tracker", {})
        self.tracker = RestaurantTracker(
            max_age=tracker_config.get("max_age"),
            n_init=tracker_config.get("n_init"),
            nms_max_overlap=tracker_config.get("nms_max_overlap"),
        )

        # -- Action model ---------------------------------------------------
        model_path = self.project_dir / "models/pose_lstm.pth"
        le_path    = self.project_dir / "models/label_encoder.pkl"

        self.action_model = PoseLSTM()
        self.action_model.load_state_dict(torch.load(model_path, map_location="cpu"))
        self.action_model.eval()

        with open(le_path, "rb") as f:
            self.label_encoder = pickle.load(f)

        # -- Pose buffers ---------------------------------------------------
        self._kp_buffer:    dict[int, list] = {}  # track_id -> [(frame_id, kp_dict)]
        self._action_labels: dict[int, str] = {}  # track_id -> latest label

        # -- Zone manager ---------------------------------------------------
        self.zone_manager = ZoneManager()

        # -- KBS engines (instantiated once, reset each frame) --------------
        self.action_kbs   = ActionKBS()
        # self.worker_kbs   = WorkerKBS()
        # self.table_kbs    = TableKBS()
        self.reid_gallery = ReIDGallery()

        # KBS engines are re-instantiated each cycle in _run_kbs to avoid Experta lru_cache deadlock

        # -- Per-track state ------------------------------------------------
        self._person_roles:        dict[int, str]   = {}  # track_id -> role
        self._global_ids:          dict[int, str]   = {}  # track_id -> global_id
        self._action_frame_counts: dict[int, int]   = {}  # track_id -> consecutive frames
        self._last_action_zone:    dict[int, tuple] = {}  # track_id -> (action, zone_type)
        self._worker_states:       dict[str, str]   = {}  # global_id -> worker state

        # -- Table state ----------------------------------------------------
        self._table_customer_counts: dict[str, int]  = {}  # zone_id -> count
        self._table_was_served:      dict[str, bool] = {}  # zone_id -> served flag

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def process_frame(
        self,
        frame,
        camera_id,
        video_id,
        frame_index,
        time_seconds,
        pose_stride=None,
    ):
        detections, keypoints_list = self.detector.detect_with_pose(frame)
        tracked_objects = self.tracker.update(detections, frame=frame)
        tracked_objects = self.enrich_tracks_with_zones(camera_id, tracked_objects)
        person_crops    = self.crop_persons(frame, tracked_objects)

        if pose_stride is None or frame_index % pose_stride == 0:
            self._extract_pose_from_detections(
                frame, video_id, frame_index,
                detections, keypoints_list, tracked_objects,
            )
            self._run_kbs(tracked_objects, person_crops)

        return {
            "camera_id":      camera_id,
            "video_id":       video_id,
            "frame_index":    frame_index,
            "time_seconds":   time_seconds,
            "detections":     detections,
            "tracked_objects": tracked_objects,
            "person_crops":   person_crops,
        }

    def enrich_tracks_with_zones(
        self,
        camera_id: str,
        tracked_objects: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        enriched_tracks: list[dict[str, Any]] = []

        for obj in tracked_objects:
            zone = self.zone_manager.get_bbox_zone(
                camera_id=camera_id,
                box=obj.get("box", [0, 0, 0, 0]),
            )
            enriched_obj = dict(obj)
            enriched_obj["zone"] = zone
            raw_zone_type = zone.get("zone_type", "unknown") if zone else "unknown"
            enriched_obj["zone_type_normalized"] = self.ZONE_TYPE_MAP.get(raw_zone_type, "unknown")
            enriched_tracks.append(enriched_obj)

        return enriched_tracks

    def crop_persons(
        self,
        frame,
        tracked_objects: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        crops: list[dict[str, Any]] = []
        height, width = frame.shape[:2]

        for obj in tracked_objects:
            box = obj.get("box", [0, 0, 0, 0])
            x1, y1, x2, y2 = [int(v) for v in box]

            x1 = max(0, min(width,  x1))
            x2 = max(0, min(width,  x2))
            y1 = max(0, min(height, y1))
            y2 = max(0, min(height, y2))

            if x1 >= x2 or y1 >= y2:
                continue

            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            crops.append({
                "track_id": obj.get("track_id"),
                "zone":     obj.get("zone", {}),
                "box":      [x1, y1, x2, y2],
                "crop":     crop.copy(),
            })

        return crops

    def draw_zones(self, frame, camera_id: str) -> None:
        camera_zones = (
            self.zone_manager.zones_config
            .get(camera_id, {})
            .get("zones", [])
        )

        for zone in camera_zones:
            points = zone.get("points", [])
            if len(points) < 3:
                continue

            polygon = np.array(points, dtype=np.int32)
            cv2.polylines(frame, [polygon], isClosed=True, color=(0, 255, 0), thickness=2)

    def draw_tracks(self, frame, tracked_objects: list[dict[str, Any]]) -> None:
        for obj in tracked_objects:
            box = obj.get("box", [0, 0, 0, 0])
            x1, y1, x2, y2 = map(int, box)
            track_id = obj.get("track_id", "?")

            action  = self._action_labels.get(track_id, "...")
            role    = self._person_roles.get(track_id, "unknown")
            gid     = self._global_ids.get(track_id)
            w_state = self._worker_states.get(gid, "") if gid else ""
            color   = self.ROLE_COLORS.get(role, (255, 255, 255))

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            label = f"{action} | {role}"
            if w_state:
                label += f" | {w_state}"
            cv2.putText(
                frame, label,
                (x1, max(35, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,
            )

            cv2.putText(
                frame, f"id:{track_id}",
                (x1 + 4, y1 + 18),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2,
            )

            if gid:
                gid_short = gid.replace("worker_", "")
                cv2.putText(
                    frame, f"gid:{gid_short}",
                    (x1 + 4, y1 + 38),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 105, 255), 2,
                )

    # -----------------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------------

    def _extract_pose_from_detections(
        self,
        frame,
        video_id,
        frame_index,
        detections,
        keypoints_list,
        tracked_objects,
    ) -> None:
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

    def _match_to_track(self, pose_box, tracked_objects) -> int | None:
        best_iou, best_id = 0.0, None
        px1, py1, px2, py2 = pose_box

        for obj in tracked_objects:
            tx1, ty1, tx2, ty2 = obj["box"]
            ix1 = max(px1, tx1)
            iy1 = max(py1, ty1)
            ix2 = min(px2, tx2)
            iy2 = min(py2, ty2)
            inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
            if inter == 0:
                continue
            union = (px2 - px1) * (py2 - py1) + (tx2 - tx1) * (ty2 - ty1) - inter
            iou = inter / union if union > 0 else 0
            if iou > best_iou:
                best_iou, best_id = iou, obj["track_id"]

        return best_id if best_iou > 0.4 else None

    def _predict_action(self, track_id: int, frame_id: int, kp_dict: dict) -> None:
        buf = self._kp_buffer.setdefault(track_id, [])
        buf.append((frame_id, kp_dict))

        # Drop frames with large gaps
        while len(buf) > 1 and buf[-1][0] - buf[-2][0] >= 200:
            buf.pop(0)

        if len(buf) > 3:
            buf.pop(0)

        if len(buf) < 3:
            return

        def normalize_kp(kp):
            lh = kp.get("left_hip",       {"x": 0, "y": 0, "conf": 0})
            rh = kp.get("right_hip",      {"x": 0, "y": 0, "conf": 0})
            ls = kp.get("left_shoulder",  {"x": 0, "y": 0, "conf": 0})
            rs = kp.get("right_shoulder", {"x": 0, "y": 0, "conf": 0})
            cx = (lh["x"] + rh["x"]) / 2
            cy = (lh["y"] + rh["y"]) / 2
            shoulder_y = (ls["y"] + rs["y"]) / 2
            torso_h    = abs(cy - shoulder_y)
            scale      = torso_h if torso_h > 1e-5 else 1.0
            return {
                name: {
                    "x":    (pt["x"] - cx) / scale,
                    "y":    (pt["y"] - cy) / scale,
                    "conf": pt["conf"],
                }
                for name, pt in kp.items()
            }

        def flatten(kp):
            kp = normalize_kp(kp)
            return [v for pt in kp.values() for v in (pt["x"], pt["y"], pt["conf"])]

        x = np.array([flatten(buf[i][1]) for i in range(3)], dtype=np.float32)
        x = torch.tensor(x).unsqueeze(0)  # (1, 3, 51)

        with torch.no_grad():
            pred = self.action_model(x).argmax(1).item()

        self._action_labels[track_id] = self.label_encoder.classes_[pred]

    def _run_kbs(self, tracked_objects: list[dict], person_crops: list[dict]) -> None:
        crop_by_id = {
            c["track_id"]: c["crop"]
            for c in person_crops
            if c.get("crop") is not None
        }

        # -- Update action_frame_counts (reset if action or zone changed) ---
        for obj in tracked_objects:
            tid       = obj["track_id"]
            action    = self._action_labels.get(tid, "unknown")
            zone_type = obj.get("zone_type_normalized", "unknown")
            key       = (action, zone_type)

            if self._last_action_zone.get(tid) != key:
                self._action_frame_counts[tid] = 0
                self._last_action_zone[tid]    = key
            else:
                self._action_frame_counts[tid] = self._action_frame_counts.get(tid, 0) + 1

        # -- Re-ID pre-check: match unknowns against existing gallery --------
        active_gids = set(self._global_ids.values())
        for obj in tracked_objects:
            tid  = obj["track_id"]
            role = self._person_roles.get(tid, "unknown")
            if role != "unknown" or tid in self._global_ids:
                continue
            crop = crop_by_id.get(tid)
            if crop is None:
                continue
            embedding   = self.reid_gallery._extract(crop)
            matched_gid = self.reid_gallery._match(embedding)
            if matched_gid is not None and matched_gid not in active_gids:
                self._person_roles[tid] = "worker"
                self._global_ids[tid]   = matched_gid
                active_gids.add(matched_gid)
                print(f"[ReID] track {tid} matched existing gallery → {matched_gid}")

        # -- ActionKBS: classify unknowns -----------------------------------
        self.action_kbs = ActionKBS()
        self.action_kbs.reset()
        for obj in tracked_objects:
            tid  = obj["track_id"]
            role = self._person_roles.get(tid, "unknown")
            if role != "unknown":
                continue  # already classified

            self.action_kbs.declare(PersonFact(
                track_id         = tid,
                role             = "unknown",
                action           = self._action_labels.get(tid, "unknown"),
                zone_type        = obj.get("zone_type_normalized", "unknown"),
                pose_frame_count = self._action_frame_counts.get(tid, 0),
                re_id_ready      = False,
            ))
        self.action_kbs.run()

        # -- Read ActionKBS results, Re-ID promoted workers -----------------
        for fact in self.action_kbs.facts.values():
            if not isinstance(fact, PersonFact):
                continue
            tid  = fact["track_id"]
            role = fact["role"]
            if role == "unknown":
                continue

            self._person_roles[tid] = role

            if role == "worker" and tid not in self._global_ids:
                crop = crop_by_id.get(tid)
                if crop is not None:
                    global_id = self.reid_gallery.process(tid, crop)
                    self._global_ids[tid] = global_id

        # -- Update table customer counts -----------------------------------
        zone_customer_counts: dict[str, int] = {}
        for obj in tracked_objects:
            tid  = obj["track_id"]
            role = self._person_roles.get(tid, "unknown")
            if role != "customer":
                continue
            zone    = obj.get("zone") or {}
            zone_id = zone.get("zone_id")
            if zone_id:
                zone_customer_counts[zone_id] = zone_customer_counts.get(zone_id, 0) + 1

        # -- Check for serving events to set was_served flag ----------------
        for obj in tracked_objects:
            tid       = obj["track_id"]
            role      = self._person_roles.get(tid, "unknown")
            action    = self._action_labels.get(tid, "unknown")
            zone      = obj.get("zone") or {}
            zone_id   = zone.get("zone_id")
            zone_type = obj.get("zone_type_normalized", "unknown")

            if (
                role == "worker"
                and action == "serving"
                and zone_type == "table"
                and zone_id
                and zone_customer_counts.get(zone_id, 0) > 0
            ):
                self._table_was_served[zone_id] = True

        # # -- TableKBS -------------------------------------------------------
        # all_zone_ids = (
        #     set(zone_customer_counts)
        #     | set(self._table_customer_counts)
        #     | set(self._table_was_served)
        # )

        # self.table_kbs = TableKBS()
        # self.table_kbs.reset()
        # for zone_id in all_zone_ids:
        #     self.table_kbs.declare(TableFact(
        #         zone_id        = zone_id,
        #         customer_count = zone_customer_counts.get(zone_id, 0),
        #         was_served     = self._table_was_served.get(zone_id, False),
        #     ))
        # self.table_kbs.run()
        # self._table_customer_counts = zone_customer_counts

        # # -- WorkerKBS ------------------------------------------------------
        # self.worker_kbs = WorkerKBS()
        # self.worker_kbs.reset()
        # for obj in tracked_objects:
        #     tid  = obj["track_id"]
        #     role = self._person_roles.get(tid, "unknown")
        #     if role != "worker":
        #         continue
        #     global_id = self._global_ids.get(tid, f"local_{tid}")
        #     self.worker_kbs.declare(WorkerFact(
        #         global_id        = global_id,
        #         action           = self._action_labels.get(tid, "unknown"),
        #         zone_type        = obj.get("zone_type_normalized", "unknown"),
        #         camera_type      = "customer_facing",
        #         pose_frame_count = self._action_frame_counts.get(tid, 0),
        #         re_id_ready      = False,
        #     ))
        # self.worker_kbs.run()

        # # -- Read WorkerKBS results -----------------------------------------
        # for fact in self.worker_kbs.facts.values():
        #     if not isinstance(fact, WorkerFact):
        #         continue
        #     self._worker_states[fact["global_id"]] = fact["state"]