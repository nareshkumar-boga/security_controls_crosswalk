"""CSV loading helpers for control libraries."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List

REQUIRED_COLUMNS = {
    "framework",
    "control_id",
    "title",
    "description",
    "domain",
    "tags",
}


def load_controls_from_csv(file_path: Path) -> List[Dict[str, str]]:
    """Load controls from a CSV file and validate the required columns."""
    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = set(reader.fieldnames or [])
        missing_columns = REQUIRED_COLUMNS - fieldnames

        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing required columns in {file_path}: {missing}")

        return [dict(row) for row in reader]
