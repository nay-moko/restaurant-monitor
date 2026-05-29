from typing import Any
import numpy as np
from ultralytics import YOLO


class PersonDetector:
    def __init__(
        self,
        model_name: str = "yolov8n.pt",
        conf_threshold: float = 0.4,
        imgsz: int = 480,
        min_box_width: int = 20,
        min_box_height: int = 20,
        device: str | None = None,
    ):
        self.model_name = model_name
        self.conf_threshold = conf_threshold
        self.imgsz = imgsz
        self.min_box_width = min_box_width
        self.min_box_height = min_box_height
        self.device = device

        self.model = YOLO(model_name)

    def detect(self, frame: np.ndarray) -> list[dict[str, Any]]:

        predict_kwargs = {
            "source": frame,
            "conf": self.conf_threshold,
            "imgsz": self.imgsz,
            "classes": [0],  
            "verbose": False,
        }

        if self.device is not None:
            predict_kwargs["device"] = self.device

        results = self.model.predict(**predict_kwargs)

        detections = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

                width = x2 - x1
                height = y2 - y1

                if width < self.min_box_width or height < self.min_box_height:
                    continue

                detections.append(
                    {
                        "track_id": None,
                        "box": [x1, y1, x2, y2],
                        "conf": round(conf, 4),
                        "class_id": 0,
                        "class_name": "person",
                    }
                )

        return detections