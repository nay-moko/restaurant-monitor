import json
import sys
from pathlib import Path

import cv2
import numpy as np


PROJECT_DIR = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_DIR))

ZONES_CONFIG_PATH = PROJECT_DIR / "config" / "zones_config.json"
TRACKING_DIR = PROJECT_DIR / "data" / "processed" / "tracking"
RAW_VIDEOS_DIR = PROJECT_DIR / "data" / "raw_videos"
OUTPUT_DIR = PROJECT_DIR / "data" / "debug" / "tracking"


def create_tracking_video(camera_id: str, video_id: str, max_frames=240):
    print(f"🎬 جاري تحضير فيديو المعاينة المتحرك للكاميرا: {camera_id} (أول دقيقتين)...")

    video_path = RAW_VIDEOS_DIR / camera_id / f"{video_id}.mp4"
    tracking_json_path = TRACKING_DIR / camera_id / f"{video_id}_detections.json"

    if not video_path.exists():
        print(f"❌ خطأ: لم يتم العثور على الفيديو الأصلي في المسار: {video_path}")
        return
    if not tracking_json_path.exists():
        print(f"❌ خطأ: لم يتم العثور على ملف جيسون التتبع في المسار: {tracking_json_path}")
        return

    with open(tracking_json_path, "r", encoding="utf-8") as f:
        tracking_data = json.load(f)

    tracked_frames = tracking_data.get("tracked_frames", [])
    tracked_frames = tracked_frames[:max_frames]
    frames_dict = {f["frame_index"]: f["detections"] for f in tracked_frames}

    camera_zones = []
    if ZONES_CONFIG_PATH.exists():
        with open(ZONES_CONFIG_PATH, "r", encoding="utf-8") as f:
            zones_config = json.load(f)
        camera_zones = zones_config.get(camera_id, {}).get("zones", [])

    cap = cv2.VideoCapture(str(video_path))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_video_path = OUTPUT_DIR / f"{camera_id}_{video_id}_preview.mp4"

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(output_video_path), fourcc, 2.0, (width, height))

    np.random.seed(42)
    colors = {i: [int(c) for c in np.random.randint(50, 255, size=3)] for i in range(1, 1000)}

    for frame_index in sorted(frames_dict.keys()):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        if not ret:
            break

        for zone in camera_zones:
            points = np.array(zone["points"], dtype=np.int32)
            cv2.polylines(frame, [points], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.putText(
                frame,
                f"Zone: {zone['zone_id']}",
                (int(points[0][0]), int(points[0][1]) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
            )

        detections = frames_dict[frame_index]
        for det in detections:
            track_id = det["track_id"]
            box = map(int, det["box"])
            x1, y1, x2, y2 = box

            color = colors.get(track_id, (255, 0, 0))

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
            cv2.putText(
                frame,
                f"ID: {track_id}",
                (x1, y1 - 12),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2,
                cv2.LINE_AA,
            )

        cv2.putText(
            frame,
            f"Frame: {frame_index} | Preview Mode (2 FPS)",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2,
        )

        out.write(frame)

    cap.release()
    out.release()
    print("✅ تم توليد فيديو المعاينة بنجاح واقتصاص أول دقيقتين!")
    print(f"📁 يمكنك مشاهدة الفيديو الآن في المسار التالي:\n{output_video_path}")


def main():
    create_tracking_video(camera_id="camera_01", video_id="video_001", max_frames=240)


if __name__ == "__main__":
    main()