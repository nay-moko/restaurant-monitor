import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_DIR))

import json
from src.zone_management.zone_manager import ZoneManager


DETECTIONS_DIR = PROJECT_DIR / "data" / "processed" / "detections"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed" / "detections_with_zones"



def enrich_file(input_path: Path, zone_manager: ZoneManager):
    camera_id = input_path.parent.name
    video_id = input_path.stem.replace("_detections", "")

    output_dir = OUTPUT_DIR / camera_id
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{video_id}_detections_with_zones.json"

    with open(input_path, "r", encoding="utf-8") as f:
        frames = json.load(f)

    enriched_frames = []

    for frame_result in frames:
        enriched_frames.append(
            zone_manager.enrich_frame_result(frame_result)
        )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(enriched_frames, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved: {output_path}")


def main():
    zone_manager = ZoneManager("config/zones_config.json")

    detection_files = sorted(DETECTIONS_DIR.glob("camera_*/*_detections.json"))

    for detection_file in detection_files:
        enrich_file(detection_file, zone_manager)


if __name__ == "__main__":
    main()