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

**7. Set environment variables**

```bash
cp .env.example .env
```

Open `.env` and fill in your PostgreSQL and Redis credentials if you are running the backend/database layer.

**8. Set up the database**

This step is only required when working on the backend/database part.

```bash
python -c "from src.storage.database import DatabaseManager; DatabaseManager().create_tables()"
```

**9. Validate zones**

Before running zone-based logic, validate the zones configuration:

```bash
python scripts/zones/validate_zones_config.py
```

To test how detections are assigned to zones:

```bash
python scripts/zones/test_zone_assignment_on_detections.py
```

**10. Run YOLO detection**

Run the detection pipeline using the configured `videos_index.json`:

```bash
python scripts/detection/run_detection.py --target-fps 2
```

To process only the first 60 seconds for testing:

```bash
python scripts/detection/run_detection.py --target-fps 2 --max-seconds 60
```

Detection results will be saved in:

```text
data/processed/detections/
```

**11. Build detection reports**

After running detection, generate the detection index and summary reports:

```bash
python scripts/reports/build_detection_reports.py
```

Reports will be saved in:

```text
data/metadata/detections/
```

**12. Optional: generate zone-enriched detections**

If needed for classification testing, generate detections with zone information:

```bash
python scripts/zones/enrich_detections_with_zones.py
python scripts/reports/build_zone_reports.py
```

Zone reports will be saved in:

```text
data/metadata/zones/
```

---

> **Note:** Steps 1–3 are required for everyone.
> Steps 4–6 must be completed before running any AI pipeline.
> Raw videos, debug files, cache files, and generated temporary outputs are ignored by Git and should not be uploaded.
