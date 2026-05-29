import json
from pathlib import Path
from typing import Any
import cv2
from src.ai_models.detector import PersonDetector

class RestaurantMonitoringPipeline:
    
    def __init__(self, config_path: str = "config/config.json"):
        self.project_dir = Path.cwd()
        self.config_path = self.project_dir / config_path

        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        detector_config = self.config["detector"]

        self.detector = PersonDetector(
            model_name=detector_config.get("model", "yolov8n.pt"),
            conf_threshold=detector_config.get("conf_threshold", 0.4),
            imgsz=detector_config.get("imgsz", 480),
            min_box_width=detector_config.get("min_box_width", 20),
            min_box_height=detector_config.get("min_box_height", 20),
            device=detector_config.get("device", None),
        )

        paths_config = self.config["paths"]

        self.videos_index_path = self.project_dir / paths_config["videos_index"]
        self.detections_dir = self.project_dir / paths_config["detections_dir"]
        self.debug_frames_dir = self.project_dir / "data" / "debug" / "detection" / "frames"
        self.debug_videos_dir = self.project_dir / "data" / "debug" / "detection" / "videos"
        self.detections_dir.mkdir(parents=True, exist_ok=True)
        self.debug_frames_dir.mkdir(parents=True, exist_ok=True)
        self.debug_videos_dir.mkdir(parents=True, exist_ok=True)

    def process_frame(
        self,
        frame,
        camera_id: str,
        video_id: str,
        frame_index: int,
        original_fps: float,
    ) -> dict[str, Any]:

        time_seconds = frame_index / original_fps if original_fps > 0 else 0.0

        detections = self.detector.detect(frame)

        return {
            "camera_id": camera_id,
            "video_id": video_id,
            "frame_index": frame_index,
            "time_seconds": round(time_seconds, 3),
            "detections": detections,
        }

    def process_video(
        self,
        video_record: dict[str, Any],
        target_fps: int | None = None,
        max_seconds: int | None = None,
        save_debug_frames: bool | None = None,
        max_debug_frames: int | None = None,
        save_debug_video: bool | None = None,
        overwrite: bool = False,
    ) -> dict[str, Any]:
  
        detector_config = self.config["detector"]
        debug_config = self.config["debug"]

        if target_fps is None:
            target_fps = detector_config.get("target_fps", 2)

        if max_seconds is None:
            max_seconds = detector_config.get("max_seconds", None)

        if save_debug_frames is None:
            save_debug_frames = debug_config.get("save_debug_frames", False)

        if max_debug_frames is None:
            max_debug_frames = debug_config.get("max_debug_frames", 30)

        if save_debug_video is None:
            save_debug_video = debug_config.get("save_debug_video", False)

        camera_id = video_record["camera_id"]
        video_id = video_record["video_id"]
        video_path = self.project_dir / video_record["path"]

        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        output_detection_dir = self.detections_dir / camera_id
        output_debug_frames_dir = self.debug_frames_dir / camera_id / video_id
        output_debug_video_dir = self.debug_videos_dir / camera_id

        output_detection_dir.mkdir(parents=True, exist_ok=True)
        output_debug_frames_dir.mkdir(parents=True, exist_ok=True)
        output_debug_video_dir.mkdir(parents=True, exist_ok=True)

        output_json_path = output_detection_dir / f"{video_id}_detections.json"
        output_debug_video_path = output_debug_video_dir / f"{video_id}_debug.mp4"

        if output_json_path.exists() and not overwrite:
            print(f" Skipped existing file: {output_json_path}")
            return {
                "camera_id": camera_id,
                "video_id": video_id,
                "status": "skipped",
                "detections_path": str(output_json_path),
            }

        cap = cv2.VideoCapture(str(video_path))

        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")

        original_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if original_fps <= 0:
            original_fps = 25.0

        frame_step = max(1, int(original_fps / target_fps))

        if max_seconds is None:
            max_frames = frame_count
        else:
            max_frames = min(frame_count, int(max_seconds * original_fps))

        writer = None
        if save_debug_video:
            writer = cv2.VideoWriter(
                str(output_debug_video_path),
                cv2.VideoWriter_fourcc(*"mp4v"),
                target_fps,
                (width, height),
            )

        all_results = []
        frame_index = 0
        sampled_count = 0
        saved_debug_count = 0

        print(f"   Processing: {camera_id}/{video_id}")
        print(f"   Video path: {video_path}")
        print(f"   Original FPS: {original_fps:.2f}")
        print(f"   Target FPS: {target_fps}")
        print(f"   Frame step: {frame_step}")
        print(f"   Max seconds: {max_seconds}")
        print(f"   Output: {output_json_path}")

        while frame_index < max_frames:
            ret, frame = cap.read()

            if not ret:
                break

            if frame_index % frame_step == 0:
                frame_result = self.process_frame(
                    frame=frame,
                    camera_id=camera_id,
                    video_id=video_id,
                    frame_index=frame_index,
                    original_fps=original_fps,
                )

                all_results.append(frame_result)

                debug_frame = frame.copy()

                if save_debug_frames or save_debug_video:
                    self._draw_detections(debug_frame, frame_result["detections"])

                if save_debug_frames and saved_debug_count < max_debug_frames:
                    debug_frame_path = output_debug_frames_dir / f"frame_{frame_index:06d}.jpg"
                    cv2.imwrite(str(debug_frame_path), debug_frame)
                    saved_debug_count += 1

                if writer is not None:
                    writer.write(debug_frame)

                sampled_count += 1

                if sampled_count % 100 == 0:
                    print(f"   sampled frames processed: {sampled_count}")

            frame_index += 1

        cap.release()

        if writer is not None:
            writer.release()

        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)

        print(f"   Finished: {camera_id}/{video_id}")
        print(f"   Saved JSON: {output_json_path}")
        print(f"   Sampled frames: {len(all_results)}")
        print()

        return {
            "camera_id": camera_id,
            "video_id": video_id,
            "status": "processed",
            "detections_path": str(output_json_path),
            "sampled_frames": len(all_results),
            "target_fps": target_fps,
        }

    def process_all_videos(
        self,
        target_fps: int | None = None,
        max_seconds: int | None = None,
        overwrite: bool = False,
    ) -> list[dict[str, Any]]:

        if not self.videos_index_path.exists():
            raise FileNotFoundError(f"videos_index.json not found: {self.videos_index_path}")

        with open(self.videos_index_path, "r", encoding="utf-8") as f:
            video_records = json.load(f)

        results = []

        for video_record in video_records:
            result = self.process_video(
                video_record=video_record,
                target_fps=target_fps,
                max_seconds=max_seconds,
                overwrite=overwrite,
            )
            results.append(result)

        return results

    def _draw_detections(self, frame, detections: list[dict[str, Any]]) -> None:

        for det in detections:
            x1, y1, x2, y2 = det["box"]
            conf = det["conf"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.putText(
                frame,
                f"person {conf:.2f}",
                (x1, max(20, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )