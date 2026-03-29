"""CSV loading helpers for control libraries."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List, Set

REQUIRED_COLUMN_NAMES = [
    "framework",
    "control_id",
    "title",
    "description",
    "domain",
    "tags",
]
REQUIRED_COLUMNS = set(REQUIRED_COLUMN_NAMES)


def _normalize_headers(headers: Iterable[str | None]) -> Set[str]:
    """Normalize CSV headers by trimming surrounding whitespace."""
    return {str(header).strip() for header in headers if header is not None}


def _validate_required_columns(fieldnames: List[str] | None, file_path: Path) -> None:
    """Raise a clear error when required columns are missing."""
    normalized_headers = _normalize_headers(fieldnames or [])
    missing_columns = REQUIRED_COLUMNS - normalized_headers
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns in {file_path}: {missing}")


def load_controls_from_csv(file_path: Path) -> List[Dict[str, str]]:
    """Load controls from a CSV file and validate the required columns.

    Notes:
    - Empty rows are skipped.
    - Missing cell values are normalized to empty strings.
    - Extra columns are ignored to keep the output structure consistent.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        _validate_required_columns(reader.fieldnames, file_path)

        controls: List[Dict[str, str]] = []
        for raw_row in reader:
            # csv.DictReader may include None keys for malformed rows; ignore them.
            row = {
                str(key).strip(): (value or "").strip()
                for key, value in raw_row.items()
                if key is not None
            }

            if not any(row.values()):
                continue

            control = {column: row.get(column, "") for column in REQUIRED_COLUMN_NAMES}
            controls.append(control)

        return controls
