import argparse
import sys
from pathlib import Path
PROJECT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_DIR))
import pandas as pd
from src.core.pipeline import RestaurantMonitoringPipeline

def main():
    parser = argparse.ArgumentParser(description="Run YOLO person detection pipeline.")

    parser.add_argument(
        "--config",
        type=str,
        default="config/config.json",
        help="Path to config file."
    )

    parser.add_argument(
        "--target-fps",
        type=int,
        default=None,
        help="How many frames per second to process."
    )

    parser.add_argument(
        "--max-seconds",
        type=int,
        default=None,
        help="Limit processing to first N seconds. Use nothing for full video."
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing detection files."
    )

    args = parser.parse_args()

    pipeline = RestaurantMonitoringPipeline(config_path=args.config)

    results = pipeline.process_all_videos(
        target_fps=args.target_fps,
        max_seconds=args.max_seconds,
        overwrite=args.overwrite,
    )

    results_df = pd.DataFrame(results)

    summary_path = Path("data/metadata/pipeline_run_summary.csv")
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    results_df.to_csv(summary_path, index=False, encoding="utf-8-sig")

    print("========== SUMMARY ==========")
    print(results_df)
    print(f"Saved run summary to: {summary_path}")


if __name__ == "__main__":
    main()