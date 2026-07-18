from __future__ import annotations
import collections.abc
collections.Mapping = collections.abc.Mapping
import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np  # أضفنا numpy لرسم المضلعات

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
    parser.add_argument("--start-sec", type=float, default=None, help="Start processing from a specific time in seconds (e.g. 532)")
    parser.add_argument("--save-debug", action="store_true", help="Save crops to disk")
    return parser.parse_args()


def open_capture(source: str) -> cv2.VideoCapture:
    if source.isdigit():
        return cv2.VideoCapture(int(source))
    return cv2.VideoCapture(source)


def resolve_process_fps(config: dict) -> float:
    """Read and validate pipeline.process_fps from the already-loaded project config.

    Raises ValueError instead of silently defaulting so a missing/invalid config
    value fails loudly at startup rather than masking a config mistake.
    """
    process_fps = config.get("pipeline", {}).get("process_fps")
    if not isinstance(process_fps, (int, float)) or isinstance(process_fps, bool) or process_fps <= 0:
        raise ValueError(
            "config.json is missing a valid 'pipeline.process_fps' value "
            f"(got {process_fps!r}). Set 'pipeline.process_fps' to a positive number "
            "of frames-per-second in config/config.json."
        )
    return float(process_fps)


def compute_pose_stride(actual_fps: float | None, process_fps: float) -> int:
    """Compute how many frames to advance between pose/action inference passes.

    Targets `process_fps` regardless of the source video's native FPS (different
    cameras in videos_index.json have different native FPS, e.g. 15.001 vs 7.0,
    so a fixed stride would not hit the same target rate across cameras). Falls
    back to a stride of 1 (inference on every frame) if the source FPS is
    unavailable/non-positive — the same fallback condition already used elsewhere
    in this file for --start-sec frame seeking — and prints that fallback so it's
    never silent.
    """
    if actual_fps and actual_fps > 0:
        return max(1, round(actual_fps / process_fps))
    print(
        "[WARNING] Could not read a valid video FPS from the capture source; "
        "falling back to pose_stride=1 (pose/action inference on every frame)."
    )
    return 1


def load_first_video_path(videos_index_path: str) -> tuple[str, str, str]:
    index_path = Path(videos_index_path)
    if not index_path.exists():
        raise FileNotFoundError(f"Video index not found: {index_path}")

    with open(index_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    if not records:
        raise ValueError(f"No video records found in: {index_path}")

    first_record = records[1]
    return first_record["path"], first_record["camera_id"], first_record["video_id"]


# --- دالة الرسم المضافة لعرض حالة الطاولة حياً على الفريم ---
def draw_custom_table_states(frame: np.ndarray, camera_id: str, pipeline: LivePipeline) -> None:
    """تستعلم من الـ ZoneManager داخل البايبلاين لترسم حدود الطاولة بناء على حالتها الزمنية المستقرة."""
    if pipeline is None:
        return

    # جلب ملخص الحالات الحالي من طبقة الـ pipeline نفسها حتى تشمل dirty/occupied/empty
    tables_status = pipeline.get_tables_current_state(camera_id)
    zone_mgr = getattr(pipeline, "zone_manager", None)
    if zone_mgr is None:
        return

    camera_zones = zone_mgr.zones_config.get(camera_id, {}).get("zones", [])

    for zone in camera_zones:
        if zone.get("zone_type") in ("table", "table_area"):
            table_id = zone.get("zone_id")
            status = tables_status.get(table_id, "empty")

            # تحديد اللون بناءً على حالة الذاكرة المؤقتة
            if status == "occupied":
                color = (0, 0, 255)  # BGR أحمر
                text = f"{table_id}: Occupied"
            elif status == "dirty":
                color = (0, 165, 255)  # BGR برتقالي
                text = f"{table_id}: Dirty"
            else:
                color = (0, 255, 0)  # BGR أخضر
                text = f"{table_id}: Empty"

            points = zone.get("points", [])
            if len(points) >= 3:
                pts = np.array(points, np.int32).reshape((-1, 1, 2))
                # رسم خطوط الطاولة
                cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=2)

                # كتابة النص التوضيحي للحالة فوق أول نقطة إحداثية للطاولة
                text_position = (int(points[0][0]), int(points[0][1] - 10))
                cv2.putText(
                    frame,
                    text,
                    text_position,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2,
                )


def main() -> None:
    args = parse_args()
    pipeline = LivePipeline(config_path=args.config)
    process_fps = resolve_process_fps(pipeline.config)

    source = args.source
    camera_id = args.camera_id
    video_id = args.video_id

    if args.first_video:
        source, camera_id, video_id = load_first_video_path(args.videos_index)

    capture = open_capture(source)

    if not capture.isOpened():
        raise ValueError(f"Cannot open video source: {source}")

    fps = capture.get(cv2.CAP_PROP_FPS)
    # يتم اشتقاق pose_stride من الـ fps الفعلي للفيديو ومعدل المعالجة المطلوب (process_fps)
    # في config.json، بدل قيمة ثابتة، حتى نستهدف نفس معدل المعالجة بغض النظر عن fps الكاميرا الأصلي
    pose_stride = compute_pose_stride(fps, process_fps)
    frame_index = 0
    if args.start_sec is not None and fps and fps > 0:
        frame_index = int(args.start_sec * fps)
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        print(f"Seeked to {args.start_sec}s (Frame: {frame_index})")

    crop_dir = Path(args.save_crops_dir) if args.save_debug else None
    if crop_dir is not None:
        crop_dir.mkdir(parents=True, exist_ok=True)

    frames_processed = 0
    try:
        while True:
            if args.max_frames is not None and frames_processed >= args.max_frames:
                break

            ret, frame = capture.read()
            if not ret:
                break

            time_seconds = frame_index / fps if fps and fps > 0 else None

            event = pipeline.process_frame(
                frame=frame,
                camera_id=camera_id,
                video_id=video_id,
                pose_stride=pose_stride,
                frame_index=frame_index,
                time_seconds=time_seconds,
            )

            try:
                # 1. رسم المكونات الافتراضية للـ pipeline
                pipeline.draw_zones(frame, camera_id)
                pipeline.draw_tracks(frame, event["tracked_objects"])
                
                # 2. حقن التغيير هنا: تشغيل دالة التلوين المعتمدة على الذاكرة الزمنية المستقرة لحالة الطاولة
                draw_custom_table_states(frame, camera_id, pipeline)
                
            except Exception as e:
                import traceback
                print(f"[ERROR] draw crashed on frame {frame_index}: {e}")
                traceback.print_exc()

            if crop_dir is not None:
                for crop_item in event["person_crops"]:
                    track_id = crop_item.get("track_id", "unknown")
                    crop_path = crop_dir / f"{camera_id}_{video_id}_frame_{frame_index:06d}_track_{track_id}.jpg"
                    cv2.imwrite(str(crop_path), crop_item["crop"])

            if args.show:
                cv2.namedWindow("Restaurant Live Pipeline", cv2.WINDOW_NORMAL)
                cv2.imshow("Restaurant Live Pipeline", frame)
                key = cv2.waitKey(1) & 0xFF 
                if key != 255:
                    print(f"[DEBUG] key pressed: {key} (chr: {chr(key) if key < 128 else '?'})")
                if key == ord("q"):
                    break

            frame_index += 1
            frames_processed += 1
            print(f"Frame {frames_processed}/{args.max_frames if args.max_frames else '?'} done", flush=True)
    finally:
        capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()