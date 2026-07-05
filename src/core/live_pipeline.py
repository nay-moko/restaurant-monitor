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
from src.kbs.reid_gallery import ReIDGallery, SessionGallery
from src.kbs.role_engine import (
    RoleEngine, ObservationFact, ScoreAccumulator, MergeRequest, RoleDecision,
)
from src.core.classifiers import PoseLSTM


class LivePipeline:
    ZONE_TYPE_MAP: dict[str, str] = {
        "table_area"           : "table",   # broad container zone
        "table"                : "table",   # single table zone (nested inside table_area) — was missing, caused zone_type_normalized="unknown"
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
        self.table_kbs    = TableKBS()
        self.reid_gallery = ReIDGallery()
        self.session_gallery = SessionGallery(ttl_seconds=1800)  # 30 mins TTL

        # KBS engines are re-instantiated each cycle in _run_kbs to avoid Experta lru_cache deadlock

        # -- Per-track state ------------------------------------------------
        self._person_roles:        dict[int, str]   = {}  # track_id -> role
        self._global_ids:          dict[int, str]   = {}  # track_id -> global_id
        self._action_frame_counts: dict[int, int]   = {}  # track_id -> consecutive frames
        self._last_action_zone:    dict[int, tuple] = {}  # track_id -> (action, zone_type)
        self._worker_states:       dict[str, str]   = {}  # global_id -> worker state

        # -- RoleEngine persistent state ------------------------------------
        self._role_accumulators: dict[str, dict]  = {}  # global_id -> accumulator dict
        self._gid_track_counts: dict[str, set[int]] = {}  # global_id -> set of track_ids

        # -- Table state ----------------------------------------------------
        self._table_customer_counts: dict[str, int]  = {}  # zone_id -> count
        self._table_was_served:      dict[str, bool] = {}  # zone_id -> served flag
        self._table_states:           dict[str, str]  = {}  # zone_id -> state
        self.person_state: list[dict[str, Any]] = []
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
        tracked_objects = self.enrich_tracks_with_zones(
            camera_id,
            tracked_objects,
            detections,
            keypoints_list,
        )
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
            "tables_current_state": self.get_tables_current_state(camera_id),
        }

    def enrich_tracks_with_zones(
        self,
        camera_id: str,
        tracked_objects: list[dict[str, Any]],
        detections: list[dict[str, Any]] | None = None,
        keypoints_list: list[np.ndarray] | None = None,
    ) -> list[dict[str, Any]]:
        enriched_tracks: list[dict[str, Any]] = []

        pose_points_by_track_id: dict[int, list[int]] = {}
        kpts_by_track_id: dict[int, np.ndarray] = {}
        if detections and keypoints_list:
            for det, kpts in zip(detections, keypoints_list):
                if kpts is None:
                    continue

                track_id = self._match_to_track(det.get("box", [0, 0, 0, 0]), tracked_objects)
                if track_id is None:
                    continue

                pose_points_by_track_id[track_id] = self._estimate_zone_point(det.get("box", [0, 0, 0, 0]), kpts)
                kpts_by_track_id[track_id] = kpts

        for obj in tracked_objects:
            track_id = obj.get("track_id")
            box = obj.get("box", [0, 0, 0, 0])
            zone_point = pose_points_by_track_id.get(track_id)
            kpts = kpts_by_track_id.get(track_id)

            if zone_point is None:
                zone_point = self._estimate_zone_point(box, None)

            zone = self.zone_manager.get_bbox_zone(
                camera_id=camera_id,
                box=box,
                keypoints=kpts,
            )
            enriched_obj = dict(obj)
            enriched_obj["zone"] = zone
            raw_zone_type = zone.get("zone_type", "unknown") if zone else "unknown"
            enriched_obj["zone_type_normalized"] = self.ZONE_TYPE_MAP.get(raw_zone_type, "unknown")
            enriched_obj["zone_name"] = zone.get("zone_name", "Unknown") if zone else "Unknown"
            enriched_obj["zone_point"] = zone_point
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

    def get_tables_current_state(self, camera_id: str) -> dict[str, str]:
        camera_zones = self.zone_manager.zones_config.get(camera_id, {}).get("zones", [])

        summary: dict[str, str] = {}
        for zone in camera_zones:
            if zone.get("zone_type") in ("table", "table_area"):
                zone_id = zone.get("zone_id")
                if zone_id:
                    summary[zone_id] = self._table_states.get(zone_id, "empty")
        return summary

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
            zone_type = obj.get("zone_type_normalized", "unknown")
            zone_name = obj.get("zone_name", "Unknown")
            track_id  = obj.get("track_id", "?")
            action    = self._action_labels.get(track_id, "...")
            role      = self._person_roles.get(track_id, "unknown")
            gid       = self._global_ids.get(track_id)
            color     = self.ROLE_COLORS.get(role, (255, 255, 255))

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            label = f"{action} | {role} | {zone_type}"
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
    def _update_person_state(self, global_id: str, local_id: int, zone_type: str):
        """
        تحديث قاعدة البيانات في الذاكرة (list of dicts) لكل شخص بناءً على الفريمات.
        """
        from datetime import datetime, timedelta

        # 1. البحث عن السجل الحالي للشخص عبر الـ global_id
        person_record = next((row for row in self.person_state if row["global_id"] == global_id), None)
        
        # 2. إذا كان الشخص يظهر لأول مرة في النظام تماماً
        if person_record is None:
            new_row = {
                "global_id": global_id,
                "local_id": local_id,
                "current_location": zone_type, # يتم تخزين الزون الموحدة (table, walk, staff)
                "Entrance date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Duration": "00:00:00",
                "_internal_frames_count": 1 # عداد الفريمات الداخلي للحساب الدقيق
            }
            self.person_state.append(new_row)
            return

        # 3. إذا كان الشخص موجوداً مسبقاً ولكن انتقل إلى زون جديدة
        if person_record["current_location"] != zone_type:
            person_record["current_location"] = zone_type
            person_record["Entrance date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            person_record["_internal_frames_count"] = 1
            person_record["Duration"] = "00:00:00"
            person_record["local_id"] = local_id # تحديث الـ local_id في حال تغير بفعل الـ DeepSORT
        else:
            # 4. الشخص لا يزال مستقراً في نفس المكان -> نزيد عداد الفريمات
            person_record["_internal_frames_count"] += 1
            person_record["local_id"] = local_id # نحدث الـ local_id باستمرار لضمان ربطه بالـ Bounding Box الحالي
            
            # حساب المدة الحقيقية: كل فريم يساوي نصف ثانية لأن النظام يعالج (2fps)
            total_seconds = person_record["_internal_frames_count"] / 2.0
            
            # تحويل الثواني إلى صيغة وقت مقروءة ومطابقة لطلب المعيد (HH:MM:SS)
            duration_timedelta = timedelta(seconds=int(total_seconds))
            person_record["Duration"] = str(duration_timedelta) 

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

    def _estimate_zone_point(
        self,
        box: list[int | float],
        kpts: np.ndarray | None,
        conf_threshold: float = 0.25,
    ) -> list[int]:
        x1, y1, x2, y2 = [int(v) for v in box]

        def visible_point(index: int) -> tuple[float, float] | None:
            if kpts is None or index >= len(kpts):
                return None
            x, y, conf = kpts[index]
            if float(conf) < conf_threshold:
                return None
            return float(x), float(y)

        def average_visible_points(indices: tuple[int, ...]) -> list[int] | None:
            points = [visible_point(index) for index in indices]
            visible_points = [point for point in points if point is not None]
            if visible_points:
                avg_x = sum(point[0] for point in visible_points) / len(visible_points)
                avg_y = sum(point[1] for point in visible_points) / len(visible_points)
                return [int(round(avg_x)), int(round(avg_y))]
            return None

        # Explicit priority order:
        # 1) ankles visible
        # 2) hips visible
        # 3) shoulders visible
        # 4) upper body only -> use the box center
        ankles_point = average_visible_points((15, 16))
        if ankles_point is not None:
            return ankles_point

        hips_point = average_visible_points((11, 12))
        if hips_point is not None:
            return hips_point

        shoulders_point = average_visible_points((5, 6))
        if shoulders_point is not None:
            return shoulders_point

        return [int(round((x1 + x2) / 2)), int(round((y1 + y2) / 2))]

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
            previous_duration_frames = self._action_frame_counts.get(tid, 0)

            if self._last_action_zone.get(tid) != key:
                self._action_frame_counts[tid] = 0
                self._last_action_zone[tid]    = key
            else:
                self._action_frame_counts[tid] = self._action_frame_counts.get(tid, 0) + 1

            obj["previous_duration_frames"] = previous_duration_frames

        # -- Re-ID pre-check: match unknowns against existing gallery --------
        self.session_gallery.purge_old()

        for obj in tracked_objects:
            tid  = obj["track_id"]
            
            # If we already linked this track ID in a previous frame to a session ID, just touch it
            if tid in self._global_ids:
                gid = self._global_ids[tid]
                if gid.startswith("session_"):
                    self.session_gallery.touch(gid)
                continue

            crop = crop_by_id.get(tid)
            if crop is None:
                continue

            # Crop too small/low-res → embedding is unreliable and is exactly
            # what causes worker X's identity to get handed to a blurry,
            # unrelated person Y. Skip ReID this frame; track stays without
            # a global_id and will be retried once a better crop comes in.
            crop_h, crop_w = crop.shape[:2]
            if crop_w < self.reid_gallery.MIN_CROP_WIDTH or crop_h < self.reid_gallery.MIN_CROP_HEIGHT:
                print(f"[ReID] track {tid}: crop too small ({crop_w}x{crop_h}) — skipping ReID this frame")
                continue

            embedding = self.reid_gallery._extract(crop)

            # 1. Check permanent Worker Gallery
            matched_worker = self.reid_gallery._match(embedding)
            if matched_worker is not None:
                self._person_roles[tid] = "worker"
                self._global_ids[tid]   = matched_worker
                self._gid_track_counts.setdefault(matched_worker, set()).add(tid)
                print(f"[ReID] track {tid} matched permanent worker → {matched_worker}")
                continue

            # 2. Check temporary Session Gallery
            matched_session = self.session_gallery.match(embedding)
            if matched_session is not None:
                self._global_ids[tid] = matched_session
                self._gid_track_counts.setdefault(matched_session, set()).add(tid)
                self.session_gallery.update_seen(matched_session, embedding)
                print(f"[ReID] track {tid} matched active session → {matched_session}")
                continue

            # 3. New person: register in Session Gallery
            new_session = self.session_gallery.register(embedding)
            self._global_ids[tid] = new_session
            self._gid_track_counts.setdefault(new_session, set()).add(tid)
            print(f"[ReID] track {tid} registered as new session → {new_session}")

        # -- RoleEngine: classify all persons via point-based evidence ------
        engine = RoleEngine()
        engine.reset()

        # Re-inject persistent accumulators from previous cycle
        for gid, acc in self._role_accumulators.items():
            engine.declare(ScoreAccumulator(
                global_id=gid,
                worker_score=acc["worker_score"],
                customer_score=acc["customer_score"],
                confirmed_role=acc["confirmed_role"],
                cycle_count=acc["cycle_count"],
                visited_tables=acc.get("visited_tables", ()),
                visited_staff=acc.get("visited_staff", False),
                zone_history=acc.get("zone_history", ()),
            ))

        # Declare one ObservationFact per tracked person
        for obj in tracked_objects:
            tid = obj["track_id"]
            gid = self._global_ids.get(tid, f"local_{tid}")
            
            zone = obj.get("zone") or {}
            zone_id = zone.get("zone_id", "unknown")

            engine.declare(ObservationFact(
                track_id         = tid,
                global_id        = gid,
                action           = self._action_labels.get(tid, "unknown"),
                zone_type        = obj.get("zone_type_normalized", "unknown"),
                zone_id          = zone_id,
                pose_frame_count = self._action_frame_counts.get(tid, 0),
                previous_duration_frames = obj.get("previous_duration_frames", 0),
                appearance_count = len(self._gid_track_counts.get(gid, set())),
                previous_role    = self._person_roles.get(tid, "unknown"),
            ))

        engine.run()
        decisions = engine.get_decisions()

        # أضف هذا التكرار لطباعة النقاط لكل شخص في الـ Terminal فورياً:
        for track_id, info in decisions.items():
            print(f"[Track {track_id}] ID: {info['global_id']} | Role: {info['role']} | Confidence: {info['confidence']}")
            print(f"   -> Worker Score: {info['worker_score']} | Customer Score: {info['customer_score']}")
            print("-" * 40)

        # Read RoleEngine decisions
        for tid, decision in engine.get_decisions().items():
            role = decision["role"]
            if role != "unknown":
                self._person_roles[tid] = role
            # Log scores for debugging
            print(
                f"  [RoleEngine] track {tid}: "
                f"role={decision['role']}  "
                f"conf={decision['confidence']:.2f}  "
                f"ws={decision['worker_score']:.1f}  "
                f"cs={decision['customer_score']:.1f}"
            )

            # Re-ID Promotion: register newly confirmed workers in permanent gallery
            gid = self._global_ids.get(tid)
            if role == "worker" and gid and gid.startswith("session_"):
                crop = crop_by_id.get(tid)
                if crop is not None:
                    embedding = self.reid_gallery._extract(crop)
                    new_worker_gid = self.reid_gallery._register(embedding)
                    
                    # Rename in our track mappings
                    self._global_ids[tid] = new_worker_gid
                    
                    # Rename in the accumulators dict so RoleEngine continues next cycle
                    if gid in self._role_accumulators:
                        acc = self._role_accumulators.pop(gid)
                        acc["global_id"] = new_worker_gid
                        self._role_accumulators[new_worker_gid] = acc
                        
                    # Transfer track counts
                    if gid in self._gid_track_counts:
                        counts = self._gid_track_counts.pop(gid)
                        self._gid_track_counts.setdefault(new_worker_gid, set()).update(counts)
                        
                    # Rename in person_state to preserve duration
                    for row in self.person_state:
                        if row["global_id"] == gid:
                            row["global_id"] = new_worker_gid
                        
                    # Remove from session gallery
                    self.session_gallery.remove(gid)
                    print(f"[ReID] Promoted {gid} to permanent worker → {new_worker_gid}")

        # Persist accumulators for next cycle
        self._role_accumulators = engine.get_accumulators()
        for obj in tracked_objects:
            tid = obj["track_id"]
            
            # الحصول على الـ global_id الموحد المحسوب بواسطة الـ ReID والـ RoleEngine
            # وإذا لم يكن مسجلاً بعد كعامل، نأخذ المعرف المؤقت المعتمد في كودكم [source: 1]
            gid = self._global_ids.get(tid, f"local_{tid}") 
            
            # الحصول على اسم الزون الموحد الجاهز في الكود (table, walk, staff) [source: 1]
            zone_type = obj.get("zone_type_normalized", "unknown") 
            
            # استدعاء دالة التحديث لبناء الـ list of dicts وحساب الـ duration
            self._update_person_state(
                global_id=gid,
                local_id=tid,
                zone_type=zone_type
            )
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

        # -- TableKBS: derive empty / occupied / dirty ---------------------
        all_zone_ids = (
            set(zone_customer_counts)
            | set(self._table_customer_counts)
            | set(self._table_was_served)
        )

        self.table_kbs.reset()
        for zone_id in all_zone_ids:
            self.table_kbs.declare(TableFact(
                zone_id=zone_id,
                customer_count=zone_customer_counts.get(zone_id, 0),
                was_served=self._table_was_served.get(zone_id, False),
            ))
        self.table_kbs.run()

        self._table_states = {
            fact["zone_id"]: fact["state"]
            for fact in self.table_kbs.facts.values()
            if isinstance(fact, TableFact)
        }
        self._table_customer_counts = zone_customer_counts

    # أضف هذا السطر في نهاية دالة _run_kbs للتحقق
        print("\n=== LIVE DATABASE STATE ===")
        for row in self.person_state:
            print(f"ID: {row['global_id']} | Loc: {row['current_location']} | Entry: {row['Entrance date']} | Dur: {row['Duration']}")
        print("===========================\n")      
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