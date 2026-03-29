"""Entry point for the control crosswalk tool."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.gap_analysis import summarize_results
from src.loader import load_controls_from_csv
from src.mapper import map_controls
from src.normalizer import normalize_controls
from src.reporter import print_console_summary, write_markdown_report


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Map security controls across framework CSV files."
    )
    parser.add_argument(
        "--source",
        default="data/nist_csf.csv",
        help="Path to source framework CSV file.",
    )
    parser.add_argument(
        "--target",
        default="data/iso27001.csv",
        help="Path to target framework CSV file.",
    )
    parser.add_argument(
        "--output",
        default="output/report.md",
        help="Path to generated Markdown report.",
    )
    return parser.parse_args()


def run(source_path: Path, target_path: Path, output_path: Path) -> None:
    """Run the complete control crosswalk workflow."""
    source_controls = normalize_controls(load_controls_from_csv(source_path))
    target_controls = normalize_controls(load_controls_from_csv(target_path))

    mappings = map_controls(source_controls, target_controls)
    summary = summarize_results(source_controls, target_controls, mappings)

    print_console_summary(summary, mappings)
    write_markdown_report(summary, mappings, output_path)
    print()
    print(f"Markdown report saved to: {output_path}")


def main() -> int:
    """Program entry point that returns an OS status code."""
    args = parse_args()
    try:
        run(Path(args.source), Path(args.target), Path(args.output))
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
