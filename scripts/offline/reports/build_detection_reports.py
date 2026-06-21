import json
from pathlib import Path

import pandas as pd


PROJECT_DIR = Path.cwd()

DETECTIONS_DIR = PROJECT_DIR / "data" / "processed" / "detections"
VIDEOS_INDEX_PATH = PROJECT_DIR / "data" / "metadata" / "videos" / "videos_index.json"
METADATA_DIR = PROJECT_DIR / "data" / "metadata" / "detections"
DETECTIONS_INDEX_PATH = METADATA_DIR / "detections_index.json"
DETECTIONS_SUMMARY_JSON_PATH = METADATA_DIR / "detections_summary.json"
DETECTIONS_SUMMARY_CSV_PATH = METADATA_DIR / "detections_summary.csv"


def load_videos_index():
    if not VIDEOS_INDEX_PATH.exists():
        print(f"⚠️ videos_index.json not found: {VIDEOS_INDEX_PATH}")
        return {}

    with open(VIDEOS_INDEX_PATH, "r", encoding="utf-8") as f:
        videos = json.load(f)

    videos_lookup = {}

    for video in videos:
        key = (video["camera_id"], video["video_id"])
        videos_lookup[key] = video

    return videos_lookup


def inspect_detection_file(json_path, videos_lookup):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    camera_id = json_path.parent.name
    video_id = json_path.stem.replace("_detections", "")

    sampled_frames = len(data)

    detections_per_frame = [len(frame.get("detections", [])) for frame in data]

    total_detections = sum(detections_per_frame)
    empty_frames = sum(1 for count in detections_per_frame if count == 0)
    non_empty_frames = sampled_frames - empty_frames

    max_detections_in_frame = max(detections_per_frame) if detections_per_frame else 0

    avg_detections_per_frame = total_detections / sampled_frames if sampled_frames > 0 else 0

    if sampled_frames > 0:
        first_frame_index = data[0].get("frame_index")
        last_frame_index = data[-1].get("frame_index")

        start_time_seconds = data[0].get("time_seconds")
        end_time_seconds = data[-1].get("time_seconds")

        json_camera_id = data[0].get("camera_id")
        json_video_id = data[0].get("video_id")
    else:
        first_frame_index = None
        last_frame_index = None
        start_time_seconds = None
        end_time_seconds = None
        json_camera_id = None
        json_video_id = None

    duration_covered_seconds = None
    estimated_sample_fps = None

    if start_time_seconds is not None and end_time_seconds is not None:
        duration_covered_seconds = round(end_time_seconds - start_time_seconds, 3)

        if duration_covered_seconds > 0:
            estimated_sample_fps = round(sampled_frames / duration_covered_seconds, 3)

    video_info = videos_lookup.get((camera_id, video_id), {})

    relative_detection_path = str(json_path.relative_to(PROJECT_DIR)).replace("\\", "/")

    record = {
        "camera_id": camera_id,
        "video_id": video_id,
        "detections_path": relative_detection_path,
        "sampled_frames": sampled_frames,
        "total_detections": total_detections,
        "empty_frames": empty_frames,
        "non_empty_frames": non_empty_frames,
        "max_detections_in_frame": max_detections_in_frame,
        "avg_detections_per_frame": round(avg_detections_per_frame, 3),
        "first_frame_index": first_frame_index,
        "last_frame_index": last_frame_index,
        "start_time_seconds": start_time_seconds,
        "end_time_seconds": end_time_seconds,
        "duration_covered_seconds": duration_covered_seconds,
        "estimated_sample_fps": estimated_sample_fps,
        "json_camera_id": json_camera_id,
        "json_video_id": json_video_id,
        "raw_video_path": video_info.get("path"),
        "original_fps": video_info.get("fps"),
        "width": video_info.get("width"),
        "height": video_info.get("height"),
        "original_duration_seconds": video_info.get("duration_seconds"),
        "original_duration_minutes": video_info.get("duration_minutes"),
    }

    return record


def main():
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DETECTIONS_DIR.exists():
        raise FileNotFoundError(f"Detections directory not found: {DETECTIONS_DIR}")

    videos_lookup = load_videos_index()

    detection_files = sorted(DETECTIONS_DIR.glob("camera_*/*_detections.json"))

    if not detection_files:
        print("❌ No detection files found.")
        return

    detections_index = []
    summary_records = []

    for json_path in detection_files:
        record = inspect_detection_file(json_path, videos_lookup)

        detections_index.append(
            {
                "camera_id": record["camera_id"],
                "video_id": record["video_id"],
                "detections_path": record["detections_path"],
            }
        )

        summary_records.append(record)

        print(
            f"✅ {record['camera_id']}/{record['video_id']} | "
            f"frames={record['sampled_frames']} | "
            f"detections={record['total_detections']}"
        )

    with open(DETECTIONS_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(detections_index, f, indent=2, ensure_ascii=False)

    with open(DETECTIONS_SUMMARY_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary_records, f, indent=2, ensure_ascii=False)

    df_summary = pd.DataFrame(summary_records)
    df_summary.to_csv(DETECTIONS_SUMMARY_CSV_PATH, index=False, encoding="utf-8-sig")

    print("\n========== DONE ==========")
    print(f"Saved detections index: {DETECTIONS_INDEX_PATH}")
    print(f"Saved detections summary JSON: {DETECTIONS_SUMMARY_JSON_PATH}")
    print(f"Saved detections summary CSV: {DETECTIONS_SUMMARY_CSV_PATH}")
    print(f"Total detection files: {len(detection_files)}")


if __name__ == "__main__":
    main()