"""Console and Markdown reporting helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return report generation time in UTC."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _escape_markdown_cell(value: str) -> str:
    """Escape table-breaking characters in Markdown cells."""
    return value.replace("|", "\\|")


def print_console_summary(summary: Dict[str, Any], mappings: List[Dict[str, Any]]) -> None:
    """Print a readable terminal summary of mappings and gaps."""
    print("=" * 72)
    print("Control Crosswalk Report")
    print("=" * 72)
    print(f"Generated: {_utc_timestamp()}")
    print(f"Source Framework: {summary['source_framework']}")
    print(f"Target Framework: {summary['target_framework']}")
    print()
    print("Summary")
    print(f"- Total source controls: {summary['total_source_controls']}")
    print(f"- Total target controls: {summary['total_target_controls']}")
    print(f"- Source controls mapped: {summary['mapped_source_controls']}")
    print(f"- Total mappings: {summary['total_mappings']}")
    print(f"- Total gaps: {summary['total_gaps']}")
    print()

    print("Mappings")
    if not mappings:
        print("- No mappings found.")
    else:
        for mapping in mappings:
            shared_tags = ", ".join(mapping["shared_tags"])
            print(
                "- "
                f"{mapping['source_control_id']} -> {mapping['target_control_id']} "
                f"| confidence: {mapping['confidence']} "
                f"| shared tags: {shared_tags}"
            )

    print()
    print("Gaps")
    if not summary["gaps"]:
        print("- No unmapped source controls.")
    else:
        for gap in summary["gaps"]:
            print(f"- {gap['control_id']} | {gap['title']}")


def build_markdown_report(summary: Dict[str, Any], mappings: List[Dict[str, Any]]) -> str:
    """Create a Markdown report string."""
    generated_at = _utc_timestamp()
    lines = [
        "# Security Control Crosswalk Report",
        "",
        f"**Generated:** {generated_at}",
        f"**Source Framework:** {summary['source_framework']}",
        f"**Target Framework:** {summary['target_framework']}",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Total source controls | {summary['total_source_controls']} |",
        f"| Total target controls | {summary['total_target_controls']} |",
        f"| Source controls mapped | {summary['mapped_source_controls']} |",
        f"| Total mappings | {summary['total_mappings']} |",
        f"| Total gaps | {summary['total_gaps']} |",
        "",
        "## Mappings",
        "",
        "| Source ID | Source Title | Target ID | Target Title | Shared Tags | Shared Count | Confidence |",
        "| --- | --- | --- | --- | --- | ---: | --- |",
    ]

    if mappings:
        for mapping in mappings:
            shared_tags = ", ".join(mapping["shared_tags"])
            lines.append(
                "| "
                f"{_escape_markdown_cell(str(mapping['source_control_id']))} | "
                f"{_escape_markdown_cell(str(mapping['source_title']))} | "
                f"{_escape_markdown_cell(str(mapping['target_control_id']))} | "
                f"{_escape_markdown_cell(str(mapping['target_title']))} | "
                f"{_escape_markdown_cell(shared_tags)} | "
                f"{mapping['shared_tag_count']} | "
                f"{mapping['confidence']} |"
            )
    else:
        lines.append("| None | None | None | None | None | 0 | N/A |")

    lines.extend(
        [
            "",
            "## Gaps",
            "",
            "| Source ID | Source Title | Domain | Tags |",
            "| --- | --- | --- | --- |",
        ]
    )

    if summary["gaps"]:
        for gap in summary["gaps"]:
            tags = ", ".join(gap["tags"])
            lines.append(
                "| "
                f"{_escape_markdown_cell(str(gap['control_id']))} | "
                f"{_escape_markdown_cell(str(gap['title']))} | "
                f"{_escape_markdown_cell(str(gap['domain']))} | "
                f"{_escape_markdown_cell(tags)} |"
            )
    else:
        lines.append("| None | No unmapped source controls | N/A | N/A |")

    lines.append("")
    return "\n".join(lines)


def write_markdown_report(
    summary: Dict[str, Any], mappings: List[Dict[str, Any]], output_path: Path
) -> None:
    """Write the Markdown report to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_markdown_report(summary, mappings), encoding="utf-8")
