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

RESULT_TIMEOUT_SECONDS = 2.0


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
        frame_index = int(uuid.uuid4().int % 10_000_000)  # معرّف فريد كافي لمطابقة الرد
        ok, jpeg = cv2.imencode(".jpg", frame)
        if not ok:
            return [], []

        header = json.dumps({"camera_id": self.camera_id, "frame_index": frame_index}).encode()
        payload = len(header).to_bytes(4, "big") + header + jpeg.tobytes()
        self.redis.rpush(REQUEST_QUEUE_KEY, payload)

        deadline = time.monotonic() + RESULT_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            msg = self.pubsub.get_message(timeout=0.1)
            if msg is None or msg["type"] != "message":
                continue
            data = json.loads(msg["data"])
            if data["frame_index"] != frame_index:
                continue  # رد لفريم قديم متأخر -- تجاهله وكمّل الانتظار

            detections = []
            for det in data["detections"]:
                x1, y1, x2, y2 = det["box"]
                if (x2 - x1) < self.min_box_width or (y2 - y1) < self.min_box_height:
                    continue
                detections.append(det)
            return detections, data["keypoints"]

        # ما وصل رد بالوقت المحدد (الـ inference service واقف أو مزحوم) --
        # نرجع قائمة فاضية بدل ما نعلّق البايبلاين كامل.
        print(f"[RemoteDetector] timeout بانتظار رد الـ inference service (camera={self.camera_id})")
        return [], []
