import json
import sys
from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_DIR))
from src.zone_management.zone_manager import ZoneManager


DETECTIONS_DIR = PROJECT_DIR / "data" / "processed" / "detections"
METADATA_DIR = PROJECT_DIR / "data" / "metadata" / "zones"


def inspect_detection_file(json_path: Path, zone_manager: ZoneManager):
    camera_id = json_path.parent.name
    video_id = json_path.stem.replace("_detections", "")

    with open(json_path, "r", encoding="utf-8") as f:
        frames = json.load(f)

    total_detections = 0
    matched_detections = 0
    unknown_detections = 0

    zone_counts = {}

    for frame in frames:
        frame_camera_id = frame.get("camera_id", camera_id)

        for detection in frame.get("detections", []):
            total_detections += 1

            zone = zone_manager.get_bbox_zone(camera_id=frame_camera_id, box=detection["box"])

            zone_id = zone.get("zone_id", "unknown")
            zone_type = zone.get("zone_type", "unknown")

            key = f"{zone_id} | {zone_type}"
            zone_counts[key] = zone_counts.get(key, 0) + 1

            if zone.get("matched"):
                matched_detections += 1
            else:
                unknown_detections += 1

    matched_rate = matched_detections / total_detections if total_detections > 0 else 0

    return {
        "camera_id": camera_id,
        "video_id": video_id,
        "file": str(json_path.relative_to(PROJECT_DIR)).replace("\\", "/"),
        "total_detections": total_detections,
        "matched_detections": matched_detections,
        "unknown_detections": unknown_detections,
        "matched_rate": round(matched_rate, 4),
        "zone_counts": zone_counts,
    }


def main():
    zone_manager = ZoneManager("config/zones_config.json")

    detection_files = sorted(DETECTIONS_DIR.glob("camera_*/*_detections.json"))

    summary = []

    for json_path in detection_files:
        record = inspect_detection_file(json_path, zone_manager)
        summary.append(record)

        print(
            f"✅ {record['camera_id']}/{record['video_id']} | "
            f"total={record['total_detections']} | "
            f"matched={record['matched_detections']} | "
            f"unknown={record['unknown_detections']} | "
            f"matched_rate={record['matched_rate']}"
        )

    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    output_json = METADATA_DIR / "zone_assignment_summary.json"
    output_csv = METADATA_DIR / "zone_assignment_summary.csv"

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    csv_rows = []
    for item in summary:
        row = item.copy()
        row.pop("zone_counts", None)
        csv_rows.append(row)

    pd.DataFrame(csv_rows).to_csv(output_csv, index=False, encoding="utf-8-sig")

    print("\n========== DONE ==========")
    print("Saved:", output_json)
    print("Saved:", output_csv)


if __name__ == "__main__":
    main()