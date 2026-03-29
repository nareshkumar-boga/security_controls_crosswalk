"""Control comparison and mapping logic."""

from __future__ import annotations

from typing import Any, Dict, List


def score_confidence(shared_tag_count: int) -> str:
    """Convert a shared tag count into a confidence label."""
    if shared_tag_count >= 3:
        return "High"
    if shared_tag_count == 2:
        return "Medium"
    return "Low"


def _safe_tag_set(raw_tags: Any) -> set[str]:
    """Build a normalized tag set from list-like values."""
    if not isinstance(raw_tags, list):
        return set()
    return {str(tag).strip().lower() for tag in raw_tags if str(tag).strip()}


def map_controls(
    source_controls: List[Dict[str, Any]],
    target_controls: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Compare every source control to every target control."""
    mappings: List[Dict[str, Any]] = []

    for source_control in source_controls:
        source_tags = _safe_tag_set(source_control.get("tags"))
        if not source_tags:
            continue

        for target_control in target_controls:
            target_tags = _safe_tag_set(target_control.get("tags"))
            shared_tags = sorted(source_tags.intersection(target_tags))

            if not shared_tags:
                continue

            mappings.append(
                {
                    "source_framework": source_control["framework"],
                    "source_control_id": source_control["control_id"],
                    "source_title": source_control["title"],
                    "target_framework": target_control["framework"],
                    "target_control_id": target_control["control_id"],
                    "target_title": target_control["title"],
                    "shared_tags": shared_tags,
                    "shared_tag_count": len(shared_tags),
                    "confidence": score_confidence(len(shared_tags)),
                }
            )

    mappings.sort(
        key=lambda item: (
            item["source_control_id"],
            -item["shared_tag_count"],
            item["target_control_id"],
        )
    )
    return mappings
