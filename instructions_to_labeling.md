# Instructions for Manual Action Labeling

This guide outlines the complete workflow to generate your dataset and label it using the custom labeling UI.

## Step 1: Extract Crops and Poses

First, you need to run the live pipeline on a specific video. This will perform tracking, extract the skeletal poses into a JSON file, and simultaneously save the matching image crops.

Run this command from the root of your project:

```powershell
python -m src.run_live --source "data/raw_videos/camera_01/video_001.mp4" --camera-id "camera_01" --video-id "video_001" --save-crops-dir "data/debug/crops" --max-frames 1000 --start-sec 532
```

*Notes on arguments:*

- `--source`: The path to the video you want to process.
- `--camera-id`: Determines the camera name prefix for crops (e.g., `camera_01`).
- `--video-id`: Determines the video name prefix for crops (e.g., `video_001`).
- `--save-crops-dir`: Where the actual `.jpg` images will be saved.
- `--max-frames`: (Optional) Limit the number of frames to avoid generating too much data at once.
- `--start-sec`: (Optional) Skip to a specific point in the video in seconds (e.g., `532`). Extracted
- `--save-debug`: (important) Save crops and pose dataset to disk

frames numbers will correctly reflect this time offset.

*Output:*

- **Images:** Saved in `data/debug/crops/camera_01_video_001_frame_...jpg`
- **JSON:** Saved in `data/debug/classification/samples/raw_poses.json`

---

## Step 2: Run the Labeling UI

Once you have the generated crops and the JSON file, launch the interactive labeling script.

```powershell
python src/utils/label_dataset.py --json "data/debug/classification/samples/raw_poses.json" --crops "data/debug/crops" --camera "camera_01"
```

*Notes on arguments:*

- `--camera`: Must match the `--camera-id` you used in Step 1 so the script can correctly reconstruct the image filenames.

---

## Step 3: Use the UI

When the UI opens, it will display a pop-up window showing the cropped person.

**Controls:**

- Press `1` : Label as **standing**
- Press `2` : Label as **sitting**
- Press `3` : Label as **walking**
- Press `4` : Label as **serving**
- Press `s` : **Skip** this image (e.g., blurry or empty box)
- Press `q` : **Quit** the UI.

**Important Features:**

- The script **auto-saves** to the JSON file immediately after every single label.
- If you press `q` and close the script, you can run the exact same command later, and it will **resume** exactly where you left off (it automatically skips files that already have a label).
