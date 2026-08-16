"""
inference_service.py
---------------------
عملية واحدة مستقلة، تحمّل نموذج YOLO مرة وحدة على GPU (context CUDA واحد
للنظام كامل بدل واحد لكل كاميرا)، وتستقبل طلبات الـ detection من كل
كاميرات run_live.py عبر قائمة انتظار Redis، وتعملها batching، وترجع
النتائج لكل كاميرا عبر Redis pub/sub.

طريقة التشغيل:
    python src/inference/inference_service.py

لازم يكون شغال *قبل* run_all_cameras.py، وبيضل شغال طول ما فيه كاميرات
تحتاج detection.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass

import cv2
import numpy as np
import redis
from ultralytics import YOLO

REQUEST_QUEUE_KEY = "inference:requests"
RESULT_CHANNEL_PREFIX = "inference:results:"

# أقصى عدد فريمات نجمعهم بالـ batch الواحد، وأقصى وقت ننتظره قبل ما نعالج
# batch جزئي (حتى ما نأخر كاميرا لحالها إذا الباقي ما بعتوش لسا).
MAX_BATCH_SIZE = 6
MAX_BATCH_WAIT_SECONDS = 0.05  # 50ms


@dataclass
class PendingRequest:
    camera_id: str
    frame_index: int
    frame: np.ndarray


class InferenceService:
    def __init__(
        self,
        model_path: str = "models/yolo/yolov8n-pose.pt",
        conf_threshold: float = 0.25,
        imgsz: int = 640,
        device: str = "cuda",
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
    ):
        # -- تحميل وحيد لموديل YOLO على GPU، context CUDA واحد فقط للنظام كامل --
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.imgsz = imgsz
        self.device = device

        self.redis = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

    def _collect_batch(self) -> list[PendingRequest]:
        """يجمع لغاية MAX_BATCH_SIZE طلب من قائمة الانتظار، بانتظار أقصاه
        MAX_BATCH_WAIT_SECONDS حتى ما توقف كاميرا الباقي لحالها."""
        batch: list[PendingRequest] = []
        deadline = time.monotonic() + MAX_BATCH_WAIT_SECONDS

        # أول عنصر: انتظار محجوب (blocking) لغاية ما يوصل شي، حتى ما نلف
        # busy-loop وإحنا مافي شي بالقائمة إطلاقًا.
        item = self.redis.blpop(REQUEST_QUEUE_KEY, timeout=1)
        if item is None:
            return batch
        batch.append(self._decode_request(item[1]))

        while len(batch) < MAX_BATCH_SIZE and time.monotonic() < deadline:
            raw = self.redis.lpop(REQUEST_QUEUE_KEY)
            if raw is None:
                time.sleep(0.002)
                continue
            batch.append(self._decode_request(raw))

        return batch

    @staticmethod
    def _decode_request(raw: bytes) -> PendingRequest:
        # الـ payload: JSON header بطول ثابت مفصول بـ '|' عن bytes الصورة
        # الخام (JPEG)، حتى نتجنب overhead تحويل base64 لكل فريم.
        header_len = int.from_bytes(raw[:4], "big")
        header = json.loads(raw[4 : 4 + header_len])
        jpeg_bytes = raw[4 + header_len :]
        frame = cv2.imdecode(np.frombuffer(jpeg_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
        return PendingRequest(
            camera_id=header["camera_id"],
            frame_index=header["frame_index"],
            frame=frame,
        )

    def _run_batch(self, batch: list[PendingRequest]) -> None:
        frames = [r.frame for r in batch]

        # -- استدعاء YOLO مرة وحدة لكل الفريمات سوا (batched inference) --
        results = self.model.predict(
            source=frames,
            conf=self.conf_threshold,
            imgsz=self.imgsz,
            classes=[0],
            device=self.device,
            verbose=False,
        )

        for req, result in zip(batch, results):
            detections = []
            keypoints_list = []
            kpts_data = result.keypoints.data.cpu().numpy() if result.keypoints is not None else None

            for i, box in enumerate(result.boxes):
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0])
                detections.append(
                    {
                        "track_id": None,
                        "box": [x1, y1, x2, y2],
                        "conf": round(conf, 4),
                        "class_id": 0,
                        "class_name": "person",
                    }
                )
                keypoints_list.append(
                    kpts_data[i].tolist() if kpts_data is not None else None
                )

            payload = json.dumps(
                {
                    "frame_index": req.frame_index,
                    "detections": detections,
                    "keypoints": keypoints_list,
                }
            )
            self.redis.publish(f"{RESULT_CHANNEL_PREFIX}{req.camera_id}", payload)

    def run_forever(self) -> None:
        print("[inference_service] جاهز، بانتظار الطلبات من الكاميرات...")
        while True:
            batch = self._collect_batch()
            if not batch:
                continue
            self._run_batch(batch)


if __name__ == "__main__":
    InferenceService().run_forever()
