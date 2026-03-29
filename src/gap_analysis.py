"""Gap analysis helpers for control mappings."""

from __future__ import annotations

from typing import Any, Dict, List


def find_unmapped_source_controls(
    source_controls: List[Dict[str, Any]], mappings: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Return source controls that do not appear in any mapping."""
    mapped_source_ids = {mapping["source_control_id"] for mapping in mappings}
    return [
        control
        for control in source_controls
        if control["control_id"] not in mapped_source_ids
    ]


def summarize_results(
    source_controls: List[Dict[str, Any]],
    target_controls: List[Dict[str, Any]],
    mappings: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Build a summary dictionary for reporting."""
    gaps = find_unmapped_source_controls(source_controls, mappings)
    mapped_source_count = len(source_controls) - len(gaps)
    source_framework = source_controls[0]["framework"] if source_controls else "Unknown"
    target_framework = target_controls[0]["framework"] if target_controls else "Unknown"

    return {
        "source_framework": source_framework,
        "target_framework": target_framework,
        "total_source_controls": len(source_controls),
        "total_target_controls": len(target_controls),
        "mapped_source_controls": mapped_source_count,
        "total_mappings": len(mappings),
        "total_gaps": len(gaps),
        "gaps": gaps,
    }
