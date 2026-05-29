import argparse
import json
from pathlib import Path

import cv2
import numpy as np


PROJECT_DIR = Path(__file__).resolve().parents[2]

ZONES_CONFIG_PATH = PROJECT_DIR / "config" / "zones_config.json"
REFERENCE_FRAMES_DIR = PROJECT_DIR / "data" / "debug" / "zones" / "reference_frames"
ZONES_PREVIEW_DIR = PROJECT_DIR / "data" / "debug" / "zones" / "zones_preview"

class ZoneAnnotator:
    def __init__(
        self,
        camera_id: str,
        zone_id: str,
        zone_type: str,
        zone_name: str,
        max_display_width: int = 1400,
    ):
        self.camera_id = camera_id
        self.zone_id = zone_id
        self.zone_type = zone_type
        self.zone_name = zone_name
        self.max_display_width = max_display_width

        self.image_path = REFERENCE_FRAMES_DIR / f"{camera_id}_reference.jpg"

        if not self.image_path.exists():
            raise FileNotFoundError(f"Reference frame not found: {self.image_path}")

        self.image = cv2.imread(str(self.image_path))

        if self.image is None:
            raise ValueError(f"Cannot read image: {self.image_path}")

        self.original_height, self.original_width = self.image.shape[:2]

        self.scale = 1.0
        if self.original_width > self.max_display_width:
            self.scale = self.max_display_width / self.original_width

        self.display_width = int(self.original_width * self.scale)
        self.display_height = int(self.original_height * self.scale)

        self.display_image = cv2.resize(
            self.image,
            (self.display_width, self.display_height)
        )

        self.points = []

    def run(self):
        window_name = f"{self.camera_id} - {self.zone_id}"

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(window_name, self._mouse_callback)

        print("\n================================")
        print(f"Camera     : {self.camera_id}")
        print(f"Zone ID    : {self.zone_id}")
        print(f"Zone Type  : {self.zone_type}")
        print(f"Zone Name  : {self.zone_name}")
        print("================================")
        print("Left click : add point")
        print("u          : undo last point")
        print("r          : reset")
        print("s or Enter : save and close")
        print("q or Esc   : quit without saving")
        print("================================")
        saved = False

        while True:
            canvas = self._draw_canvas()
            cv2.imshow(window_name, canvas)

            key = cv2.waitKey(20) & 0xFF

            if key == ord("u"):
                if self.points:
                    removed = self.points.pop()
                    print(f"Undo: {removed}")

            elif key == ord("r"):
                self.points = []
                print("Reset points.")

            elif key == ord("s") or key == 13:
                if len(self.points) < 3:
                    print("❌")
                    continue

                self._save_zone()
                self._save_preview()
                print("Saved zone")
                saved = True
                break

            elif key == ord("q") or key == 27:
                print("Quit without saving.")
                break

        cv2.destroyWindow(window_name)
        cv2.destroyAllWindows()

        if saved:
            print(f"Coordinates saved in: {ZONES_CONFIG_PATH}")
            print(f"Preview saved in: {ZONES_PREVIEW_DIR / f'{self.camera_id}_zones_preview.jpg'}")

    def _mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            original_x = int(x / self.scale)
            original_y = int(y / self.scale)

            self.points.append([original_x, original_y])
            print(f"Point added: [{original_x}, {original_y}]")

    def _draw_canvas(self):
        canvas = self.display_image.copy()

        scaled_points = [
            (int(x * self.scale), int(y * self.scale))
            for x, y in self.points
        ]

        for i, point in enumerate(scaled_points):
            cv2.circle(canvas, point, 6, (0, 0, 255), -1)
            cv2.putText(
                canvas,
                str(i + 1),
                (point[0] + 8, point[1] - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

        if len(scaled_points) >= 2:
            for i in range(len(scaled_points) - 1):
                cv2.line(canvas, scaled_points[i], scaled_points[i + 1], (0, 255, 0), 2)

        if len(scaled_points) >= 3:
            cv2.line(canvas, scaled_points[-1], scaled_points[0], (0, 255, 0), 2)

        cv2.putText(
            canvas,
            f"{self.camera_id} | {self.zone_id} | {self.zone_type}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        cv2.putText(
            canvas,
            "click points | s=save | u=undo | r=reset | q=quit",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        return canvas

    def _load_zones_config(self):
        if ZONES_CONFIG_PATH.exists():
            with open(ZONES_CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)

        return {}

    def _save_zone(self):
        zones_config = self._load_zones_config()

        if self.camera_id not in zones_config:
            zones_config[self.camera_id] = {
                "image_size": {
                    "width": self.original_width,
                    "height": self.original_height
                },
                "zones": []
            }

        zones = zones_config[self.camera_id].get("zones", [])

        zones = [
            zone for zone in zones
            if zone.get("zone_id") != self.zone_id
        ]

        zones.append({
            "zone_id": self.zone_id,
            "zone_type": self.zone_type,
            "zone_name": self.zone_name,
            "points": self.points
        })

        zones_config[self.camera_id]["image_size"] = {
            "width": self.original_width,
            "height": self.original_height
        }
        zones_config[self.camera_id]["zones"] = zones

        ZONES_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(ZONES_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(zones_config, f, indent=2, ensure_ascii=False)

    def _save_preview(self):
        zones_config = self._load_zones_config()
        camera_config = zones_config.get(self.camera_id, {})
        zones = camera_config.get("zones", [])

        preview = self.image.copy()

        for zone in zones:
            points = np.array(zone["points"], dtype=np.int32)

            cv2.polylines(
                preview,
                [points],
                isClosed=True,
                color=(0, 255, 0),
                thickness=3
            )

            x, y = points[0]
            label = f"{zone['zone_id']} ({zone['zone_type']})"

            cv2.putText(
                preview,
                label,
                (int(x), int(y) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        ZONES_PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
        output_path = ZONES_PREVIEW_DIR / f"{self.camera_id}_zones_preview.jpg"
        cv2.imwrite(str(output_path), preview)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--camera", required=True)
    parser.add_argument("--zone-id", required=True)
    parser.add_argument("--zone-type", required=True)
    parser.add_argument("--zone-name", required=True)

    args = parser.parse_args()

    annotator = ZoneAnnotator(
        camera_id=args.camera,
        zone_id=args.zone_id,
        zone_type=args.zone_type,
        zone_name=args.zone_name
    )

    annotator.run()


if __name__ == "__main__":
    main()