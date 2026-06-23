from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.core.live_pipeline import LivePipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the live in-memory pipeline")
    parser.add_argument("--source", default="0", help="Camera index or path to a video file")
    parser.add_argument("--camera-id", default="live_camera", help="Camera label used in analytics")
    parser.add_argument("--video-id", default="live_stream", help="Stream label used in analytics")
    parser.add_argument("--first-video", action="store_true", help="Use the first recorded video from videos_index.json")
    parser.add_argument("--videos-index", default="data/metadata/videos/videos_index.json", help="Path to videos_index.json")
    parser.add_argument("--config", default="config/config.json", help="Project config path")
    parser.add_argument("--max-frames", type=int, default=100, help="Optional frame limit for testing")
    parser.add_argument("--save-crops-dir", default="data/debug/crops", help="Optional directory to save person crops for RE-ID prep")
    parser.add_argument("--show", action="store_true", help="Show annotated frames in a window")
    return parser.parse_args()


def open_capture(source: str) -> cv2.VideoCapture:
    if source.isdigit():
        return cv2.VideoCapture(int(source))
    return cv2.VideoCapture(source)


def load_first_video_path(videos_index_path: str) -> tuple[str, str, str]:
    index_path = Path(videos_index_path)
    if not index_path.exists():
        raise FileNotFoundError(f"Video index not found: {index_path}")

    with open(index_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    if not records:
        raise ValueError(f"No video records found in: {index_path}")

    first_record = records[0]
    return first_record["path"], first_record["camera_id"], first_record["video_id"]


def main() -> None:
    args = parse_args()
    pipeline = LivePipeline(config_path=args.config)

    source = args.source
    camera_id = args.camera_id
    video_id = args.video_id

    if args.first_video:
        source, camera_id, video_id = load_first_video_path(args.videos_index)

    capture = open_capture(source)

    if not capture.isOpened():
        raise ValueError(f"Cannot open video source: {source}")

    crop_dir = Path(args.save_crops_dir) if args.save_crops_dir else None
    if crop_dir is not None:
        crop_dir.mkdir(parents=True, exist_ok=True)

    frame_index = 0
    try:
        while True:
            if args.max_frames is not None and frame_index >= args.max_frames:
                break

            ret, frame = capture.read()
            if not ret:
                break

            fps = capture.get(cv2.CAP_PROP_FPS)
            time_seconds = frame_index / fps if fps and fps > 0 else None

            event = pipeline.process_frame(
                frame=frame,
                camera_id=camera_id,
                video_id=video_id,
                frame_index=frame_index,
                time_seconds=time_seconds,
            )

            pipeline.draw_zones(frame, camera_id)
            pipeline.draw_tracks(frame, event["tracked_objects"])

            if crop_dir is not None:
                for crop_item in event["person_crops"]:
                    track_id = crop_item.get("track_id", "unknown")
                    crop_path = crop_dir / f"{camera_id}_{video_id}_frame_{frame_index:06d}_track_{track_id}.jpg"
                    cv2.imwrite(str(crop_path), crop_item["crop"])

            if args.show:
                cv2.imshow("Restaurant Live Pipeline", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            frame_index += 1
    finally:
        capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()