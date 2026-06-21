import json
import argparse
import sys
import cv2
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
from src.ai_models.tracker import RestaurantTracker


def process_tracking_for_video(detection_file_path, output_file_path, raw_videos_dir):
    print(f"\n🎬 جاري معالجة التتبع للملف: {detection_file_path.name}")

    with open(detection_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        frames_list = data
        camera_id = frames_list[0].get("camera_id") if len(frames_list) > 0 else "unknown"
        video_id = frames_list[0].get("video_id") if len(frames_list) > 0 else detection_file_path.stem
    else:
        camera_id = data.get("camera_id")
        video_id = data.get("video_id")
        frames_list = data.get("detections_per_frame", data.get("frames", []))

    video_path = Path(raw_videos_dir) / camera_id / f"{video_id}.mp4"
    cap = None
    if video_path.exists():
        print(f"📹 تم العثور على الفيديو الأصلي: {video_path}")
        cap = cv2.VideoCapture(str(video_path))
    else:
        print("⚠️ تحذير: الفيديو الأصلي غير موجود. التتبع سيعتمد على الحركة فقط.")

    tracker = RestaurantTracker()
    tracked_frames = []

    for frame_data in frames_list:
        frame_index = frame_data["frame_index"]
        time_seconds = frame_data["time_seconds"]
        detections = frame_data["detections"]

        frame_img = None
        if cap is not None and cap.isOpened():
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame_img = cap.read()
            if not ret:
                frame_img = None

        tracked_res = tracker.update(detections, frame=frame_img)

        tracked_frames.append(
            {
                "camera_id": camera_id,
                "video_id": video_id,
                "frame_index": frame_index,
                "time_seconds": time_seconds,
                "detections": tracked_res,
            }
        )

    if cap is not None:
        cap.release()

    output_data = {
        "camera_id": camera_id,
        "video_id": video_id,
        "tracking_method": "DeepSORT",
        "tracked_frames": tracked_frames,
    }

    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    print(f"✅ تم حفظ ملف التتبع بنجاح في: {output_file_path}")


def main():
    parser = argparse.ArgumentParser(description="تشغيل مرحلة التتبع DeepSORT")
    parser.add_argument("--input-dir", default="data/processed/detections", help="مجلد ملفات الكشف")
    parser.add_argument("--output-dir", default="data/processed/tracking", help="مجلد حفظ ملفات التتبع")
    parser.add_argument("--videos-dir", default="data/raw_videos", help="مجلد الفيديوهات الأصلية")
    args = parser.parse_args()

    input_path = Path(args.input_dir)
    output_path = Path(args.output_dir)

    detection_files = list(input_path.glob("**/*.json"))
    if not detection_files:
        print("❌ لم يتم العثور على أي ملفات كشف JSON.")
        return

    for det_file in detection_files:
        relative_path = det_file.relative_to(input_path)
        video_output_path = output_path / relative_path
        process_tracking_for_video(det_file, video_output_path, args.videos_dir)


if __name__ == "__main__":
    main()