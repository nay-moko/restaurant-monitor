import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
from src.core.pipeline import RestaurantMonitoringPipeline


def process_detection_for_video(pipeline, video_record, target_fps, max_seconds, overwrite):
    camera_id = video_record["camera_id"]
    video_id = video_record["video_id"]

    print(f"\n🎬 Processing detection for: {camera_id}/{video_id}")
    result = pipeline.process_video(
        video_record=video_record,
        target_fps=target_fps,
        max_seconds=max_seconds,
        overwrite=overwrite,
    )
    print(f"✅ Detection saved to: {result['detections_path']}")


def main():
    parser = argparse.ArgumentParser(description="Run YOLO detection on recorded videos")
    parser.add_argument("--input-json", default="data/metadata/videos/videos_index.json", help="Video index file")
    parser.add_argument("--target-fps", type=int, default=None, help="Optional frame sampling rate")
    parser.add_argument("--max-seconds", type=int, default=None, help="Optional max duration per video")
    parser.add_argument("--overwrite", action="store_true", help="Recompute detections even if JSON exists")
    args = parser.parse_args()

    input_path = Path(args.input_json)

    if not input_path.exists():
        raise FileNotFoundError(f"Video index not found: {input_path}")

    pipeline = RestaurantMonitoringPipeline()

    with open(input_path, "r", encoding="utf-8") as f:
        video_records = json.load(f)

    for video_record in video_records:
        process_detection_for_video(
            pipeline=pipeline,
            video_record=video_record,
            target_fps=args.target_fps,
            max_seconds=args.max_seconds,
            overwrite=args.overwrite,
        )


if __name__ == "__main__":
    main()