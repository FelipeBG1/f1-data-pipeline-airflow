import json
from pathlib import Path


def save_json_snapshot(data, file_path):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def save_csv_snapshot(df, file_path):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(path, index=False)