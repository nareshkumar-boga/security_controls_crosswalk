# Security Controls Crosswalk

`security_controls_crosswalk` is a defensive cybersecurity utility that maps controls across frameworks using shared tags and keywords.  
It helps analysts compare coverage, identify likely control alignments, and detect gaps where source controls have no target match.

## Overview

Security teams often need to translate one framework into another (for example, NIST CSF to ISO 27001).  
This project ingests control libraries from CSV files, normalizes them, calculates shared-tag overlap, scores mapping confidence, and produces both terminal and Markdown reports.

## Features

- Load source and target framework controls from CSV
- Validate required CSV columns before processing
- Normalize records and semicolon-separated tags safely
- Compare every source control with every target control
- Score mappings by shared tags:
  - `High` for 3 or more
  - `Medium` for 2
  - `Low` for 1
- Identify source controls with no matches
- Print a readable terminal summary
- Generate a professional report at `output/report.md`
- Use only the Python standard library

## Supported Frameworks

The tool is framework-agnostic and supports any control catalog in the required CSV format.  
Typical examples include:

- NIST CSF
- ISO 27001
- CIS Controls
- PCI DSS
- MITRE ATT&CK

## Project Structure

```text
security_controls_crosswalk/
|-- README.md
|-- requirements.txt
|-- main.py
|-- data/
|   |-- nist_csf.csv
|   `-- iso27001.csv
|-- output/
|   `-- .gitkeep
|-- src/
|   |-- __init__.py
|   |-- loader.py
|   |-- normalizer.py
|   |-- mapper.py
|   |-- gap_analysis.py
|   `-- reporter.py
`-- tests/
    |-- __init__.py
    |-- test_loader.py
    |-- test_normalizer.py
    `-- test_mapper.py
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/nareshkumar-boga/security_controls_crosswalk.git
cd security_controls_crosswalk
```

2. Ensure Python is installed (3.8+ recommended):

```bash
python --version
```

No third-party dependencies are required.

## CSV Input Format

Each CSV must include these columns:

- `framework`
- `control_id`
- `title`
- `description`
- `domain`
- `tags`

`tags` must be semicolon-separated values.

Example:

```csv
framework,control_id,title,description,domain,tags
NIST CSF,PR.AC-01,Identity And Access Control,Enforce access policy,Protect,access; identity; authentication
```

## Usage

### Default run

```bash
python main.py
```

This compares:

- source: `data/nist_csf.csv`
- target: `data/iso27001.csv`
- output: `output/report.md`

### Custom run

```bash
python main.py --source data/cis_controls.csv --target data/pci_dss.csv --output output/cis_to_pci.md
```

### Run tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Sample Output

```text
========================================================================
Control Crosswalk Report
========================================================================
Generated: 2026-03-29 11:20:00 UTC
Source Framework: NIST CSF
Target Framework: ISO 27001

Summary
- Total source controls: 5
- Total target controls: 5
- Source controls mapped: 5
- Total mappings: 10
- Total gaps: 0
```

The generated Markdown report includes summary metrics, detailed mappings, and gap analysis tables.

## Roadmap

- Add optional weighting for high-value tags
- Add optional minimum confidence filter in CLI
- Export mapping output as JSON and CSV
- Add integration tests for report generation
- Add batch mode for framework-to-framework comparisons

## Security And Ethical Use

This tool is intended for defensive cybersecurity, governance, risk, and compliance analysis.  
Results should support human review, not replace audit judgment or be used to misrepresent compliance status.

## License

This repository includes a [LICENSE](LICENSE) file. Review it before reuse or redistribution.
