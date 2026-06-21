import json
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[3]

ZONED_DIR = PROJECT_DIR / "data" / "processed" / "detections_with_zones"
METADATA_DIR = PROJECT_DIR / "data" / "metadata" / "zones"
INDEX_PATH = METADATA_DIR / "detections_with_zones_index.json"
SUMMARY_JSON_PATH = METADATA_DIR / "detections_with_zones_summary.json"
SUMMARY_CSV_PATH = METADATA_DIR / "detections_with_zones_summary.csv"


def inspect_file(json_path: Path):
    camera_id = json_path.parent.name
    video_id = json_path.stem.replace("_detections_with_zones", "")

    with open(json_path, "r", encoding="utf-8") as f:
        frames = json.load(f)

    total_detections = 0
    matched = 0
    unknown = 0
    zone_type_counts = {}

    for frame in frames:
        for detection in frame.get("detections", []):
            total_detections += 1

            zone = detection.get("zone", {})
            zone_type = zone.get("zone_type", "unknown")

            zone_type_counts[zone_type] = zone_type_counts.get(zone_type, 0) + 1

            if zone.get("matched"):
                matched += 1
            else:
                unknown += 1

    matched_rate = matched / total_detections if total_detections else 0

    return {
        "camera_id": camera_id,
        "video_id": video_id,
        "file": str(json_path.relative_to(PROJECT_DIR)).replace("\\", "/"),
        "frames": len(frames),
        "total_detections": total_detections,
        "matched": matched,
        "unknown": unknown,
        "matched_rate": round(matched_rate, 4),
        "zone_type_counts": zone_type_counts,
    }


def main():
    files = sorted(ZONED_DIR.glob("camera_*/*_detections_with_zones.json"))

    if not files:
        print("❌ No detections_with_zones files found.")
        return

    index = []
    summary = []

    for file in files:
        record = inspect_file(file)
        summary.append(record)

        index.append(
            {
                "camera_id": record["camera_id"],
                "video_id": record["video_id"],
                "detections_with_zones_path": record["file"],
            }
        )

        print(
            f"✅ {record['camera_id']}/{record['video_id']} | "
            f"matched_rate={record['matched_rate']}"
        )

    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    with open(SUMMARY_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    csv_rows = []
    for item in summary:
        row = item.copy()
        row.pop("zone_type_counts", None)
        csv_rows.append(row)

    pd.DataFrame(csv_rows).to_csv(SUMMARY_CSV_PATH, index=False, encoding="utf-8-sig")

    print("\n========== DONE ==========")
    print("Saved:", INDEX_PATH)
    print("Saved:", SUMMARY_JSON_PATH)
    print("Saved:", SUMMARY_CSV_PATH)


if __name__ == "__main__":
    main()