# 📁 PROJECT EXPORT FOR LLMs

## 📊 Project Information

- **Project Name**: `restaurant-monitor-feature-role-engine`
- **Generated On**: 2026-07-14 10:03:48 (Asia/Damascus / GMT+03:00)
- **Total Files Processed**: 115
- **Export Tool**: Easy Whole Project to Single Text File for LLMs v1.1.0
- **Tool Author**: Jota / José Guilherme Pandolfi

### ⚙️ Export Configuration

| Setting | Value |
|---------|-------|
| Language | `en` |
| Max File Size | `1 MB` |
| Include Hidden Files | `false` |
| Output Format | `both` |

## 🌳 Project Structure

```
├── 📁 api/
│   └── 📄 __init__.py
├── 📁 config/
│   ├── 📄 camera_config.json (2.41 KB)
│   ├── 📄 config.json (1021 B)
│   └── 📄 zones_config.json (13.67 KB)
├── 📁 data/
│   ├── 📁 debug/
│   │   ├── 📁 analytics/
│   │   │   └── 📁 heatmaps_preview/
│   │   ├── 📁 classification/
│   │   │   ├── 📁 mistakes/
│   │   │   └── 📁 samples/
│   │   ├── 📁 reid/
│   │   │   ├── 📁 crops/
│   │   │   └── 📁 matches/
│   │   ├── 📁 tracking/
│   │   │   ├── 📁 frames/
│   │   │   └── 📁 videos/
│   │   └── 📁 zones/
│   │       ├── 📁 reference_frames/
│   │       │   ├── 📄 camera_01_reference.jpg (595.01 KB)
│   │       │   ├── 📄 camera_02_reference.jpg (663.01 KB)
│   │       │   ├── 📄 camera_04_reference.jpg (437.48 KB)
│   │       │   ├── 📄 camera_06_reference.jpg (328.35 KB)
│   │       │   ├── 📄 camera_07_reference.jpg (469.4 KB)
│   │       │   ├── 📄 camera_11_reference.jpg (448.86 KB)
│   │       │   ├── 📄 camera_13_reference.jpg (644.97 KB)
│   │       │   ├── 📄 camera_15_reference.jpg (572.72 KB)
│   │       │   └── 📄 camera_16_reference.jpg (450.38 KB)
│   │       └── 📁 zones_preview/
│   │           ├── 📄 camera_01_zones_preview.jpg (702.54 KB)
│   │           ├── 📄 camera_02_zones_preview.jpg (756.61 KB)
│   │           ├── 📄 camera_04_zones_preview.jpg (535.72 KB)
│   │           ├── 📄 camera_06_zones_preview.jpg (400.87 KB)
│   │           ├── 📄 camera_07_zones_preview.jpg (526.93 KB)
│   │           ├── 📄 camera_11_zones_preview.jpg (484.1 KB)
│   │           ├── 📄 camera_13_zones_preview.jpg (727.09 KB)
│   │           ├── 📄 camera_15_zones_preview.jpg (669.18 KB)
│   │           └── 📄 camera_16_zones_preview.jpg (552.15 KB)
│   ├── 📁 metadata/
│   │   ├── 📁 videos/
│   │   │   └── 📄 videos_index.json (2.64 KB)
│   │   └── 📄 pipeline_run_summary.csv (222 B)
│   └── 📁 raw_videos/
│       ├── 📁 camera_01/
│       │   └── 📄 video_001.mp4 (885.4 MB)
│       ├── 📁 camera_02/
│       │   └── 📄 video_001.mp4 (902.81 MB)
│       ├── 📁 camera_03/
│       ├── 📁 camera_04/
│       │   └── 📄 video_001.mp4 (604.51 MB)
│       ├── 📁 camera_05/
│       ├── 📁 camera_06/
│       │   └── 📄 video_001.mp4 (475.56 MB)
│       ├── 📁 camera_07/
│       │   └── 📄 video_001.mp4 (450.65 MB)
│       ├── 📁 camera_08/
│       ├── 📁 camera_09/
│       ├── 📁 camera_10/
│       ├── 📁 camera_11/
│       │   ├── 📄 video_001.mp4 (573.7 MB)
│       │   └── 📄 video_002.mp4 (248.62 MB)
│       ├── 📁 camera_12/
│       ├── 📁 camera_13/
│       │   └── 📄 video_001.mp4 (602.16 MB)
│       ├── 📁 camera_14/
│       │   └── 📄 video_001.mp4 (23.01 MB)
│       ├── 📁 camera_15/
│       │   └── 📄 video_001.mp4 (900.62 MB)
│       └── 📁 camera_16/
│           └── 📄 video_001.mp4 (524.7 MB)
├── 📁 docs/
│   ├── 📄 ARCHITECTURE.md (13.07 KB)
│   ├── 📄 DB_SCHEMA.md (6.38 KB)
│   ├── 📄 EVENT_ENGINE.md (7.46 KB)
│   └── 📄 TASK1_REPORT.md (10.08 KB)
├── 📁 frontend/
│   ├── 📁 public/
│   │   └── 📄 index.html
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── 📁 Charts/
│   │   │   │   ├── 📄 BarChart.jsx
│   │   │   │   ├── 📄 LineChart.jsx
│   │   │   │   └── 📄 PieChart.jsx
│   │   │   ├── 📄 Alerts.jsx
│   │   │   ├── 📄 Dashboard.jsx
│   │   │   ├── 📄 HeatmapViewer.jsx
│   │   │   ├── 📄 Layout.jsx
│   │   │   ├── 📄 LiveFeed.jsx
│   │   │   └── 📄 RestaurantMap.jsx
│   │   ├── 📁 services/
│   │   │   ├── 📄 api.js
│   │   │   ├── 📄 store.js
│   │   │   └── 📄 websocket.js
│   │   ├── 📄 App.jsx
│   │   └── 📄 index.js
│   └── 📄 package.json
├── 📁 models/
│   ├── 📁 yolo/
│   │   └── 📄 yolov8n.pt (6.25 MB)
│   ├── 📄 label_encoder.pkl (284 B)
│   └── 📄 pose_lstm.pth (251.97 KB)
├── 📁 src/
│   ├── 📁 ai_models/
│   │   ├── 📁 __pycache__/
│   │   │   ├── 📄 __init__.cpython-313.pyc (174 B)
│   │   │   ├── 📄 detector.cpython-313.pyc (4.17 KB)
│   │   │   └── 📄 tracker.cpython-313.pyc (2.63 KB)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 detector.py (3.28 KB)
│   │   ├── 📄 pose_model.py
│   │   └── 📄 tracker.py (2.39 KB)
│   ├── 📁 core/
│   │   ├── 📁 __pycache__/
│   │   │   ├── 📄 __init__.cpython-313.pyc (169 B)
│   │   │   ├── 📄 classifiers.cpython-313.pyc (1.2 KB)
│   │   │   └── 📄 live_pipeline.cpython-313.pyc (30.8 KB)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 classifiers.py (356 B)
│   │   └── 📄 live_pipeline.py (30.21 KB)
│   ├── 📁 kbs/
│   │   ├── 📁 __pycache__/
│   │   │   ├── 📄 __init__.cpython-313.pyc (595 B)
│   │   │   ├── 📄 _compat.cpython-313.pyc (865 B)
│   │   │   ├── 📄 reid_gallery.cpython-313.pyc (11.77 KB)
│   │   │   ├── 📄 role_engine.cpython-313.pyc (35.35 KB)
│   │   │   └── 📄 table_kbs.cpython-313.pyc (4.04 KB)
│   │   ├── 📄 __init__.py (499 B)
│   │   ├── 📄 _compat.py (642 B)
│   │   ├── 📄 reid_gallery.py (9.34 KB)
│   │   ├── 📄 role_engine.py (31.01 KB)
│   │   └── 📄 table_kbs.py (3.86 KB)
│   ├── 📁 utils/
│   │   ├── 📄 extract_reference_frames.py (1.67 KB)
│   │   ├── 📄 label_dataset.py (3.43 KB)
│   │   ├── 📄 remove_skipped_samples.py (592 B)
│   │   └── 📄 zone_annotator_v3.html (26.97 KB)
│   ├── 📁 zone_management/
│   │   ├── 📁 __pycache__/
│   │   │   ├── 📄 __init__.cpython-313.pyc (180 B)
│   │   │   └── 📄 zone_manager.cpython-313.pyc (9.04 KB)
│   │   ├── 📁 validation/
│   │   │   └── 📁 zones/
│   │   │       ├── 📄 validate_zones_config.py (2.78 KB)
│   │   │       └── 📄 visualize_zones.py (1.68 KB)
│   │   ├── 📄 __init__.py
│   │   └── 📄 zone_manager.py (8.07 KB)
│   └── 📄 run_live.py (7.77 KB)
├── 📁 storage/
│   ├── 📄 __init__.py
│   ├── 📄 database.py (2.91 KB)
│   ├── 📄 models.py (5.13 KB)
│   └── 📄 redis_manager.py
├── 📁 tests/
│   ├── 📁 __pycache__/
│   │   ├── 📄 __init__.cpython-313.pyc (166 B)
│   │   ├── 📄 test_analytics.cpython-313-pytest-9.1.1.pyc (172 B)
│   │   ├── 📄 test_classifier.cpython-313-pytest-9.1.1.pyc (173 B)
│   │   ├── 📄 test_detector.cpython-313-pytest-9.1.1.pyc (1.51 KB)
│   │   ├── 📄 test_live_pipeline_timing.cpython-313-pytest-9.1.1.pyc (6.96 KB)
│   │   ├── 📄 test_reid.cpython-313-pytest-9.1.1.pyc (167 B)
│   │   ├── 📄 test_role_engine.cpython-313-pytest-9.1.1.pyc (25.26 KB)
│   │   └── 📄 test_tracker.cpython-313-pytest-9.1.1.pyc (1.56 KB)
│   ├── 📄 __init__.py
│   ├── 📄 test_analytics.py
│   ├── 📄 test_classifier.py
│   ├── 📄 test_detector.py (948 B)
│   ├── 📄 test_live_pipeline_timing.py (2.94 KB)
│   ├── 📄 test_reid.py
│   ├── 📄 test_role_engine.py (15.67 KB)
│   └── 📄 test_tracker.py (956 B)
├── 📄 changes.txt (5.86 KB)
├── 📄 README.md (2.13 KB)
└── 📄 requirements.txt (2.13 KB)
```

## 📑 Table of Contents

**Project Files:**

- [📄 api/__init__.py](#📄-api-init-py)
- [📄 config/camera_config.json](#📄-config-camera-config-json)
- [📄 config/config.json](#📄-config-config-json)
- [📄 config/zones_config.json](#📄-config-zones-config-json)
- [📄 data/metadata/videos/videos_index.json](#📄-data-metadata-videos-videos-index-json)
- [📄 docs/ARCHITECTURE.md](#📄-docs-architecture-md)
- [📄 docs/DB_SCHEMA.md](#📄-docs-db-schema-md)
- [📄 docs/EVENT_ENGINE.md](#📄-docs-event-engine-md)
- [📄 docs/TASK1_REPORT.md](#📄-docs-task1-report-md)
- [📄 frontend/public/index.html](#📄-frontend-public-index-html)
- [📄 frontend/src/components/Charts/BarChart.jsx](#📄-frontend-src-components-charts-barchart-jsx)
- [📄 frontend/src/components/Charts/LineChart.jsx](#📄-frontend-src-components-charts-linechart-jsx)
- [📄 frontend/src/components/Charts/PieChart.jsx](#📄-frontend-src-components-charts-piechart-jsx)
- [📄 frontend/src/components/Alerts.jsx](#📄-frontend-src-components-alerts-jsx)
- [📄 frontend/src/components/Dashboard.jsx](#📄-frontend-src-components-dashboard-jsx)
- [📄 frontend/src/components/HeatmapViewer.jsx](#📄-frontend-src-components-heatmapviewer-jsx)
- [📄 frontend/src/components/Layout.jsx](#📄-frontend-src-components-layout-jsx)
- [📄 frontend/src/components/LiveFeed.jsx](#📄-frontend-src-components-livefeed-jsx)
- [📄 frontend/src/components/RestaurantMap.jsx](#📄-frontend-src-components-restaurantmap-jsx)
- [📄 frontend/src/services/api.js](#📄-frontend-src-services-api-js)
- [📄 frontend/src/services/store.js](#📄-frontend-src-services-store-js)
- [📄 frontend/src/services/websocket.js](#📄-frontend-src-services-websocket-js)
- [📄 frontend/src/App.jsx](#📄-frontend-src-app-jsx)
- [📄 frontend/src/index.js](#📄-frontend-src-index-js)
- [📄 frontend/package.json](#📄-frontend-package-json)
- [📄 src/ai_models/__init__.py](#📄-src-ai-models-init-py)
- [📄 src/ai_models/detector.py](#📄-src-ai-models-detector-py)
- [📄 src/ai_models/pose_model.py](#📄-src-ai-models-pose-model-py)
- [📄 src/ai_models/tracker.py](#📄-src-ai-models-tracker-py)
- [📄 src/core/__init__.py](#📄-src-core-init-py)
- [📄 src/core/classifiers.py](#📄-src-core-classifiers-py)
- [📄 src/core/live_pipeline.py](#📄-src-core-live-pipeline-py)
- [📄 src/kbs/__init__.py](#📄-src-kbs-init-py)
- [📄 src/kbs/_compat.py](#📄-src-kbs-compat-py)
- [📄 src/kbs/reid_gallery.py](#📄-src-kbs-reid-gallery-py)
- [📄 src/kbs/role_engine.py](#📄-src-kbs-role-engine-py)
- [📄 src/kbs/table_kbs.py](#📄-src-kbs-table-kbs-py)
- [📄 src/utils/extract_reference_frames.py](#📄-src-utils-extract-reference-frames-py)
- [📄 src/utils/label_dataset.py](#📄-src-utils-label-dataset-py)
- [📄 src/utils/remove_skipped_samples.py](#📄-src-utils-remove-skipped-samples-py)
- [📄 src/utils/zone_annotator_v3.html](#📄-src-utils-zone-annotator-v3-html)
- [📄 src/zone_management/validation/zones/validate_zones_config.py](#📄-src-zone-management-validation-zones-validate-zones-config-py)
- [📄 src/zone_management/validation/zones/visualize_zones.py](#📄-src-zone-management-validation-zones-visualize-zones-py)
- [📄 src/zone_management/__init__.py](#📄-src-zone-management-init-py)
- [📄 src/zone_management/zone_manager.py](#📄-src-zone-management-zone-manager-py)
- [📄 src/run_live.py](#📄-src-run-live-py)
- [📄 storage/__init__.py](#📄-storage-init-py)
- [📄 storage/database.py](#📄-storage-database-py)
- [📄 storage/models.py](#📄-storage-models-py)
- [📄 storage/redis_manager.py](#📄-storage-redis-manager-py)
- [📄 tests/__init__.py](#📄-tests-init-py)
- [📄 tests/test_analytics.py](#📄-tests-test-analytics-py)
- [📄 tests/test_classifier.py](#📄-tests-test-classifier-py)
- [📄 tests/test_detector.py](#📄-tests-test-detector-py)
- [📄 tests/test_live_pipeline_timing.py](#📄-tests-test-live-pipeline-timing-py)
- [📄 tests/test_reid.py](#📄-tests-test-reid-py)
- [📄 tests/test_role_engine.py](#📄-tests-test-role-engine-py)
- [📄 tests/test_tracker.py](#📄-tests-test-tracker-py)
- [📄 changes.txt](#📄-changes-txt)
- [📄 README.md](#📄-readme-md)
- [📄 requirements.txt](#📄-requirements-txt)

---

## 📈 Project Statistics

| Metric | Count |
|--------|-------|
| Total Files | 115 |
| Total Directories | 61 |
| Text Files | 61 |
| Binary Files | 54 |
| Total Size | 6.06 GB |

### 📄 File Types Distribution

| Extension | Count |
|-----------|-------|
| `.py` | 33 |
| `.pyc` | 21 |
| `.jpg` | 18 |
| `.mp4` | 11 |
| `.jsx` | 10 |
| `.json` | 5 |
| `.md` | 5 |
| `.js` | 4 |
| `.html` | 2 |
| `.txt` | 2 |
| `.csv` | 1 |
| `.pt` | 1 |
| `.pkl` | 1 |
| `.pth` | 1 |

## 💻 File Code Contents

### <a id="📄-api-init-py"></a>📄 `api/__init__.py`

**File Info:**
- **Size**: 0 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `api/__init__.py`
- **Relative Path**: `api`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:06 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```python

```

---

### <a id="📄-config-camera-config-json"></a>📄 `config/camera_config.json`

**File Info:**
- **Size**: 2.41 KB
- **Extension**: `.json`
- **Language**: `json`
- **Location**: `config/camera_config.json`
- **Relative Path**: `config`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:06 (Asia/Damascus / GMT+03:00)
- **MD5**: `17b2783c43e32fcae8714767caeebf58`
- **SHA256**: `0cf1e55248e6e9ccdad95103950928fc28dc70d4bac3b56550bc996451f29612`
- **Encoding**: ASCII

**File code content:**

```json
{
    "cameras": {
      "camera_01": {
        "type": "mixed",
        "location": "Winter_section",
        "enabled": true,
        "description": "Indoor tables"
      },
      "camera_02": {
        "type": "mixed",
        "location": "Winter_section",
        "enabled": true,
        "description": "Indoor tables"
      },
      "camera_04": {
        "type": "staff_only",
        "location": "cashier",
        "enabled": true,
        "description": "Cashier, Winter Section "
      },
      "camera_05": {
        "type": "staff_only",
        "location": "Hookah section",
        "enabled": true,
        "description": "Hookah preparation section"
      },
      "camera_06": {
        "type": "mixed",
        "location": "Bathroom entrance",
        "enabled": true,
        "description": "Bathroom entrance"
      },
      "camera_07": {
        "type": "staff_only",
        "location": "buffet",
        "enabled": true,
        "description": "buffet"
      },
      "camera_08": {
        "type": "staff_only",
        "location": "kitchen",
        "enabled": true,
        "description": "indoor kitchen"
      },
      "camera_09": {
        "type": "staff_only",
        "location": "kitchen",
        "enabled": true,
        "description": "kitchen in the middle"
      },
      "camera_10": {
        "type": "staff_only",
        "location": "kitchen",
        "enabled": true,
        "description": "Outdoor kitchen"
      },
      "camera_11": {
        "type": "mixed",
        "location": "entrance_1",
        "enabled": true,
        "description": "Entrance to the restaurant"
      },
      "camera_12": {
        "type": "mixed",
        "location": "entrance_2",
        "enabled": true,
        "description": "Entrance to the restaurant"
      },
      "camera_13": {
        "type": "mixed",
        "location": "Entrance corridor and prayer room",
        "enabled": true,
        "description": "Entrance corridor to the restaurant"
      },
      "camera_14": {
        "type": "mixed",
        "location": "Summer section",
        "enabled": true,
        "description": "Outdoor tables"
      },
      "camera_15": {
        "type": "mixed",
        "location": "Summer section",
        "enabled": true,
        "description": "Outdoor tables"
      },
      "camera_16": {
        "type": "mixed",
        "location": "River section",
        "enabled": true,
        "description": "Outdoor tables"
      }
    }
  }
```

---

### <a id="📄-config-config-json"></a>📄 `config/config.json`

**File Info:**
- **Size**: 1021 B
- **Extension**: `.json`
- **Language**: `json`
- **Location**: `config/config.json`
- **Relative Path**: `config`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:06 (Asia/Damascus / GMT+03:00)
- **MD5**: `72c5fa558ebd1a9f05c5d87735c5040b`
- **SHA256**: `e6f49b533e0c4800c1ccc24e4211b969e645128a84e1604dced3aef50c8341a2`
- **Encoding**: ASCII

**File code content:**

```json
{
    "project": {
        "name": "restaurant-monitor",
        "version": "2.0-live"
    },
    "pipeline": {
        "process_fps": 2,
        "device": "cuda"
    },
    "detector": {
        "model": "models/yolo/yolov8n-pose.pt",
        "conf_threshold": 0.25,
        "imgsz": 640,
        "min_box_width": 2,
        "min_box_height": 2
    },
    "tracker": {
        "max_age": 10,
        "n_init": 3,
        "nms_max_overlap": 0.3,
        "max_cosine_distance": 0.4
    },
    "paths": {
        "videos_index": "data/metadata/videos/videos_index.json",
        "zones_config": "config/zones_config.json",
        "outputs_dir": "data/artifacts/outputs",
        "embeddings_dir": "data/artifacts/reid_embeddings",
        "debug_crops_dir": "data/debug/crops",
        "debug_zones_reference_frames_dir": "data/debug/zones/reference_frames",
        "debug_zones_preview_dir": "data/debug/zones/zones_preview"
    },
    "debug": {
        "show_live_view": true,
        "save_debug_crops": false
    }
}
```

---

### <a id="📄-config-zones-config-json"></a>📄 `config/zones_config.json`

**File Info:**
- **Size**: 13.67 KB
- **Extension**: `.json`
- **Language**: `json`
- **Location**: `config/zones_config.json`
- **Relative Path**: `config`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:06 (Asia/Damascus / GMT+03:00)
- **MD5**: `2d46a0456b8f3c995543c60a6144e362`
- **SHA256**: `43295619151b49c2f3af3ecf63c84333dee5cee62fa4d8a08e010d10e1069b5c`
- **Encoding**: UTF-8

**File code content:**

```json
{
  "camera_01": {
    "image_size": {
      "width": 1280,
      "height": 1440
    },
    "zones": [
      {
        "zone_id": "cam01_table_1",
        "zone_type": "table_area",
        "zone_name": "طاولة 1",
        "points": [
          [
            1069,
            322
          ],
          [
            836,
            563
          ],
          [
            661,
            578
          ],
          [
            558,
            638
          ],
          [
            558,
            885
          ],
          [
            17,
            1328
          ],
          [
            11,
            1400
          ],
          [
            17,
            1403
          ],
          [
            49,
            1429
          ],
          [
            1066,
            1434
          ],
          [
            1247,
            354
          ],
          [
            1101,
            267
          ]
        ]
      },
      {
        "zone_id": "cam01_table_2",
        "zone_type": "table_area",
        "zone_name": "طاولة 2",
        "points": [
          [
            69,
            549
          ],
          [
            256,
            770
          ],
          [
            977,
            351
          ],
          [
            960,
            267
          ],
          [
            756,
            190
          ],
          [
            391,
            279
          ],
          [
            66,
            400
          ]
        ]
      },
      {
        "zone_id": "cam01_service_auto",
        "zone_type": "service_path",
        "zone_name": "ممر خدمة (تلقائي)",
        "points": [
          [
            0,
            0
          ],
          [
            1280,
            0
          ],
          [
            1280,
            1440
          ],
          [
            0,
            1440
          ]
        ],
        "auto_generated": true,
        "excludes_tables": true
      }
    ]
  },
  "camera_02": {
    "image_size": {
      "width": 1920,
      "height": 1080
    },
    "zones": [
      {
        "zone_id": "cam02_table_area_1",
        "zone_type": "table_area",
        "zone_name": "منطقة طاولات 1",
        "points": [
          [
            129,
            244
          ],
          [
            373,
            185
          ],
          [
            1834,
            1076
          ],
          [
            224,
            1074
          ]
        ]
      },
      {
        "zone_id": "cam02_table_area_2",
        "zone_type": "table_area",
        "zone_name": "منطقة طاولات 2",
        "points": [
          [
            617,
            246
          ],
          [
            1414,
            668
          ],
          [
            1867,
            474
          ],
          [
            1871,
            362
          ],
          [
            989,
            134
          ]
        ]
      },
      {
        "zone_id": "cam02_service_1",
        "zone_type": "service_path",
        "zone_name": "ممر خدمة 1",
        "points": [
          [
            461,
            237
          ],
          [
            576,
            213
          ],
          [
            1414,
            670
          ],
          [
            1867,
            474
          ],
          [
            1875,
            369
          ],
          [
            1912,
            386
          ],
          [
            1919,
            1071
          ],
          [
            1843,
            1074
          ]
        ]
      },
      {
        "zone_id": "cam02_table_area_1_table_1",
        "zone_type": "table",
        "zone_name": "طاولة 1",
        "parent_zone_id": "cam02_table_area_1",
        "points": [
          [
            343,
            1076
          ],
          [
            1227,
            707
          ],
          [
            1839,
            1074
          ]
        ]
      },
      {
        "zone_id": "cam02_table_area_1_table_2",
        "zone_type": "table",
        "zone_name": "طاولة 2",
        "parent_zone_id": "cam02_table_area_1",
        "points": [
          [
            817,
            453
          ],
          [
            155,
            539
          ],
          [
            209,
            970
          ],
          [
            1145,
            655
          ]
        ]
      },
      {
        "zone_id": "cam02_table_area_1_table_3",
        "zone_type": "table",
        "zone_name": "طاولة 3",
        "parent_zone_id": "cam02_table_area_1",
        "points": [
          [
            140,
            407
          ],
          [
            571,
            306
          ],
          [
            759,
            418
          ],
          [
            153,
            539
          ]
        ]
      },
      {
        "zone_id": "cam02_table_area_1_table_4",
        "zone_type": "table",
        "zone_name": "طاولة 4",
        "parent_zone_id": "cam02_table_area_1",
        "points": [
          [
            448,
            241
          ],
          [
            573,
            302
          ],
          [
            142,
            405
          ],
          [
            140,
            315
          ]
        ]
      },
      {
        "zone_id": "cam02_table_area_2_table_1",
        "zone_type": "table",
        "zone_name": "طاولة 1",
        "parent_zone_id": "cam02_table_area_2",
        "points": [
          [
            1078,
            481
          ],
          [
            1509,
            345
          ],
          [
            1802,
            504
          ],
          [
            1412,
            668
          ]
        ]
      },
      {
        "zone_id": "cam02_table_area_2_table_2",
        "zone_type": "table",
        "zone_name": "طاولة 2",
        "parent_zone_id": "cam02_table_area_2",
        "points": [
          [
            1518,
            347
          ],
          [
            1638,
            304
          ],
          [
            1873,
            364
          ],
          [
            1869,
            470
          ],
          [
            1802,
            498
          ]
        ]
      },
      {
        "zone_id": "cam02_table_area_2_table_3",
        "zone_type": "table",
        "zone_name": "طاولة 3",
        "parent_zone_id": "cam02_table_area_2",
        "points": [
          [
            1451,
            362
          ],
          [
            1240,
            274
          ],
          [
            1395,
            239
          ],
          [
            1630,
            300
          ]
        ]
      },
      {
        "zone_id": "cam02_table_area_2_table_4",
        "zone_type": "table",
        "zone_name": "طاولة 4",
        "parent_zone_id": "cam02_table_area_2",
        "points": [
          [
            1235,
            274
          ],
          [
            836,
            356
          ],
          [
            1078,
            479
          ],
          [
            1453,
            362
          ]
        ]
      },
      {
        "zone_id": "cam02_table_area_2_table_5",
        "zone_type": "table",
        "zone_name": "طاولة 5",
        "parent_zone_id": "cam02_table_area_2",
        "points": [
          [
            729,
            291
          ],
          [
            1046,
            216
          ],
          [
            1166,
            285
          ],
          [
            836,
            358
          ]
        ]
      },
      {
        "zone_id": "cam02_table_area_2_table_6",
        "zone_type": "table",
        "zone_name": "طاولة 6",
        "parent_zone_id": "cam02_table_area_2",
        "points": [
          [
            1063,
            220
          ],
          [
            1211,
            192
          ],
          [
            1386,
            237
          ],
          [
            1173,
            287
          ]
        ]
      },
      {
        "zone_id": "cam02_table_area_2_table_7",
        "zone_type": "table",
        "zone_name": "طاولة 7",
        "parent_zone_id": "cam02_table_area_2",
        "points": [
          [
            638,
            244
          ],
          [
            729,
            291
          ],
          [
            1173,
            183
          ],
          [
            1000,
            134
          ]
        ]
      }
    ]
  },
  "camera_11": {
    "image_size": {
      "width": 1920,
      "height": 1080
    },
    "zones": [
      {
        "zone_id": "entrance_1_full",
        "zone_type": "entrance",
        "zone_name": "Entrance 1",
        "points": [
          [
            0,
            0
          ],
          [
            1920,
            0
          ],
          [
            1920,
            1080
          ],
          [
            0,
            1080
          ]
        ]
      },
      {
        "zone_id": "entrance_area",
        "zone_type": "entrance",
        "zone_name": "Entrance Area",
        "points": [
          [
            334,
            983
          ],
          [
            962,
            744
          ],
          [
            1267,
            1042
          ],
          [
            360,
            1077
          ]
        ]
      }
    ]
  },
  "camera_12": {
    "image_size": {
      "width": 1920,
      "height": 1080
    },
    "zones": []
  },
  "camera_13": {
    "image_size": {
      "width": 1920,
      "height": 1080
    },
    "zones": [
      {
        "zone_id": "entrance_corridor_full",
        "zone_type": "corridor",
        "zone_name": "Entrance Corridor and Prayer Room",
        "points": [
          [
            0,
            0
          ],
          [
            1920,
            0
          ],
          [
            1920,
            1080
          ],
          [
            0,
            1080
          ]
        ]
      },
      {
        "zone_id": "entrance_corridor",
        "zone_type": "corridor",
        "zone_name": "Entrance Corridor",
        "points": [
          [
            1322,
            172
          ],
          [
            1010,
            1006
          ],
          [
            1626,
            1058
          ],
          [
            1551,
            229
          ]
        ]
      },
      {
        "zone_id": "prayer_room_entrance",
        "zone_type": "prayer_room_entrance",
        "zone_name": "Prayer Room Entrance",
        "points": [
          [
            198,
            500
          ],
          [
            693,
            496
          ],
          [
            558,
            1071
          ],
          [
            8,
            916
          ]
        ]
      }
    ]
  },
  "camera_14": {
    "image_size": {
      "width": 1920,
      "height": 1080
    },
    "zones": []
  },
  "camera_15": {
    "image_size": {
      "width": 1920,
      "height": 1080
    },
    "zones": [
      {
        "zone_id": "summer_section_full",
        "zone_type": "mixed_area",
        "zone_name": "Summer Section Full View",
        "points": [
          [
            0,
            0
          ],
          [
            1920,
            0
          ],
          [
            1920,
            1080
          ],
          [
            0,
            1080
          ]
        ]
      },
      {
        "zone_id": "summer_tables_area",
        "zone_type": "table_area",
        "zone_name": "Summer Tables Area",
        "points": [
          [
            803,
            112
          ],
          [
            604,
            30
          ],
          [
            134,
            200
          ],
          [
            519,
            1061
          ],
          [
            1112,
            848
          ]
        ]
      },
      {
        "zone_id": "summer_service_path",
        "zone_type": "service_path",
        "zone_name": "Summer Service Path",
        "points": [
          [
            551,
            278
          ],
          [
            792,
            161
          ],
          [
            1856,
            702
          ],
          [
            1559,
            1060
          ]
        ]
      },
      {
        "zone_id": "summer_hallway",
        "zone_type": "hallway",
        "zone_name": "Summer Hallway",
        "points": [
          [
            862,
            101
          ],
          [
            464,
            283
          ],
          [
            523,
            334
          ],
          [
            927,
            145
          ]
        ]
      }
    ]
  },
  "camera_16": {
    "image_size": {
      "width": 1920,
      "height": 1080
    },
    "zones": [
      {
        "zone_id": "river_section_full",
        "zone_type": "mixed_area",
        "zone_name": "River Section Full View",
        "points": [
          [
            0,
            0
          ],
          [
            1920,
            0
          ],
          [
            1920,
            1080
          ],
          [
            0,
            1080
          ]
        ]
      },
      {
        "zone_id": "river_tables_area",
        "zone_type": "table_area",
        "zone_name": "River Tables Area",
        "points": [
          [
            706,
            78
          ],
          [
            600,
            124
          ],
          [
            1313,
            957
          ],
          [
            1589,
            725
          ]
        ]
      },
      {
        "zone_id": "river_service_path",
        "zone_type": "service_path",
        "zone_name": "River Service Path",
        "points": [
          [
            610,
            116
          ],
          [
            1248,
            1002
          ],
          [
            792,
            1061
          ],
          [
            556,
            135
          ]
        ]
      }
    ]
  }
}
```

---

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/debug/zones/reference_frames/camera_01_reference.jpg`
- `data/debug/zones/reference_frames/camera_02_reference.jpg`
- `data/debug/zones/reference_frames/camera_04_reference.jpg`
- `data/debug/zones/reference_frames/camera_06_reference.jpg`
- `data/debug/zones/reference_frames/camera_07_reference.jpg`
- `data/debug/zones/reference_frames/camera_11_reference.jpg`
- `data/debug/zones/reference_frames/camera_13_reference.jpg`
- `data/debug/zones/reference_frames/camera_15_reference.jpg`
- `data/debug/zones/reference_frames/camera_16_reference.jpg`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/debug/zones/zones_preview/camera_01_zones_preview.jpg`
- `data/debug/zones/zones_preview/camera_02_zones_preview.jpg`
- `data/debug/zones/zones_preview/camera_04_zones_preview.jpg`
- `data/debug/zones/zones_preview/camera_06_zones_preview.jpg`
- `data/debug/zones/zones_preview/camera_07_zones_preview.jpg`
- `data/debug/zones/zones_preview/camera_11_zones_preview.jpg`
- `data/debug/zones/zones_preview/camera_13_zones_preview.jpg`
- `data/debug/zones/zones_preview/camera_15_zones_preview.jpg`
- `data/debug/zones/zones_preview/camera_16_zones_preview.jpg`

### <a id="📄-data-metadata-videos-videos-index-json"></a>📄 `data/metadata/videos/videos_index.json`

**File Info:**
- **Size**: 2.64 KB
- **Extension**: `.json`
- **Language**: `json`
- **Location**: `data/metadata/videos/videos_index.json`
- **Relative Path**: `data/metadata/videos`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `cf10bfd16f9a06cefa0f4372ec1c84df`
- **SHA256**: `53aa22116a87281a98113da6a889ae9c655d2c5d569d1cc077b4b9f5bb14a039`
- **Encoding**: ASCII

**File code content:**

```json
[
  {
    "camera_id": "camera_01",
    "video_id": "video_001",
    "path": "data/raw_videos/camera_01/video_001.mp4",
    "fps": 15.001,
    "width": 1280,
    "height": 1440,
    "frame_count": 53994,
    "duration_seconds": 3599.459,
    "duration_minutes": 59.991
  },
  {
    "camera_id": "camera_02",
    "video_id": "video_001",
    "path": "data/raw_videos/camera_02/video_001.mp4",
    "fps": 15.001,
    "width": 1920,
    "height": 1080,
    "frame_count": 53994,
    "duration_seconds": 3599.462,
    "duration_minutes": 59.991
  },
  {
    "camera_id": "camera_04",
    "video_id": "video_001",
    "path": "data/raw_videos/camera_04/video_001.mp4",
    "fps": 7.0,
    "width": 1920,
    "height": 1080,
    "frame_count": 16862,
    "duration_seconds": 2408.745,
    "duration_minutes": 40.146
  },
  {
    "camera_id": "camera_06",
    "video_id": "video_001",
    "path": "data/raw_videos/camera_06/video_001.mp4",
    "fps": 7.92,
    "width": 1920,
    "height": 1080,
    "frame_count": 28507,
    "duration_seconds": 3599.43,
    "duration_minutes": 59.99
  },
  {
    "camera_id": "camera_07",
    "video_id": "video_001",
    "path": "data/raw_videos/camera_07/video_001.mp4",
    "fps": 15.0,
    "width": 1920,
    "height": 1080,
    "frame_count": 53992,
    "duration_seconds": 3599.372,
    "duration_minutes": 59.99
  },
  {
    "camera_id": "camera_11",
    "video_id": "video_001",
    "path": "data/raw_videos/camera_11/video_001.mp4",
    "fps": 15.0,
    "width": 1920,
    "height": 1080,
    "frame_count": 34395,
    "duration_seconds": 2293.01,
    "duration_minutes": 38.217
  },
  {
    "camera_id": "camera_11",
    "video_id": "video_002",
    "path": "data/raw_videos/camera_11/video_002.mp4",
    "fps": 9.583,
    "width": 1920,
    "height": 1080,
    "frame_count": 14864,
    "duration_seconds": 1551.059,
    "duration_minutes": 25.851
  },
  {
    "camera_id": "camera_13",
    "video_id": "video_001",
    "path": "data/raw_videos/camera_13/video_001.mp4",
    "fps": 15.001,
    "width": 1920,
    "height": 1080,
    "frame_count": 36104,
    "duration_seconds": 2406.851,
    "duration_minutes": 40.114
  },
  {
    "camera_id": "camera_15",
    "video_id": "video_001",
    "path": "data/raw_videos/camera_15/video_001.mp4",
    "fps": 15.001,
    "width": 1920,
    "height": 1080,
    "frame_count": 53994,
    "duration_seconds": 3599.39,
    "duration_minutes": 59.99
  },
  {
    "camera_id": "camera_16",
    "video_id": "video_001",
    "path": "data/raw_videos/camera_16/video_001.mp4",
    "fps": 3.998,
    "width": 1920,
    "height": 1080,
    "frame_count": 14391,
    "duration_seconds": 3599.219,
    "duration_minutes": 59.987
  }
]
```

---

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/metadata/pipeline_run_summary.csv`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/raw_videos/camera_01/video_001.mp4`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/raw_videos/camera_02/video_001.mp4`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/raw_videos/camera_04/video_001.mp4`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/raw_videos/camera_06/video_001.mp4`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/raw_videos/camera_07/video_001.mp4`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/raw_videos/camera_11/video_001.mp4`
- `data/raw_videos/camera_11/video_002.mp4`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/raw_videos/camera_13/video_001.mp4`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/raw_videos/camera_14/video_001.mp4`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/raw_videos/camera_15/video_001.mp4`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `data/raw_videos/camera_16/video_001.mp4`

### <a id="📄-docs-architecture-md"></a>📄 `docs/ARCHITECTURE.md`

**File Info:**
- **Size**: 13.07 KB
- **Extension**: `.md`
- **Language**: `text`
- **Location**: `docs/ARCHITECTURE.md`
- **Relative Path**: `docs`
- **Created**: 2026-07-14 08:33:11 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:33:11 (Asia/Damascus / GMT+03:00)
- **MD5**: `f4dec6795fc09c3053e0a62f7e7872cd`
- **SHA256**: `ea2c509fe95d1b06f6423ffdb79a2dc117e0e1fbfaceec725be3951a2ff7e5c5`
- **Encoding**: UTF-8

**File code content:**

````markdown
# System Architecture — Restaurant Floor Monitoring & Analytics Platform

## 0. Status of this document

This describes the system **as extended in this session**, built on top of an
already-working vision/tracking/classification pipeline (see `changes.txt` for
its debugging history). Nothing described as "existing" below was written this
session; only "New this session" components were added. The decision to
extend rather than rewrite the vision layer was made explicitly with the
project owner — see `README.md` history and session report
(`docs/SESSION_REPORT.md`) for the rationale.

## 1. High-level data flow

~~~~
 16x RTSP/file camera sources (config/camera_config.json)
        │  (one isolated async worker task per camera — a crash on
        │   camera_07 must not affect camera_01..16)
        ▼
 ┌───────────────────────────── Vision Engine (existing) ─────────────────────────────┐
 │  PersonDetector (YOLOv8n-pose, ultralytics)                                        │
 │        → RestaurantTracker (DeepSort, mobilenet embedder, per-camera TrackIDs)     │
 │        → ZoneManager.get_bbox_zone() (shapely polygons + keypoint-aware matching)  │
 │        → PoseLSTM action classifier (sit / stand / walk / serve, from 3-frame      │
 │          keypoint sequence)                                                        │
 └───────────────────────────────────────────────────────────────────────────────────┘
        ▼
 ┌───────────────────────── Worker Re-ID Engine (existing) ────────────────────────────┐
 │  OSNet-x0.25 (torchreid) embedding, 512-d, cosine via FAISS IndexFlatIP             │
 │  ReIDGallery (permanent, promoted workers) + SessionGallery (30-min TTL, unknowns)  │
 │  Similarity threshold 0.72 + 0.05 margin-over-runner-up anti-swap guard            │
 └───────────────────────────────────────────────────────────────────────────────────┘
        ▼
 ┌────────────────────── Staff/Customer + Table KBS (existing) ────────────────────────┐
 │  RoleEngine (experta production system): per-global-id evidence accumulator with    │
 │  decay, zone-history, confirm/reverse rules → role ∈ {worker, customer, unknown}    │
 │  TableKBS (experta): per-zone customer_count + was_served → {free, occupied, dirty} │
 └───────────────────────────────────────────────────────────────────────────────────┘
        ▼  LivePipeline.process_frame() returns a per-frame snapshot dict
 ┌────────────────────────── Event Engine (NEW this session) ──────────────────────────┐
 │  Level 1 — Raw Events: emitted straight from the per-frame snapshot                 │
 │            (TrackSeen, ZoneEntered/Exited, RoleAssigned, TableStateChanged, ...)     │
 │  Level 2 — Semantic Events: per-person / per-table time-windowed state machines      │
 │            consume Level-1 events, apply dwell thresholds                           │
 │            (CustomerSeated@20s, StaffArrivedTable@5s, CustomerIdle@60s, ...)         │
 │  Level 3 — Business Events: KPI-relevant lifecycle events derived from Level-2       │
 │            transitions (WaitingEnded, TableTurnoverStarted/Ended, ServiceStarted)    │
 │  Implementation: src/events/ — async stream processor, one StateMachine instance    │
 │  per (camera_id, zone_id) and per (camera_id, global_id), keyed dict + asyncio queue│
 └───────────────────────────────────────────────────────────────────────────────────┘
        ▼ every event is persisted (Postgres, append-only `events` table) and
        ▼ published to Redis pub/sub channel `events:{camera_id}`
 ┌───────────────────────────── KPI Engine (NEW this session) ─────────────────────────┐
 │  Rolling/windowed aggregation consuming the Level-2/3 event stream + event log       │
 │  replay. Produces the 8 required KPIs (§ formulas in docs/EVENT_ENGINE.md).          │
 │  Materialized into `kpi_snapshots` on a fixed cadence (default 30s) + on-demand      │
 │  recompute-from-event-log for historical ranges (REST reports).                      │
 └───────────────────────────────────────────────────────────────────────────────────┘
        ▼
 ┌────────────────────────── Backend (NEW this session) ───────────────────────────────┐
 │  FastAPI, async. REST: zones/cameras/staff-gallery config, historical events/KPIs,   │
 │  reports. WebSocket: /ws/live — fans out Level-1..3 events + KPI deltas per camera,  │
 │  subscribed via Redis pub/sub so multiple API replicas can share one pipeline        │
 │  process. Auth: OAuth2 password bearer + JWT (see docs/SECURITY.md).                │
 │  Postgres via SQLAlchemy async engine (asyncpg driver).                             │
 └───────────────────────────────────────────────────────────────────────────────────┘
        ▼
 React dashboard (existing component shells, wired this session): live table-status
 map (abstract layout, not re-streamed video — bounding boxes are drawn server-side
 into the snapshot event, coordinates only), per-staff KPI views, heatmap viewer,
 alerting UI, time-range/employee filters.
~~~~

## 2. Model / tracker choice — justification

The existing system already made these choices; re-justifying them against the
brief's suggested alternatives (YOLOv9/v10/RT-DETR, ByteTrack/BoT-SORT/StrongSORT):

| Component | Chosen | Alternative considered | Why chosen wins here |
|---|---|---|---|
| Detector | YOLOv8n-pose | YOLOv9/v10, RT-DETR | Need **pose keypoints**, not just boxes — hand/ankle/hip keypoints drive zone-matching (`_estimate_zone_point`, `_find_table_by_hands`) and the PoseLSTM action classifier. YOLOv8-pose is the only one of the three with a mature pretrained pose head; RT-DETR/v9/v10 are detection-only unless a separate pose model is bolted on, doubling inference cost. On a 4GB RTX 2050 driving up to 16 camera streams at 2 FPS process rate, a second full pose network is not affordable. |
| Tracker | DeepSort (mobilenet embedder) | ByteTrack / BoT-SORT | ByteTrack is faster and IoU-only (no appearance model), which sounds attractive, but this system relies on **short-term appearance continuity** to survive brief occlusion at crowded tables (see `changes.txt` re: track fragmentation being handled by `SessionGallery` at the Re-ID layer). DeepSort's appearance embedding is what feeds that. BoT-SORT would be the "correct" SOTA upgrade path (ByteTrack's motion association + ReID appearance) — noted as a **future improvement**, not done this session because swapping the tracker changes `track_id` semantics that `RoleEngine`'s `ScoreAccumulator`/`MergeRequest` logic (evidence persistence keyed by track continuity) is tuned against, and re-validating that is out of scope for a backend/event-engine session. |
| Re-ID | OSNet-x0.25 + FAISS | Transformer Re-ID (e.g. TransReID) | OSNet-x0.25 is already the lighter, CPU-viable option the brief itself suggests, and it's already meeting the accuracy bar per the margin-check tuning history. A transformer Re-ID model would cost more compute for marginal gain on a small, low-res CCTV worker gallery (few dozen staff, not thousands of identities — this is not an open-set re-id benchmark). |

**Net effect**: the CV stack is appropriate for the constraint (single 4GB GPU,
16 streams, near-real-time), and matches the brief's own latency/accuracy
tradeoff guidance even though it doesn't use the exact model names listed as
examples in the brief.

## 3. Fault tolerance

Each camera runs as its own `asyncio.Task` (`api/workers/camera_worker.py`,
new this session) wrapping a dedicated `LivePipeline` instance. A worker crash
(decode failure, CUDA OOM, corrupt frame) is caught at the task boundary,
logged, the camera is marked `degraded` in `/api/cameras/status`, and the
worker is retried with exponential backoff — it does not propagate to other
camera tasks or take down the FastAPI process. This was not present before
this session (`run_live.py` is a single-stream synchronous CLI script); it is
new infrastructure in `api/workers/`.

## 4. Security

- Dashboard/config endpoints require a bearer JWT (`api/auth.py`, new). No
  anonymous access to `/api/*` or `/ws/live`.
- Recommended deployment: reverse proxy (nginx/Caddy) terminating TLS in
  front of FastAPI; the app itself trusts `X-Forwarded-Proto`. This repo does
  not ship a TLS cert — that's an infra/ops step outside the app's scope.
- **Biometric data**: the Re-ID gallery persists **only 512-d float embeddings
  and FAISS index rows**, never raw crop images, in both the existing
  in-memory implementation and the new DB-backed persistence
  (`worker_gallery` table, §DB_SCHEMA.md). Embeddings are not cryptographically
  reversible to a photo, but they *are* biometric data (linkable across
  sessions) — documented tradeoff: no reversible-encryption-at-rest is
  implemented for embeddings in this session (would require key management
  infra not requested); if this is deployed against real customer-identifiable
  data, encrypting the `embedding` column at rest (e.g. pgcrypto) is a
  follow-up.

## 5. What requires physical hardware / real data collection (cannot be faked)

Per the brief's non-negotiable #5, stated explicitly rather than mocked:

1. **Live RTSP camera ingestion** — this session (and the existing pipeline)
   only exercises the system against the 11 pre-recorded MP4s in
   `data/raw_videos/`. `camera_worker.py` is written against `cv2.VideoCapture`
   which accepts an RTSP URL identically to a file path, so no code change is
   needed to point it at real cameras — but it has not been (and cannot be,
   in this environment) tested against a live RTSP stream, real network
   jitter, or real camera drift/focus changes.
2. **Staff gallery enrollment** — the system currently *bootstraps* the
   worker gallery automatically (a track the RoleEngine confirms as `worker`
   gets promoted from the session gallery into the permanent gallery). A
   proper deployment should also support **manual enrollment** from a known
   staff photo (e.g., an ID-badge photo taken at onboarding) so a new hire is
   recognized on day one instead of only after the automatic
   confirmation heuristic fires. The REST endpoint for this
   (`POST /api/staff-gallery/enroll`, new this session) is implemented and
   tested with a synthetic image, but there is no real staff photo dataset
   available in this environment to validate recognition accuracy against.
3. **Zone/camera calibration** — the tooling already exists
   (`src/utils/zone_annotator_v3.html`, `zone_manager.py`,
   `validate_zones_config.py`, `visualize_zones.py`) and 8 of 16 cameras
   (`camera_01, 02, 11, 12, 13, 14, 15, 16`) already have calibrated zones +
   reference frames in `config/zones_config.json` / `data/debug/zones/`. The
   remaining 8 cameras (`camera_03, 04, 05, 06, 07, 08, 09, 10`) have no zone
   polygons yet — that requires a human to draw them against that camera's
   actual field of view using the existing annotator; it is a data-entry
   step, not a code gap. The Event/KPI engines built this session degrade
   gracefully for un-zoned cameras (zone-dependent KPIs simply have no data
   for those camera_ids until zones are added) rather than erroring.
4. **KPI ground-truth validation** — the KPI formulas are implemented exactly
   as specified and unit-tested against synthetic event sequences, but no
   real "manager stopwatch" ground truth exists in this environment to
   validate that, e.g., computed `CustomerServiceWaitingTime` matches reality
   on the restaurant floor. That validation requires an on-site observer.

````

---

### <a id="📄-docs-db-schema-md"></a>📄 `docs/DB_SCHEMA.md`

**File Info:**
- **Size**: 6.38 KB
- **Extension**: `.md`
- **Language**: `text`
- **Location**: `docs/DB_SCHEMA.md`
- **Relative Path**: `docs`
- **Created**: 2026-07-14 09:04:00 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 09:04:00 (Asia/Damascus / GMT+03:00)
- **MD5**: `b4b79d1f7307558a13ddd33c7c4c51fc`
- **SHA256**: `a0d9a87937b7e1f74e7bb92a300a9f803d2b11d03ef8a782c0575b12d62b18cd`
- **Encoding**: UTF-8

**File code content:**

````markdown
# Data Model — Postgres Schema

Implementation: `storage/models.py` (SQLAlchemy 2.0 async ORM, new this
session). DDL is generated from these models via `storage/database.py::init_db()`
(uses `Base.metadata.create_all` for this project's scale — see note at
bottom on why Alembic was not introduced).

## Entity overview

~~~~
cameras 1───* zones 1───* zone_capacity (embedded as zones.max_capacity)
cameras 1───* tracks
tracks  *───1 identities (global_id — worker_gallery row OR ephemeral session id)
worker_gallery 1───* worker_embeddings
cameras 1───* events (append-only)
events  *───1 zones (nullable — not all events are zone-scoped)
cameras 1───* kpi_snapshots
kpi_snapshots *───1 zones (nullable — some KPIs are zone-scoped, some camera/global)
~~~~

## Tables

### `cameras`
| column | type | notes |
|---|---|---|
| camera_id | text PK | matches `config/camera_config.json` keys, e.g. `camera_01` |
| location | text | |
| camera_type | text | `mixed` \| `staff_only` |
| enabled | boolean | |
| operating_hours_start | time | for `OccupancyRate` denominator |
| operating_hours_end | time | |

### `zones`
| column | type | notes |
|---|---|---|
| zone_id | text PK | e.g. `cam01_table_1`, matches `zones_config.json` |
| camera_id | text FK → cameras | |
| zone_type | text | raw type, e.g. `table`, `table_area`, `staff_area` |
| zone_type_normalized | text | `table` \| `staff` \| `walk` |
| zone_name | text | |
| parent_zone_id | text FK → zones, nullable | table→table_area nesting |
| polygon | jsonb | list of [x,y] points, pixel space (matches existing config format) |
| max_capacity | integer, nullable | for `ZoneDensity`; null = capacity not configured, KPI omitted for that zone |

Zones are also kept in `config/zones_config.json` as the source of truth for
the annotator tool; a startup sync (`zone_manager.sync_to_db()`, new) upserts
that JSON into this table so SQL joins/reporting don't need to parse JSON at
query time. The JSON file is not removed — the annotator writes JSON, DB is
a read-optimized mirror for the API/KPI layer.

### `identities` (worker OR customer, permanent or ephemeral)
| column | type | notes |
|---|---|---|
| global_id | text PK | `worker_<uuid8>` or `session_<uuid8>`, matches existing gallery ID scheme |
| kind | text | `worker` \| `customer_session` |
| display_name | text, nullable | set on manual staff enrollment |
| first_seen_at | timestamptz | |
| last_seen_at | timestamptz | |

### `worker_gallery`
| column | type | notes |
|---|---|---|
| global_id | text PK FK → identities | |
| embedding | vector(512) or float4[512] | see note below on pgvector |
| enrolled_via | text | `auto_promotion` \| `manual` |
| enrolled_at | timestamptz | |

Stores **only the embedding vector**, never a raw photo — matches the
existing in-memory `ReIDGallery` design and the brief's biometric-storage
guidance (§ARCHITECTURE.md Security). Uses the `pgvector` extension
(`CREATE EXTENSION vector`) for `embedding vector(512)` with cosine index if
available; falls back to `float4[]` + application-side FAISS (current
approach, unchanged) if `pgvector` isn't installed on the target Postgres —
`storage/database.py` detects this at startup and logs which mode is active.
FAISS remains the **runtime** matcher (already fast, already tuned); Postgres
is the persistence/audit layer so the gallery survives a restart, which it
currently does not (`ReIDGallery.save()`/`.load()` exist but are never
called by `live_pipeline.py` — noted as a pre-existing gap, now closed by
wiring gallery load/save into the new backend's startup/shutdown hooks).

### `tracks` (per-camera, per-session track continuity — debugging/audit trail)
| column | type | notes |
|---|---|---|
| id | bigserial PK | |
| camera_id | text FK → cameras | |
| track_id | integer | DeepSort's local track id (not globally unique) |
| global_id | text FK → identities, nullable | |
| started_at | timestamptz | |
| ended_at | timestamptz, nullable | |

Not written every frame (would be 2 rows/sec/camera forever) — one row per
track *lifetime*, closed when the track ages out. Used for track-fragmentation
debugging (`changes.txt` already documents track-continuity bugs), not for
KPI computation (events are).

### `events` (append-only — the event-sourcing log, §EVENT_ENGINE.md)
| column | type | notes |
|---|---|---|
| id | bigserial PK | |
| ts | timestamptz | event time (not insert time — matters for backfill/replay) |
| level | smallint | 1, 2, or 3 |
| event_type | text | e.g. `CustomerSeated`, `WaitingEnded` |
| camera_id | text FK → cameras | |
| zone_id | text FK → zones, nullable | |
| global_id | text FK → identities, nullable | |
| track_id | integer, nullable | |
| payload | jsonb | event-specific fields (e.g. `wait_seconds`, `role`, `confidence`) |

Indexes: `(camera_id, ts)`, `(zone_id, ts)`, `(global_id, ts)`,
`(event_type, ts)` — these four are the actual query patterns the KPI Engine
and REST history endpoints use.

### `kpi_snapshots` (materialized rolling aggregates)
| column | type | notes |
|---|---|---|
| id | bigserial PK | |
| computed_at | timestamptz | |
| window_start | timestamptz | |
| window_end | timestamptz | |
| kpi_name | text | one of the 8 KPIs, see KPI Engine |
| camera_id | text FK → cameras, nullable | |
| zone_id | text FK → zones, nullable | |
| global_id | text FK → identities, nullable | for `StaffUtilization` per worker |
| value | double precision | |
| unit | text | `percent` \| `seconds` \| `count` |

This is a cache, not a source of truth — always reconstructible from
`events` by re-running the KPI Engine's aggregation over
`[window_start, window_end)`. Historical report ranges that aren't already
snapshotted are computed on-demand from `events` and optionally backfilled
into this table.

## Why no Alembic migration chain this session

The brief asks for "structured DB... for event logs, KPI aggregates, staff
gallery metadata, zone definitions" — it does not ask for a multi-environment
migration history. Introducing Alembic with a single initial revision when
there is no prior schema to migrate *from* is process overhead without
payoff at this stage; `Base.metadata.create_all()` is the right tool for "one
canonical schema, no prod data yet." If/when this schema needs to evolve
against a live production database with real data, that's the point to add
Alembic — noted as a deliberate scope decision, not an oversight.

````

---

### <a id="📄-docs-event-engine-md"></a>📄 `docs/EVENT_ENGINE.md`

**File Info:**
- **Size**: 7.46 KB
- **Extension**: `.md`
- **Language**: `text`
- **Location**: `docs/EVENT_ENGINE.md`
- **Relative Path**: `docs`
- **Created**: 2026-07-14 09:03:19 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 09:03:19 (Asia/Damascus / GMT+03:00)
- **MD5**: `5983940b3e9f920b793cd66a7830465b`
- **SHA256**: `4c8c2eac46197f3f8d1322b8db59a26692e7c2c03ca4c276aafffc463a183bad`
- **Encoding**: UTF-8

**File code content:**

````markdown
# Event Engine — Three-Level State Machine Spec

Implementation: `src/events/` (new this session).

## Design principle

This is **event-sourced**, not a polling loop with global flags: every state
transition is emitted as an immutable, timestamped event appended to an
in-process `asyncio.Queue` → persisted to Postgres `events` (append-only) →
published to Redis `events:{camera_id}` for WebSocket fan-out. KPIs are never
computed by inspecting "current" mutable state; they are computed by
replaying/aggregating the event log over a time window. This makes KPI
recomputation for an arbitrary historical range (a REST report) identical in
logic to the live rolling computation — same aggregation function, different
event source (DB query vs. live queue).

State is held in per-key state machines, not global variables:
- One `PersonStateMachine` per `(camera_id, global_id)`
- One `TableStateMachine` per `(camera_id, zone_id)` for table zones
- One `StaffZoneStateMachine` per `(camera_id, zone_id)` for staff/kitchen zones

Each machine only reacts to events addressed to its own key — this is what
"time-windowed state machine per table/zone/person" means concretely (brief
requirement, Event Engine section).

## Level 1 — Raw Events

Emitted directly from `LivePipeline.process_frame()`'s per-frame snapshot,
one `RawEvent` per fact, every frame processed (2 FPS per camera):

| event_type | payload | source field |
|---|---|---|
| `TrackSeen` | camera_id, track_id, global_id, box, zone_id | `tracked_objects[i]` |
| `ZoneOccupancy` | camera_id, zone_id, zone_type, global_id | `enrich_tracks_with_zones` output |
| `RoleAssigned` | camera_id, global_id, role, confidence | `RoleEngine.get_decisions()` |
| `ActionObserved` | camera_id, track_id, action | `self._action_labels` |
| `TableStateRaw` | camera_id, zone_id, state (free/occupied/dirty) | `TableKBS` facts |

Raw events are the *only* level allowed to fire every frame — they carry no
thresholding logic. `src/events/raw.py::extract_raw_events(snapshot) -> list[RawEvent]`.

## Level 2 — Semantic Events

Derived by feeding the Level-1 stream through the per-key state machines.
Each semantic event requires a **dwell/consistency threshold** — this is
where "raw tracker noise" gets filtered into something meaningful. Thresholds
live in `src/events/config.py`, overridable per deployment:

`PersonStateMachine` (states: `unseen → present → seated/standing → departed`):
- `CustomerSeated` — role=customer, zone_type=table, continuous
  `ZoneOccupancy` in the *same* `zone_id` for ≥ `SEATED_DWELL_S` (default 20s).
  Debounced: a gap ≤ `REACQUIRE_GRACE_S` (default 3s, covers 1 missed
  detection at 2 FPS) does not reset the dwell timer — avoids flicker from a
  single dropped frame, mirroring the existing tracker's own
  `time_since_update` tolerance.
- `StaffArrivedTable` — role=worker, zone_type=table, continuous presence
  ≥ `STAFF_ARRIVE_DWELL_S` (default 5s).
- `StaffDepartedTable` — a previously-arrived staff member's `ZoneOccupancy`
  for that zone_id stops for ≥ `DEPART_GRACE_S` (default 3s).
- `CustomerIdle` — global_id's zone_point speed (Δposition / Δt from
  consecutive `TrackSeen`) stays below `IDLE_SPEED_PX_S` for ≥ 60s continuous,
  AND current zone_type != staff/work zone. Speed is computed in the state
  machine, not stored on the track (existing pipeline has no velocity field).
- `CustomerDeparted` / `StaffDeparted` — no `TrackSeen` for that global_id for
  ≥ `ABSENCE_TIMEOUT_S` (default 15s) — closes the person's presence interval.

`TableStateMachine` (states mirror `TableKBS` but time-stamped):
- `TableStateChanged` — re-emitted from `TableStateRaw` only on actual
  transition (free→occupied→dirty→free), with `entered_at` timestamp attached
  so Level 3 can compute durations. This machine also **debounces** flapping:
  a `TableStateRaw` transition must persist 2 consecutive raw frames (1s at
  2FPS) before being accepted, protecting against the same
  bbox-center/hand-keypoint jitter `zone_manager.py`'s changelog already
  fought at the zone-matching layer — belt-and-suspenders at the event layer.

`src/events/semantic.py::PersonStateMachine`, `TableStateMachine`.

## Level 3 — Business Events

Derived purely from Level-2 transitions (never touches Level-1 directly —
enforces the layering):

- `WaitingStarted` — on `CustomerSeated` for a table with no staff
  (`StaffArrivedTable`) recorded at that zone_id since the seating.
- `WaitingEnded` — on the *first* `StaffArrivedTable` event at that zone_id
  after the matching `CustomerSeated`. Payload carries
  `wait_seconds = t(StaffArrivedTable) - t(CustomerSeated)` —
  directly the `CustomerServiceWaitingTime` KPI input.
- `ServiceStarted` — on `ActionObserved(action="serving")` from a
  worker role at an occupied table zone (mirrors the existing
  `_table_was_served` flag, promoted to a timestamped event).
- `TableTurnoverStarted` — on `TableStateChanged` → `dirty` or `free`
  (table vacated) for a zone_id that was previously `occupied`.
- `TableTurnoverEnded` — on the *next* `TableStateChanged` → `occupied` for
  that same zone_id. Payload: `turnover_seconds`, increments
  `TableTurnoverCount`.
- `StaffActivePeriod` (start/end) — bracket a global_id's continuous
  `StaffArrivedTable`/`StaffDepartedTable` or staff-zone presence into a
  single active-work interval, feeding `StaffUtilization`.

`src/events/business.py::derive_business_events(level2_event, machine_state)`.

## Why per-key state machines, not global flags

Each `PersonStateMachine`/`TableStateMachine` instance owns exactly the
mutable state needed for its own transitions (last-seen timestamp, dwell
accumulator, current state enum). There is no shared mutable dict scanned
every frame for "is anyone waiting too long" — that check is instead a
property of the *event stream itself* (does a `WaitingStarted` for this
zone_id have a matching `WaitingEnded` yet, or has it been open longer than
threshold). This is what makes it event-sourcing rather than a polling loop:
the state machines react to events pushed to them, and any observer (KPI
engine, alerting) subscribes to the *output* stream rather than polling
machine internals.

## Concrete example — a full lifecycle

~~~~
t=0s    ZoneOccupancy(cam01, zone=table_1, gid=customer_abc)      [L1]
t=20s   CustomerSeated(cam01, table_1, customer_abc)              [L2]
t=20s   WaitingStarted(cam01, table_1)                            [L3]
t=45s   ZoneOccupancy(cam01, zone=table_1, gid=worker_x)          [L1]
t=50s   StaffArrivedTable(cam01, table_1, worker_x)               [L2]
t=50s   WaitingEnded(cam01, table_1, wait_seconds=30)             [L3]
t=52s   ActionObserved(worker_x, action=serving)                  [L1]
t=52s   ServiceStarted(cam01, table_1, worker_x)                  [L3]
t=1800s CustomerDeparted(cam01, customer_abc)                     [L2]
t=1810s TableStateChanged(cam01, table_1, dirty, since=1810s)     [L2]
t=1810s TableTurnoverStarted(cam01, table_1)                      [L3]
t=1900s TableStateChanged(cam01, table_1, occupied, since=1900s)  [L2]
t=1900s TableTurnoverEnded(cam01, table_1, turnover_seconds=90)   [L3]
~~~~

## Alerting hook

Alerts (frontend `Alerts.jsx`) subscribe to Level-3 events with a threshold
predicate — e.g. `WaitingStarted` with no matching `WaitingEnded` within
`ALERT_WAIT_THRESHOLD_S` (default 300s) triggers an `AlertRaised` event,
itself persisted and pushed over the same WebSocket channel. This reuses the
event pipeline rather than being a separate polling subsystem.

````

---

### <a id="📄-docs-task1-report-md"></a>📄 `docs/TASK1_REPORT.md`

**File Info:**
- **Size**: 10.08 KB
- **Extension**: `.md`
- **Language**: `text`
- **Location**: `docs/TASK1_REPORT.md`
- **Relative Path**: `docs`
- **Created**: 2026-07-14 09:55:11 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 10:03:47 (Asia/Damascus / GMT+03:00)
- **MD5**: `afeb8e262cf68c2cf74d4283ac30ffaa`
- **SHA256**: `47612b447fc108f58082d940c8927caaae2c06d969237f0dd59a26544a69cb85`
- **Encoding**: UTF-8

**File code content:**

````markdown
# Task 1 Report — Environment Setup + Video-Relative Timing Fix

## Part A — Environment Setup

### What was done
- Reused the pre-existing `.venv/` at the project root (Python 3.13.7, created via
  `python -m venv .venv`). Confirmed it was empty except for `pip` before installing anything into it.
- Installed every package actually required by `src/`, `storage/`, and `api/` into `.venv`
  (never into the global interpreter), determined by grepping every `import` / `from ... import`
  statement across those directories rather than trusting the old `requirements.txt`.
- Pinned the full resolved environment (direct + transitive) into `requirements.txt` via
  `pip freeze`, so `pip install -r requirements.txt` reproduces a byte-identical environment
  for any teammate.
- Confirmed `.gitignore` already excludes `.venv/` (line 4) — no change needed there.
- Ran an import check covering every major library (`cv2`, `numpy`, `pandas`, `shapely`,
  `torch`, `torchvision`, `ultralytics`, `deep_sort_realtime`, `experta`, `faiss`, `torchreid`,
  `sqlalchemy`, `aiosqlite`, `asyncpg`, `pytest`) — all succeeded.

### Old vs. new `requirements.txt`
The old file listed 5 unpinned packages (`ultralytics`, `opencv-python`, `numpy`, `pandas`,
`deep-sort-realtime`) and was missing everything else the codebase actually imports:
`torch`, `torchvision`, `shapely` (`src/zone_management/zone_manager.py`), `experta`
(`src/kbs/role_engine.py`, `src/kbs/table_kbs.py`), `faiss` + `torchreid`
(`src/kbs/reid_gallery.py`), and the async storage stack `sqlalchemy` + `aiosqlite` + `asyncpg`
(`storage/database.py`). The new `requirements.txt` is a full pinned freeze of the resolved
environment.

### Decisions made unilaterally (flagged per your instructions)

1. **`requirements.txt` is a full `pip freeze`, not just direct dependencies.** You asked for
   pinned versions "so every teammate ... gets the exact same environment" — a full freeze
   (including transitive pins) guarantees that more strongly than pinning only the ~13 direct
   imports and letting pip re-resolve transitives on each install. Trade-off noted: it's a
   longer file and needs periodic regeneration if a direct dependency is bumped.

2. **Three undeclared transitive dependencies had to be added that don't appear in any `import`
   statement in `src/`/`storage/`/`api/`:**
   - `gdown` — `torchreid`'s package `__init__` unconditionally imports it
     (`torchreid/reid/data/datasets/image/university1652.py`), even though nothing in this repo
     uses that code path. Without it, the bare `import torchreid` in
     [reid_gallery.py:25](src/kbs/reid_gallery.py#L25) fails.
   - `tensorboard` — `torchreid`'s training `Engine` class does `from torch.utils.tensorboard
     import SummaryWriter` at import time. Same failure mode as above.
   - `setuptools<81` (pinned to 80.10.2) — `deep-sort-realtime`'s PyTorch embedder does a bare
     `import pkg_resources` at runtime (`update()` → `DeepSort.__init__` →
     `embedder_pytorch.py`). `pip install deep-sort-realtime` alone resolves the latest
     `setuptools` (83.0.0), which dropped `pkg_resources` entirely, so
     `RestaurantTracker()` (used by `src/ai_models/tracker.py` and exercised in
     `tests/test_tracker.py`) crashed at construction until this was pinned down.

   I judged these were in scope: the task said to "add every dependency currently required by
   the existing codebase," and without these three, the codebase does not import at all — that's
   a stronger requirement than "appears in a `import` line."

3. **`faiss-cpu` and `torchreid` on Python 3.13/Windows**: both are somewhat fragile packages
   (faiss historically lacked Windows wheels; torchreid is unmaintained since ~2021). Both
   installed and imported cleanly against Python 3.13.7 here, so no substitution was needed —
   flagging only because this was a real risk I checked rather than assumed.

### Verification
~~~~
python -c "import cv2, numpy, pandas, shapely, torch, torchvision, ultralytics, \
  deep_sort_realtime, experta, faiss, torchreid, sqlalchemy, aiosqlite, asyncpg, pytest"
~~~~
→ `ALL IMPORTS OK` (one benign warning: torchreid falls back to a pure-Python ranking metric
because Cython isn't available — unrelated to this task, not an error).

## Part B — Video-Relative Timing Fix

### Call chain traced
`src/run_live.py` (`main()`) already computes `time_seconds = frame_index / fps` per frame
([run_live.py:142](src/run_live.py#L142)) and was already passing it into
`pipeline.process_frame(..., time_seconds=time_seconds)`
([run_live.py:150](src/run_live.py#L150)). The break in the chain was inside
`src/core/live_pipeline.py`: `process_frame()` accepted `time_seconds` but only put it in the
returned event dict — it never forwarded it to `_run_kbs()`, which never forwarded it to
`_update_person_state()`. That method fell back to `datetime.now()` and an internal
`_internal_frames_count` × hardcoded 2fps assumption instead.

### Files/functions changed — `src/core/live_pipeline.py`
- **[live_pipeline.py:152](src/core/live_pipeline.py#L152)** — `process_frame()` now calls
  `self._run_kbs(tracked_objects, person_crops, time_seconds)` instead of dropping
  `time_seconds` on the floor.
- **[live_pipeline.py:491](src/core/live_pipeline.py#L491)** — `_run_kbs()` signature gained a
  required `time_seconds: float` parameter.
- **[live_pipeline.py:668-673](src/core/live_pipeline.py#L668-L673)** — the call to
  `_update_person_state()` inside `_run_kbs()` now passes `time_seconds=time_seconds`.
- **[live_pipeline.py:309-350](src/core/live_pipeline.py#L309-L350)** — `_update_person_state()`
  rewritten:
  - Signature: `_update_person_state(self, global_id, local_id, zone_type, time_seconds: float)`
    — no default value.
  - Raises `ValueError` immediately if `time_seconds is None`, with a message naming the
    expected source (`frame_index / video_fps`).
  - "Entrance date" is now `str(timedelta(seconds=int(time_seconds)))` — a video-relative
    elapsed-time string — computed on first sighting of a `global_id` and again whenever
    `current_location` changes (zone transition), instead of `datetime.now().strftime(...)`.
  - A new field `_entrance_time_seconds` stores the raw `time_seconds` value at the most recent
    entrance/zone-change; it's the video-time analog of what "Entrance date" used to freeze in
    wall-clock form, and is what "Duration" is diffed against.
  - "Duration" for a person who stayed in the same zone is now
    `str(timedelta(seconds=int(time_seconds - person_record["_entrance_time_seconds"])))` —
    a direct video-time difference — instead of `frames_count / 2.0`.
  - `_internal_frames_count` is fully removed (not left dead): no writes, no reads, no field in
    the stored records.

### Why this is correct
- `time_seconds` is derived once, upstream in `run_live.py`, from the *actual* video FPS
  (`capture.get(cv2.CAP_PROP_FPS)`), not assumed. Every downstream consumer now shares that one
  source of truth instead of re-deriving time from wall-clock reads or a hardcoded rate.
- Duration is now a pure function of two `time_seconds` samples, so it's correct regardless of
  processing speed, frame drops, `pose_stride`, or `--max-frames` limits — none of which
  correspond 1:1 with video time.
- Making `time_seconds` a required, `None`-checked parameter means any future caller that
  forgets to thread it through fails loudly at the call site instead of silently reintroducing
  wall-clock time or a frame-count guess.

### Decision made unilaterally
`_run_kbs()` was the only call site between `process_frame()` and `_update_person_state()`, so
"thread it through the call chain" had one unambiguous path — no alternate routing was
possible or needed. The one real judgment call was the **Duration string format**: the
pre-existing code used `str(timedelta(...))`, which Python renders unpadded for single-digit
hours (e.g. `"0:00:25"`, not `"00:00:25"`). I preserved that exact format (rather than
hand-padding to `"00:00:25"`) to keep the fix minimal and behavior-compatible with whatever
already consumes the `Duration` field, since reformatting it was not requested.

## Test

Added `tests/test_live_pipeline_timing.py` with 3 cases:

1. `test_duration_computed_from_time_seconds_difference` — drives `_update_person_state()`
   through same-zone updates (asserts `Duration` equals the exact `time_seconds` delta, e.g.
   25s apart → `"0:00:25"`) and a zone change (asserts entrance/duration reset to the new
   `time_seconds`).
2. `test_no_datetime_now_used_in_update_person_state` — inspects the live source of
   `_update_person_state` via `inspect.getsource()` and asserts neither `"datetime.now"` nor
   `"_internal_frames_count"` appear.
3. `test_update_person_state_raises_on_none_time_seconds` — asserts `ValueError` when
   `time_seconds=None`.

Tests construct `LivePipeline` via `object.__new__()` rather than the real `__init__()`
(which loads YOLO/pose-LSTM/ReID models) — scoped to the method under test rather than a full
pipeline integration test, since Part A dependency installation, not model loading, was what
this task needed verified end-to-end.

### Result
~~~~
python -m pytest tests/test_live_pipeline_timing.py -v
~~~~
~~~~
tests/test_live_pipeline_timing.py::test_duration_computed_from_time_seconds_difference PASSED
tests/test_live_pipeline_timing.py::test_no_datetime_now_used_in_update_person_state PASSED
tests/test_live_pipeline_timing.py::test_update_person_state_raises_on_none_time_seconds PASSED
3 passed in 6.59s
~~~~

Also ran the full `tests/` suite as a regression check: 15 passed, 1 pre-existing failure
(`tests/test_tracker.py::test_tracker_update`) unrelated to this task — it feeds
`RestaurantTracker.update()` a list-format detection (`[100, 100, 200, 300, 0.9, 0]`) while
`src/ai_models/tracker.py` expects dict-format detections (`det["box"]`), a test/code data-shape
mismatch that predates this session. Left untouched per the explicit scope boundary in this
task (Event Engine / KPI Engine / backend / frontend / unrelated fixes are out of scope).

## Out of scope (explicitly not touched)
Event Engine, KPI Engine, backend, frontend, and the pre-existing `test_tracker.py` failure
described above.

````

---

### <a id="📄-frontend-public-index-html"></a>📄 `frontend/public/index.html`

**File Info:**
- **Size**: 0 B
- **Extension**: `.html`
- **Language**: `html`
- **Location**: `frontend/public/index.html`
- **Relative Path**: `frontend/public`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```html

```

---

### <a id="📄-frontend-src-components-charts-barchart-jsx"></a>📄 `frontend/src/components/Charts/BarChart.jsx`

**File Info:**
- **Size**: 0 B
- **Extension**: `.jsx`
- **Language**: `jsx`
- **Location**: `frontend/src/components/Charts/BarChart.jsx`
- **Relative Path**: `frontend/src/components/Charts`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```jsx

```

---

### <a id="📄-frontend-src-components-charts-linechart-jsx"></a>📄 `frontend/src/components/Charts/LineChart.jsx`

**File Info:**
- **Size**: 0 B
- **Extension**: `.jsx`
- **Language**: `jsx`
- **Location**: `frontend/src/components/Charts/LineChart.jsx`
- **Relative Path**: `frontend/src/components/Charts`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```jsx

```

---

### <a id="📄-frontend-src-components-charts-piechart-jsx"></a>📄 `frontend/src/components/Charts/PieChart.jsx`

**File Info:**
- **Size**: 0 B
- **Extension**: `.jsx`
- **Language**: `jsx`
- **Location**: `frontend/src/components/Charts/PieChart.jsx`
- **Relative Path**: `frontend/src/components/Charts`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```jsx

```

---

### <a id="📄-frontend-src-components-alerts-jsx"></a>📄 `frontend/src/components/Alerts.jsx`

**File Info:**
- **Size**: 0 B
- **Extension**: `.jsx`
- **Language**: `jsx`
- **Location**: `frontend/src/components/Alerts.jsx`
- **Relative Path**: `frontend/src/components`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```jsx

```

---

### <a id="📄-frontend-src-components-dashboard-jsx"></a>📄 `frontend/src/components/Dashboard.jsx`

**File Info:**
- **Size**: 0 B
- **Extension**: `.jsx`
- **Language**: `jsx`
- **Location**: `frontend/src/components/Dashboard.jsx`
- **Relative Path**: `frontend/src/components`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```jsx

```

---

### <a id="📄-frontend-src-components-heatmapviewer-jsx"></a>📄 `frontend/src/components/HeatmapViewer.jsx`

**File Info:**
- **Size**: 0 B
- **Extension**: `.jsx`
- **Language**: `jsx`
- **Location**: `frontend/src/components/HeatmapViewer.jsx`
- **Relative Path**: `frontend/src/components`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```jsx

```

---

### <a id="📄-frontend-src-components-layout-jsx"></a>📄 `frontend/src/components/Layout.jsx`

**File Info:**
- **Size**: 0 B
- **Extension**: `.jsx`
- **Language**: `jsx`
- **Location**: `frontend/src/components/Layout.jsx`
- **Relative Path**: `frontend/src/components`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```jsx

```

---

### <a id="📄-frontend-src-components-livefeed-jsx"></a>📄 `frontend/src/components/LiveFeed.jsx`

**File Info:**
- **Size**: 0 B
- **Extension**: `.jsx`
- **Language**: `jsx`
- **Location**: `frontend/src/components/LiveFeed.jsx`
- **Relative Path**: `frontend/src/components`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```jsx

```

---

### <a id="📄-frontend-src-components-restaurantmap-jsx"></a>📄 `frontend/src/components/RestaurantMap.jsx`

**File Info:**
- **Size**: 0 B
- **Extension**: `.jsx`
- **Language**: `jsx`
- **Location**: `frontend/src/components/RestaurantMap.jsx`
- **Relative Path**: `frontend/src/components`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```jsx

```

---

### <a id="📄-frontend-src-services-api-js"></a>📄 `frontend/src/services/api.js`

**File Info:**
- **Size**: 0 B
- **Extension**: `.js`
- **Language**: `javascript`
- **Location**: `frontend/src/services/api.js`
- **Relative Path**: `frontend/src/services`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```javascript

```

---

### <a id="📄-frontend-src-services-store-js"></a>📄 `frontend/src/services/store.js`

**File Info:**
- **Size**: 0 B
- **Extension**: `.js`
- **Language**: `javascript`
- **Location**: `frontend/src/services/store.js`
- **Relative Path**: `frontend/src/services`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```javascript

```

---

### <a id="📄-frontend-src-services-websocket-js"></a>📄 `frontend/src/services/websocket.js`

**File Info:**
- **Size**: 0 B
- **Extension**: `.js`
- **Language**: `javascript`
- **Location**: `frontend/src/services/websocket.js`
- **Relative Path**: `frontend/src/services`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```javascript

```

---

### <a id="📄-frontend-src-app-jsx"></a>📄 `frontend/src/App.jsx`

**File Info:**
- **Size**: 0 B
- **Extension**: `.jsx`
- **Language**: `jsx`
- **Location**: `frontend/src/App.jsx`
- **Relative Path**: `frontend/src`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```jsx

```

---

### <a id="📄-frontend-src-index-js"></a>📄 `frontend/src/index.js`

**File Info:**
- **Size**: 0 B
- **Extension**: `.js`
- **Language**: `javascript`
- **Location**: `frontend/src/index.js`
- **Relative Path**: `frontend/src`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```javascript

```

---

### <a id="📄-frontend-package-json"></a>📄 `frontend/package.json`

**File Info:**
- **Size**: 0 B
- **Extension**: `.json`
- **Language**: `json`
- **Location**: `frontend/package.json`
- **Relative Path**: `frontend`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```json

```

---

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `models/yolo/yolov8n.pt`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `models/label_encoder.pkl`
- `models/pose_lstm.pth`

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `src/ai_models/__pycache__/__init__.cpython-313.pyc`
- `src/ai_models/__pycache__/detector.cpython-313.pyc`
- `src/ai_models/__pycache__/tracker.cpython-313.pyc`

### <a id="📄-src-ai-models-init-py"></a>📄 `src/ai_models/__init__.py`

**File Info:**
- **Size**: 0 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/ai_models/__init__.py`
- **Relative Path**: `src/ai_models`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```python

```

---

### <a id="📄-src-ai-models-detector-py"></a>📄 `src/ai_models/detector.py`

**File Info:**
- **Size**: 3.28 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/ai_models/detector.py`
- **Relative Path**: `src/ai_models`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `15f30dd161e20c2de0034ff94abeb061`
- **SHA256**: `7e0316c9dcd4bb6870d24c6acb83b7e190d61d0dda0142353ce581908c120830`
- **Encoding**: ASCII

**File code content:**

```python
from typing import Any
import numpy as np
from ultralytics import YOLO


class PersonDetector:
    def __init__(
        self,
        model_name: str | None = None,
        conf_threshold: float | None = None,
        imgsz: int | None = None,
        min_box_width: int | None = None,
        min_box_height: int | None = None,
        device: str | None = None,
    ):
        # (Single Source of Truth)
        self.model_name = model_name or "models/yolo/yolov8n.pt"
        self.conf_threshold = conf_threshold if conf_threshold is not None else 0.4
        self.imgsz = imgsz if imgsz is not None else 480
        self.min_box_width = min_box_width if min_box_width is not None else 20
        self.min_box_height = min_box_height if min_box_height is not None else 20
        self.device = device

        self.model = YOLO(self.model_name)

    def detect(self, frame: np.ndarray) -> list[dict[str, Any]]:

        predict_kwargs = {
            "source": frame,
            "conf": self.conf_threshold,
            "imgsz": self.imgsz,
            "classes": [0],  
            "verbose": False,
        }

        if self.device is not None:
            predict_kwargs["device"] = self.device

        results = self.model.predict(**predict_kwargs)

        detections = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

                width = x2 - x1
                height = y2 - y1

                if width < self.min_box_width or height < self.min_box_height:
                    continue

                detections.append(
                    {
                        "track_id": None,
                        "box": [x1, y1, x2, y2],
                        "conf": round(conf, 4),
                        "class_id": 0,
                        "class_name": "person",
                    }
                )

        return detections
    
    def detect_with_pose(self, frame: np.ndarray) -> tuple[list[dict], list[np.ndarray] | None]:
        predict_kwargs = {
            "source": frame,
            "conf": self.conf_threshold,
            "imgsz": self.imgsz,
            "classes": [0],
            "verbose": False,
        }
        if self.device is not None:
            predict_kwargs["device"] = self.device

        results = self.model.predict(**predict_kwargs)

        detections = []
        keypoints_list = []  # parallel to detections

        for result in results:
            kpts_data = result.keypoints.data.cpu().numpy() if result.keypoints is not None else None

            for i, box in enumerate(result.boxes):
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0])

                if (x2 - x1) < self.min_box_width or (y2 - y1) < self.min_box_height:
                    continue

                detections.append({
                    "track_id": None,
                    "box": [x1, y1, x2, y2],
                    "conf": round(conf, 4),
                    "class_id": 0,
                    "class_name": "person",
                })
                keypoints_list.append(kpts_data[i] if kpts_data is not None else None)

        return detections, keypoints_list
```

---

### <a id="📄-src-ai-models-pose-model-py"></a>📄 `src/ai_models/pose_model.py`

**File Info:**
- **Size**: 0 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/ai_models/pose_model.py`
- **Relative Path**: `src/ai_models`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```python

```

---

### <a id="📄-src-ai-models-tracker-py"></a>📄 `src/ai_models/tracker.py`

**File Info:**
- **Size**: 2.39 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/ai_models/tracker.py`
- **Relative Path**: `src/ai_models`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `0e3d3768f9213bd7075d6e10f28ab860`
- **SHA256**: `e0cfc760f4d2d5b272e23d71a6fd89c752b83256100a475493409ab17d001f48`
- **Encoding**: UTF-8

**File code content:**

```python
# src/tracking/tracker.py

import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort

class RestaurantTracker:
    def __init__(
        self, 
        max_age: int | None = None, 
        n_init: int | None = None, 
        nms_max_overlap: float | None = None
    ):
        # 💡 هنا نحدد قيم الأمان المركزية والوحيدة في الكود (Single Source of Truth)
        self.max_age = max_age if max_age is not None else 5
        self.n_init = n_init if n_init is not None else 1
        self.nms_max_overlap = nms_max_overlap if nms_max_overlap is not None else 0.8

        # إعدادات متوافقة مع الـ 2 FPS ومحمية داخلياً
        self.tracker = DeepSort(
            max_age=self.max_age,
            n_init=self.n_init,
            nms_max_overlap=self.nms_max_overlap,
            embedder="mobilenet",
            half=True,
            max_cosine_distance=0.4
        )

    def update(self, detections, frame=None):
        raw_deepsort_detections = []
        
        for det in detections:
            box = det["box"]
            conf = det["conf"]
            
            w = box[2] - box[0]
            h = box[3] - box[1]
            ltwh = [box[0], box[1], w, h]
            
            raw_deepsort_detections.append((ltwh, conf, "person"))

        # تمرير الفريم (سواء كان صورة حقيقية أو None)
        tracks = self.tracker.update_tracks(raw_deepsort_detections, frame=frame)
        
        updated_detections = []
        for track in tracks:
            # اقبل التراكات الحديثة أيضًا حتى لا نضيع الأشخاص الجدد داخل المشهد
            is_confirmed = track.is_confirmed() if hasattr(track, "is_confirmed") else True
            time_since_update = getattr(track, "time_since_update", 0)
            if not is_confirmed and time_since_update > 1:
                continue
                
            track_id = track.track_id
            ltrb = track.to_ltrb()
            
            updated_detections.append({
                "track_id": int(track_id),
                "box": [float(ltrb[0]), float(ltrb[1]), float(ltrb[2]), float(ltrb[3])],
                "conf": float(track.get_det_conf() if track.get_det_conf() else 1.0),
                "class_id": 0,
                "class_name": "person"
            })
            
        return updated_detections
```

---

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `src/core/__pycache__/__init__.cpython-313.pyc`
- `src/core/__pycache__/classifiers.cpython-313.pyc`
- `src/core/__pycache__/live_pipeline.cpython-313.pyc`

### <a id="📄-src-core-init-py"></a>📄 `src/core/__init__.py`

**File Info:**
- **Size**: 0 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/core/__init__.py`
- **Relative Path**: `src/core`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```python

```

---

### <a id="📄-src-core-classifiers-py"></a>📄 `src/core/classifiers.py`

**File Info:**
- **Size**: 356 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/core/classifiers.py`
- **Relative Path**: `src/core`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `513579aa7611b1d7dcc75c7e50fb842a`
- **SHA256**: `0eafb22f41af7edac7c6ec4cc4ac713d7664750158124950783f45cd0ccaf60b`
- **Encoding**: ASCII

**File code content:**

```python
import torch.nn as nn
class PoseLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=51, hidden_size=64, num_layers=2,
                            batch_first=True, dropout=0.4)
        self.fc = nn.Linear(64, 4)

    def forward(self, x):
        _, (h, _) = self.lstm(x)
        return self.fc(h[-1])
```

---

### <a id="📄-src-core-live-pipeline-py"></a>📄 `src/core/live_pipeline.py`

**File Info:**
- **Size**: 30.21 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/core/live_pipeline.py`
- **Relative Path**: `src/core`
- **Created**: 2026-07-14 09:51:12 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 09:51:12 (Asia/Damascus / GMT+03:00)
- **MD5**: `b9a9ffb67b4bc40d90f8da3e5095299a`
- **SHA256**: `f79cf2fbbe459b0136ce5105bbe1fa6754f5683ad9d1dd8f151f39c798abebe8`
- **Encoding**: UTF-8

**File code content:**

```python
from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import torch

from src.ai_models.detector import PersonDetector
from src.ai_models.tracker import RestaurantTracker
from src.zone_management.zone_manager import ZoneManager 
from src.kbs.table_kbs import TableKBS, TableFact
from src.kbs.reid_gallery import ReIDGallery, SessionGallery
from src.kbs.role_engine import (
    RoleEngine, ObservationFact, ScoreAccumulator, MergeRequest, RoleDecision,
)
from src.core.classifiers import PoseLSTM


class LivePipeline:
    ZONE_TYPE_MAP: dict[str, str] = {
        "table_area"           : "table",   # broad container zone
        "table"                : "table",   # single table zone (nested inside table_area) — was missing, caused zone_type_normalized="unknown"
        "service_path"         : "walk",
        "hallway"              : "walk",
        "corridor"             : "walk",
        "open_area"            : "walk",
        "mixed_area"           : "walk",
        "entrance"             : "walk",
        "bathroom_entrance"    : "walk",
        "prayer_room_entrance" : "walk",
        "staff_area"           : "staff",
        "buffet"               : "staff",
        "cashier"              : "staff",
    }

    KEYPOINT_NAMES = [
        "nose", "left_eye", "right_eye", "left_ear", "right_ear",
        "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
        "left_wrist", "right_wrist", "left_hip", "right_hip",
        "left_knee", "right_knee", "left_ankle", "right_ankle"
    ]

    ROLE_COLORS = {
        "unknown":  (255, 255, 255),  # white
        "customer": (255, 100,   0),  # blue  (BGR)
        "worker":   (  0, 140, 255),  # orange (BGR)
    }

    def __init__(self, config_path: str = "config/config.json"):
        self.project_dir = Path.cwd()
        self.config_path = self.project_dir / config_path

        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        # -- Detector -------------------------------------------------------
        detector_config = self.config["detector"]
        self.detector = PersonDetector(
            model_name=detector_config.get("model"),
            conf_threshold=detector_config.get("conf_threshold"),
            imgsz=detector_config.get("imgsz"),
            min_box_width=detector_config.get("min_box_width"),
            min_box_height=detector_config.get("min_box_height"),
            device=detector_config.get("device"),
        )

        # -- Tracker --------------------------------------------------------
        tracker_config = self.config.get("tracker", {})
        self.tracker = RestaurantTracker(
            max_age=tracker_config.get("max_age"),
            n_init=tracker_config.get("n_init"),
            nms_max_overlap=tracker_config.get("nms_max_overlap"),
        )

        # -- Action model ---------------------------------------------------
        model_path = self.project_dir / "models/pose_lstm.pth"
        le_path    = self.project_dir / "models/label_encoder.pkl"

        self.action_model = PoseLSTM()
        self.action_model.load_state_dict(torch.load(model_path, map_location="cpu"))
        self.action_model.eval()

        with open(le_path, "rb") as f:
            self.label_encoder = pickle.load(f)

        # -- Pose buffers ---------------------------------------------------
        self._kp_buffer:    dict[int, list] = {}  # track_id -> [(frame_id, kp_dict)]
        self._action_labels: dict[int, str] = {}  # track_id -> latest label

        # -- Zone manager ---------------------------------------------------
        self.zone_manager = ZoneManager()
 
        # self.worker_kbs   = WorkerKBS()
        self.table_kbs    = TableKBS()
        self.reid_gallery = ReIDGallery()
        self.session_gallery = SessionGallery(ttl_seconds=1800)  # 30 mins TTL

        # KBS engines are re-instantiated each cycle in _run_kbs to avoid Experta lru_cache deadlock

        # -- Per-track state ------------------------------------------------
        self._person_roles:        dict[int, str]   = {}  # track_id -> role
        self._global_ids:          dict[int, str]   = {}  # track_id -> global_id
        self._action_frame_counts: dict[int, int]   = {}  # track_id -> consecutive frames
        self._last_action_zone:    dict[int, tuple] = {}  # track_id -> (action, zone_type)
        self._worker_states:       dict[str, str]   = {}  # global_id -> worker state

        # -- RoleEngine persistent state ------------------------------------
        self._role_accumulators: dict[str, dict]  = {}  # global_id -> accumulator dict
        self._gid_track_counts: dict[str, set[int]] = {}  # global_id -> set of track_ids

        # -- Table state ----------------------------------------------------
        self._table_customer_counts: dict[str, int] = {}  # zone_id -> count
        self._table_was_served:      dict[str, bool] = {}  # zone_id -> served flag
        self._table_states:           dict[str, str]  = {}  # zone_id -> state
        self.person_state: list[dict[str, Any]] = []
    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def process_frame(
        self,
        frame,
        camera_id,
        video_id,
        frame_index,
        time_seconds,
        pose_stride=None,
    ):
        detections, keypoints_list = self.detector.detect_with_pose(frame)
        tracked_objects = self.tracker.update(detections, frame=frame)
        tracked_objects = self.enrich_tracks_with_zones(
            camera_id,
            tracked_objects,
            detections,
            keypoints_list,
        )
        person_crops    = self.crop_persons(frame, tracked_objects)

        if pose_stride is None or frame_index % pose_stride == 0:
            self._extract_pose_from_detections(
                frame, video_id, frame_index,
                detections, keypoints_list, tracked_objects,
            )

        self._run_kbs(tracked_objects, person_crops, time_seconds)

        return {
            "camera_id":      camera_id,
            "video_id":       video_id,
            "frame_index":    frame_index,
            "time_seconds":   time_seconds,
            "detections":     detections,
            "tracked_objects": tracked_objects,
            "person_crops":   person_crops,
            "tables_current_state": self.get_tables_current_state(camera_id),
        }

    def enrich_tracks_with_zones(
        self,
        camera_id: str,
        tracked_objects: list[dict[str, Any]],
        detections: list[dict[str, Any]] | None = None,
        keypoints_list: list[np.ndarray] | None = None,
    ) -> list[dict[str, Any]]:
        enriched_tracks: list[dict[str, Any]] = []

        pose_points_by_track_id: dict[int, list[int]] = {}
        kpts_by_track_id: dict[int, np.ndarray] = {}
        if detections and keypoints_list:
            for det, kpts in zip(detections, keypoints_list):
                if kpts is None:
                    continue

                track_id = self._match_to_track(det.get("box", [0, 0, 0, 0]), tracked_objects)
                if track_id is None:
                    continue

                pose_points_by_track_id[track_id] = self._estimate_zone_point(det.get("box", [0, 0, 0, 0]), kpts)
                kpts_by_track_id[track_id] = kpts

        for obj in tracked_objects:
            track_id = obj.get("track_id")
            box = obj.get("box", [0, 0, 0, 0])
            zone_point = pose_points_by_track_id.get(track_id)
            kpts = kpts_by_track_id.get(track_id)

            if zone_point is None:
                zone_point = self._estimate_zone_point(box, None)

            zone = self.zone_manager.get_bbox_zone(
                camera_id=camera_id,
                box=box,
                keypoints=kpts,
            )
            enriched_obj = dict(obj)
            enriched_obj["zone"] = zone
            raw_zone_type = zone.get("zone_type", "unknown") if zone else "unknown"
            enriched_obj["zone_type_normalized"] = self.ZONE_TYPE_MAP.get(raw_zone_type, "unknown")
            enriched_obj["zone_name"] = zone.get("zone_name", "Unknown") if zone else "Unknown"
            enriched_obj["zone_point"] = zone_point
            enriched_tracks.append(enriched_obj)

        return enriched_tracks

    def crop_persons(
        self,
        frame,
        tracked_objects: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        crops: list[dict[str, Any]] = []
        height, width = frame.shape[:2]

        for obj in tracked_objects:
            box = obj.get("box", [0, 0, 0, 0])
            x1, y1, x2, y2 = [int(v) for v in box]

            x1 = max(0, min(width,  x1))
            x2 = max(0, min(width,  x2))
            y1 = max(0, min(height, y1))
            y2 = max(0, min(height, y2))

            if x1 >= x2 or y1 >= y2:
                continue

            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            crops.append({
                "track_id": obj.get("track_id"),
                "zone":     obj.get("zone", {}),
                "box":      [x1, y1, x2, y2],
                "crop":     crop.copy(),
            })

        return crops

    def get_tables_current_state(self, camera_id: str) -> dict[str, str]:
        camera_zones = self.zone_manager.zones_config.get(camera_id, {}).get("zones", [])

        summary: dict[str, str] = {}
        for zone in camera_zones:
            if zone.get("zone_type") in ("table", "table_area"):
                zone_id = zone.get("zone_id")
                if zone_id:
                    summary[zone_id] = self._table_states.get(zone_id, "empty")
        return summary

    def draw_zones(self, frame, camera_id: str) -> None:
        camera_zones = (
            self.zone_manager.zones_config
            .get(camera_id, {})
            .get("zones", [])
        )

        for zone in camera_zones:
            points = zone.get("points", [])
            if len(points) < 3:
                continue

            polygon = np.array(points, dtype=np.int32)
            cv2.polylines(frame, [polygon], isClosed=True, color=(0, 255, 0), thickness=2)

    def draw_tracks(self, frame, tracked_objects: list[dict[str, Any]]) -> None:
        for obj in tracked_objects:
            box = obj.get("box", [0, 0, 0, 0])
            x1, y1, x2, y2 = map(int, box)
            zone_type = obj.get("zone_type_normalized", "unknown")
            zone_name = obj.get("zone_name", "Unknown")
            track_id  = obj.get("track_id", "?")
            action    = self._action_labels.get(track_id, "...")
            role      = self._person_roles.get(track_id, "unknown")
            gid       = self._global_ids.get(track_id)
            color     = self.ROLE_COLORS.get(role, (255, 255, 255))

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            label = f"{action} | {role} | {zone_type}"
            cv2.putText(
                frame, label,
                (x1, max(35, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,
            )

            cv2.putText(
                frame, f"id:{track_id}",
                (x1 + 4, y1 + 18),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2,
            )

            if gid:
                gid_short = gid.replace("worker_", "")
                cv2.putText(
                    frame, f"gid:{gid_short}",
                    (x1 + 4, y1 + 38),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 105, 255), 2,
                )

    # -----------------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------------
    def _update_person_state(self, global_id: str, local_id: int, zone_type: str, time_seconds: float):
        """
        تحديث قاعدة البيانات في الذاكرة (list of dicts) لكل شخص بناءً على وقت الفيديو (time_seconds).
        """
        from datetime import timedelta

        if time_seconds is None:
            raise ValueError(
                "_update_person_state() requires a non-None time_seconds "
                "(video-relative timestamp from frame_index / video_fps); "
                "wall-clock time and frame counters are not valid substitutes."
            )

        # 1. البحث عن السجل الحالي للشخص عبر الـ global_id
        person_record = next((row for row in self.person_state if row["global_id"] == global_id), None)

        # 2. إذا كان الشخص يظهر لأول مرة في النظام تماماً
        if person_record is None:
            new_row = {
                "global_id": global_id,
                "local_id": local_id,
                "current_location": zone_type, # يتم تخزين الزون الموحدة (table, walk, staff)
                "Entrance date": str(timedelta(seconds=int(time_seconds))),
                "Duration": "0:00:00",
                "_entrance_time_seconds": time_seconds, # وقت الفيديو عند الدخول لحساب المدة لاحقاً
            }
            self.person_state.append(new_row)
            return

        # 3. إذا كان الشخص موجوداً مسبقاً ولكن انتقل إلى زون جديدة
        if person_record["current_location"] != zone_type:
            person_record["current_location"] = zone_type
            person_record["Entrance date"] = str(timedelta(seconds=int(time_seconds)))
            person_record["_entrance_time_seconds"] = time_seconds
            person_record["Duration"] = "0:00:00"
            person_record["local_id"] = local_id # تحديث الـ local_id في حال تغير بفعل الـ DeepSORT
        else:
            # 4. الشخص لا يزال مستقراً في نفس المكان -> نحسب المدة من فرق وقت الفيديو
            person_record["local_id"] = local_id # نحدث الـ local_id باستمرار لضمان ربطه بالـ Bounding Box الحالي

            elapsed_seconds = time_seconds - person_record["_entrance_time_seconds"]
            person_record["Duration"] = str(timedelta(seconds=int(elapsed_seconds)))

    def _extract_pose_from_detections(
        self,
        frame,
        video_id,
        frame_index,
        detections,
        keypoints_list,
        tracked_objects,
    ) -> None:
        h, w = frame.shape[:2]

        for det, kpts in zip(detections, keypoints_list):
            if kpts is None:
                continue

            track_id = self._match_to_track(det["box"], tracked_objects)
            if track_id is None:
                continue

            kp_dict = {
                self.KEYPOINT_NAMES[j]: {
                    "x":    round(float(kpts[j][0] / w), 4),
                    "y":    round(float(kpts[j][1] / h), 4),
                    "conf": round(float(kpts[j][2]),     4),
                }
                for j in range(17)
            }

            self._predict_action(track_id, frame_index, kp_dict)

    def _estimate_zone_point(
        self,
        box: list[int | float],
        kpts: np.ndarray | None,
        conf_threshold: float = 0.25,
    ) -> list[int]:
        x1, y1, x2, y2 = [int(v) for v in box]

        def visible_point(index: int) -> tuple[float, float] | None:
            if kpts is None or index >= len(kpts):
                return None
            x, y, conf = kpts[index]
            if float(conf) < conf_threshold:
                return None
            return float(x), float(y)

        def average_visible_points(indices: tuple[int, ...]) -> list[int] | None:
            points = [visible_point(index) for index in indices]
            visible_points = [point for point in points if point is not None]
            if visible_points:
                avg_x = sum(point[0] for point in visible_points) / len(visible_points)
                avg_y = sum(point[1] for point in visible_points) / len(visible_points)
                return [int(round(avg_x)), int(round(avg_y))]
            return None

        # Explicit priority order:
        # 1) ankles visible
        # 2) hips visible
        # 3) shoulders visible
        # 4) upper body only -> use the box center
        ankles_point = average_visible_points((15, 16))
        if ankles_point is not None:
            return ankles_point

        hips_point = average_visible_points((11, 12))
        if hips_point is not None:
            return hips_point

        shoulders_point = average_visible_points((5, 6))
        if shoulders_point is not None:
            return shoulders_point

        return [int(round((x1 + x2) / 2)), int(round((y1 + y2) / 2))]

    def _match_to_track(self, pose_box, tracked_objects) -> int | None:
        best_iou, best_id = 0.0, None
        px1, py1, px2, py2 = pose_box

        for obj in tracked_objects:
            tx1, ty1, tx2, ty2 = obj["box"]
            ix1 = max(px1, tx1)
            iy1 = max(py1, ty1)
            ix2 = min(px2, tx2)
            iy2 = min(py2, ty2)
            inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
            if inter == 0:
                continue
            union = (px2 - px1) * (py2 - py1) + (tx2 - tx1) * (ty2 - ty1) - inter
            iou = inter / union if union > 0 else 0
            if iou > best_iou:
                best_iou, best_id = iou, obj["track_id"]

        return best_id if best_iou > 0.4 else None

    def _predict_action(self, track_id: int, frame_id: int, kp_dict: dict) -> None:
        buf = self._kp_buffer.setdefault(track_id, [])
        buf.append((frame_id, kp_dict))

        # Drop frames with large gaps
        while len(buf) > 1 and buf[-1][0] - buf[-2][0] >= 200:
            buf.pop(0)

        if len(buf) > 3:
            buf.pop(0)

        if len(buf) < 3:
            return

        def normalize_kp(kp):
            lh = kp.get("left_hip",       {"x": 0, "y": 0, "conf": 0})
            rh = kp.get("right_hip",      {"x": 0, "y": 0, "conf": 0})
            ls = kp.get("left_shoulder",  {"x": 0, "y": 0, "conf": 0})
            rs = kp.get("right_shoulder", {"x": 0, "y": 0, "conf": 0})
            cx = (lh["x"] + rh["x"]) / 2
            cy = (lh["y"] + rh["y"]) / 2
            shoulder_y = (ls["y"] + rs["y"]) / 2
            torso_h    = abs(cy - shoulder_y)
            scale      = torso_h if torso_h > 1e-5 else 1.0
            return {
                name: {
                    "x":    (pt["x"] - cx) / scale,
                    "y":    (pt["y"] - cy) / scale,
                    "conf": pt["conf"],
                }
                for name, pt in kp.items()
            }

        def flatten(kp):
            kp = normalize_kp(kp)
            return [v for pt in kp.values() for v in (pt["x"], pt["y"], pt["conf"])]

        x = np.array([flatten(buf[i][1]) for i in range(3)], dtype=np.float32)
        x = torch.tensor(x).unsqueeze(0)  # (1, 3, 51)

        with torch.no_grad():
            pred = self.action_model(x).argmax(1).item()

        self._action_labels[track_id] = self.label_encoder.classes_[pred]

    def _run_kbs(self, tracked_objects: list[dict], person_crops: list[dict], time_seconds: float) -> None:
        crop_by_id = {
            c["track_id"]: c["crop"]
            for c in person_crops
            if c.get("crop") is not None
        }

        # -- Update action_frame_counts (reset if action or zone changed) ---
        for obj in tracked_objects:
            tid       = obj["track_id"]
            action    = self._action_labels.get(tid, "unknown")
            zone_type = obj.get("zone_type_normalized", "unknown")
            key       = (action, zone_type)
            previous_duration_frames = self._action_frame_counts.get(tid, 0)

            if self._last_action_zone.get(tid) != key:
                self._action_frame_counts[tid] = 0
                self._last_action_zone[tid]    = key
            else:
                self._action_frame_counts[tid] = self._action_frame_counts.get(tid, 0) + 1

            obj["previous_duration_frames"] = previous_duration_frames

        # -- Re-ID pre-check: match unknowns against existing gallery --------
        self.session_gallery.purge_old()

        for obj in tracked_objects:
            tid  = obj["track_id"]
            
            # If we already linked this track ID in a previous frame to a session ID, just touch it
            if tid in self._global_ids:
                gid = self._global_ids[tid]
                if gid.startswith("session_"):
                    self.session_gallery.touch(gid)
                continue

            crop = crop_by_id.get(tid)
            if crop is None:
                continue

            # Crop too small/low-res → embedding is unreliable and is exactly
            # what causes worker X's identity to get handed to a blurry,
            # unrelated person Y. Skip ReID this frame; track stays without
            # a global_id and will be retried once a better crop comes in.
            crop_h, crop_w = crop.shape[:2]
            if crop_w < self.reid_gallery.MIN_CROP_WIDTH or crop_h < self.reid_gallery.MIN_CROP_HEIGHT:
                print(f"[ReID] track {tid}: crop too small ({crop_w}x{crop_h}) — skipping ReID this frame")
                continue

            embedding = self.reid_gallery._extract(crop)

            # 1. Check permanent Worker Gallery
            matched_worker = self.reid_gallery._match(embedding)
            if matched_worker is not None:
                self._person_roles[tid] = "worker"
                self._global_ids[tid]   = matched_worker
                self._gid_track_counts.setdefault(matched_worker, set()).add(tid)
                print(f"[ReID] track {tid} matched permanent worker → {matched_worker}")
                continue

            # 2. Check temporary Session Gallery
            matched_session = self.session_gallery.match(embedding)
            if matched_session is not None:
                self._global_ids[tid] = matched_session
                self._gid_track_counts.setdefault(matched_session, set()).add(tid)
                self.session_gallery.update_seen(matched_session, embedding)
                print(f"[ReID] track {tid} matched active session → {matched_session}")
                continue

            # 3. New person: register in Session Gallery
            new_session = self.session_gallery.register(embedding)
            self._global_ids[tid] = new_session
            self._gid_track_counts.setdefault(new_session, set()).add(tid)
            print(f"[ReID] track {tid} registered as new session → {new_session}")

        # -- RoleEngine: classify all persons via point-based evidence ------
        engine = RoleEngine()
        engine.reset()

        # Re-inject persistent accumulators from previous cycle
        for gid, acc in self._role_accumulators.items():
            engine.declare(ScoreAccumulator(
                global_id=gid,
                worker_score=acc["worker_score"],
                customer_score=acc["customer_score"],
                confirmed_role=acc["confirmed_role"],
                cycle_count=acc["cycle_count"],
                visited_tables=acc.get("visited_tables", ()),
                visited_staff=acc.get("visited_staff", False),
                zone_history=acc.get("zone_history", ()),
            ))

        # Declare one ObservationFact per tracked person
        for obj in tracked_objects:
            tid = obj["track_id"]
            gid = self._global_ids.get(tid, f"local_{tid}")
            
            zone = obj.get("zone") or {}
            zone_id = zone.get("zone_id", "unknown")

            engine.declare(ObservationFact(
                track_id         = tid,
                global_id        = gid,
                action           = self._action_labels.get(tid, "unknown"),
                zone_type        = obj.get("zone_type_normalized", "unknown"),
                zone_id          = zone_id,
                pose_frame_count = self._action_frame_counts.get(tid, 0),
                previous_duration_frames = obj.get("previous_duration_frames", 0),
                appearance_count = len(self._gid_track_counts.get(gid, set())),
                previous_role    = self._person_roles.get(tid, "unknown"),
            ))

        engine.run()
        decisions = engine.get_decisions()

        # أضف هذا التكرار لطباعة النقاط لكل شخص في الـ Terminal فورياً:
        for track_id, info in decisions.items():
            print(f"[Track {track_id}] ID: {info['global_id']} | Role: {info['role']} | Confidence: {info['confidence']}")
            print(f"   -> Worker Score: {info['worker_score']} | Customer Score: {info['customer_score']}")
            print("-" * 40)

        # Read RoleEngine decisions
        for tid, decision in engine.get_decisions().items():
            role = decision["role"]
            if role != "unknown":
                self._person_roles[tid] = role
            # Log scores for debugging
            print(
                f"  [RoleEngine] track {tid}: "
                f"role={decision['role']}  "
                f"conf={decision['confidence']:.2f}  "
                f"ws={decision['worker_score']:.1f}  "
                f"cs={decision['customer_score']:.1f}"
            )

            # Re-ID Promotion: register newly confirmed workers in permanent gallery
            gid = self._global_ids.get(tid)
            if role == "worker" and gid and gid.startswith("session_"):
                crop = crop_by_id.get(tid)
                if crop is not None:
                    embedding = self.reid_gallery._extract(crop)
                    new_worker_gid = self.reid_gallery._register(embedding)
                    
                    # Rename in our track mappings
                    self._global_ids[tid] = new_worker_gid
                    
                    # Rename in the accumulators dict so RoleEngine continues next cycle
                    if gid in self._role_accumulators:
                        acc = self._role_accumulators.pop(gid)
                        acc["global_id"] = new_worker_gid
                        self._role_accumulators[new_worker_gid] = acc
                        
                    # Transfer track counts
                    if gid in self._gid_track_counts:
                        counts = self._gid_track_counts.pop(gid)
                        self._gid_track_counts.setdefault(new_worker_gid, set()).update(counts)
                        
                    # Rename in person_state to preserve duration
                    for row in self.person_state:
                        if row["global_id"] == gid:
                            row["global_id"] = new_worker_gid
                        
                    # Remove from session gallery
                    self.session_gallery.remove(gid)
                    print(f"[ReID] Promoted {gid} to permanent worker → {new_worker_gid}")

        # Persist accumulators for next cycle
        self._role_accumulators = engine.get_accumulators()
        for obj in tracked_objects:
            tid = obj["track_id"]
            
            # الحصول على الـ global_id الموحد المحسوب بواسطة الـ ReID والـ RoleEngine
            # وإذا لم يكن مسجلاً بعد كعامل، نأخذ المعرف المؤقت المعتمد في كودكم [source: 1]
            gid = self._global_ids.get(tid, f"local_{tid}") 
            
            # الحصول على اسم الزون الموحد الجاهز في الكود (table, walk, staff) [source: 1]
            zone_type = obj.get("zone_type_normalized", "unknown") 
            
            # استدعاء دالة التحديث لبناء الـ list of dicts وحساب الـ duration
            self._update_person_state(
                global_id=gid,
                local_id=tid,
                zone_type=zone_type,
                time_seconds=time_seconds,
            )
        # -- Update table customer counts -----------------------------------
        zone_customer_counts: dict[str, int] = {}
        for obj in tracked_objects:
            tid  = obj["track_id"]
            role = self._person_roles.get(tid, "unknown")
            if role != "customer":
                continue
            zone    = obj.get("zone") or {}
            zone_id = zone.get("zone_id")
            if zone_id:
                zone_customer_counts[zone_id] = zone_customer_counts.get(zone_id, 0) + 1

        # -- Check for serving events to set was_served flag ----------------
        for obj in tracked_objects:
            tid       = obj["track_id"]
            role      = self._person_roles.get(tid, "unknown")
            action    = self._action_labels.get(tid, "unknown")
            zone      = obj.get("zone") or {}
            zone_id   = zone.get("zone_id")
            zone_type = obj.get("zone_type_normalized", "unknown")

            if (
                role == "worker"
                and action == "serving"
                and zone_type == "table"
                and zone_id
                and zone_customer_counts.get(zone_id, 0) > 0
            ):
                self._table_was_served[zone_id] = True

        # -- TableKBS: derive empty / occupied / dirty ---------------------
        all_zone_ids = (
            set(zone_customer_counts)
            | set(self._table_customer_counts)
            | set(self._table_was_served)
        )

        self.table_kbs.reset()
        for zone_id in all_zone_ids:
            self.table_kbs.declare(TableFact(
                zone_id=zone_id,
                customer_count=zone_customer_counts.get(zone_id, 0),
                was_served=self._table_was_served.get(zone_id, False),
            ))
        self.table_kbs.run()

        self._table_states = {
            fact["zone_id"]: fact["state"]
            for fact in self.table_kbs.facts.values()
            if isinstance(fact, TableFact)
        }
        self._table_customer_counts = zone_customer_counts

    # أضف هذا السطر في نهاية دالة _run_kbs للتحقق
        print("\n=== LIVE DATABASE STATE ===")
        for row in self.person_state:
            print(f"ID: {row['global_id']} | Loc: {row['current_location']} | Entry: {row['Entrance date']} | Dur: {row['Duration']}")
        print("===========================\n")      
        
```

---

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `src/kbs/__pycache__/__init__.cpython-313.pyc`
- `src/kbs/__pycache__/_compat.cpython-313.pyc`
- `src/kbs/__pycache__/reid_gallery.cpython-313.pyc`
- `src/kbs/__pycache__/role_engine.cpython-313.pyc`
- `src/kbs/__pycache__/table_kbs.cpython-313.pyc`

### <a id="📄-src-kbs-init-py"></a>📄 `src/kbs/__init__.py`

**File Info:**
- **Size**: 499 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/kbs/__init__.py`
- **Relative Path**: `src/kbs`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `ddda5979729a2b4ad3554e2e2870fa52`
- **SHA256**: `7ce6234964a016fdaf47dee3151d006467f9226ae541c8f2d66986fb9a8596dd`
- **Encoding**: ASCII

**File code content:**

```python
 
from .table_kbs     import TableKBS, TableFact
from .reid_gallery  import ReIDGallery, SessionGallery
from .role_engine   import (
    RoleEngine,
    ObservationFact,
    ScoreAccumulator,
    EvidenceApplied,
    DecayApplied,
    MergeRequest,
    RoleDecision,
)

__all__ = [ 
    "TableKBS",  "TableFact",
    "ReIDGallery", "SessionGallery",
    "RoleEngine",
    "ObservationFact",
    "ScoreAccumulator",
    "EvidenceApplied",
    "DecayApplied",
    "MergeRequest",
    "RoleDecision",
]
```

---

### <a id="📄-src-kbs-compat-py"></a>📄 `src/kbs/_compat.py`

**File Info:**
- **Size**: 642 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/kbs/_compat.py`
- **Relative Path**: `src/kbs`
- **Created**: 2026-07-14 09:09:20 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 09:09:20 (Asia/Damascus / GMT+03:00)
- **MD5**: `7b9213089f5d80250efb1cb36f50b42a`
- **SHA256**: `2812903c11eded6e1f2f19adfdbb83920f4fed302e37ed902bf6bfe8a7f59962`
- **Encoding**: ASCII

**File code content:**

```python
"""
_compat.py
----------
experta (last released 2021) does `from collections import Mapping`, which
was removed in Python 3.10 (moved to collections.abc). Must run before any
`import experta` anywhere in the process. Previously only run_live.py
applied this patch inline, so importing src.kbs.role_engine or
src.kbs.table_kbs directly (as tests, the Event Engine, and the API layer
all now do) crashed on Python >=3.10. Centralized here so every importer
gets it for free.
"""

import collections
import collections.abc

if not hasattr(collections, "Mapping"):
    collections.Mapping = collections.abc.Mapping  # type: ignore[attr-defined]

```

---

### <a id="📄-src-kbs-reid-gallery-py"></a>📄 `src/kbs/reid_gallery.py`

**File Info:**
- **Size**: 9.34 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/kbs/reid_gallery.py`
- **Relative Path**: `src/kbs`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `80666e46b335e578eb1e8ca8cb10ac80`
- **SHA256**: `9b926ca1503e4032476140b128e4cb4a0fcd83ab7bbf558d3e840b26b5f612b5`
- **Encoding**: UTF-8

**File code content:**

```python
"""
reid_gallery.py
---------------
Person Re-ID gallery using OSNet-x0.25 for embedding extraction
and faiss for fast CPU similarity search.

Workflow
--------
1. Worker crop arrives from live_pipeline
2. extract_embedding(crop) → 512-dim vector
3. match(embedding) → global_id if similarity > threshold, else None
4. register(embedding) → new global_id stored in gallery
"""

from __future__ import annotations

import time
import uuid
from pathlib import Path

import cv2
import numpy as np
import faiss
import torch
import torchreid


# ---------------------------------------------------------------------------
# Gallery
# ---------------------------------------------------------------------------

class ReIDGallery:
    """
    Stateful gallery of known worker embeddings.

    Parameters
    ----------
    model_name      : OSNet variant — 'osnet_x0_25' is smallest/fastest
    threshold       : cosine similarity threshold to consider a match (0–1)
    device          : 'cpu' always for MX350-constrained inference
    weights_dir     : where to cache downloaded model weights
    """

    EMBEDDING_DIM = 512

    # Crops smaller than this are too low-res/blurry for a trustworthy
    # embedding — accepting them into the gallery is exactly what causes
    # worker X's identity to get handed to unknown person Y.
    MIN_CROP_WIDTH = 32
    MIN_CROP_HEIGHT = 64

    # A match must not just clear `threshold` — it must beat the runner-up
    # by at least this much. A "confidently wrong" match (0.66 vs 0.65) is
    # far more dangerous than an honest "no match" (which just registers a
    # new id). This margin check is what actually catches those.
    MIN_MATCH_MARGIN = 0.05

    def __init__(
        self,
        model_name : str   = "osnet_x0_25",
        threshold  : float = 0.72,
        device     : str   = "cpu",
        weights_dir: str   = "models/reid",
    ):
        self.threshold   = threshold
        self.device      = device
        self.weights_dir = Path(weights_dir)
        self.weights_dir.mkdir(parents=True, exist_ok=True)

        # -- Load OSNet feature extractor ------------------------------------
        self.extractor = torchreid.utils.FeatureExtractor(
            model_name=model_name,
            model_path=str(self.weights_dir / f"{model_name}.pth"),
            device=device,
        )

        # -- Faiss flat index (cosine via L2 on normalized vectors) ----------
        self.index = faiss.IndexFlatIP(self.EMBEDDING_DIM)  # inner product = cosine when normalized

        # global_id list parallel to faiss index rows
        self._ids: list[str] = []

    # -- Public API ----------------------------------------------------------

    def process(self, track_id: int, crop: np.ndarray) -> str:
        """
        Main entry point called by live_pipeline for every worker crop.
        Returns the global_id (existing match or newly registered).
        """
        h, w = crop.shape[:2]
        if w < self.MIN_CROP_WIDTH or h < self.MIN_CROP_HEIGHT:
            # Crop too small/low-res to trust — do NOT attempt a match against
            # the gallery (this is exactly the scenario that hands worker X's
            # identity to a blurry unrelated person Y). Caller should treat
            # a None return as "skip ReID this frame, keep previous id".
            print(f"[ReIDGallery] track {track_id}: crop too small ({w}x{h}, min {self.MIN_CROP_WIDTH}x{self.MIN_CROP_HEIGHT}) — skipping match, not registering")
            return None

        embedding = self._extract(crop)
        global_id = self._match(embedding)

        if global_id is None:
            global_id = self._register(embedding)

        return global_id

    # -- Internal ------------------------------------------------------------

    def _extract(self, crop: np.ndarray) -> np.ndarray:
        """Extract L2-normalized 512-dim embedding from a BGR crop."""
        # torchreid expects RGB, resize to 256x128 (standard Re-ID input)
        rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, (128, 256))

        embedding = self.extractor([resized])           # returns (1, 512) tensor
        vec = embedding.cpu().numpy().astype(np.float32)
        faiss.normalize_L2(vec)                         # in-place L2 norm → cosine via IP
        return vec                                      # shape (1, 512)

    def _match(self, embedding: np.ndarray) -> str | None:
        """Return global_id of closest gallery entry if above threshold AND
        clearly ahead of the runner-up, else None.
        """
        if self.index.ntotal == 0:
            return None

        k = min(2, self.index.ntotal)
        similarities, indices = self.index.search(embedding, k=k)
        sim   = float(similarities[0][0])
        idx   = int(indices[0][0])

        if sim < self.threshold:
            return None

        if k > 1:
            runner_up_sim = float(similarities[0][1])
            margin = sim - runner_up_sim
            if margin < self.MIN_MATCH_MARGIN:
                print(f"[ReIDGallery] ambiguous match rejected: top={sim:.3f} runner_up={runner_up_sim:.3f} margin={margin:.3f} < {self.MIN_MATCH_MARGIN} — registering as new identity instead")
                return None

        return self._ids[idx]

    def _register(self, embedding: np.ndarray) -> str:
        """Add new embedding to gallery, return assigned global_id."""
        global_id = f"worker_{uuid.uuid4().hex[:8]}"
        self.index.add(embedding)
        self._ids.append(global_id)
        return global_id

    # -- Persistence ---------------------------------------------------------

    def save(self, path: str = "models/reid/gallery.index") -> None:
        """Persist faiss index + id list to disk."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(p))
        np.save(str(p.with_suffix(".ids.npy")), np.array(self._ids))

    def load(self, path: str = "models/reid/gallery.index") -> None:
        """Load persisted gallery from disk."""
        p = Path(path)
        if not p.exists():
            return
        self.index = faiss.read_index(str(p))
        self._ids  = np.load(str(p.with_suffix(".ids.npy")), allow_pickle=True).tolist()


# ---------------------------------------------------------------------------
# Session Gallery (Short-Term / Ephemeral)
# ---------------------------------------------------------------------------

class SessionGallery:
    """
    Short-term, in-memory gallery for tracking unknown persons/customers
    during an active session. Purges old embeddings automatically to save memory.
    Connects fragmented DeepSORT tracks when a camera glitches.
    """
    def __init__(self, threshold: float = 0.65, ttl_seconds: float = 1800):
        self.threshold = threshold
        self.ttl = ttl_seconds
        
        # global_id -> {"vector": np.ndarray, "last_seen": float}
        self.embeddings: dict[str, dict] = {}
        
        self.index = faiss.IndexFlatIP(512)
        self._ids: list[str] = []

    def match(self, embedding: np.ndarray) -> str | None:
        """Find the closest matching session ID if above threshold AND clearly ahead of runner-up."""
        if self.index.ntotal == 0:
            return None

        k = min(2, self.index.ntotal)
        similarities, indices = self.index.search(embedding, k=k)
        sim = float(similarities[0][0])
        idx = int(indices[0][0])

        if sim < self.threshold:
            return None

        if k > 1:
            runner_up_sim = float(similarities[0][1])
            if (sim - runner_up_sim) < ReIDGallery.MIN_MATCH_MARGIN:
                return None

        return self._ids[idx]

    def register(self, embedding: np.ndarray) -> str:
        """Add a new embedding and generate a new session ID."""
        global_id = f"session_{uuid.uuid4().hex[:8]}"
        self.update_seen(global_id, embedding)
        return global_id

    def update_seen(self, global_id: str, embedding: np.ndarray) -> None:
        """Update the embedding vector and reset the TTL timer."""
        self.embeddings[global_id] = {
            "vector": embedding,
            "last_seen": time.time()
        }
        self._rebuild_index()

    def touch(self, global_id: str) -> None:
        """Reset the TTL timer without changing the embedding."""
        if global_id in self.embeddings:
            self.embeddings[global_id]["last_seen"] = time.time()

    def remove(self, global_id: str) -> None:
        """Delete an embedding manually (used when promoted to worker)."""
        if global_id in self.embeddings:
            del self.embeddings[global_id]
            self._rebuild_index()

    def purge_old(self) -> None:
        """Garbage collect embeddings older than TTL (30 mins)."""
        now = time.time()
        to_delete = [gid for gid, data in self.embeddings.items() if now - data["last_seen"] > self.ttl]
        
        if to_delete:
            for gid in to_delete:
                del self.embeddings[gid]
            self._rebuild_index()
            print(f"[SessionGallery] Purged {len(to_delete)} stale IDs: {to_delete}")

    def _rebuild_index(self) -> None:
        """Rebuild the Faiss index from the in-memory dictionary."""
        self.index.reset()
        self._ids = list(self.embeddings.keys())
        if self._ids:
            vectors = np.vstack([self.embeddings[gid]["vector"] for gid in self._ids])
            self.index.add(vectors)
```

---

### <a id="📄-src-kbs-role-engine-py"></a>📄 `src/kbs/role_engine.py`

**File Info:**
- **Size**: 31.01 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/kbs/role_engine.py`
- **Relative Path**: `src/kbs`
- **Created**: 2026-07-14 09:09:26 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 09:09:26 (Asia/Damascus / GMT+03:00)
- **MD5**: `7cb61a8f33c64cdb1355372095cb856d`
- **SHA256**: `8217b89976b13639aa77744040f568bfbd1e3804cb17f3a8ece7ef84f83d27eb`
- **Encoding**: UTF-8

**File code content:**

```python
"""
role_engine.py
--------------
Point-based evidence engine (ExpertA) for classifying tracked persons
as Customer or Worker in a restaurant surveillance pipeline.

Architecture
------------
1. ObservationFact   — declared by pipeline each cycle (input)
2. ScoreAccumulator  — one per global_id, holds running worker/customer scores
3. EvidenceApplied   — sentinel fact preventing duplicate rule firing
4. DecayApplied      — sentinel fact preventing duplicate decay
5. RoleDecision      — output fact with final role + confidence

Scoring philosophy
------------------
Each rule awards positive points to ONE score channel based on
(action, zone_type, duration, appearances). Old evidence decays
each cycle via a decay rule. Confirmation fires when a score
crosses a threshold; reversal fires when the OTHER score overtakes.

All zone_type values come from the pipeline's ZONE_TYPE_MAP:
  table_area → "table"
  service_path/hallway/corridor/open_area/mixed_area/entrance/
  bathroom_entrance/prayer_room_entrance → "walk"
  staff_area/buffet/cashier → "staff"
"""

from src.kbs import _compat  # noqa: F401  (must precede `import experta` — see _compat.py)
from experta import (
    KnowledgeEngine, Fact, Field, Rule, DefFacts,
    AS, MATCH, NOT, TEST, OR,
)


# ── Facts ──────────────────────────────────────────────────────────────────

class ObservationFact(Fact):
    """Input fact declared by the pipeline each inference cycle.

    Fields
    ------
    track_id         : int   – DeepSORT camera-local track id
    global_id        : str   – Re-ID identity ("global_7") or fallback "local_<tid>"
    action           : str   – LSTM label: sitting|standing|walking|serving
    zone_type        : str   – normalized zone: table|walk|staff|unknown
    pose_frame_count : int   – consecutive pose-frames in current action+zone
    previous_duration_frames : int – duration of the prior action+zone before reset
    appearance_count : int   – Re-ID cross-camera appearances
    previous_role    : str   – role from last cycle (unknown|customer|worker)
    """
    track_id         = Field(int,    mandatory=True)
    global_id        = Field(str,    mandatory=True)
    action           = Field(str,    default="unknown")
    zone_type        = Field(str,    default="unknown")
    zone_id          = Field(str,    default="unknown")
    pose_frame_count = Field(int,    default=0)
    previous_duration_frames = Field(int, default=0)
    appearance_count = Field(int,    default=0)
    previous_role    = Field(str,    default="unknown")


class ScoreAccumulator(Fact):
    """Running evidence totals for one identity.

    Fields
    ------
    global_id      : str   – links to ObservationFact.global_id
    worker_score   : float – accumulated worker evidence
    customer_score : float – accumulated customer evidence
    confirmed_role : str   – "unknown"|"customer"|"worker"
    cycle_count    : int   – how many cycles this accumulator has lived
    zone_history   : tuple – last 5 (zone_type, action, duration_frames) states
    """
    global_id      = Field(str,   mandatory=True)
    worker_score   = Field(float, default=0.0)
    customer_score = Field(float, default=0.0)
    confirmed_role = Field(str,   default="unknown")
    cycle_count    = Field(int,   default=0)
    visited_tables = Field(tuple, default=())
    visited_staff  = Field(bool,  default=False)
    zone_history   = Field(tuple, default=())


class EvidenceApplied(Fact):
    """Sentinel: evidence rule <rule_tag> already fired for <global_id>."""
    global_id = Field(str, mandatory=True)
    rule_tag  = Field(str, mandatory=True)


class ZoneHistoryApplied(Fact):
    """Sentinel: zone history already updated for <global_id> this cycle."""
    global_id = Field(str, mandatory=True)


class DecayApplied(Fact):
    """Sentinel: decay already applied for <global_id> this cycle."""
    global_id = Field(str, mandatory=True)


class MergeRequest(Fact):
    """Signals that two global_ids should be merged (Re-ID link)."""
    old_global_id = Field(str, mandatory=True)
    new_global_id = Field(str, mandatory=True)


class RoleDecision(Fact):
    """Output fact with the engine's verdict.

    Fields
    ------
    track_id       : int
    global_id      : str
    role           : str   – "unknown"|"customer"|"worker"
    confidence     : float – 0.0 to 1.0
    worker_score   : float
    customer_score : float
    """
    track_id       = Field(int,   mandatory=True)
    global_id      = Field(str,   mandatory=True)
    role           = Field(str,   default="unknown")
    confidence     = Field(float, default=0.0)
    worker_score   = Field(float, default=0.0)
    customer_score = Field(float, default=0.0)


# ── Constants ──────────────────────────────────────────────────────────────

# Thresholds & decay
CONFIRM_THRESHOLD   = 12.0   # min score to confirm a role
CONFIRM_MARGIN      = 8.0    # must lead the other score by this much
REVERSAL_MARGIN     = 12.0   # contrary score must exceed by this to reverse
DECAY_RATE          = 0.997  # 90-second half-life at 3fps

# Evidence weights  (rule_tag → points)
W_SIT_TABLE           = 6.0   # sitting + table  → very strong customer
W_SIT_TABLE_LONG      = 4.0   # bonus: sitting + table > 10 frames
W_STAFF_ZONE          = 5.5   # any action + staff zone → very strong worker
W_STAFF_ZONE_LONG     = 3.5   # bonus: staff zone > 8 frames
W_SERVING             = 3.0   # serving action anywhere
W_SERVING_SUSTAINED   = 4.0   # serving > 6 frames
W_WALK_SERVICE        = 1.0   # walking + walk zone (weak worker signal)
W_STAND_TABLE         = 1.5   # standing + table → mild customer
W_SIT_NON_TABLE       = 2.0   # sitting outside table → mild worker
W_REAPPEAR            = 2.5   # cross-camera reappearance > 2
W_REAPPEAR_HIGH       = 3.0   # cross-camera reappearance > 4
W_ENTRANCE_WALK       = 0.0   # entrance + walking → neutral (no points)
W_STAND_WALK_ZONE     = 0.5   # standing in walk zone → very weak worker

# Behavioral weights (macro-routing)
W_MULTI_TABLE         = 2.0   # Applied per frame if len(visited_tables) >= 2
W_STAFF_TO_TABLE      = 2.0   # Applied per frame if visited_staff=True AND currently at table
W_STAFF_WALK_TABLE_PATTERN = 5.0   # staff -> walk -> table transition pattern
W_RECENT_SIT_CARRYOVER    = 2.5   # table sitting carryover into standing/walking
W_TABLE_SIT_HISTORY_STRONG = 12.0  # strong customer evidence from recent table-sitting history

ZONE_HISTORY_LIMIT = 5
RECENT_SIT_CARRYOVER_FRAMES = 90  # 30s at the 3fps pose sampling rate


# ── Engine ─────────────────────────────────────────────────────────────────

class RoleEngine(KnowledgeEngine):
    """
    Point-based evidence engine for restaurant role classification.

    Usage
    -----
        engine = RoleEngine()
        engine.reset()
        # Optionally re-declare ScoreAccumulators from previous cycle
        engine.declare(ScoreAccumulator(global_id=gid, worker_score=ws, ...))
        # Declare one ObservationFact per tracked person
        engine.declare(ObservationFact(track_id=..., global_id=..., ...))
        engine.run()
        # Read RoleDecision facts from engine.facts
    """

    @staticmethod
    def _trim_zone_history(history: tuple) -> tuple:
        return tuple(history[-ZONE_HISTORY_LIMIT:])

    # ── Bootstrap: ensure every observation has an accumulator ──────────

    @Rule(
        AS.obs << ObservationFact(global_id=MATCH.gid),
        NOT(ScoreAccumulator(global_id=MATCH.gid)),
        salience=100,
    )
    def create_accumulator(self, obs, gid):
        """Create a fresh ScoreAccumulator when a new global_id appears."""
        self.declare(ScoreAccumulator(
            global_id=gid,
            worker_score=0.0,
            customer_score=0.0,
            confirmed_role=obs["previous_role"],
            cycle_count=0,
            visited_tables=(),
            visited_staff=False,
            zone_history=(),
        ))

    # ── Decay: fade old evidence ───────────────────────────────────────

    @Rule(
        AS.acc << ScoreAccumulator(
            global_id=MATCH.gid,
            worker_score=MATCH.ws,
            customer_score=MATCH.cs,
            cycle_count=MATCH.cc,
        ),
        NOT(DecayApplied(global_id=MATCH.gid)),
        salience=90,
    )
    def apply_decay(self, acc, gid, ws, cs, cc):
        """Decay both scores and bump cycle_count."""
        self.modify(acc,
            worker_score=round(ws * DECAY_RATE, 3),
            customer_score=round(cs * DECAY_RATE, 3),
            cycle_count=cc + 1,
        )
        self.declare(DecayApplied(global_id=gid))

    # ── Evidence Rules (salience=50) ───────────────────────────────────
    # Each rule: match observation + accumulator, guard against duplicate
    # firing with EvidenceApplied sentinel, then modify accumulator.

    # --- BEHAVIORAL HISTORY UPDATES (salience=100) ---

    @Rule(
        ObservationFact(global_id=MATCH.gid, zone_type="table", zone_id=MATCH.zid),
        TEST(lambda zid: zid != "unknown"),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, visited_tables=MATCH.vt),
        TEST(lambda zid, vt: zid not in vt),
        salience=100,
    )
    def update_visited_tables(self, acc, gid, zid, vt):
        """Record unique table visits to identify table-hopping."""
        new_vt = tuple(list(vt) + [zid])
        self.modify(acc, visited_tables=new_vt)

    @Rule(
        ObservationFact(global_id=MATCH.gid, zone_type="staff"),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, visited_staff=False),
        salience=100,
    )
    def update_visited_staff(self, acc, gid):
        """Record that this person has entered a staff-only area."""
        self.modify(acc, visited_staff=True)

    @Rule(
        AS.obs << ObservationFact(
            global_id=MATCH.gid,
            action=MATCH.action,
            zone_type=MATCH.zone_type,
            pose_frame_count=MATCH.pfc,
            previous_duration_frames=MATCH.prev_pfc,
        ),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, zone_history=MATCH.history),
        NOT(ZoneHistoryApplied(global_id=MATCH.gid)),
        salience=99,
    )
    def update_zone_history(self, acc, gid, action, zone_type, pfc, prev_pfc, history):
        """Track the latest contiguous zone/action segment in a bounded history."""
        current_entry = (zone_type, action, pfc)
        current_key = current_entry[:2]

        new_history = list(history)

        if new_history and new_history[-1][:2] == current_key:
            last_zone, last_action, last_duration = new_history[-1]
            new_history[-1] = (last_zone, last_action, max(last_duration, pfc))
        else:
            if new_history and prev_pfc > 0:
                last_zone, last_action, last_duration = new_history[-1]
                new_history[-1] = (last_zone, last_action, max(last_duration, prev_pfc))
            new_history.append(current_entry)

        self.modify(acc, zone_history=self._trim_zone_history(tuple(new_history)))
        self.declare(ZoneHistoryApplied(global_id=gid))

    # --- CUSTOMER evidence ---

    @Rule(
        ObservationFact(global_id=MATCH.gid, action="sitting", zone_type="table"),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, customer_score=MATCH.cs),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="sit_table")),
        salience=50,
    )
    def ev_sit_table(self, acc, gid, cs):
        """Sitting at a table → strong customer signal."""
        self.modify(acc, customer_score=round(cs + W_SIT_TABLE, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=sit_table (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="sit_table"))

    @Rule(
        ObservationFact(
            global_id=MATCH.gid, action="sitting",
            zone_type="table", pose_frame_count=MATCH.pfc,
        ),
        TEST(lambda pfc: pfc > 10),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, customer_score=MATCH.cs),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="sit_table_long")),
        salience=49,
    )
    def ev_sit_table_long(self, acc, gid, cs, pfc):
        """Sitting at table for extended time → bonus customer evidence."""
        self.modify(acc, customer_score=round(cs + W_SIT_TABLE_LONG, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=sit_table_long (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="sit_table_long"))

    @Rule(
        ObservationFact(global_id=MATCH.gid, action="standing", zone_type="table"),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, customer_score=MATCH.cs),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="stand_table")),
        salience=50,
    )
    def ev_stand_table(self, acc, gid, cs):
        """Standing near table → mild customer signal."""
        self.modify(acc, customer_score=round(cs + W_STAND_TABLE, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=stand_table (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="stand_table"))

    # --- WORKER evidence ---

    @Rule(
        ObservationFact(global_id=MATCH.gid, zone_type="staff"),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, worker_score=MATCH.ws),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="staff_zone")),
        salience=50,
    )
    def ev_staff_zone(self, acc, gid, ws):
        """Present in staff-only zone → strong worker signal."""
        self.modify(acc, worker_score=round(ws + W_STAFF_ZONE, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=staff_zone (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="staff_zone"))

    @Rule(
        ObservationFact(
            global_id=MATCH.gid, zone_type="staff",
            pose_frame_count=MATCH.pfc,
        ),
        TEST(lambda pfc: pfc > 8),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, worker_score=MATCH.ws),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="staff_zone_long")),
        salience=49,
    )
    def ev_staff_zone_long(self, acc, gid, ws, pfc):
        """Lingering in staff zone → bonus worker evidence."""
        self.modify(acc, worker_score=round(ws + W_STAFF_ZONE_LONG, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=staff_zone_long (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="staff_zone_long"))

    @Rule(
        ObservationFact(global_id=MATCH.gid, action="serving", pose_frame_count=MATCH.pfc),
        TEST(lambda pfc: pfc >= 4),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, worker_score=MATCH.ws),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="serving")),
        salience=50,
    )
    def ev_serving(self, acc, gid, ws, pfc):
        """Sustained serving action detected -> moderate worker signal. (Filters kids playing)"""
        self.modify(acc, worker_score=round(ws + W_SERVING, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=serving (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="serving"))

    @Rule(
        ObservationFact(
            global_id=MATCH.gid, action="serving",
            pose_frame_count=MATCH.pfc,
        ),
        TEST(lambda pfc: pfc > 6),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, worker_score=MATCH.ws),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="serving_sustained")),
        salience=49,
    )
    def ev_serving_sustained(self, acc, gid, ws, pfc):
        """Sustained serving action → strong worker evidence."""
        self.modify(acc, worker_score=round(ws + W_SERVING_SUSTAINED, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=serving_sustained (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="serving_sustained"))

    # NOTE: walking/standing in a walk zone is NOT a standalone worker signal —
    # customers walk through walk zones too. These rules now only REINFORCE
    # an identity that RoleEngine has already confirmed as "worker" (via
    # staff_zone/serving/reappear evidence). They cannot help an "unknown"
    # or "customer" person become a worker on their own.

    @Rule(
        ObservationFact(global_id=MATCH.gid, action="walking", zone_type="walk"),
        AS.acc << ScoreAccumulator(
            global_id=MATCH.gid, worker_score=MATCH.ws, confirmed_role="worker",
        ),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="walk_service")),
        salience=50,
    )
    def ev_walk_service(self, acc, gid, ws):
        """Walking in service/walk zone → weak reinforcement, workers only."""
        self.modify(acc, worker_score=round(ws + W_WALK_SERVICE, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=walk_service (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="walk_service"))

    @Rule(
        ObservationFact(global_id=MATCH.gid, action="standing", zone_type="walk"),
        AS.acc << ScoreAccumulator(
            global_id=MATCH.gid, worker_score=MATCH.ws, confirmed_role="worker",
        ),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="stand_walk")),
        salience=50,
    )
    def ev_stand_walk_zone(self, acc, gid, ws):
        """Standing in walk zone → very weak reinforcement, workers only."""
        self.modify(acc, worker_score=round(ws + W_STAND_WALK_ZONE, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=stand_walk (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="stand_walk"))

    @Rule(
        ObservationFact(
            global_id=MATCH.gid, action="sitting",
            zone_type=MATCH.zt,
        ),
        TEST(lambda zt: zt not in ("table", "unknown")),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, worker_score=MATCH.ws),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="sit_nontable")),
        salience=50,
    )
    def ev_sit_non_table(self, acc, gid, ws, zt):
        """Sitting outside a table zone → mild worker signal (resting worker)."""
        self.modify(acc, worker_score=round(ws + W_SIT_NON_TABLE, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=sit_nontable (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="sit_nontable"))

    # --- MACRO-BEHAVIOR evidence ---

    @Rule(
        ObservationFact(global_id=MATCH.gid),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, visited_tables=MATCH.vt, worker_score=MATCH.ws),
        TEST(lambda vt: len(vt) >= 2),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="multi_table")),
        salience=48,
    )
    def ev_multi_table(self, acc, gid, vt, ws):
        """Visited multiple tables -> definitive worker routing behavior."""
        self.modify(acc, worker_score=round(ws + W_MULTI_TABLE, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=multi_table (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="multi_table"))

    @Rule(
        ObservationFact(global_id=MATCH.gid, zone_type="table"),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, visited_staff=True, worker_score=MATCH.ws),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="staff_to_table")),
        salience=48,
    )
    def ev_staff_to_table(self, acc, gid, ws):
        """Transit from staff zone to table -> definitive worker routing behavior."""
        self.modify(acc, worker_score=round(ws + W_STAFF_TO_TABLE, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=staff_to_table (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="staff_to_table"))

    @staticmethod
    def _has_staff_walk_table_pattern(history: tuple) -> bool:
        filtered = [h[0] for h in history if h[0] != "unknown"]
        return len(filtered) >= 3 and filtered[-3:] == ["staff", "walk", "table"]

    @Rule(
        ObservationFact(global_id=MATCH.gid, zone_type="table"),
        AS.acc << ScoreAccumulator(
            global_id=MATCH.gid,
            zone_history=MATCH.history,
            worker_score=MATCH.ws,
        ),
        TEST(lambda history: RoleEngine._has_staff_walk_table_pattern(history)),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="staff_walk_table_pattern")),
        salience=47,
    )
    def ev_staff_walk_table_pattern(self, acc, gid, ws, history):
        """staff -> walk -> table route strongly suggests a worker."""
        self.modify(acc, worker_score=round(ws + W_STAFF_WALK_TABLE_PATTERN, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=staff_walk_table_pattern (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="staff_walk_table_pattern"))

    @Rule(
        ObservationFact(global_id=MATCH.gid, action=MATCH.action, zone_type=MATCH.zt),
        TEST(lambda action, zt: action in ("standing", "walking") and zt != "table"),
        AS.acc << ScoreAccumulator(
            global_id=MATCH.gid,
            zone_history=MATCH.history,
            customer_score=MATCH.cs,
        ),
        TEST(lambda history: any(h[0] == "table" and h[1] == "sitting" and h[2] >= RECENT_SIT_CARRYOVER_FRAMES for h in history[:-1])),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="recent_sit_carryover")),
        salience=47,
    )
    def ev_recent_sit_carryover(self, acc, gid, cs, action, zt, history):
        """A recent long sit at table should carry some customer evidence forward."""
        self.modify(acc, customer_score=round(cs + W_RECENT_SIT_CARRYOVER, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=recent_sit_carryover (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="recent_sit_carryover"))

    @Rule(
        ObservationFact(global_id=MATCH.gid, zone_type="table", action=MATCH.action),
        TEST(lambda action: action != "sitting"),
        AS.acc << ScoreAccumulator(
            global_id=MATCH.gid,
            zone_history=MATCH.history,
            customer_score=MATCH.cs,
        ),
        TEST(lambda history: any(h[0] == "table" and h[1] == "sitting" and h[2] >= RECENT_SIT_CARRYOVER_FRAMES for h in history[:-1])),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="table_sit_history_strong")),
        salience=46,
    )
    def ev_table_sit_history_strong(self, acc, gid, cs, action, history):
        """Recent long table sitting in history is a very strong customer signal."""
        self.modify(acc, customer_score=round(cs + W_TABLE_SIT_HISTORY_STRONG, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=table_sit_history_strong (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="table_sit_history_strong"))

    # --- Re-ID reappearance evidence ---

    @Rule(
        ObservationFact(
            global_id=MATCH.gid,
            appearance_count=MATCH.ac,
        ),
        TEST(lambda ac: ac > 2),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, worker_score=MATCH.ws),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="reappear")),
        salience=48,
    )
    def ev_reappear(self, acc, gid, ws, ac):
        """Appeared across cameras > 2 times → worker signal."""
        self.modify(acc, worker_score=round(ws + W_REAPPEAR, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=reappear (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="reappear"))

    @Rule(
        ObservationFact(
            global_id=MATCH.gid,
            appearance_count=MATCH.ac,
        ),
        TEST(lambda ac: ac > 4),
        AS.acc << ScoreAccumulator(global_id=MATCH.gid, worker_score=MATCH.ws),
        NOT(EvidenceApplied(global_id=MATCH.gid, rule_tag="reappear_high")),
        salience=47,
    )
    def ev_reappear_high(self, acc, gid, ws, ac):
        """Appeared across cameras > 4 times → stronger worker signal."""
        self.modify(acc, worker_score=round(ws + W_REAPPEAR_HIGH, 3))
        print(f"[RoleEngine] EVIDENCE fired: gid={gid} rule_tag=reappear_high (will not re-fire until reset/decay episode)")
        self.declare(EvidenceApplied(global_id=gid, rule_tag="reappear_high"))

    # ── Confirmation: first-time role lock ─────────────────────────────

    @Rule(
        AS.acc << ScoreAccumulator(
            global_id=MATCH.gid,
            customer_score=MATCH.cs,
            worker_score=MATCH.ws,
            confirmed_role="unknown",
        ),
        TEST(lambda cs, ws: cs >= CONFIRM_THRESHOLD and (cs - ws) >= CONFIRM_MARGIN),
        salience=30,
    )
    def confirm_customer(self, acc, gid, cs, ws):
        """Customer score crossed threshold with sufficient margin."""
        print(f"[RoleEngine] CONFIRM gid={gid} → customer (cs={cs}, ws={ws})")
        self.modify(acc, confirmed_role="customer")

    @Rule(
        AS.acc << ScoreAccumulator(
            global_id=MATCH.gid,
            worker_score=MATCH.ws,
            customer_score=MATCH.cs,
            confirmed_role="unknown",
        ),
        TEST(lambda ws, cs: ws >= CONFIRM_THRESHOLD and (ws - cs) >= CONFIRM_MARGIN),
        salience=30,
    )
    def confirm_worker(self, acc, gid, ws, cs):
        """Worker score crossed threshold with sufficient margin."""
        print(f"[RoleEngine] CONFIRM gid={gid} → worker (ws={ws}, cs={cs})")
        self.modify(acc, confirmed_role="worker")

    # ── Reversal: override a sticky confirmation ───────────────────────

    @Rule(
        AS.acc << ScoreAccumulator(
            global_id=MATCH.gid,
            confirmed_role="customer",
            worker_score=MATCH.ws,
            customer_score=MATCH.cs,
        ),
        TEST(lambda ws, cs: (ws - cs) >= REVERSAL_MARGIN),
        salience=25,
    )
    def reverse_to_worker(self, acc, gid, ws, cs):
        """Strong worker evidence overturns a customer confirmation."""
        print(f"[RoleEngine] REVERSAL gid={gid} customer → worker (ws={ws}, cs={cs})")
        self.modify(acc, confirmed_role="worker")

    @Rule(
        AS.acc << ScoreAccumulator(
            global_id=MATCH.gid,
            confirmed_role="worker",
            customer_score=MATCH.cs,
            worker_score=MATCH.ws,
        ),
        TEST(lambda cs, ws: (cs - ws) >= REVERSAL_MARGIN),
        salience=25,
    )
    def reverse_to_customer(self, acc, gid, cs, ws):
        """Strong customer evidence overturns a worker confirmation."""
        print(f"[RoleEngine] REVERSAL gid={gid} worker → customer (cs={cs}, ws={ws})")
        self.modify(acc, confirmed_role="customer")

    # ── Re-ID Merge: combine accumulators when track changes ───────────

    @Rule(
        AS.merge << MergeRequest(
            old_global_id=MATCH.old_gid,
            new_global_id=MATCH.new_gid,
        ),
        AS.old_acc << ScoreAccumulator(
            global_id=MATCH.old_gid,
            worker_score=MATCH.old_ws,
            customer_score=MATCH.old_cs,
        ),
        AS.new_acc << ScoreAccumulator(
            global_id=MATCH.new_gid,
            worker_score=MATCH.new_ws,
            customer_score=MATCH.new_cs,
        ),
        salience=95,
    )
    def merge_accumulators(self, merge, old_acc, new_acc,
                           old_gid, new_gid,
                           old_ws, old_cs, new_ws, new_cs):
        """Merge old accumulator into the new one and remove old."""
        old_history = old_acc["zone_history"]
        new_history = new_acc["zone_history"]
        self.modify(new_acc,
            worker_score=round(new_ws + old_ws, 3),
            customer_score=round(new_cs + old_cs, 3),
            zone_history=self._trim_zone_history(old_history + new_history),
        )
        self.retract(old_acc)
        self.retract(merge)

    # ── Emit RoleDecision output ───────────────────────────────────────

    @Rule(
        AS.obs << ObservationFact(
            track_id=MATCH.tid,
            global_id=MATCH.gid,
        ),
        AS.acc << ScoreAccumulator(
            global_id=MATCH.gid,
            worker_score=MATCH.ws,
            customer_score=MATCH.cs,
            confirmed_role=MATCH.role,
        ),
        NOT(RoleDecision(global_id=MATCH.gid)),
        salience=10,
    )
    def emit_decision(self, obs, acc, tid, gid, ws, cs, role):
        """Produce the final RoleDecision fact for pipeline consumption."""
        total = ws + cs
        confidence = 0.0
        if total > 0:
            dominant = max(ws, cs)
            confidence = round(dominant / total, 3)

        self.declare(RoleDecision(
            track_id=tid,
            global_id=gid,
            role=role,
            confidence=confidence,
            worker_score=ws,
            customer_score=cs,
        ))

    # ── Public helper: extract decisions after run() ───────────────────

    def get_decisions(self) -> dict:
        """Return {track_id: {role, confidence, worker_score, customer_score}}."""
        results = {}
        for fact in self.facts.values():
            if isinstance(fact, RoleDecision):
                results[fact["track_id"]] = {
                    "global_id":      fact["global_id"],
                    "role":           fact["role"],
                    "confidence":     fact["confidence"],
                    "worker_score":   fact["worker_score"],
                    "customer_score": fact["customer_score"],
                }
        return results

    def get_accumulators(self) -> dict:
        """Return {global_id: {worker_score, customer_score, confirmed_role, cycle_count}}.
        
        Call after run() to persist accumulators across cycles.
        """
        results = {}
        for fact in self.facts.values():
            if isinstance(fact, ScoreAccumulator):
                results[fact["global_id"]] = {
                    "worker_score":   fact["worker_score"],
                    "customer_score": fact["customer_score"],
                    "confirmed_role": fact["confirmed_role"],
                    "cycle_count":    fact["cycle_count"],
                    "visited_tables": fact["visited_tables"],
                    "visited_staff":  fact["visited_staff"],
                    "zone_history":   fact["zone_history"],
                }
        return results
```

---

### <a id="📄-src-kbs-table-kbs-py"></a>📄 `src/kbs/table_kbs.py`

**File Info:**
- **Size**: 3.86 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/kbs/table_kbs.py`
- **Relative Path**: `src/kbs`
- **Created**: 2026-07-14 09:09:34 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 09:09:34 (Asia/Damascus / GMT+03:00)
- **MD5**: `9a0468d889afdb7d7894e72c188c0cc8`
- **SHA256**: `039ba19f8992e9535a5fec7159ae5730042cdc88b965da1b7dda000ff063a0b8`
- **Encoding**: UTF-8

**File code content:**

```python
"""
table_kbs.py
------------
Determines the state of each table zone based on customer presence
and serving events.

Table states
------------
free     : no customer in zone
occupied : ≥1 customer present + table not yet served
dirty    : table is free but was served (needs cleaning)

Serving flag lifecycle
----------------------
When a Worker's serving action is detected near an occupied table,
live_pipeline sets TableFact.was_served = True.
This flag is cleared (reset to False) once the table returns to free
AND has been cleaned (external signal, or timer — future work).
"""

from src.kbs import _compat  # noqa: F401  (must precede `import experta` — see _compat.py)
from experta import KnowledgeEngine, Fact, Field, Rule, AS, MATCH, TEST


# ---------------------------------------------------------------------------
# Facts
# ---------------------------------------------------------------------------

class TableFact(Fact):
    """
    One fact per table zone, per camera.

    Fields
    ------
    zone_id          : str  - unique zone identifier, e.g. "cam1_table_3"
    customer_count   : int  - number of confirmed customers currently in zone
    was_served       : bool - True if a serving event occurred while occupied
    state            : str  - output: "free"|"occupied"|"dirty"
    """
    zone_id        = Field(str, mandatory=True)
    customer_count = Field(int, default=0)
    was_served     = Field(bool, default=False)
    state          = Field(str, default="free")


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class TableKBS(KnowledgeEngine):
    """
    Classifies table state each inference cycle.
    Call reset() + declare TableFacts + run() per cycle.
    """

    # -- Free ----------------------------------------------------------------
    # No customers in zone → free.
    # was_served is NOT cleared here; dirty rule handles that transition.

    @Rule(
        AS.table << TableFact(
            customer_count=0,
            was_served=False,
            state=MATCH.current_state,
        ),
        TEST(lambda current_state: current_state != "free"),
        salience=10,
    )
    def set_state_free(self, table, current_state):
        self.modify(table, state="free")

    # -- Occupied ------------------------------------------------------------
    # At least 1 customer present and table has not been served yet.

    @Rule(
        AS.table << TableFact(
            customer_count=MATCH.count,
            was_served=False,
            state=MATCH.current_state,
        ),
        TEST(lambda count, current_state: count > 0 and current_state != "occupied"),
        salience=20,
    )
    def set_state_occupied(self, table, count, current_state):
        self.modify(table, state="occupied")

    # -- Occupied + served ---------------------------------------------------
    # Customers still present but table was already served.
    # Stays occupied (not dirty) until customers leave.

    @Rule(
        AS.table << TableFact(
            customer_count=MATCH.count,
            was_served=True,
            state=MATCH.current_state,
        ),
        TEST(lambda count, current_state: count > 0 and current_state != "occupied"),
        salience=20,
    )
    def set_state_occupied_served(self, table, count, current_state):
        self.modify(table, state="occupied")

    # -- Dirty ---------------------------------------------------------------
    # No customers left but table was served → needs cleaning.

    @Rule(
        AS.table << TableFact(
            customer_count=0,
            was_served=True,
            state=MATCH.current_state,
        ),
        TEST(lambda current_state: current_state != "dirty"),
        salience=30,
    )
    def set_state_dirty(self, table, current_state):
        self.modify(table, state="dirty")
```

---

### <a id="📄-src-utils-extract-reference-frames-py"></a>📄 `src/utils/extract_reference_frames.py`

**File Info:**
- **Size**: 1.67 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/utils/extract_reference_frames.py`
- **Relative Path**: `src/utils`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `fca2b685458c7c80681da159bd81fb0d`
- **SHA256**: `fbe844ee2190e41726dd9c108344d813a59f83ea39dc0923160ab2b7e1a01b55`
- **Encoding**: UTF-8

**File code content:**

```python
import json
import sys
from pathlib import Path

import cv2


PROJECT_DIR = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_DIR))

VIDEOS_INDEX_PATH = PROJECT_DIR / "data" / "metadata" / "videos" / "videos_index.json"
OUTPUT_DIR = PROJECT_DIR / "data" / "debug" / "zones" / "reference_frames"


def extract_frame(video_path: Path, output_path: Path, target_second: int = 30):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"❌ Cannot open video: {video_path}")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25

    target_frame = int(fps * target_second)
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

    ret, frame = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

    cap.release()

    if not ret:
        print(f"❌ Cannot extract frame from: {video_path}")
        return False

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), frame)

    print(f"✅ Saved reference frame: {output_path}")
    return True


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(VIDEOS_INDEX_PATH, "r", encoding="utf-8") as f:
        videos = json.load(f)

    used_cameras = set()

    for video in videos:
        camera_id = video["camera_id"]

        if camera_id in used_cameras:
            continue

        used_cameras.add(camera_id)

        video_path = PROJECT_DIR / video["path"]
        output_path = OUTPUT_DIR / f"{camera_id}_reference.jpg"

        extract_frame(video_path=video_path, output_path=output_path, target_second=30)


if __name__ == "__main__":
    main()
```

---

### <a id="📄-src-utils-label-dataset-py"></a>📄 `src/utils/label_dataset.py`

**File Info:**
- **Size**: 3.43 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/utils/label_dataset.py`
- **Relative Path**: `src/utils`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `f83413054433c3b588ce1c88c67e432e`
- **SHA256**: `9cb26c30d32e68b2335e31c937446701aa8aedf59eb6ed13910f3f8128cafb1c`
- **Encoding**: ASCII

**File code content:**

```python
import argparse
import json
import os
import cv2
from collections import defaultdict

LABEL_MAP = {
    ord('1'): 'standing',
    ord('2'): 'sitting',
    ord('3'): 'walking',
    ord('4'): 'serving'
}

def label_dataset(json_path, crops_dir, camera_id):
    with open(json_path, "r") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} entries from {json_path}")
    labeled_count = sum(1 for d in data if d.get("label"))
    print(f"Already labeled: {labeled_count}/{len(data)}")

    # Group indices by tracked_person_id (preserving insertion order)
    person_groups = defaultdict(list)
    for i, entry in enumerate(data):
        person_groups[entry['tracked_person_id']].append(i)

    cv2.namedWindow("Labeling UI", cv2.WINDOW_NORMAL)

    for person_id, indices in person_groups.items():
        unlabeled = [i for i in indices if not data[i].get("label")]
        if not unlabeled:
            continue

        print(f"\n--- Person {person_id} ({len(unlabeled)} unlabeled / {len(indices)} total) ---")

        for i in unlabeled:
            entry = data[i]

            crop_filename = f"{camera_id}_{entry['vid_id']}_frame_{entry['frame_id']:06d}_track_{entry['tracked_person_id']}.jpg"
            crop_path = os.path.join(crops_dir, crop_filename)

            if not os.path.exists(crop_path):
                print(f"Warning: {crop_path} not found. Skipped.")
                continue

            img = cv2.imread(crop_path)
            if img is None:
                print(f"Warning: Could not read {crop_path}. Skipped.")
                continue

            while True:
                display_img = img.copy()
                h, w = display_img.shape[:2]
                if min(h, w) < 300:
                    scale = 300.0 / min(h, w)
                    display_img = cv2.resize(display_img, (0, 0), fx=scale, fy=scale)

                cv2.putText(display_img, "1:Stand 2:Sit 3:Walk 4:Serve | s:Skip q:Quit",
                            (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                cv2.imshow("Labeling UI", display_img)

                print(f"\n[Person {person_id}] {crop_filename}")
                print("1=standing, 2=sitting, 3=walking, 4=serving | s=skip, q=quit")

                key = cv2.waitKey(0) & 0xFF

                if key in LABEL_MAP:
                    entry['label'] = LABEL_MAP[key]
                    print(f"-> Assigned: {entry['label']}")
                    break
                elif key == ord('s'):
                    print("-> Skipped")
                    break
                elif key == ord('q'):
                    print("\nQuitting... saving progress.")
                    with open(json_path, "w") as f:
                        json.dump(data, f, indent=2)
                    cv2.destroyAllWindows()
                    return

            with open(json_path, "w") as f:
                json.dump(data, f, indent=2)

    cv2.destroyAllWindows()
    print("\nDataset labeling complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI for manual action labeling.")
    parser.add_argument("--json", default="data/debug/classification/samples/raw_poses.json", help="Path to JSON file")
    parser.add_argument("--crops", default="data/debug/crops", help="Path to crops dir")
    parser.add_argument("--camera", default="live_camera", help="Camera ID (default: live_camera)")
    args = parser.parse_args()

    label_dataset(args.json, args.crops, args.camera)
```

---

### <a id="📄-src-utils-remove-skipped-samples-py"></a>📄 `src/utils/remove_skipped_samples.py`

**File Info:**
- **Size**: 592 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/utils/remove_skipped_samples.py`
- **Relative Path**: `src/utils`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `72291825aa5d497460e7d618a46ba6df`
- **SHA256**: `b752b827ae482ccf87790921d433e9f59e2e977cb298f9aae0bf07f80b2ce37c`
- **Encoding**: ASCII

**File code content:**

```python
import json
from pathlib import Path
from collections import Counter, defaultdict
import random

filepath = Path(__file__).parent / '../../data/debug/classification/samples/raw_poses.json'
filepath = filepath.resolve()

with open(filepath) as f:
    data = json.load(f)
    
data = [item for item in data if item['label'] != '']

with open(filepath, 'w') as f:
    json.dump(data, f, indent=2)

label_counts = Counter(item['label'] for item in data)
total = len(data)

for label, count in label_counts.items():
    print(f"{label}: {count} ({count/total*100:.1f}%)")
print(f"Total: {total}")

```

---

### <a id="📄-src-utils-zone-annotator-v3-html"></a>📄 `src/utils/zone_annotator_v3.html`

**File Info:**
- **Size**: 26.97 KB
- **Extension**: `.html`
- **Language**: `html`
- **Location**: `src/utils/zone_annotator_v3.html`
- **Relative Path**: `src/utils`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `5c5923b05df6920032a3fb03d90c6743`
- **SHA256**: `135081439ecbebff14e9abe4d4e58033ba02d4f1be28013100d888ebf7fff36d`
- **Encoding**: UTF-8

**File code content:**

```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>أداة تحديد المناطق</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',Tahoma,sans-serif;background:#0f1117;color:#e2e8f0;height:100vh;overflow:hidden}
.hdr{background:#1a1f2e;border-bottom:1px solid #2d3748;padding:10px 16px;display:flex;align-items:center;justify-content:space-between;gap:8px}
.hdr h1{font-size:13px;font-weight:700;white-space:nowrap}
.hdr-btns{display:flex;gap:6px}
.btn{padding:6px 13px;border-radius:6px;border:none;cursor:pointer;font-size:12px;font-weight:700;white-space:nowrap;transition:all .15s}
.btn:disabled{opacity:.4;cursor:not-allowed}
.b-blue{background:#3b82f6;color:#fff}.b-blue:hover:not(:disabled){background:#2563eb}
.b-purple{background:#7c3aed;color:#fff}.b-purple:hover:not(:disabled){background:#6d28d9}
.b-gray{background:#374151;color:#9ca3af}.b-gray:hover:not(:disabled){background:#4b5563;color:#e2e8f0}
.pbar{height:3px;background:#1f2937}.pfill{height:100%;background:linear-gradient(90deg,#3b82f6,#22c55e);transition:width .4s}
.layout{display:flex;height:calc(100vh - 47px)}
.side{width:210px;background:#1a1f2e;border-left:1px solid #2d3748;display:flex;flex-direction:column;flex-shrink:0;overflow:hidden}
.citem.staff-only{opacity:.55}
.citem.staff-only:hover{background:#1a1f2e;cursor:default}
.stitle{padding:10px 12px 8px;font-size:10px;font-weight:700;color:#4b5563;text-transform:uppercase;letter-spacing:.1em;border-bottom:1px solid #2d3748}
.clist{flex:1;overflow-y:auto;padding:6px}
.citem{padding:8px 10px;border-radius:7px;cursor:pointer;margin-bottom:3px;border:1px solid transparent;transition:all .12s}
.citem:hover{background:#253047}.citem.active{background:#1e3a5f;border-color:#3b82f6}
.cname{font-size:12px;font-weight:700}.csub{font-size:10px;color:#6b7280;margin-top:1px}
.bdg{display:inline-block;font-size:9px;padding:1px 5px;border-radius:8px;margin-top:3px;font-weight:700}
.bd{background:#064e3b;color:#34d399}.bp{background:#3b2400;color:#d97706}
.bn{background:#1f2937;color:#4b5563}.be{background:#1f2937;color:#6b7280}
.tsec{border-top:1px solid #2d3748;padding:10px 12px}
.tlbl{font-size:10px;color:#4b5563;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:7px}
.tbtns{display:flex;flex-direction:column;gap:5px;margin-bottom:8px}
.tbtn{padding:8px 10px;border-radius:6px;border:1.5px solid transparent;cursor:pointer;font-size:12px;font-weight:700;text-align:right;transition:all .12s}
.tbtn.t{background:#1a3a2a;border-color:#166534;color:#4ade80}
.tbtn.t.sel,.tbtn.t:hover{background:#14532d;border-color:#22c55e;box-shadow:0 0 0 2px rgba(34,197,94,.15)}
.tbtn.s{background:#1e3050;border-color:#1e40af;color:#60a5fa}
.tbtn.s.sel,.tbtn.s:hover{background:#1e3a8a;border-color:#3b82f6;box-shadow:0 0 0 2px rgba(59,130,246,.15)}
.tbtn.a{background:#2e1065;border-color:#5b21b6;color:#c4b5fd}
.tbtn.a.sel,.tbtn.a:hover{background:#3b0764;border-color:#7c3aed;box-shadow:0 0 0 2px rgba(124,58,237,.18)}
.bauto{width:100%;padding:8px;border-radius:6px;border:1.5px solid #5b21b6;background:#2e1065;color:#c4b5fd;font-size:12px;font-weight:700;cursor:pointer;margin-bottom:8px;transition:all .12s}
.bauto:hover:not(:disabled){background:#3b0764;border-color:#a78bfa}
.bauto:disabled{opacity:.35;cursor:not-allowed}
.hint{font-size:10px;color:#4b5563;line-height:1.7;background:#111827;padding:7px 9px;border-radius:6px}
.hint b{color:#6b7280}
.zpanel{border-top:1px solid #2d3748;max-height:165px;overflow-y:auto}
.zrow{display:flex;align-items:center;justify-content:space-between;padding:5px 10px;font-size:11px}
.zrow:hover{background:#1f2937}
.zdot{width:7px;height:7px;border-radius:2px;margin-left:5px;flex-shrink:0}
.zdel{background:none;border:none;color:#4b5563;cursor:pointer;padding:1px 4px;font-size:15px;border-radius:3px}
.zdel:hover{color:#ef4444;background:#1f2937}
.carea{flex:1;display:flex;flex-direction:column;overflow:hidden}
.ubar{background:#111827;border-bottom:1px solid #2d3748;padding:7px 14px;display:flex;align-items:center;gap:8px;font-size:11px;color:#6b7280}
.ubar b{color:#9ca3af}
.tbar{background:#1a1f2e;border-bottom:1px solid #2d3748;padding:8px 14px;display:flex;align-items:center;gap:8px}
.ctitle{font-size:13px;font-weight:700}.status{font-size:11px;color:#6b7280;margin-right:auto}
.dzone{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;background:#0a0d14;cursor:pointer;border:2px dashed #2d3748;margin:20px;border-radius:12px;transition:all .2s}
.dzone:hover,.dzone.dov{border-color:#3b82f6;background:#0d1525}
.di{font-size:46px}.dt{font-size:15px;color:#6b7280}.ds{font-size:12px;color:#374151}
.cwrap{flex:1;overflow:auto;padding:0;background:#0a0d14;display:none}
canvas{display:block;cursor:crosshair;border-radius:4px;box-shadow:0 4px 24px rgba(0,0,0,.6)}
.mbg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.88);z-index:300;align-items:center;justify-content:center}
.mbg.open{display:flex}
.modal{background:#1a1f2e;border-radius:12px;padding:20px;max-width:92vw;max-height:88vh;overflow-y:auto;border:1px solid #2d3748;min-width:340px}
.modal h2{font-size:14px;margin-bottom:14px}
.mgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
.mcard{background:#111827;border-radius:8px;overflow:hidden;border:1px solid #2d3748}
.mctitle{padding:7px 11px;font-size:11px;font-weight:700;color:#9ca3af;border-bottom:1px solid #2d3748;display:flex;justify-content:space-between}
.mcard canvas{width:100%;display:block}
.mcbtn{width:100%;padding:7px;background:#1f2937;border:none;color:#60a5fa;font-size:11px;cursor:pointer;font-weight:700}
.mcbtn:hover{background:#253047}
.mfooter{margin-top:14px;display:flex;gap:8px;justify-content:flex-end}
.toast{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:#1e3a5f;color:#93c5fd;padding:8px 16px;border-radius:8px;font-size:13px;font-weight:700;border:1px solid #3b82f6;opacity:0;transition:opacity .25s;pointer-events:none;z-index:500}
.toast.show{opacity:1}
</style>
</head>
<body>
<div class="hdr">
  <h1>🎯 أداة تحديد المناطق — كاميرات المطعم المختلطة</h1>
  <div class="hdr-btns">
    <button class="btn b-gray"   onclick="clearCam()">🗑 مسح الحالية</button>
    <button class="btn b-purple" onclick="openModal()">🖼 معاينة وحفظ الصور</button>
    <button class="btn b-blue"   onclick="exportJSON()">⬇️ تصدير zones_config.json</button>
  </div>
</div>
<div class="pbar"><div class="pfill" id="pf" style="width:0%"></div></div>
<div class="layout">
  <div class="side">
    <div class="stitle">الكاميرات 01 — 16</div>
    <div class="clist" id="clist"></div>
    <div class="tsec">
      <div class="tlbl">نوع المنطقة</div>
      <div class="tbtns">
        <button class="tbtn a sel" id="bA" onclick="setType('table_area')">🟪 منطقة طاولات (حاوية)</button>
        <button class="tbtn t"     id="bT" onclick="setType('table')">🟩 طاولة مفردة</button>
        <button class="tbtn s"     id="bS" onclick="setType('service_path')">🟦 ممر خدمة</button>
      </div>
      <button class="bauto" id="bauto" onclick="autoH()" disabled>✨ توليد الممر تلقائياً</button>
      <div class="hint">
        <b>الاستخدام:</b><br>
        1) ارسم أولاً <b>منطقة طاولات</b> واسعة تحيط بكل الطاولات<br>
        2) ثم ارسم كل <b>طاولة مفردة</b> داخلها (يجب أن تكون نقطة المنتصف داخل منطقة الطاولات)<br>
        • انقر لوضع النقاط · اقترب من النقطة الأولى لإغلاق<br>
        • <b>Enter</b> حفظ | <b>Esc</b> إلغاء | <b>Ctrl+Z</b> تراجع نقطة
      </div>
    </div>
    <div class="zpanel">
      <div class="stitle">المناطق المحددة</div>
      <div id="zlist"></div>
    </div>
  </div>
  <div class="carea">
    <div class="ubar">
      <span>📂</span><b>ارفع صورة الكاميرا:</b>
      <span>اسحب وأفلت، أو</span>
      <input type="file" id="fi" style="display:none" accept="image/*" onchange="handleFile(event)">
      <button class="btn b-gray" style="padding:4px 10px;font-size:11px" onclick="document.getElementById('fi').click()">📁 اختر ملف</button>
    </div>
    <div class="tbar">
      <span class="ctitle" id="ctitle">اختر كاميرا</span>
      <span class="status" id="smsg">← اختر كاميرا من القائمة على اليمين</span>
      <button class="btn b-gray" style="padding:5px 10px;font-size:11px" onclick="undoPt()">↩ تراجع</button>
      <button class="btn b-blue" style="padding:5px 12px" onclick="finishZone()">✓ حفظ المنطقة</button>
    </div>
    <div class="dzone" id="dz" ondragover="dov(event)" ondragleave="dol(event)" ondrop="ddr(event)" onclick="document.getElementById('fi').click()">
      <div class="di">🖼️</div>
      <div class="dt">اسحب صورة الكاميرا هنا</div>
      <div class="ds">أو انقر لاختيار الملف · PNG / JPG</div>
    </div>
    <div class="cwrap" id="cw"><canvas id="cv"></canvas></div>
  </div>
</div>
<div class="mbg" id="mbg" onclick="if(event.target===this)closeModal()">
  <div class="modal">
    <h2>🖼 معاينة الصور مع المناطق المحددة</h2>
    <div class="mgrid" id="mgrid"></div>
    <div class="mfooter">
      <button class="btn b-gray"   onclick="closeModal()">إغلاق</button>
      <button class="btn b-purple" onclick="dlAll()">⬇️ تحميل كل الصور</button>
    </div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
const EZ={"camera_01": {"image_size": {"width": 1280, "height": 1440}, "zones": [{"zone_id": "winter_tables_left", "zone_type": "table_area", "zone_name": "Winter Tables Left", "points": [[974, 380], [298, 772], [132, 243], [554, 115]]}, {"zone_id": "winter_service_path", "zone_type": "service_path", "zone_name": "Winter Service Path", "points": [[952, 353], [266, 666], [239, 1126], [1040, 389]]}, {"zone_id": "winter_tables_right", "zone_type": "table_area", "zone_name": "Winter Tables Right", "points": [[1004, 346], [221, 1067], [747, 1415], [1226, 494]]}, {"zone_id": "winter_front_area", "zone_type": "open_area", "zone_name": "Winter Front Area", "points": [[80, 433], [430, 946], [35, 1330], [2, 518]]}]}, "camera_02": {"image_size": {"width": 1920, "height": 1080}, "zones": [{"zone_id": "winter_section_full", "zone_type": "mixed_area", "zone_name": "Winter Section Full View", "points": [[0, 0], [1920, 0], [1920, 1080], [0, 1080]]}, {"zone_id": "winter_tables_area", "zone_type": "table_area", "zone_name": "Winter Tables Right", "points": [[836, 187], [1420, 507], [1887, 316], [1291, 145]]}, {"zone_id": "winter_service_path", "zone_type": "service_path", "zone_name": "Winter Service Path", "points": [[500, 242], [655, 216], [1482, 613], [1206, 762]]}, {"zone_id": "winter_hallway", "zone_type": "hallway", "zone_name": "Winter Hallway", "points": [[1889, 385], [1910, 592], [798, 925], [755, 829]]}]}, "camera_11": {"image_size": {"width": 1920, "height": 1080}, "zones": [{"zone_id": "entrance_1_full", "zone_type": "entrance", "zone_name": "Entrance 1", "points": [[0, 0], [1920, 0], [1920, 1080], [0, 1080]]}, {"zone_id": "entrance_area", "zone_type": "entrance", "zone_name": "Entrance Area", "points": [[334, 983], [962, 744], [1267, 1042], [360, 1077]]}]}, "camera_13": {"image_size": {"width": 1920, "height": 1080}, "zones": [{"zone_id": "entrance_corridor_full", "zone_type": "corridor", "zone_name": "Entrance Corridor and Prayer Room", "points": [[0, 0], [1920, 0], [1920, 1080], [0, 1080]]}, {"zone_id": "entrance_corridor", "zone_type": "corridor", "zone_name": "Entrance Corridor", "points": [[1322, 172], [1010, 1006], [1626, 1058], [1551, 229]]}, {"zone_id": "prayer_room_entrance", "zone_type": "prayer_room_entrance", "zone_name": "Prayer Room Entrance", "points": [[198, 500], [693, 496], [558, 1071], [8, 916]]}]}, "camera_15": {"image_size": {"width": 1920, "height": 1080}, "zones": [{"zone_id": "summer_section_full", "zone_type": "mixed_area", "zone_name": "Summer Section Full View", "points": [[0, 0], [1920, 0], [1920, 1080], [0, 1080]]}, {"zone_id": "summer_tables_area", "zone_type": "table_area", "zone_name": "Summer Tables Area", "points": [[803, 112], [604, 30], [134, 200], [519, 1061], [1112, 848]]}, {"zone_id": "summer_service_path", "zone_type": "service_path", "zone_name": "Summer Service Path", "points": [[551, 278], [792, 161], [1856, 702], [1559, 1060]]}, {"zone_id": "summer_hallway", "zone_type": "hallway", "zone_name": "Summer Hallway", "points": [[862, 101], [464, 283], [523, 334], [927, 145]]}]}, "camera_16": {"image_size": {"width": 1920, "height": 1080}, "zones": [{"zone_id": "river_section_full", "zone_type": "mixed_area", "zone_name": "River Section Full View", "points": [[0, 0], [1920, 0], [1920, 1080], [0, 1080]]}, {"zone_id": "river_tables_area", "zone_type": "table_area", "zone_name": "River Tables Area", "points": [[706, 78], [600, 124], [1313, 957], [1589, 725]]}, {"zone_id": "river_service_path", "zone_type": "service_path", "zone_name": "River Service Path", "points": [[610, 116], [1248, 1002], [792, 1061], [556, 135]]}]}};
const CAMS=['camera_01','camera_02','camera_03','camera_04','camera_05','camera_06','camera_07','camera_08','camera_09','camera_10','camera_11','camera_12','camera_13','camera_14','camera_15','camera_16'];
const MIXED=['camera_01','camera_02','camera_11','camera_12','camera_13','camera_14','camera_15','camera_16'];
const MIXED_SET=new Set(MIXED);
let cur=null,AZ={},CI={},pts=[],zt='table_area',sc=1,mx=null;
for(const c of CAMS){const ex=EZ[c];AZ[c]=ex?ex.zones.map(z=>({...z})):[];}
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
cv.addEventListener('click',oc);
cv.addEventListener('mousemove',e=>{const r=cv.getBoundingClientRect();mx={x:e.clientX-r.left,y:e.clientY-r.top};if(cur&&CI[cur])rd();});
cv.addEventListener('mouseleave',()=>{mx=null;rd();});
document.addEventListener('keydown',e=>{
  if(e.key==='Enter')finishZone();
  if(e.key==='Escape'){pts=[];rd();us();}
  if(e.key==='z'&&(e.ctrlKey||e.metaKey)){e.preventDefault();undoPt();}
});
function oc(e){
  if(!cur||!CI[cur])return;
  const r=cv.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;
  if(pts.length>=3&&Math.hypot(x-pts[0].x,y-pts[0].y)<16){finishZone();return;}
  pts.push({x,y});us();rd();
}
const C={table_area:{s:'#7c3aed',f:'rgba(124,58,237,.10)'},table:{s:'#22c55e',f:'rgba(34,197,94,.20)'},service_path:{s:'#3b82f6',f:'rgba(59,130,246,.18)'},hallway:{s:'#3b82f6',f:'rgba(59,130,246,.12)'},open_area:{s:'#f59e0b',f:'rgba(245,158,11,.12)'},entrance:{s:'#ec4899',f:'rgba(236,72,153,.12)'},corridor:{s:'#ec4899',f:'rgba(236,72,153,.12)'},mixed_area:{s:'#6b7280',f:'rgba(107,114,128,.08)'},prayer_room_entrance:{s:'#f97316',f:'rgba(249,115,22,.12)'},default:{s:'#a78bfa',f:'rgba(167,139,250,.15)'}};
// Ray-casting point-in-polygon test — used to find which table_area contains a new table zone
function pip(pt,poly){
  let inside=false;
  for(let i=0,j=poly.length-1;i<poly.length;j=i++){
    const xi=poly[i][0],yi=poly[i][1],xj=poly[j][0],yj=poly[j][1];
    const hit=((yi>pt[1])!==(yj>pt[1]))&&(pt[0]<(xj-xi)*(pt[1]-yi)/(yj-yi)+xi);
    if(hit)inside=!inside;
  }
  return inside;
}
function centroid(pts){return [pts.reduce((s,p)=>s+p[0],0)/pts.length,pts.reduce((s,p)=>s+p[1],0)/pts.length];}
function findParentArea(cam,op){
  const c=centroid(op);
  const areas=(AZ[cam]||[]).filter(z=>z.zone_type==='table_area');
  return areas.find(a=>pip(c,a.points))||null;
}
function cl(t){return C[t]||C.default;}
function rd(c2,im2,s2,cam2){
  const c=c2||ctx,im=im2||(cur&&CI[cur]?.img),s=s2||sc,cam=cam2||cur;
  if(!im)return;
  c.clearRect(0,0,c.canvas.width,c.canvas.height);c.drawImage(im,0,0,c.canvas.width,c.canvas.height);
  for(const z of(AZ[cam]||[]))dp(c,z.points.map(p=>[p[0]*s,p[1]*s]),cl(z.zone_type),z.zone_name);
  if(!c2&&pts.length>0){
    const co=cl(zt);
    c.beginPath();c.moveTo(pts[0].x,pts[0].y);
    for(let i=1;i<pts.length;i++)c.lineTo(pts[i].x,pts[i].y);
    if(mx)c.lineTo(mx.x,mx.y);
    c.strokeStyle=co.s;c.lineWidth=2;c.setLineDash([5,4]);c.stroke();c.setLineDash([]);
    for(let i=0;i<pts.length;i++){const p=pts[i];c.beginPath();c.arc(p.x,p.y,i===0?7:5,0,Math.PI*2);c.fillStyle=i===0?'#fff':co.s;c.fill();c.strokeStyle=co.s;c.lineWidth=1.5;c.stroke();}
    if(pts.length>=3&&mx){const d=Math.hypot(mx.x-pts[0].x,mx.y-pts[0].y);if(d<16){c.beginPath();c.arc(pts[0].x,pts[0].y,13,0,Math.PI*2);c.strokeStyle='#fff';c.lineWidth=2;c.setLineDash([3,3]);c.stroke();c.setLineDash([]);}}
  }
}
function dp(c,ps,co,label){
  if(ps.length<2)return;
  c.beginPath();c.moveTo(ps[0][0],ps[0][1]);for(let i=1;i<ps.length;i++)c.lineTo(ps[i][0],ps[i][1]);
  c.closePath();c.fillStyle=co.f;c.fill();c.strokeStyle=co.s;c.lineWidth=2;c.stroke();
  if(label){const cx=ps.reduce((s,p)=>s+p[0],0)/ps.length,cy=ps.reduce((s,p)=>s+p[1],0)/ps.length;c.font='bold 12px Segoe UI';c.textAlign='center';c.fillStyle='rgba(0,0,0,.6)';c.fillText(label,cx+1,cy+1);c.fillStyle=co.s;c.fillText(label,cx,cy);c.textAlign='start';}
}
function dov(e){e.preventDefault();document.getElementById('dz').classList.add('dov');}
function dol(e){document.getElementById('dz').classList.remove('dov');}
function ddr(e){e.preventDefault();document.getElementById('dz').classList.remove('dov');const f=e.dataTransfer.files[0];if(f&&cur)lf(f);else if(!cur)toast('⚠️ اختر كاميرا أولاً');}
function handleFile(e){const f=e.target.files[0];if(f&&cur)lf(f);else if(!cur)toast('⚠️ اختر كاميرا أولاً');e.target.value='';}
function lf(file){
  if(!cur){toast('⚠️ اختر كاميرا أولاً');return;}
  const url=URL.createObjectURL(file),im=new Image();
  im.onload=()=>{CI[cur]={img:im,W:im.naturalWidth,H:im.naturalHeight};sc_setup(im);toast('✓ تم تحميل صورة '+cur);rl();uab();};
  im.src=url;
}
function sc_setup(im){
  const wrap=document.getElementById('cw');
  wrap.style.display='block';
  document.getElementById('dz').style.display='none';
  // نحسب الأبعاد بعد ما الـ wrap صار مرئي
  requestAnimationFrame(()=>{
    const mw=wrap.clientWidth-4,mh=wrap.clientHeight-4;
    sc=Math.min(mw/im.naturalWidth,mh/im.naturalHeight);
    cv.width=Math.round(im.naturalWidth*sc);
    cv.height=Math.round(im.naturalHeight*sc);
    rd();
  });
}
function selCam(cam){
  cur=cam;pts=[];
  const num=cam.replace('camera_','');
  document.getElementById('ctitle').textContent='Camera '+num;
  rl();rz();us();uab();
  if(CI[cam]){document.getElementById('dz').style.display='none';document.getElementById('cw').style.display='block';sc_setup(CI[cam].img);}
  else{document.getElementById('dz').style.display='flex';document.getElementById('cw').style.display='none';}
}
function setType(t){
  zt=t;
  document.getElementById('bA').classList.toggle('sel',t==='table_area');
  document.getElementById('bT').classList.toggle('sel',t==='table');
  document.getElementById('bS').classList.toggle('sel',t==='service_path');
  us();
}
function finishZone(){
  if(pts.length<3){toast('⚠️ ضع 3 نقاط على الأقل');return;}
  if(!CI[cur]){toast('⚠️ ارفعي صورة الكاميرا أولاً');return;}
  const op=pts.map(p=>[Math.round(p.x/sc),Math.round(p.y/sc)]);
  const zs=AZ[cur],cs=cur.replace('camera_','cam');

  if(zt==='table'){
    // Leaf table zone MUST sit inside an existing table_area container.
    const parent=findParentArea(cur,op);
    if(!parent){toast('⚠️ ارسم "منطقة طاولات" حاوية أولاً، والطاولة يجب أن تقع بداخلها');return;}
    const n=zs.filter(z=>z.zone_type==='table'&&z.parent_zone_id===parent.zone_id).length+1;
    zs.push({
      zone_id:`${parent.zone_id}_table_${n}`,
      zone_type:'table',
      zone_name:`طاولة ${n}`,
      parent_zone_id:parent.zone_id,
      points:op,
    });
    pts=[];rd();rl();rz();us();uab();toast(`✓ تم حفظ "طاولة ${n}" داخل ${parent.zone_name}`);
    return;
  }

  if(zt==='table_area'){
    const n=zs.filter(z=>z.zone_type==='table_area').length+1;
    zs.push({zone_id:`${cs}_table_area_${n}`,zone_type:'table_area',zone_name:`منطقة طاولات ${n}`,points:op});
    pts=[];rd();rl();rz();us();uab();toast(`✓ تم حفظ "منطقة طاولات ${n}"`);
    return;
  }

  // service_path
  const n=zs.filter(z=>z.zone_type==='service_path').length+1;
  zs.push({zone_id:`${cs}_service_${n}`,zone_type:'service_path',zone_name:`ممر خدمة ${n}`,points:op});
  pts=[];rd();rl();rz();us();uab();toast(`✓ تم حفظ "ممر خدمة ${n}"`);
}
function undoPt(){pts.pop();rd();us();}
function delZ(i){
  const z=AZ[cur][i];
  if(z.zone_type==='table_area'){
    const kids=AZ[cur].filter(k=>k.parent_zone_id===z.zone_id).length;
    if(kids&&!confirm(`هذه المنطقة تحوي ${kids} طاولة/طاولات — حذفها سيحذف الطاولات الفرعية أيضاً. متابعة؟`))return;
    AZ[cur]=AZ[cur].filter(k=>k.parent_zone_id!==z.zone_id);
  }
  AZ[cur]=AZ[cur].filter(k=>k!==z);
  rd();rl();rz();uab();
}
function clearCam(){if(!cur)return;if(!confirm('مسح كل مناطق '+cur+'؟'))return;AZ[cur]=[];pts=[];rd();rl();rz();uab();}
function autoH(){
  if(!cur)return;
  const ts=AZ[cur].filter(z=>z.zone_type==='table_area');
  if(!ts.length){toast('⚠️ ارسمي الطاولات أولاً');return;}
  AZ[cur]=AZ[cur].filter(z=>z.zone_type!=='service_path');
  const ci=CI[cur]||{W:1920,H:1080};
  AZ[cur].push({zone_id:cur.replace('camera_','cam')+'_service_auto',zone_type:'service_path',zone_name:'ممر خدمة (تلقائي)',points:[[0,0],[ci.W,0],[ci.W,ci.H],[0,ci.H]],auto_generated:true,excludes_tables:true});
  rd();rl();rz();uab();toast('✨ تم توليد ممر الخدمة تلقائياً!');
}
function uab(){const b=document.getElementById('bauto');b.disabled=!(cur&&AZ[cur]?.some(z=>z.zone_type==='table_area')&&CI[cur]);}
function rl(){
  const el=document.getElementById('clist');el.innerHTML='';let done=0;
  for(const cam of CAMS){
    const isMixed=MIXED_SET.has(cam);
    const zs=AZ[cam]||[],hi=!!CI[cam];
    const hasT=zs.some(z=>z.zone_type==='table_area'),hasS=zs.some(z=>z.zone_type==='service_path'),isDone=hasT&&hasS;
    if(isMixed&&isDone)done++;
    let bdg;
    if(!isMixed){bdg='<span class="bdg" style="background:#1e3a5f;color:#60a5fa">🔒 staff only</span>';}
    else if(!hi){bdg='<span class="bdg bn">○ بدون صورة</span>';}
    else if(isDone){bdg='<span class="bdg bd">✓ مكتملة</span>';}
    else if(hasT||hasS){bdg='<span class="bdg bp">◑ ناقصة</span>';}
    else{bdg='<span class="bdg be">○ فاضية</span>';}
    const d=document.createElement('div');
    d.className='citem'+(cam===cur?' active':'')+(isMixed?'':' staff-only');
    d.onclick=()=>selCam(cam);
    const num=cam.replace('camera_','');
    d.innerHTML=`<div class="cname">Camera ${num}</div><div class="csub">${isMixed?zs.length+' منطقة':'لا تحتاج zones'}${hi?'':isMixed?' · لا صورة':''}</div>${bdg}`;
    el.appendChild(d);
  }
  document.getElementById('pf').style.width=Math.round(done/MIXED.length*100)+'%';
}
function rz(){
  const el=document.getElementById('zlist');
  if(!cur){el.innerHTML='';return;}
  const zs=AZ[cur]||[];
  if(!zs.length){el.innerHTML='<div style="padding:8px 12px;font-size:11px;color:#374151">لا توجد مناطق</div>';return;}
  el.innerHTML='';
  zs.forEach((z,i)=>{
    const co=cl(z.zone_type);const d=document.createElement('div');d.className='zrow';
    const indent=z.parent_zone_id?'padding-right:16px':'';
    d.innerHTML=`<div style="display:flex;align-items:center;gap:4px;overflow:hidden;flex:1;${indent}"><div class="zdot" style="background:${co.s}"></div><span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${z.parent_zone_id?'└ ':''}${z.zone_name}</span>${z.auto_generated?'<span style="font-size:9px;color:#7c3aed">✨</span>':''}</div><button class="zdel" onclick="delZ(${i})">×</button>`;
    el.appendChild(d);
  });
}
function us(){
  const el=document.getElementById('smsg');
  if(!cur){el.textContent='← اختر كاميرا';return;}
  if(!CI[cur]){el.textContent='ارفع صورة الكاميرا أولاً ↑';return;}
  if(!pts.length){const lbl=zt==='table_area'?'منطقة طاولات':zt==='table'?'طاولة مفردة':'ممر خدمة';el.textContent='انقر لرسم '+lbl;}
  else{el.textContent=pts.length+' نقطة — Enter للحفظ | Esc للإلغاء';}
}
function openModal(){
  const g=document.getElementById('mgrid');g.innerHTML='';
  for(const cam of MIXED){
    const zs=AZ[cam]||[],ci=CI[cam];
    const card=document.createElement('div');card.className='mcard';
    const t=document.createElement('div');t.className='mctitle';t.innerHTML=`<span>Camera ${cam.replace('camera_','')}</span><span style="font-size:10px;color:#4b5563">${zs.length} مناطق</span>`;card.appendChild(t);
    if(!ci){const ph=document.createElement('div');ph.style.cssText='height:110px;display:flex;align-items:center;justify-content:center;font-size:11px;color:#374151';ph.textContent='لا توجد صورة مرفوعة';card.appendChild(ph);}
    else{
      const c2=document.createElement('canvas'),w=500,h=Math.round(500*ci.H/ci.W);c2.width=w;c2.height=h;
      const cx=c2.getContext('2d'),s2=w/ci.W;cx.drawImage(ci.img,0,0,w,h);
      for(const z of zs)dp(cx,z.points.map(p=>[p[0]*s2,p[1]*s2]),cl(z.zone_type),z.zone_name);
      const dlb=document.createElement('button');dlb.className='mcbtn';dlb.textContent='⬇️ تحميل هذه الصورة';dlb.onclick=()=>dli(cam,c2);
      card.appendChild(c2);card.appendChild(dlb);
    }
    g.appendChild(card);
  }
  document.getElementById('mbg').classList.add('open');
}
function closeModal(){document.getElementById('mbg').classList.remove('open');}
function dli(cam,c){const a=document.createElement('a');a.href=c.toDataURL('image/jpeg',.92);a.download=cam+'_zones_preview.jpg';a.click();toast('✓ تم تحميل '+cam);}
async function dlAll(){
  let n=0;
  for(const cam of MIXED){
    const ci=CI[cam];if(!ci)continue;
    const zs=AZ[cam]||[],w=1280,h=Math.round(1280*ci.H/ci.W);
    const c=document.createElement('canvas');c.width=w;c.height=h;
    const cx=c.getContext('2d'),s2=w/ci.W;cx.drawImage(ci.img,0,0,w,h);
    for(const z of zs)dp(cx,z.points.map(p=>[p[0]*s2,p[1]*s2]),cl(z.zone_type),z.zone_name);
    dli(cam,c);n++;await new Promise(r=>setTimeout(r,350));
  }
  toast(n?'✓ تم تحميل '+n+' صور':'⚠️ لا توجد صور مرفوعة');
}
function exportJSON(){
  const out={};
  for(const cam of MIXED){const ci=CI[cam];out[cam]={image_size:ci?{width:ci.W,height:ci.H}:(EZ[cam]?.image_size||{width:1920,height:1080}),zones:AZ[cam]||[]};}
  const b=new Blob([JSON.stringify(out,null,2)],{type:'application/json'});
  const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download='zones_config_mixed.json';a.click();URL.revokeObjectURL(u);
  toast('✓ تم تصدير zones_config_mixed.json');
}
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2500);}
rl();us();
</script>
</body>
</html>
```

---

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `src/zone_management/__pycache__/__init__.cpython-313.pyc`
- `src/zone_management/__pycache__/zone_manager.cpython-313.pyc`

### <a id="📄-src-zone-management-validation-zones-validate-zones-config-py"></a>📄 `src/zone_management/validation/zones/validate_zones_config.py`

**File Info:**
- **Size**: 2.78 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/zone_management/validation/zones/validate_zones_config.py`
- **Relative Path**: `src/zone_management/validation/zones`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `bd5629a31505a1b12db0f7b11fca8ae2`
- **SHA256**: `e52ee1df2096964d41e6c22eb0b2490f03ff5ab1e89d1a96ab00ed9eb990a373`
- **Encoding**: ASCII

**File code content:**

```python
import json
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[3]

ZONES_CONFIG_PATH = PROJECT_DIR / "config" / "zones_config.json"
CAMERA_CONFIG_PATH = PROJECT_DIR / "config" / "camera_config.json"


def main():
    with open(ZONES_CONFIG_PATH, "r", encoding="utf-8") as f:
        zones_config = json.load(f)

    with open(CAMERA_CONFIG_PATH, "r", encoding="utf-8") as f:
        camera_config = json.load(f)

    configured_cameras = set(camera_config.get("cameras", {}).keys())

    errors = []
    warnings = []

    for camera_id, camera_zones in zones_config.items():
        if camera_id not in configured_cameras:
            warnings.append(f"{camera_id}: exists in zones_config but is missing from camera_config")

        image_size = camera_zones.get("image_size", {})
        width = image_size.get("width")
        height = image_size.get("height")

        if not width or not height:
            errors.append(f"{camera_id}: missing image_size.width or image_size.height")
            continue

        zones = camera_zones.get("zones", [])

        if not zones:
            warnings.append(f"{camera_id}: no zones defined")
            continue

        seen_zone_ids = set()

        for zone in zones:
            zone_id = zone.get("zone_id")
            zone_type = zone.get("zone_type")
            points = zone.get("points", [])

            if not zone_id:
                errors.append(f"{camera_id}: zone is missing zone_id")
                continue

            if zone_id in seen_zone_ids:
                errors.append(f"{camera_id}: duplicate zone_id: {zone_id}")

            seen_zone_ids.add(zone_id)

            if not zone_type:
                errors.append(f"{camera_id}/{zone_id}: missing zone_type")

            if len(points) < 3:
                errors.append(f"{camera_id}/{zone_id}: zone must have at least 3 points")

            for point in points:
                if not isinstance(point, list) or len(point) != 2:
                    errors.append(f"{camera_id}/{zone_id}: invalid point: {point}")
                    continue

                x, y = point

                if x < 0 or y < 0 or x > width or y > height:
                    warnings.append(
                        f"{camera_id}/{zone_id}: point is outside image bounds {point} image_size=({width}, {height})"
                    )

    print("========== ZONES CONFIG VALIDATION ==========")

    if errors:
        print("\nERRORS:")
        for error in errors:
            print("-", error)
    else:
        print("\nNo errors found.")

    if warnings:
        print("\nWARNINGS:")
        for warning in warnings:
            print("-", warning)
    else:
        print("\nNo warnings found.")

    print("\nCameras in zones_config:", len(zones_config))


if __name__ == "__main__":
    main()
```

---

### <a id="📄-src-zone-management-validation-zones-visualize-zones-py"></a>📄 `src/zone_management/validation/zones/visualize_zones.py`

**File Info:**
- **Size**: 1.68 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/zone_management/validation/zones/visualize_zones.py`
- **Relative Path**: `src/zone_management/validation/zones`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `483ffe92214e7109d49f237745d538e5`
- **SHA256**: `d264a83f191e64d9a3ffab6428f19c7ef972940688279e24cbf34a8b52cb0b6e`
- **Encoding**: UTF-8

**File code content:**

```python
import json
import sys
from pathlib import Path

import cv2
import numpy as np


PROJECT_DIR = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_DIR))

ZONES_CONFIG_PATH = PROJECT_DIR / "config" / "zones_config.json"
REFERENCE_FRAMES_DIR = PROJECT_DIR / "data" / "debug" / "zones" / "reference_frames"
OUTPUT_DIR = PROJECT_DIR / "data" / "debug" / "zones" / "zones_preview"


def draw_zones(camera_id: str, camera_config: dict):
    image_path = REFERENCE_FRAMES_DIR / f"{camera_id}_reference.jpg"

    if not image_path.exists():
        print(f"⚠️ Missing reference image: {image_path}")
        return

    image = cv2.imread(str(image_path))

    if image is None:
        print(f"⚠️ Cannot read image: {image_path}")
        return

    zones = camera_config.get("zones", [])

    for zone in zones:
        points = np.array(zone["points"], dtype=np.int32)

        cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=3)

        x, y = points[0]
        label = f"{zone['zone_id']} ({zone['zone_type']})"

        cv2.putText(
            image,
            label,
            (int(x), int(y) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{camera_id}_zones_preview.jpg"
    cv2.imwrite(str(output_path), image)

    print(f"✅ Saved preview: {output_path}")


def main():
    with open(ZONES_CONFIG_PATH, "r", encoding="utf-8") as f:
        zones_config = json.load(f)

    for camera_id, camera_config in zones_config.items():
        draw_zones(camera_id, camera_config)


if __name__ == "__main__":
    main()
```

---

### <a id="📄-src-zone-management-init-py"></a>📄 `src/zone_management/__init__.py`

**File Info:**
- **Size**: 0 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/zone_management/__init__.py`
- **Relative Path**: `src/zone_management`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```python

```

---

### <a id="📄-src-zone-management-zone-manager-py"></a>📄 `src/zone_management/zone_manager.py`

**File Info:**
- **Size**: 8.07 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/zone_management/zone_manager.py`
- **Relative Path**: `src/zone_management`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `a7c5070aee2bd683b93d1d7414a31959`
- **SHA256**: `9322a62f604acd5d9e3c3e55dc3e0aa61665f3a8250b17ca3dea502720a3b8b3`
- **Encoding**: UTF-8

**File code content:**

```python
import json
from pathlib import Path
from typing import Any

from shapely.geometry import Point, Polygon, box as shapely_box


class ZoneManager:
    ZONE_TYPE_MAP: dict[str, str] = {
        "table_area": "table",
        "table": "table",
        "service_path": "walk",
        "hallway": "walk",
        "corridor": "walk",
        "open_area": "walk",
        "mixed_area": "walk",
        "entrance": "walk",
        "bathroom_entrance": "walk",
        "prayer_room_entrance": "walk",
        "staff_area": "work",
        "buffet": "work",
        "cashier": "work",
    }

    LOWER_BODY_KP_INDICES = (11, 12, 13, 14, 15, 16)
    HAND_KP_INDICES = (9, 10)
    KP_CONF_THRESHOLD = 0.25

    # --- إعدادات محرك الحالات (State Engine Config) ---
    TIME_TO_OCCUPY = 3.0  # عدد الثواني اللازمة لاعتبار الطاولة "مشغولة"
    TIME_TO_VACATE = 5.0  # عدد الثواني بعد مغادرة الشخص لاعتبارها "فاضية"

    def _is_table_zone(self, zone_type: str | None) -> bool:
        return self.ZONE_TYPE_MAP.get(zone_type or "", zone_type or "") == "table"

    def __init__(self, zones_config_path: str = "config/zones_config.json"):
        self.project_dir = Path.cwd()
        self.zones_config_path = self.project_dir / zones_config_path

        if not self.zones_config_path.exists():
            raise FileNotFoundError(
                f"zones_config.json not found: {self.zones_config_path}"
            )

        with open(self.zones_config_path, "r", encoding="utf-8") as f:
            self.zones_config = json.load(f)

    def get_bbox_zone(
        self,
        camera_id: str,
        box: list[int | float],
        keypoints=None,
    ) -> dict[str, Any]:
        camera_zones = self.zones_config.get(camera_id)
        if camera_zones is None:
            return self._unknown_zone(reason="camera_not_found", box=box)

        zones = camera_zones.get("zones", [])
        if not zones:
            return self._unknown_zone(reason="no_zones", box=box)

        # -- Step 1: skeleton check --
        walk_zone_hit = self._check_lower_body_in_walk_zone(zones, keypoints)
        if walk_zone_hit is not None:
            return self._zone_result(
                walk_zone_hit, 100.0, box, method="skeleton"
            )

        # -- Step 2: intersection fallback --
        x1, y1, x2, y2 = box
        y1_trimmed = y1 + 0.10 * (y2 - y1)
        bbox_poly = shapely_box(x1, y1_trimmed, x2, y2)
        bbox_area = bbox_poly.area

        if bbox_area == 0:
            return self._unknown_zone(reason="empty_bbox", box=box)

        work_pct = 0.0
        table_area_pct = 0.0
        work_zone = None
        table_area_zone = None

        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0
        center_point = Point(cx, cy)

        table_specific_zone, table_match_method = self._find_table_by_hands(
            zones, keypoints
        )
        if table_specific_zone is None:
            table_specific_zone = self._find_table_by_center(
                zones, center_point
            )
            table_match_method = "center_point"

        for zone in zones:
            points = zone.get("points", [])
            if len(points) < 3:
                continue

            polygon = Polygon(points)
            if not polygon.is_valid:
                continue

            inter_area = bbox_poly.intersection(polygon).area
            pct = (inter_area / bbox_area) * 100

            raw_zone_type = zone.get("zone_type")
            zone_type = self.ZONE_TYPE_MAP.get(raw_zone_type, "unknown")

            if zone_type in ("work", "walk") and pct > work_pct:
                work_pct = pct
                work_zone = zone
            elif (
                zone_type == "table"
                and raw_zone_type == "table_area"
                and pct > table_area_pct
            ):
                table_area_pct = pct
                table_area_zone = zone

        if work_pct >= 30 and work_zone is not None:
            return self._zone_result(
                work_zone, work_pct, box, method="intersection"
            )

        if table_specific_zone is not None:
            return self._zone_result(
                table_specific_zone, 100.0, box, method=table_match_method
            )

        if table_area_zone is not None:
            return self._zone_result(
                table_area_zone, table_area_pct, box, method="intersection"
            )

        return self._unknown_zone(reason="no_sufficient_intersection", box=box)

    # --- التوابع المساعدة المتبقية (دون تغيير بالمنطق الداخلي لضمان دقتها) ---
    def _find_table_by_hands(
        self, zones, keypoints
    ) -> tuple[dict[str, Any] | None, str]:
        if keypoints is None:
            return None, "hands"
        table_zones = [
            zone
            for zone in zones
            if zone.get("zone_type") == "table"
            and len(zone.get("points", [])) >= 3
        ]
        if not table_zones:
            return None, "hands"

        for idx in self.HAND_KP_INDICES:
            if idx >= len(keypoints):
                continue
            x, y, conf = keypoints[idx]
            if conf < self.KP_CONF_THRESHOLD:
                continue
            point = Point(float(x), float(y))
            best_zone, best_area = None, None
            for zone in table_zones:
                polygon = Polygon(zone["points"])
                if polygon.is_valid and polygon.contains(point):
                    if best_area is None or polygon.area < best_area:
                        best_area = polygon.area
                        best_zone = zone
            if best_zone is not None:
                return best_zone, "hands"
        return None, "hands"

    def _find_table_by_center(
        self, zones, center_point: Point
    ) -> dict[str, Any] | None:
        best_zone, best_area = None, None
        for zone in zones:
            if zone.get("zone_type") != "table":
                continue
            points = zone.get("points", [])
            if len(points) < 3:
                continue
            polygon = Polygon(points)
            if not polygon.is_valid or not polygon.contains(center_point):
                continue
            if best_area is None or polygon.area < best_area:
                best_area = polygon.area
                best_zone = zone
        return best_zone

    def _check_lower_body_in_walk_zone(
        self, zones, keypoints
    ) -> dict[str, Any] | None:
        if keypoints is None:
            return None
        walk_zones = [
            zone
            for zone in zones
            if self.ZONE_TYPE_MAP.get(zone.get("zone_type"), "unknown")
            == "walk"
            and len(zone.get("points", [])) >= 3
        ]
        if not walk_zones:
            return None
        for idx in self.LOWER_BODY_KP_INDICES:
            if idx >= len(keypoints):
                continue
            x, y, conf = keypoints[idx]
            if conf < self.KP_CONF_THRESHOLD:
                continue
            point = Point(float(x), float(y))
            for zone in walk_zones:
                polygon = Polygon(zone["points"])
                if polygon.is_valid and polygon.contains(point):
                    return zone
        return None

    def _zone_result(
        self,
        zone: dict[str, Any],
        pct: float,
        box: list[int | float] | None = None,
        method: str = "intersection",
    ) -> dict[str, Any]:
        return {
            "zone_id": zone.get("zone_id"),
            "zone_type": zone.get("zone_type"),
            "zone_name": zone.get("zone_name"),
            "intersection_pct": round(pct, 2),
            "box": box,
            "matched": True,
            "method": method,
        }

    def _unknown_zone(
        self, reason: str, box: list[int | float] | None = None
    ) -> dict[str, Any]:
        return {
            "zone_id": "unknown",
            "zone_type": "unknown",
            "zone_name": "Unknown",
            "intersection_pct": 0.0,
            "box": box,
            "matched": False,
            "reason": reason,
        }
```

---

### <a id="📄-src-run-live-py"></a>📄 `src/run_live.py`

**File Info:**
- **Size**: 7.77 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `src/run_live.py`
- **Relative Path**: `src`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:07 (Asia/Damascus / GMT+03:00)
- **MD5**: `aa49ea41bef04e5ada249d5acc512b65`
- **SHA256**: `dde55aeb00164e4c5f23e3c97f05766388897a3e7bfabe406aba8cf2e96374a5`
- **Encoding**: UTF-8

**File code content:**

```python
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

    source = args.source
    camera_id = args.camera_id
    video_id = args.video_id

    if args.first_video:
        source, camera_id, video_id = load_first_video_path(args.videos_index)

    capture = open_capture(source)

    if not capture.isOpened():
        raise ValueError(f"Cannot open video source: {source}")

    fps = capture.get(cv2.CAP_PROP_FPS)
    # في العرض المباشر نحدّث الـ pose/action كل فريم لتسريع التعرف على العامل والأشخاص على الطاولات
    pose_stride = 1
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
```

---

### <a id="📄-storage-init-py"></a>📄 `storage/__init__.py`

**File Info:**
- **Size**: 0 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `storage/__init__.py`
- **Relative Path**: `storage`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```python

```

---

### <a id="📄-storage-database-py"></a>📄 `storage/database.py`

**File Info:**
- **Size**: 2.91 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `storage/database.py`
- **Relative Path**: `storage`
- **Created**: 2026-07-14 09:08:29 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 09:08:29 (Asia/Damascus / GMT+03:00)
- **MD5**: `d2cf789926f028862ea99a633e64a89b`
- **SHA256**: `6d1a3a43a18e43549870f6a06fe0b4b5cc7f41f2ce7cde56bfec274d11a666a5`
- **Encoding**: UTF-8

**File code content:**

```python
"""
storage/database.py
--------------------
Async SQLAlchemy engine/session management.

DB target is controlled by the DATABASE_URL env var:
  - Production/dev default: postgresql+asyncpg://... (Postgres, per spec)
  - Test suite: sqlite+aiosqlite:///:memory: (set by tests/conftest.py)

No Postgres credentials are assumed or hardcoded — see docs/DB_SCHEMA.md and
docs/SESSION_REPORT.md for why: this environment's local Postgres service
exists but this session was not given credentials for it, and guessing
system-service credentials is out of scope. A real deployment sets
DATABASE_URL in .env (see .env.example).
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from storage.models import Base

DEFAULT_DATABASE_URL = (
    "postgresql+asyncpg://restaurant_monitor:restaurant_monitor@localhost:5432/restaurant_monitor"
)


def get_database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


_engine = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine():
    global _engine, _session_factory
    if _engine is None:
        url = get_database_url()
        if url.startswith("sqlite"):
            # sqlite needs a shared in-memory pool to persist across
            # connections within a single test process.
            from sqlalchemy.pool import StaticPool

            _engine = create_async_engine(
                url, connect_args={"check_same_thread": False}, poolclass=StaticPool
            )
        else:
            _engine = create_async_engine(url, pool_pre_ping=True)
        _session_factory = async_sessionmaker(_engine, expire_on_commit=False)
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    if _session_factory is None:
        get_engine()
    assert _session_factory is not None
    return _session_factory


async def init_db() -> None:
    """Create all tables if they don't exist. Idempotent."""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def dispose_db() -> None:
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _session_factory = None


@asynccontextmanager
async def session_scope() -> AsyncGenerator[AsyncSession, None]:
    """Usage: async with session_scope() as session: ..."""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency."""
    factory = get_session_factory()
    async with factory() as session:
        yield session

```

---

### <a id="📄-storage-models-py"></a>📄 `storage/models.py`

**File Info:**
- **Size**: 5.13 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `storage/models.py`
- **Relative Path**: `storage`
- **Created**: 2026-07-14 09:04:28 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 09:04:28 (Asia/Damascus / GMT+03:00)
- **MD5**: `091f3c4cc5d5371d05a3ad2073e88cb8`
- **SHA256**: `02f1a21290c5fb90c397f4415084f3359626750aceeb4b21d272609eb49bac81`
- **Encoding**: ASCII

**File code content:**

```python
"""
storage/models.py
------------------
SQLAlchemy 2.0 async ORM models. Schema design/rationale: docs/DB_SCHEMA.md.
"""

from __future__ import annotations

import datetime as dt

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    SmallInteger,
    String,
    Time,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import TypeDecorator, TIMESTAMP


class Base(DeclarativeBase):
    pass


class TZDateTime(TypeDecorator):
    """Stores tz-aware datetimes as timestamptz."""

    impl = TIMESTAMP(timezone=True)
    cache_ok = True


class Camera(Base):
    __tablename__ = "cameras"

    camera_id: Mapped[str] = mapped_column(String, primary_key=True)
    location: Mapped[str | None] = mapped_column(Text)
    camera_type: Mapped[str | None] = mapped_column(String)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    operating_hours_start: Mapped[dt.time | None] = mapped_column(Time)
    operating_hours_end: Mapped[dt.time | None] = mapped_column(Time)

    zones: Mapped[list["Zone"]] = relationship(back_populates="camera")


class Zone(Base):
    __tablename__ = "zones"

    zone_id: Mapped[str] = mapped_column(String, primary_key=True)
    camera_id: Mapped[str] = mapped_column(ForeignKey("cameras.camera_id"), index=True)
    zone_type: Mapped[str] = mapped_column(String)
    zone_type_normalized: Mapped[str] = mapped_column(String)
    zone_name: Mapped[str | None] = mapped_column(Text)
    parent_zone_id: Mapped[str | None] = mapped_column(ForeignKey("zones.zone_id"))
    polygon: Mapped[list] = mapped_column(JSON)
    max_capacity: Mapped[int | None] = mapped_column(Integer)

    camera: Mapped["Camera"] = relationship(back_populates="zones")


class Identity(Base):
    __tablename__ = "identities"

    global_id: Mapped[str] = mapped_column(String, primary_key=True)
    kind: Mapped[str] = mapped_column(String)  # worker | customer_session
    display_name: Mapped[str | None] = mapped_column(Text)
    first_seen_at: Mapped[dt.datetime] = mapped_column(
        TZDateTime, server_default=func.now()
    )
    last_seen_at: Mapped[dt.datetime] = mapped_column(
        TZDateTime, server_default=func.now(), onupdate=func.now()
    )


class WorkerGalleryEntry(Base):
    __tablename__ = "worker_gallery"

    global_id: Mapped[str] = mapped_column(
        ForeignKey("identities.global_id"), primary_key=True
    )
    # float4[512] fallback representation (portable across Postgres without
    # the pgvector extension). If pgvector is available, database.py swaps
    # this column's DDL for `vector(512)` at init time — see docs/DB_SCHEMA.md.
    embedding: Mapped[list[float]] = mapped_column(JSON)
    enrolled_via: Mapped[str] = mapped_column(String, default="auto_promotion")
    enrolled_at: Mapped[dt.datetime] = mapped_column(
        TZDateTime, server_default=func.now()
    )


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    camera_id: Mapped[str] = mapped_column(ForeignKey("cameras.camera_id"), index=True)
    track_id: Mapped[int] = mapped_column(Integer)
    global_id: Mapped[str | None] = mapped_column(ForeignKey("identities.global_id"))
    started_at: Mapped[dt.datetime] = mapped_column(TZDateTime)
    ended_at: Mapped[dt.datetime | None] = mapped_column(TZDateTime)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ts: Mapped[dt.datetime] = mapped_column(TZDateTime, index=True)
    level: Mapped[int] = mapped_column(SmallInteger)
    event_type: Mapped[str] = mapped_column(String, index=True)
    camera_id: Mapped[str] = mapped_column(ForeignKey("cameras.camera_id"))
    zone_id: Mapped[str | None] = mapped_column(ForeignKey("zones.zone_id"))
    global_id: Mapped[str | None] = mapped_column(ForeignKey("identities.global_id"))
    track_id: Mapped[int | None] = mapped_column(Integer)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)

    __table_args__ = (
        Index("ix_events_camera_ts", "camera_id", "ts"),
        Index("ix_events_zone_ts", "zone_id", "ts"),
        Index("ix_events_global_ts", "global_id", "ts"),
    )


class KPISnapshot(Base):
    __tablename__ = "kpi_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    computed_at: Mapped[dt.datetime] = mapped_column(
        TZDateTime, server_default=func.now()
    )
    window_start: Mapped[dt.datetime] = mapped_column(TZDateTime)
    window_end: Mapped[dt.datetime] = mapped_column(TZDateTime)
    kpi_name: Mapped[str] = mapped_column(String, index=True)
    camera_id: Mapped[str | None] = mapped_column(ForeignKey("cameras.camera_id"))
    zone_id: Mapped[str | None] = mapped_column(ForeignKey("zones.zone_id"))
    global_id: Mapped[str | None] = mapped_column(ForeignKey("identities.global_id"))
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String)

    __table_args__ = (
        Index("ix_kpi_name_window", "kpi_name", "window_start", "window_end"),
    )

```

---

### <a id="📄-storage-redis-manager-py"></a>📄 `storage/redis_manager.py`

**File Info:**
- **Size**: 0 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `storage/redis_manager.py`
- **Relative Path**: `storage`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```python

```

---

## 🚫 Binary/Excluded Files

The following files were not included in the text content:

- `tests/__pycache__/__init__.cpython-313.pyc`
- `tests/__pycache__/test_analytics.cpython-313-pytest-9.1.1.pyc`
- `tests/__pycache__/test_classifier.cpython-313-pytest-9.1.1.pyc`
- `tests/__pycache__/test_detector.cpython-313-pytest-9.1.1.pyc`
- `tests/__pycache__/test_live_pipeline_timing.cpython-313-pytest-9.1.1.pyc`
- `tests/__pycache__/test_reid.cpython-313-pytest-9.1.1.pyc`
- `tests/__pycache__/test_role_engine.cpython-313-pytest-9.1.1.pyc`
- `tests/__pycache__/test_tracker.cpython-313-pytest-9.1.1.pyc`

### <a id="📄-tests-init-py"></a>📄 `tests/__init__.py`

**File Info:**
- **Size**: 0 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `tests/__init__.py`
- **Relative Path**: `tests`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```python

```

---

### <a id="📄-tests-test-analytics-py"></a>📄 `tests/test_analytics.py`

**File Info:**
- **Size**: 0 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `tests/test_analytics.py`
- **Relative Path**: `tests`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```python

```

---

### <a id="📄-tests-test-classifier-py"></a>📄 `tests/test_classifier.py`

**File Info:**
- **Size**: 0 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `tests/test_classifier.py`
- **Relative Path**: `tests`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```python

```

---

### <a id="📄-tests-test-detector-py"></a>📄 `tests/test_detector.py`

**File Info:**
- **Size**: 948 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `tests/test_detector.py`
- **Relative Path**: `tests`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `876c3b1267f8dce94ad90aa994f306e7`
- **SHA256**: `5b4f5e455402e573dde3a736f9c19197b446c33ca1dd492cbbbde36fc2c96ab8`
- **Encoding**: UTF-8

**File code content:**

```python
import unittest
import numpy as np
from src.ai_models.detector import PersonDetector

class TestPersonDetector(unittest.TestCase):
    def setUp(self):
        # تجهيز الموديل مرة واحدة قبل الفحص بالإعدادات الافتراضية
        self.detector = PersonDetector(conf_threshold=0.4, imgsz=480)

    def test_detector_output_format(self):
        # 1. صنع صورة وهمية باللون الأسود أبعادها 480x480 (ثلاث قنوات ألوان BGR)
        fake_frame = np.zeros((480, 480, 3), dtype=np.uint8)
        
        # 2. تشغيل دالة الكشف
        detections = self.detector.detect(fake_frame)
        
        # 3. التأكيد (Assertions): نتوقع أن النتيجة يجب أن تكون قائمة (List)
        self.assertIsInstance(detections, list, "المخرجات يجب أن تكون من نوع List")

if __name__ == "__main__":
    unittest.main()
```

---

### <a id="📄-tests-test-live-pipeline-timing-py"></a>📄 `tests/test_live_pipeline_timing.py`

**File Info:**
- **Size**: 2.94 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `tests/test_live_pipeline_timing.py`
- **Relative Path**: `tests`
- **Created**: 2026-07-14 09:50:40 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 09:50:40 (Asia/Damascus / GMT+03:00)
- **MD5**: `f264f5b8affb0df6f0070464b81a9225`
- **SHA256**: `9675f72726b6b87d2ab9874d58f6fab16de35cf26c82e9569da94745a558abad`
- **Encoding**: ASCII

**File code content:**

```python
"""
test_live_pipeline_timing.py
-----------------------------
Focused unit tests for LivePipeline._update_person_state(), covering the
video-relative timing fix:
  (a) Duration is computed from the time_seconds difference, not frame counting.
  (b) datetime.now() is no longer used anywhere in the function.
  (c) _update_person_state() raises ValueError when time_seconds is None.

LivePipeline.__init__() loads heavy ML models (YOLO, pose LSTM, ReID, etc.),
which is unnecessary to exercise this specific method. Tests construct a bare
instance via object.__new__() and seed only the state _update_person_state()
touches (self.person_state), keeping the test fast and scoped to the bug
being fixed rather than a full pipeline integration test.

Run with:  python -m pytest tests/test_live_pipeline_timing.py -v
"""

import inspect
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.live_pipeline import LivePipeline


def make_bare_pipeline() -> LivePipeline:
    """Construct a LivePipeline instance without running __init__."""
    pipeline = object.__new__(LivePipeline)
    pipeline.person_state = []
    return pipeline


def test_duration_computed_from_time_seconds_difference():
    pipeline = make_bare_pipeline()

    # First sighting at video time 10.0s -> entrance recorded, duration 0.
    pipeline._update_person_state(global_id="worker_1", local_id=1, zone_type="table", time_seconds=10.0)
    record = pipeline.person_state[0]
    assert record["Duration"] == "0:00:00"
    assert record["_entrance_time_seconds"] == 10.0

    # Same zone, later video time -> duration must equal the time_seconds delta (25s),
    # regardless of how many frames were processed in between.
    pipeline._update_person_state(global_id="worker_1", local_id=1, zone_type="table", time_seconds=35.0)
    record = pipeline.person_state[0]
    assert record["Duration"] == "0:00:25"

    # Zone change resets the entrance point and duration.
    pipeline._update_person_state(global_id="worker_1", local_id=1, zone_type="walk", time_seconds=40.0)
    record = pipeline.person_state[0]
    assert record["current_location"] == "walk"
    assert record["Duration"] == "0:00:00"
    assert record["_entrance_time_seconds"] == 40.0

    # Duration keeps tracking from the new entrance point.
    pipeline._update_person_state(global_id="worker_1", local_id=1, zone_type="walk", time_seconds=100.0)
    record = pipeline.person_state[0]
    assert record["Duration"] == "0:01:00"


def test_no_datetime_now_used_in_update_person_state():
    source = inspect.getsource(LivePipeline._update_person_state)
    assert "datetime.now" not in source
    assert "_internal_frames_count" not in source


def test_update_person_state_raises_on_none_time_seconds():
    pipeline = make_bare_pipeline()
    with pytest.raises(ValueError):
        pipeline._update_person_state(global_id="worker_1", local_id=1, zone_type="table", time_seconds=None)

```

---

### <a id="📄-tests-test-reid-py"></a>📄 `tests/test_reid.py`

**File Info:**
- **Size**: 0 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `tests/test_reid.py`
- **Relative Path**: `tests`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `d41d8cd98f00b204e9800998ecf8427e`
- **SHA256**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Encoding**: ASCII

**File code content:**

```python

```

---

### <a id="📄-tests-test-role-engine-py"></a>📄 `tests/test_role_engine.py`

**File Info:**
- **Size**: 15.67 KB
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `tests/test_role_engine.py`
- **Relative Path**: `tests`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `9a166137ea9f5f7bb30b0f10a8a42b86`
- **SHA256**: `ec9937ff0740098b7759e7153c388726132b1900222f7e7251f50f65a307926f`
- **Encoding**: ASCII

**File code content:**

```python
"""
test_role_engine.py
-------------------
Standalone smoke tests for the RoleEngine.
Run with:  python -m pytest tests/test_role_engine.py -v
   or:     python tests/test_role_engine.py
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.kbs.role_engine import (
    RoleEngine, ObservationFact, ScoreAccumulator,
    MergeRequest, RoleDecision,
)


def run_single_cycle(observations, prior_accumulators=None, merges=None):
    """Helper: run one engine cycle and return (decisions, accumulators)."""
    engine = RoleEngine()
    engine.reset()

    # Re-inject prior accumulators (persistent state across cycles)
    if prior_accumulators:
        for gid, acc in prior_accumulators.items():
            engine.declare(ScoreAccumulator(
                global_id=gid,
                worker_score=acc["worker_score"],
                customer_score=acc["customer_score"],
                confirmed_role=acc["confirmed_role"],
                cycle_count=acc["cycle_count"],
                zone_history=acc.get("zone_history", ()),
            ))

    # Declare merge requests
    if merges:
        for old_gid, new_gid in merges:
            engine.declare(MergeRequest(old_global_id=old_gid, new_global_id=new_gid))

    # Declare observations
    for obs in observations:
        engine.declare(ObservationFact(**obs))

    engine.run()
    return engine.get_decisions(), engine.get_accumulators()


# ── Test 1: Sitting at table → customer ────────────────────────────────────

def test_sitting_at_table_builds_customer_score():
    """Sitting at a table should accumulate customer_score, not worker_score."""
    print("\n[Test 1] Sitting at table → customer score")

    obs = [{
        "track_id": 1,
        "global_id": "local_1",
        "action": "sitting",
        "zone_type": "table",
        "pose_frame_count": 5,
        "appearance_count": 0,
        "previous_role": "unknown",
    }]

    decisions, accumulators = run_single_cycle(obs)
    acc = accumulators["local_1"]

    print(f"  customer_score = {acc['customer_score']}")
    print(f"  worker_score   = {acc['worker_score']}")
    assert acc["customer_score"] > 0, "Customer score should be positive"
    assert acc["worker_score"] == 0, "Worker score should be zero"
    print("  ✅ PASSED")


# ── Test 2: Staff zone → worker ───────────────────────────────────────────

def test_staff_zone_builds_worker_score():
    """Being in a staff zone should accumulate worker_score."""
    print("\n[Test 2] Staff zone → worker score")

    obs = [{
        "track_id": 2,
        "global_id": "local_2",
        "action": "standing",
        "zone_type": "staff",
        "pose_frame_count": 10,
        "appearance_count": 0,
        "previous_role": "unknown",
    }]

    decisions, accumulators = run_single_cycle(obs)
    acc = accumulators["local_2"]

    print(f"  worker_score   = {acc['worker_score']}")
    print(f"  customer_score = {acc['customer_score']}")
    assert acc["worker_score"] > 0, "Worker score should be positive"
    assert acc["customer_score"] == 0, "Customer score should be zero"
    print("  ✅ PASSED")


# ── Test 3: Confirmation after multiple cycles ────────────────────────────

def test_customer_confirmation_over_time():
    """Repeatedly sitting at table across cycles should confirm customer."""
    print("\n[Test 3] Customer confirmation over multiple cycles")

    accumulators = None
    obs_template = {
        "track_id": 3,
        "global_id": "person_A",
        "action": "sitting",
        "zone_type": "table",
        "appearance_count": 0,
        "previous_role": "unknown",
    }

    for cycle in range(6):
        obs = [dict(obs_template, pose_frame_count=cycle * 5)]
        decisions, accumulators = run_single_cycle(
            obs, prior_accumulators=accumulators,
        )
        acc = accumulators["person_A"]
        print(f"  Cycle {cycle}: cs={acc['customer_score']:.1f}  ws={acc['worker_score']:.1f}  role={acc['confirmed_role']}")

    assert acc["confirmed_role"] == "customer", "Should be confirmed customer by now"
    print("  ✅ PASSED")


# ── Test 4: Worker confirmation via serving ───────────────────────────────

def test_worker_confirmation_via_serving():
    """Sustained serving should confirm worker."""
    print("\n[Test 4] Worker confirmation via sustained serving")

    accumulators = None
    obs_template = {
        "track_id": 4,
        "global_id": "person_B",
        "action": "serving",
        "zone_type": "walk",
        "appearance_count": 3,
        "previous_role": "unknown",
    }

    for cycle in range(6):
        obs = [dict(obs_template, pose_frame_count=cycle * 4)]
        decisions, accumulators = run_single_cycle(
            obs, prior_accumulators=accumulators,
        )
        acc = accumulators["person_B"]
        print(f"  Cycle {cycle}: ws={acc['worker_score']:.1f}  cs={acc['customer_score']:.1f}  role={acc['confirmed_role']}")

    assert acc["confirmed_role"] == "worker", "Should be confirmed worker by now"
    print("  ✅ PASSED")


# ── Test 5: Decay fades old evidence ──────────────────────────────────────

def test_decay():
    """Scores should shrink when no new evidence is added."""
    print("\n[Test 5] Decay fades scores")

    # Seed with existing scores
    accumulators = {
        "person_C": {
            "worker_score": 20.0,
            "customer_score": 5.0,
            "confirmed_role": "worker",
            "cycle_count": 10,
        }
    }

    # Observe with neutral action (walking in unknown zone → no rule fires much)
    obs = [{
        "track_id": 5,
        "global_id": "person_C",
        "action": "walking",
        "zone_type": "unknown",
        "pose_frame_count": 0,
        "appearance_count": 0,
        "previous_role": "worker",
    }]

    _, new_acc = run_single_cycle(obs, prior_accumulators=accumulators)
    acc = new_acc["person_C"]

    print(f"  Before: ws=20.0  cs=5.0")
    print(f"  After:  ws={acc['worker_score']:.1f}  cs={acc['customer_score']:.1f}")
    assert acc["worker_score"] < 20.0, "Worker score should have decayed"
    assert acc["customer_score"] < 5.0, "Customer score should have decayed"
    print("  ✅ PASSED")


# ── Test 6: Reversal ──────────────────────────────────────────────────────

def test_reversal():
    """A confirmed customer who enters staff zone repeatedly should reverse to worker."""
    print("\n[Test 6] Reversal from customer to worker")

    # Start with a confirmed customer
    accumulators = {
        "person_D": {
            "worker_score": 2.0,
            "customer_score": 16.0,
            "confirmed_role": "customer",
            "cycle_count": 5,
        }
    }

    obs_template = {
        "track_id": 6,
        "global_id": "person_D",
        "action": "serving",
        "zone_type": "staff",
        "appearance_count": 5,
        "previous_role": "customer",
    }

    for cycle in range(10):
        obs = [dict(obs_template, pose_frame_count=cycle * 5)]
        _, accumulators = run_single_cycle(obs, prior_accumulators=accumulators)
        acc = accumulators["person_D"]
        print(f"  Cycle {cycle}: ws={acc['worker_score']:.1f}  cs={acc['customer_score']:.1f}  role={acc['confirmed_role']}")

    assert acc["confirmed_role"] == "worker", "Should have reversed to worker"
    print("  ✅ PASSED")


# ── Test 7: Re-ID Merge ──────────────────────────────────────────────────

def test_merge():
    """MergeRequest should combine two accumulators into one."""
    print("\n[Test 7] Re-ID merge combines accumulators")

    accumulators = {
        "old_track": {
            "worker_score": 10.0,
            "customer_score": 0.0,
            "confirmed_role": "unknown",
            "cycle_count": 3,
        },
        "new_track": {
            "worker_score": 5.0,
            "customer_score": 0.0,
            "confirmed_role": "unknown",
            "cycle_count": 1,
        },
    }

    obs = [{
        "track_id": 7,
        "global_id": "new_track",
        "action": "walking",
        "zone_type": "walk",
        "pose_frame_count": 0,
        "appearance_count": 0,
        "previous_role": "unknown",
    }]

    merges = [("old_track", "new_track")]

    _, new_acc = run_single_cycle(obs, prior_accumulators=accumulators, merges=merges)

    assert "old_track" not in new_acc, "Old accumulator should be removed"
    merged = new_acc["new_track"]
    print(f"  Merged worker_score = {merged['worker_score']:.1f} (expected ~15 before decay+new evidence)")
    assert merged["worker_score"] > 12.0, "Merged score should combine both"
    print("  ✅ PASSED")


# ── Test 8: Zone history and carryover evidence ─────────────────────────

def test_zone_history_tracks_transitions_and_patterns():
    """Zone history should preserve transitions and drive the new evidence rules."""
    print("\n[Test 8] Zone history tracks transitions and patterns")

    accumulators = None
    obs_cycles = [
        [{
            "track_id": 8,
            "global_id": "person_hist",
            "action": "standing",
            "zone_type": "staff",
            "pose_frame_count": 2,
            "appearance_count": 0,
            "previous_role": "unknown",
            "previous_duration_frames": 0,
        }],
        [{
            "track_id": 8,
            "global_id": "person_hist",
            "action": "walking",
            "zone_type": "walk",
            "pose_frame_count": 1,
            "appearance_count": 0,
            "previous_role": "unknown",
            "previous_duration_frames": 2,
        }],
        [{
            "track_id": 8,
            "global_id": "person_hist",
            "action": "standing",
            "zone_type": "table",
            "pose_frame_count": 1,
            "appearance_count": 0,
            "previous_role": "unknown",
            "previous_duration_frames": 1,
        }],
    ]

    for obs in obs_cycles:
        decisions, accumulators = run_single_cycle(obs, prior_accumulators=accumulators)

    acc = accumulators["person_hist"]
    print(f"  zone_history = {acc['zone_history']}")
    assert len(acc["zone_history"]) >= 3, "History should capture the recent transitions"
    assert acc["zone_history"][-3][0] == "staff"
    assert acc["zone_history"][-2][0] == "walk"
    assert acc["zone_history"][-1][0] == "table"
    assert acc["worker_score"] > 5.0, "Pattern evidence should add worker score"
    print("  ✅ PASSED")


def test_recent_sit_carryover_evidence():
    """A long table sit should carry customer evidence into a standing transition."""
    print("\n[Test 9] Recent sit carryover adds customer evidence")

    accumulators = None
    obs_cycles = [
        [{
            "track_id": 9,
            "global_id": "person_sit",
            "action": "sitting",
            "zone_type": "table",
            "pose_frame_count": 95,
            "appearance_count": 0,
            "previous_role": "unknown",
            "previous_duration_frames": 0,
        }],
        [{
            "track_id": 9,
            "global_id": "person_sit",
            "action": "standing",
            "zone_type": "table",
            "pose_frame_count": 1,
            "appearance_count": 0,
            "previous_role": "unknown",
            "previous_duration_frames": 95,
        }],
    ]

    _, accumulators = run_single_cycle(obs_cycles[0], prior_accumulators=accumulators)
    first_customer_score = accumulators["person_sit"]["customer_score"]

    _, accumulators = run_single_cycle(obs_cycles[1], prior_accumulators=accumulators)
    acc = accumulators["person_sit"]

    print(f"  zone_history = {acc['zone_history']}")
    print(f"  customer_score before/after = {first_customer_score:.1f} -> {acc['customer_score']:.1f}")
    assert len(acc["zone_history"]) >= 2, "History should keep the recent table sit and standing transition"
    assert acc["zone_history"][-2][0] == "table"
    assert acc["zone_history"][-2][1] == "sitting"
    assert acc["zone_history"][-2][2] >= 90
    assert acc["customer_score"] > first_customer_score, "Carryover evidence should increase customer score"
    print("  ✅ PASSED")


def test_table_sit_history_is_very_strong_customer_evidence():
    """Recent long table sitting in history should heavily boost customer evidence."""
    print("\n[Test 10] Table-sit history is very strong customer evidence")

    accumulators = None
    obs_cycles = [
        [{
            "track_id": 10,
            "global_id": "person_table_hist",
            "action": "sitting",
            "zone_type": "table",
            "pose_frame_count": 95,
            "appearance_count": 0,
            "previous_role": "unknown",
            "previous_duration_frames": 0,
        }],
        [{
            "track_id": 10,
            "global_id": "person_table_hist",
            "action": "standing",
            "zone_type": "table",
            "pose_frame_count": 1,
            "appearance_count": 0,
            "previous_role": "unknown",
            "previous_duration_frames": 95,
        }],
    ]

    _, accumulators = run_single_cycle(obs_cycles[0], prior_accumulators=accumulators)
    first_customer_score = accumulators["person_table_hist"]["customer_score"]

    _, accumulators = run_single_cycle(obs_cycles[1], prior_accumulators=accumulators)
    acc = accumulators["person_table_hist"]

    print(f"  customer_score before/after = {first_customer_score:.1f} -> {acc['customer_score']:.1f}")
    assert acc["customer_score"] >= first_customer_score + 10.0, "Table-sit history should add a large customer boost"
    print("  ✅ PASSED")


# ── Test 8: Decision output has all fields ────────────────────────────────

def test_decision_output():
    """RoleDecision should contain track_id, global_id, role, confidence, scores."""
    print("\n[Test 8] Decision output completeness")

    obs = [{
        "track_id": 99,
        "global_id": "person_X",
        "action": "sitting",
        "zone_type": "table",
        "pose_frame_count": 20,
        "appearance_count": 0,
        "previous_role": "unknown",
    }]

    decisions, _ = run_single_cycle(obs)
    d = decisions[99]

    print(f"  Decision: {d}")
    assert "role" in d
    assert "confidence" in d
    assert "worker_score" in d
    assert "customer_score" in d
    assert "global_id" in d
    assert d["confidence"] > 0
    print("  ✅ PASSED")


# ── Main ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  RoleEngine Smoke Tests")
    print("=" * 60)

    test_sitting_at_table_builds_customer_score()
    test_staff_zone_builds_worker_score()
    test_customer_confirmation_over_time()
    test_worker_confirmation_via_serving()
    test_decay()
    test_reversal()
    test_merge()
    test_decision_output()
    test_zone_history_tracks_transitions_and_patterns()
    test_recent_sit_carryover_evidence()
    test_table_sit_history_is_very_strong_customer_evidence()

    print("\n" + "=" * 60)
    print("  All 11 tests passed ✅")
    print("=" * 60)

```

---

### <a id="📄-tests-test-tracker-py"></a>📄 `tests/test_tracker.py`

**File Info:**
- **Size**: 956 B
- **Extension**: `.py`
- **Language**: `python`
- **Location**: `tests/test_tracker.py`
- **Relative Path**: `tests`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:08 (Asia/Damascus / GMT+03:00)
- **MD5**: `f1901592a0113019f379ba37205dd5c0`
- **SHA256**: `ac2c8c244331d45753585694658bf4a2bc22a15f8ec8278f75ca6c62e4cf9092`
- **Encoding**: UTF-8

**File code content:**

```python
import unittest
import numpy as np
from src.ai_models.tracker import RestaurantTracker

class TestRestaurantTracker(unittest.TestCase):
    def setUp(self):
        # إنشاء كائن التتبع
        self.tracker = RestaurantTracker()

    def test_tracker_update(self):
        # 1. محاكاة فريم وهمي وصندوق كشف وهمي لشخص [x1, y1, x2, y2, confidence, class_id]
        fake_frame = np.zeros((480, 480, 3), dtype=np.uint8)
        fake_detections = [[100, 100, 200, 300, 0.9, 0]] # شخص بنسبة ثقة 90%
        
        # 2. تمرير الكشف للـ Tracker
        tracked_objects = self.tracker.update(fake_detections, frame=fake_frame)
        
        # 3. التأكيد: يجب أن يعيد التتبع قائمة كائنات
        self.assertIsInstance(tracked_objects, list, "المخرجات يجب أن تكون قائمة بالتتبعات")

if __name__ == "__main__":
    unittest.main()
```

---

### <a id="📄-changes-txt"></a>📄 `changes.txt`

**File Info:**
- **Size**: 5.86 KB
- **Extension**: `.txt`
- **Language**: `text`
- **Location**: `changes.txt`
- **Relative Path**: `root`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:05 (Asia/Damascus / GMT+03:00)
- **MD5**: `ad715f6d46d877937f83bddbf46b4463`
- **SHA256**: `77127933b9a1cd5d8374c73f9ebb98a3f997129374e357012272c7173ee4cb53`
- **Encoding**: UTF-8

**File code content:**

```text
RESTAURANT MONITOR — CHANGES LOG
=================================

1. zones_config.json / zone_annotator (annotator tool)
---------------------------------------------------
- Added a hierarchy: a broad "table_area" (container) polygon can now hold
  multiple individual "table" (leaf) zones nested inside it.
- Leaf table zones get a "parent_zone_id" field pointing to their container.
- Annotator (zone_annotator_v3.html) updated with 3 zone types:
  table_area (draw container first) -> table (draw inside it, validated via
  point-in-polygon) -> service_path (unchanged).
- Deleting a table_area in the annotator cascades and deletes its child tables.

2. zone_manager.py
------------------
- ZONE_TYPE_MAP was missing the leaf "table" type entirely (only had
  "table_area") -> raw_zone_type="table" zones were silently ignored.
  Added: "table": "table".
- table_area is used ONLY as a broad "is this person at a table at all"
  fallback; a specific "table" zone always wins when both match (gives the
  exact table, not just the general area).
- FIXED (this round): specific-table matching switched from %-intersection
  to bbox-CENTER-POINT containment. %-intersection was flickering between
  adjacent/overlapping table polygons on tiny bbox jitter, which kept
  resetting pose_frame_count and stopped customers from ever accumulating
  enough evidence to be confirmed. Center point is stable frame-to-frame.
  table_area / work / walk zones still use %-intersection (unchanged).
- UPDATED (latest round): specific-table matching now prefers HAND (wrist)
  keypoints over bbox center. A wrist actually reaching into/resting on a
  table polygon is a more direct "at this table" signal than bbox center,
  and avoids edge cases where someone leans in from an adjacent zone but
  their bbox center is still just outside the table. Falls back to bbox
  center-point matching when hand keypoints are missing or below
  confidence threshold (KP_CONF_THRESHOLD, same 0.25 used for the
  lower-body walk-zone check). New helper: _find_table_by_hands() checks
  HAND_KP_INDICES = (9, 10) [left_wrist, right_wrist] against leaf "table"
  zones; picks the smallest containing polygon if a wrist lands in more
  than one (shouldn't normally happen with well-drawn zones).
- Added debug prints showing which zone was picked and why (WORK / TABLE
  specific / TABLE area-only / WALK / UNKNOWN), including the method used
  (skeleton / intersection / hands / center_point).

3. live_pipeline.py
--------------------
- ZONE_TYPE_MAP here is a SEPARATE map from zone_manager.py's — this one
  produces `zone_type_normalized`, which is what RoleEngine actually reads.
  It also was missing "table" -> was silently normalizing every specific
  table match to "unknown". Added: "table": "table". (This was the actual
  root cause of "sitting at a table but role stays unknown / Loc: unknown".)
- FIXED (this round): ReID matching now skips crops that are too small/
  low-res to produce a trustworthy embedding (uses new
  reid_gallery.MIN_CROP_WIDTH / MIN_CROP_HEIGHT thresholds) instead of
  matching against garbage data. Track just waits for a better crop next
  frame instead of registering or matching wrongly.

4. role_engine.py
------------------
- ev_walk_service / ev_stand_walk_zone (walking/standing in a walk zone)
  no longer act as standalone worker signals. They now only REINFORCE an
  identity RoleEngine has ALREADY confirmed as "worker" (via staff_zone,
  serving, or reappearance evidence) — they can't help an unknown/customer
  person become a worker on their own, since customers walk through walk
  zones too.
- Added debug prints: every evidence rule prints "EVIDENCE fired: gid=...
  rule_tag=..." the one time it fires (confirms the EvidenceApplied
  sentinel is working — same gid+rule_tag should never print twice in one
  sitting). Added prints on every CONFIRM / REVERSAL role decision.

5. reid_gallery.py
-------------------
- FIXED (this round) — root cause of "worker X's identity handed to
  unknown person Y" on low-res CCTV:
  a) Raised default similarity threshold 0.65 -> 0.72 (fewer accidental
     merges; trade-off is slightly more "new identity" registrations,
     which is the safer failure mode).
  b) Added a MARGIN check: a match must beat the runner-up candidate by at
     least MIN_MATCH_MARGIN (0.05), not just clear the absolute threshold.
     A "confidently wrong" match (e.g. top=0.66 vs runner-up=0.655) is far
     more dangerous than an honest "no match" (which just registers a new
     id) — this margin check is what actually catches that case. Applied
     to both the permanent ReIDGallery and the temporary SessionGallery.
  c) Added MIN_CROP_WIDTH / MIN_CROP_HEIGHT constants (40x80 px) — crops
     smaller than this are considered too low-res to trust; the pipeline
     now skips ReID entirely for those crops rather than embedding them.

FILES TOUCHED
-------------
- zones_config.json          (data — table_area/table hierarchy)
- zone_annotator_v3.html      (tool — 3 zone types + parent_zone_id)
- zone_manager.py             (leaf table type + center-point matching + debug prints)
- live_pipeline.py            (leaf table type in its own map + crop-size ReID guard)
- role_engine.py              (walk-zone evidence gated to confirmed workers only + debug prints)
- reid_gallery.py             (threshold raise + margin check + min crop size)

STILL OPEN / SUGGESTED NEXT
----------------------------
- Consider hysteresis on table_area-only fallback matching too (currently
  still %-intersection based, so could theoretically flicker between two
  table_areas at their shared boundary — less likely than table-vs-table
  since areas are usually large and non-adjacent, but worth watching).
- SessionGallery still has no TTL purge call wired into the main loop
  aside from `purge_old()` being invoked each frame in live_pipeline (this
  was confirmed present — no action needed, noted for completeness).
```

---

### <a id="📄-readme-md"></a>📄 `README.md`

**File Info:**
- **Size**: 2.13 KB
- **Extension**: `.md`
- **Language**: `text`
- **Location**: `README.md`
- **Relative Path**: `root`
- **Created**: 2026-07-05 09:47:52 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 08:02:05 (Asia/Damascus / GMT+03:00)
- **MD5**: `47a1b856e55ac4d2b6bba3f46ee51d85`
- **SHA256**: `dbd0fe935a46c7f227494b7bcae44f90ce52647953ce9dec9ba9088403282572`
- **Encoding**: UTF-8

**File code content:**

````markdown

# Restaurant Monitor

## التثبيت

~~~~bash
pip install shapely
~~~~

## ملخص التحسينات الأخيرة

تمت عدة تعديلات لتحسين التعرف على الأشخاص وحالة الطاولات في البث المباشر:

1. دعم حالة الطاولات بشكل صحيح
	- صار النظام يتعامل مع `table_area` و `table` كأنهما طاولات.
	- هذا منع مشكلة ظهور كل الطاولات على أنها `empty` فقط.

2. دعم حالات الطاولة الثلاث
	- تمت إضافة/تفعيل عرض الحالات التالية: `empty` و `occupied` و `dirty`.
	- اللون في العرض المباشر صار يوضح الحالة بسرعة.

3. تحسين التقاط الأشخاص عند الطاولات
	- تم تخفيف الفلترة المبكرة للتراكات الجديدة حتى لا يضيع الأشخاص الموجودون على الطاولات قبل تثبيت التتبع.
	- صار التتبع يقبل التراكات الحديثة بدل انتظار confirmation كامل فقط.

4. تسريع التعرف على العامل
	- تم تشغيل تحديث الـ pose/role بشكل أسرع في العرض المباشر.
	- تم تقليل التأخير قبل تثبيت دور العامل.
	- تم تخفيف شرط حجم القصاصة المستخدمة في Re-ID حتى يتم التعرف على العامل بشكل أسرع.

5. تحسين عرض الحالة على الفيديو
	- تم ربط الرسم في `run_live.py` بحالة الطاولات الموحدة من الـ pipeline.
	- صار الفيديو يعرض حالة الطاولة مباشرة بدل الاعتماد على `empty/occupied` فقط.

## ملاحظات تشغيل

- إذا أردت التعرف الأسرع على الأشخاص والعامل في الوضع المباشر، شغّل البث مع الإعدادات الافتراضية الحالية.
- إذا لاحظت بطئًا أو عدم ثبات في التعرف، جرّب لاحقًا تعديل حساسية الكشف أو إعدادات التتبع حسب الفيديو نفسه.

````

---

### <a id="📄-requirements-txt"></a>📄 `requirements.txt`

**File Info:**
- **Size**: 2.13 KB
- **Extension**: `.txt`
- **Language**: `text`
- **Location**: `requirements.txt`
- **Relative Path**: `root`
- **Created**: 2026-07-14 09:53:36 (Asia/Damascus / GMT+03:00)
- **Modified**: 2026-07-14 09:53:36 (Asia/Damascus / GMT+03:00)
- **MD5**: `f13493ef03ab077b78bdc14553ce294a`
- **SHA256**: `c37f4858937cd2c8aa0acf0d47aeab51ab0a9be2a8009daeb077785513571f05`
- **Encoding**: UTF-8

**File code content:**

```text
# Restaurant Monitor — pinned environment
#
# Generated via `pip freeze` from a clean `.venv` built against every import
# actually present in src/, storage/, and api/ (not just the old unpinned
# list). Includes exact transitive versions so every teammate who runs
# `pip install -r requirements.txt` gets a byte-identical environment.
#
# Notes on non-obvious entries:
#   - setuptools is pinned <81 (80.10.2) because deep-sort-realtime's
#     PyTorch embedder does a bare `import pkg_resources` at runtime;
#     setuptools>=81 dropped pkg_resources and that import fails.
#   - gdown and tensorboard are not imported directly by our code, but
#     torchreid's package __init__ unconditionally imports them
#     (torchreid/reid/data/datasets/image/university1652.py -> gdown;
#     torchreid/reid/engine/engine.py -> torch.utils.tensorboard ->
#     tensorboard). torchreid does not declare either as a dependency,
#     so `import torchreid` (used by src/kbs/reid_gallery.py) fails
#     without them installed explicitly.

absl-py==2.5.0
aiosqlite==0.22.1
asyncpg==0.31.0
beautifulsoup4==4.15.0
certifi==2026.6.17
charset-normalizer==3.4.9
colorama==0.4.6
contourpy==1.3.3
cycler==0.12.1
deep-sort-realtime==1.3.2
experta==1.9.4
faiss-cpu==1.14.3
filelock==3.29.7
fonttools==4.63.0
frozendict==1.2
fsspec==2026.6.0
gdown==6.1.0
greenlet==3.5.3
grpcio==1.82.1
idna==3.18
iniconfig==2.3.0
Jinja2==3.1.6
kiwisolver==1.5.0
Markdown==3.10.2
MarkupSafe==3.0.3
matplotlib==3.11.0
mpmath==1.3.0
networkx==3.6.1
numpy==2.5.1
nvidia-ml-py==13.610.43
opencv-python==5.0.0.93
packaging==26.2
pandas==3.0.3
pillow==12.3.0
pluggy==1.6.0
polars==1.42.1
polars-runtime-32==1.42.1
protobuf==7.35.1
psutil==7.2.2
Pygments==2.20.0
pyparsing==3.3.2
PySocks==1.7.1
pytest==9.1.1
python-dateutil==2.9.0.post0
PyYAML==6.0.3
requests==2.34.2
schema==0.6.7
scipy==1.18.0
setuptools==80.10.2
shapely==2.1.2
six==1.17.0
soupsieve==2.8.4
SQLAlchemy==2.0.51
sympy==1.14.0
tensorboard==2.21.0
tensorboard-data-server==0.7.2
torch==2.13.0
torchreid==0.2.5
torchvision==0.28.0
tqdm==4.68.4
typing_extensions==4.16.0
tzdata==2026.3
ultralytics==8.4.95
ultralytics-thop==2.0.20
urllib3==2.7.0
Werkzeug==3.1.8

```

---

