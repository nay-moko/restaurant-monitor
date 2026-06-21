## ⚙️ Quick Setup

```bash
# 1. Clone the project
git clone <repo-url>
cd restaurant-monitor

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

**4. Place your videos**

Put the raw videos inside `data/raw_videos/`, grouped by camera:

```text
data/raw_videos/
├── camera_01/
│   └── video_001.mp4
├── camera_02/
│   └── video_001.mp4
└── ...
```

Then make sure the video metadata file exists:

```text
data/metadata/videos/videos_index.json
```

**5. Download models**

Place the YOLO model in:

```text
models/yolo/yolov8n.pt
```

If the file does not exist, Ultralytics may download it automatically when running the detector.

**6. Configure the system**

Make sure these files are ready:

```text
config/config.json
config/camera_config.json
config/zones_config.json
config/thresholds.json
```

`camera_config.json` defines the camera type and location.

`zones_config.json` defines the zone polygons for each camera.

`thresholds.json` defines confidence thresholds and rule parameters.

**7. Data layout**

The data folders are now grouped by purpose:

```text
data/
├── raw_videos/
├── processed/
│   ├── detections/
│   ├── detections_with_zones/
│   └── tracking/
├── metadata/
│   ├── videos/
│   ├── detections/
│   └── zones/
├── debug/
│   ├── detection/
│   ├── tracking/
│   ├── zones/
│   ├── classification/
│   └── reid/
├── analysis/
└── artifacts/
	├── outputs/
	└── reid_embeddings/
```

**8. Script layout**

The scripts are now separated by purpose:

```text
scripts/
├── offline/
│   ├── data/
│   ├── detection/
│   ├── tracking/
│   ├── reports/
│   └── zones/
├── validation/
│   ├── tracking/
│   └── zones/
└── live/
```

**9. Set environment variables**

```bash
cp .env.example .env
```

Open `.env` and fill in your PostgreSQL and Redis credentials if you are running the backend/database layer.

**10. Set up the database**

This step is only required when working on the backend/database part.

```bash
python -c "from src.storage.database import DatabaseManager; DatabaseManager().create_tables()"
```

**11. Validate zones**

Before running zone-based logic, validate the zones configuration:

```bash
python scripts/validation/zones/validate_zones_config.py
```

To test how detections are assigned to zones:

```bash
python scripts/validation/zones/test_zone_assignment_on_detections.py
```

To visualize the zone layout on the reference frames:

```bash
python scripts/validation/zones/visualize_zones.py
```

To generate the tracking preview video:

```bash
python scripts/validation/tracking/visualize_tracking_video.py
```

**12. Run the live pipeline**

Run the real-time in-memory pipeline. The frame is read once, passed to the detector, then passed directly to the tracker, and each tracked person is cropped in RAM for the next RE-ID stage.

```bash
python scripts/live/run_live.py --source 0 --show
```

Use a video file instead of a camera by passing its path to `--source`.

To limit testing to a small number of frames:

```bash
python scripts/live/run_live.py --source 0 --max-frames 100 --show
```

This path keeps data in RAM. It does not write detector JSON between stages.

**13. Offline detection pipeline**

Run detection on recorded videos:

```bash
python scripts/offline/detection/run_detection.py
```

Run tracking from saved detection JSON:

```bash
python scripts/offline/tracking/run_tracking.py
```

Extract reference frames for zone annotation:

```bash
python scripts/offline/data/extract_reference_frames.py
```

Enrich detections with zones:

```bash
python scripts/offline/zones/enrich_detections_with_zones.py
```

Build detection reports:

After running detection, generate the detection index and summary reports:

```bash
python scripts/offline/reports/build_detection_reports.py
```

Reports will be saved in:

```text
data/metadata/detections/
```

Build zone reports:

```bash
python scripts/offline/reports/build_zone_reports.py
```

Zone reports will be saved in:

```text
data/metadata/zones/
```

---

> **Note:** Steps 1–3 are required for everyone.
> Steps 4–6 must be completed before running any AI pipeline.
> Raw videos, debug files, cache files, and generated temporary outputs are ignored by Git and should not be uploaded.
