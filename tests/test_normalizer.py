"""Tests for normalization helpers."""

import unittest

from src.normalizer import normalize_blank, normalize_controls, normalize_tags


class TestNormalizer(unittest.TestCase):
    """Validate blank handling, tag cleanup, and record normalization."""

    def test_normalize_blank_handles_none_and_whitespace(self) -> None:
        """normalize_blank should produce safe trimmed strings."""
        self.assertEqual("", normalize_blank(None))
        self.assertEqual("", normalize_blank("   "))
        self.assertEqual("value", normalize_blank("  value  "))
        self.assertEqual("42", normalize_blank(42))

    def test_normalize_tags_trims_lowercases_and_drops_empty_tags(self) -> None:
        """normalize_tags should clean and split semicolon-separated values."""
        tags = normalize_tags(" Access ; identity; ; AUTHENTICATION ;  ")
        self.assertEqual(["access", "identity", "authentication"], tags)

    def test_normalize_tags_blank_input_returns_empty_list(self) -> None:
        """normalize_tags should return [] for blank or whitespace-only input."""
        self.assertEqual([], normalize_tags(""))
        self.assertEqual([], normalize_tags("   "))

    def test_normalize_controls_builds_consistent_structure(self) -> None:
        """normalize_controls should normalize strings and convert tags to list."""
        controls = [
            {
                "framework": " NIST CSF ",
                "control_id": " PR.AC-01 ",
                "title": " Access Control ",
                "description": None,
                "domain": " Protect ",
                "tags": " Access ; Identity ; Authentication ",
            }
        ]

        normalized = normalize_controls(controls)

        self.assertEqual(1, len(normalized))
        self.assertEqual("NIST CSF", normalized[0]["framework"])
        self.assertEqual("PR.AC-01", normalized[0]["control_id"])
        self.assertEqual("Access Control", normalized[0]["title"])
        self.assertEqual("", normalized[0]["description"])
        self.assertEqual("Protect", normalized[0]["domain"])
        self.assertEqual(
            ["access", "identity", "authentication"], normalized[0]["tags"]
        )


if __name__ == "__main__":
    unittest.main()

