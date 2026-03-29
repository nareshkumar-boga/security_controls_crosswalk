"""Normalization helpers for control data."""

from __future__ import annotations

from typing import Any, Dict, List


def normalize_blank(value: Any) -> str:
    """Convert blank-like values into a safe trimmed string."""
    if value is None:
        return ""
    return str(value).strip()


def normalize_tags(raw_tags: str) -> List[str]:
    """Convert a semicolon-separated tag string into normalized tags."""
    if not raw_tags.strip():
        return []

    tags: List[str] = []
    seen = set()
    for tag in raw_tags.split(";"):
        cleaned_tag = tag.strip().lower()
        if cleaned_tag and cleaned_tag not in seen:
            tags.append(cleaned_tag)
            seen.add(cleaned_tag)
    return tags


def normalize_controls(controls: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Normalize control records into a consistent structure."""
    normalized_controls: List[Dict[str, Any]] = []

    for control in controls:
        normalized_control: Dict[str, Any] = {
            "framework": normalize_blank(control.get("framework")),
            "control_id": normalize_blank(control.get("control_id")),
            "title": normalize_blank(control.get("title")),
            "description": normalize_blank(control.get("description")),
            "domain": normalize_blank(control.get("domain")),
            "tags": normalize_tags(normalize_blank(control.get("tags"))),
        }
        normalized_controls.append(normalized_control)

    return normalized_controls
