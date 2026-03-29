"""Console and Markdown reporting helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


def print_console_summary(summary: Dict[str, Any], mappings: List[Dict[str, Any]]) -> None:
    """Print a readable terminal summary of mappings and gaps."""
    print("Control Crosswalk Report")
    print(f"Source Framework: {summary['source_framework']}")
    print(f"Target Framework: {summary['target_framework']}")
    print()
    print("Summary")
    print(f"- Total source controls: {summary['total_source_controls']}")
    print(f"- Total target controls: {summary['total_target_controls']}")
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
                f"| shared tags: {shared_tags} "
                f"| confidence: {mapping['confidence']}"
            )

    print()
    print("Gaps")
    if not summary["gaps"]:
        print("- No unmapped source controls.")
    else:
        for gap in summary["gaps"]:
            print(f"- {gap['control_id']} | {gap['title']}")


def build_markdown_report(
    summary: Dict[str, Any], mappings: List[Dict[str, Any]]
) -> str:
    """Create a Markdown report string."""
    lines = [
        "# Control Crosswalk Report",
        "",
        f"**Source Framework:** {summary['source_framework']}",
        f"**Target Framework:** {summary['target_framework']}",
        "",
        "## Mapping Summary",
        "",
        f"- Total source controls: {summary['total_source_controls']}",
        f"- Total target controls: {summary['total_target_controls']}",
        f"- Total mappings: {summary['total_mappings']}",
        f"- Total gaps: {summary['total_gaps']}",
        "",
        "## Detailed Mappings",
        "",
        "| Source Control | Source Title | Target Control | Target Title | Shared Tags | Confidence |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    if mappings:
        for mapping in mappings:
            shared_tags = ", ".join(mapping["shared_tags"])
            lines.append(
                f"| {mapping['source_control_id']} | {mapping['source_title']} | "
                f"{mapping['target_control_id']} | {mapping['target_title']} | "
                f"{shared_tags} | {mapping['confidence']} |"
            )
    else:
        lines.append("| None | None | None | None | None | None |")

    lines.extend(
        [
            "",
            "## Gaps",
            "",
            "| Source Control | Title | Domain | Tags |",
            "| --- | --- | --- | --- |",
        ]
    )

    if summary["gaps"]:
        for gap in summary["gaps"]:
            tags = ", ".join(gap["tags"])
            lines.append(
                f"| {gap['control_id']} | {gap['title']} | {gap['domain']} | {tags} |"
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
    report_content = build_markdown_report(summary, mappings)
    output_path.write_text(report_content, encoding="utf-8")
