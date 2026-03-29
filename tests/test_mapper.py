"""Tests for mapping and confidence logic."""

import unittest

from src.mapper import map_controls, score_confidence


class TestMapper(unittest.TestCase):
    """Validate confidence scoring and control mapping behavior."""

    def test_score_confidence_boundaries(self) -> None:
        """Boundary values should map to expected confidence levels."""
        self.assertEqual("Low", score_confidence(1))
        self.assertEqual("Medium", score_confidence(2))
        self.assertEqual("High", score_confidence(3))
        self.assertEqual("High", score_confidence(4))

    def test_map_controls_only_includes_overlapping_tags(self) -> None:
        """Mappings should only be created when at least one tag overlaps."""
        source_controls = [
            {
                "framework": "NIST CSF",
                "control_id": "S-1",
                "title": "Source 1",
                "tags": ["access", "identity", "authentication"],
            }
        ]
        target_controls = [
            {
                "framework": "ISO 27001",
                "control_id": "T-1",
                "title": "Target Overlap",
                "tags": ["identity", "authentication", "authorization"],
            },
            {
                "framework": "ISO 27001",
                "control_id": "T-2",
                "title": "Target No Overlap",
                "tags": ["asset", "risk"],
            },
        ]

        mappings = map_controls(source_controls, target_controls)

        self.assertEqual(1, len(mappings))
        mapping = mappings[0]
        self.assertEqual("S-1", mapping["source_control_id"])
        self.assertEqual("T-1", mapping["target_control_id"])
        self.assertEqual(["authentication", "identity"], mapping["shared_tags"])
        self.assertEqual(2, mapping["shared_tag_count"])
        self.assertEqual("Medium", mapping["confidence"])

    def test_map_controls_includes_expected_fields(self) -> None:
        """Each mapping should include source, target, and confidence metadata."""
        source_controls = [
            {
                "framework": "NIST CSF",
                "control_id": "S-2",
                "title": "Source 2",
                "tags": ["logging", "monitoring", "incident"],
            }
        ]
        target_controls = [
            {
                "framework": "ISO 27001",
                "control_id": "T-3",
                "title": "Target 3",
                "tags": ["incident", "monitoring", "logging"],
            }
        ]

        mappings = map_controls(source_controls, target_controls)
        mapping = mappings[0]

        expected_keys = {
            "source_framework",
            "source_control_id",
            "source_title",
            "target_framework",
            "target_control_id",
            "target_title",
            "shared_tags",
            "shared_tag_count",
            "confidence",
        }
        self.assertTrue(expected_keys.issubset(set(mapping.keys())))
        self.assertEqual("High", mapping["confidence"])

    def test_map_controls_sort_order_is_stable_and_expected(self) -> None:
        """Mappings should sort by source id, shared count desc, target id."""
        source_controls = [
            {
                "framework": "NIST CSF",
                "control_id": "S-1",
                "title": "Source 1",
                "tags": ["a", "b", "c"],
            },
            {
                "framework": "NIST CSF",
                "control_id": "S-2",
                "title": "Source 2",
                "tags": ["x", "y", "z"],
            },
        ]
        target_controls = [
            {
                "framework": "ISO 27001",
                "control_id": "T-2",
                "title": "Target 2",
                "tags": ["a", "b"],
            },
            {
                "framework": "ISO 27001",
                "control_id": "T-1",
                "title": "Target 1",
                "tags": ["a", "b", "c"],
            },
            {
                "framework": "ISO 27001",
                "control_id": "T-3",
                "title": "Target 3",
                "tags": ["x"],
            },
        ]

        mappings = map_controls(source_controls, target_controls)
        ordered_pairs = [
            (item["source_control_id"], item["target_control_id"], item["shared_tag_count"])
            for item in mappings
        ]

        self.assertEqual(
            [
                ("S-1", "T-1", 3),
                ("S-1", "T-2", 2),
                ("S-2", "T-3", 1),
            ],
            ordered_pairs,
        )

    def test_map_controls_returns_empty_when_no_overlaps(self) -> None:
        """No shared tags should produce no mappings."""
        source_controls = [
            {
                "framework": "NIST CSF",
                "control_id": "S-1",
                "title": "Source 1",
                "tags": ["access"],
            }
        ]
        target_controls = [
            {
                "framework": "ISO 27001",
                "control_id": "T-1",
                "title": "Target 1",
                "tags": ["risk"],
            }
        ]

        self.assertEqual([], map_controls(source_controls, target_controls))


if __name__ == "__main__":
    unittest.main()
