from src.extract.f1_results_api import fetch_race_results, parse_race_results
from src.extract.snapshot_utils import save_json_snapshot, save_csv_snapshot
from src.load.save_to_db import save_to_db
from src.load.load_dimensional_model import build_and_load_dimensional_model


def run_pipeline(create_snapshots=False):
    season = 2025
    raw_data = fetch_race_results(season)
    df = parse_race_results(raw_data)

    if create_snapshots:
        save_json_snapshot(raw_data, f"data/raw/json/race_results_{season}.json")
        save_csv_snapshot(df, f"data/raw/csv/race_results_{season}.csv")

    save_to_db(df, "raw_race_results")
    build_and_load_dimensional_model()


if __name__ == "__main__":
    run_pipeline(create_snapshots=True)