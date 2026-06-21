import json
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[3] # حسب موقع الملف الجديد
TRACKING_DIR = PROJECT_DIR / "data" / "processed" / "tracking"
METADATA_DIR = PROJECT_DIR / "data" / "metadata" / "tracking"
SUMMARY_CSV_PATH = METADATA_DIR / "tracking_summary.csv"
SUMMARY_JSON_PATH = METADATA_DIR / "tracking_summary.json"

def inspect_tracking_file(json_path: Path):
    camera_id = json_path.parent.name
    video_id = json_path.stem.replace("_tracking", "")
    
    with open(json_path, "r", encoding="utf-8") as f:
        frames = json.load(f)
        
    # سلات لجمع البيانات الإحصائية للتتبع
    all_ids = set()
    id_start_frames = {}
    id_end_frames = {}
    max_people_in_single_frame = 0
    
    for frame in frames:
        # قراءة الكائنات المتتبعة في هذا الفريم
        tracked_objects = frame.get("tracked_objects", [])
        current_frame_people = len(tracked_objects)
        
        # حساب أقصى زحمة في فريم واحد
        if current_frame_people > max_people_in_single_frame:
            max_people_in_single_frame = current_frame_people
            
        frame_index = frame.get("frame_index", 0)
        
        for obj in tracked_objects:
            track_id = obj.get("track_id")
            if track_id is not None:
                all_ids.add(track_id)
                # تسجيل أول ظهور للـ ID
                if track_id not in id_start_frames:
                    id_start_frames[track_id] = frame_index
                # تحديث آخر ظهور للـ ID باستمرار
                id_end_frames[track_id] = frame_index

    total_unique_people = len(all_ids)
    
    return {
        "camera_id": camera_id,
        "video_id": video_id,
        "total_frames_processed": len(frames),
        "total_unique_people_detected": total_unique_people,
        "max_people_at_once": max_people_in_single_frame,
        "file": str(json_path.relative_to(PROJECT_DIR)).replace("\\", "/")
    }

def main():
    # كود البحث عن ملفات التتبع وحفظ الـ CSV والـ JSON بنفس طريقتكِ تماماً...
    pass

if __name__ == "__main__":
    main()