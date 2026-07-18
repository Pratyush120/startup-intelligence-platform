"""
Utility helper functions.
"""

import json
from datetime import datetime
from pathlib import Path

from config.config import Config


def save_raw_json(data, source_name):
    """
    Save raw collected data into timestamped folders.
    """

    today = datetime.now().strftime("%Y-%m-%d")

    output_dir = Config.RAW_DATA_DIR / today

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"{source_name}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return file_path
