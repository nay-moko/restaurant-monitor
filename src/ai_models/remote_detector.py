"""
remote_detector.py
-------------------
بديل PersonDetector -- بدل ما يحمّل YOLO محليًا ويفتح CUDA context خاص فيه،
هاد الكلاس يبعت الفريم لـ src/inference/inference_service.py عبر Redis
وياخد النتيجة. نفس الـ interface تمامًا متل PersonDetector.detect_with_pose
حتى نقدر نبدّل واحد بالتاني بسطر واحد بـ live_pipeline.py.
"""

from __future__ import annotations

import json
import time
import uuid
from typing import Any

import cv2
import numpy as np
import redis

from src.inference.inference_service import REQUEST_QUEUE_KEY, RESULT_CHANNEL_PREFIX

RESULT_TIMEOUT_SECONDS = 1.5
INFER_MAX_SIDE = 640   # لازم يساوي detector.imgsz بالكونفيغ
JPEG_QUALITY = 80

class RemoteDetector:
    def __init__(
        self,
        camera_id: str,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        min_box_width: int = 2,
        min_box_height: int = 2,
    ):
        self.camera_id = camera_id
        self.min_box_width = min_box_width
        self.min_box_height = min_box_height

        self.redis = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(f"{RESULT_CHANNEL_PREFIX}{camera_id}")



    def detect_with_pose(self, frame: np.ndarray) -> tuple[list[dict], list[Any] | None]:
        frame_index = int(uuid.uuid4().int % 10_000_000)

        # -- تصغير قبل الترميز: الموديل أصلًا بيصغّر لـ imgsz، فما في أي خسارة دقة --
        h, w = frame.shape[:2]
        scale = min(1.0, INFER_MAX_SIDE / float(max(h, w)))
        if scale < 1.0:
            small = cv2.resize(
                frame, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA
            )
        else:
            small = frame

        ok, jpeg = cv2.imencode(".jpg", small, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
        if not ok:
            return [], []

        header = json.dumps(
            {
                "camera_id": self.camera_id,
                "frame_index": frame_index,
                "ts": time.time(),  # حتى السيرفس يقدر يرمي الطلبات القديمة
            }
        ).encode()
        payload = len(header).to_bytes(4, "big") + header + jpeg.tobytes()
        self.redis.rpush(REQUEST_QUEUE_KEY, payload)

        inv = 1.0 / scale if scale > 0 else 1.0
        deadline = time.monotonic() + RESULT_TIMEOUT_SECONDS

        while time.monotonic() < deadline:
            msg = self.pubsub.get_message(timeout=0.1)
            if msg is None or msg["type"] != "message":
                continue
            data = json.loads(msg["data"])
            if data["frame_index"] != frame_index:
                continue

            detections = []
            keypoints = []
            raw_kpts = data.get("keypoints") or []

            for i, det in enumerate(data["detections"]):
                # -- إرجاع الإحداثيات لمقياس الفريم الأصلي --
                x1, y1, x2, y2 = [int(round(v * inv)) for v in det["box"]]
                if (x2 - x1) < self.min_box_width or (y2 - y1) < self.min_box_height:
                    continue
                det = dict(det)
                det["box"] = [x1, y1, x2, y2]
                detections.append(det)

                kp = raw_kpts[i] if i < len(raw_kpts) else None
                if kp is not None:
                    kp = [[p[0] * inv, p[1] * inv] + list(p[2:]) for p in kp]
                keypoints.append(kp)

            return detections, keypoints

        print(f"[RemoteDetector] timeout (camera={self.camera_id})", flush=True)
        return [], []
