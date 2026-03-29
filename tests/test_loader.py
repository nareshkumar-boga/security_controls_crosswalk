"""Tests for CSV loader behavior."""

import tempfile
import unittest
from pathlib import Path

from src.loader import load_controls_from_csv


class TestLoader(unittest.TestCase):
    """Validate CSV loading and required-column checks."""

    def _write_temp_csv(self, content: str) -> Path:
        """Create a temporary CSV file and return its path."""
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8", newline=""
        )
        with temp_file:
            temp_file.write(content)
        self.addCleanup(lambda: Path(temp_file.name).unlink(missing_ok=True))
        return Path(temp_file.name)

    def test_load_valid_csv_returns_rows(self) -> None:
        """Loader should parse valid CSV rows into dictionaries."""
        csv_content = (
            "framework,control_id,title,description,domain,tags\n"
            "NIST CSF,ID.AM-01,Asset Inventory,Inventory assets,Asset,asset; risk\n"
            "NIST CSF,PR.AC-01,Access Control,Manage access,Protect,access; identity\n"
        )
        csv_path = self._write_temp_csv(csv_content)

        rows = load_controls_from_csv(csv_path)

        self.assertEqual(2, len(rows))
        self.assertEqual("NIST CSF", rows[0]["framework"])
        self.assertEqual("PR.AC-01", rows[1]["control_id"])

    def test_missing_single_required_column_raises_value_error(self) -> None:
        """Loader should fail when one required column is absent."""
        csv_content = (
            "framework,control_id,title,description,domain\n"
            "NIST CSF,ID.AM-01,Asset Inventory,Inventory assets,Asset\n"
        )
        csv_path = self._write_temp_csv(csv_content)

        with self.assertRaises(ValueError) as error_context:
            load_controls_from_csv(csv_path)

        self.assertIn("tags", str(error_context.exception))

    def test_missing_multiple_required_columns_raises_value_error(self) -> None:
        """Loader should fail when multiple required columns are absent."""
        csv_content = (
            "framework,control_id,title,description\n"
            "NIST CSF,ID.AM-01,Asset Inventory,Inventory assets\n"
        )
        csv_path = self._write_temp_csv(csv_content)

        with self.assertRaises(ValueError) as error_context:
            load_controls_from_csv(csv_path)

        error_message = str(error_context.exception)
        self.assertIn("domain", error_message)
        self.assertIn("tags", error_message)

    def test_header_only_csv_returns_empty_list(self) -> None:
        """Loader should return an empty list when no rows exist."""
        csv_content = "framework,control_id,title,description,domain,tags\n"
        csv_path = self._write_temp_csv(csv_content)

        rows = load_controls_from_csv(csv_path)

        self.assertEqual([], rows)


if __name__ == "__main__":
    unittest.main()

