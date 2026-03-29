"""Entry point for the control crosswalk tool."""

from pathlib import Path

from src.gap_analysis import summarize_results
from src.loader import load_controls_from_csv
from src.mapper import map_controls
from src.normalizer import normalize_controls
from src.reporter import print_console_summary, write_markdown_report


def main() -> None:
    """Run the control crosswalk workflow."""
    source_path = Path("data/nist_csf.csv")
    target_path = Path("data/iso27001.csv")

    source_controls = normalize_controls(load_controls_from_csv(source_path))
    target_controls = normalize_controls(load_controls_from_csv(target_path))

    mappings = map_controls(source_controls, target_controls)
    summary = summarize_results(source_controls, target_controls, mappings)

    print_console_summary(summary, mappings)
    write_markdown_report(summary, mappings, Path("output/report.md"))


if __name__ == "__main__":
    main()
