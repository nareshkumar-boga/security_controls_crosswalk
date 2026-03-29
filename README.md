# control-crosswalk

`control-crosswalk` is a beginner-friendly Python project for defensively mapping security controls across frameworks. It loads control libraries from CSV files, normalizes them into a shared structure, compares controls using tags, highlights likely mappings with confidence scores, identifies gaps, and exports both terminal output and a Markdown report.

## Features

- Load control libraries from CSV files
- Validate required control columns before processing
- Normalize records into a consistent Python structure
- Compare controls using shared security tags and keywords
- Generate mappings with `High`, `Medium`, and `Low` confidence
- Identify source controls that do not map to any target control
- Print a readable terminal summary
- Save a Markdown report to `output/report.md`
- Use only the Python standard library

## Supported Framework Examples

- NIST CSF
- ISO 27001
- CIS Controls
- PCI DSS
- MITRE ATT&CK

The starter project includes sample CSV files for NIST CSF and ISO 27001, but the code is designed so you can add other frameworks in the same format.

## Folder Structure

```text
control-crosswalk/
|-- README.md
|-- requirements.txt
|-- main.py
|-- data/
|   |-- iso27001.csv
|   `-- nist_csf.csv
|-- output/
|   `-- .gitkeep
`-- src/
    |-- __init__.py
    |-- gap_analysis.py
    |-- loader.py
    |-- mapper.py
    |-- normalizer.py
    `-- reporter.py
```

## CSV Input Format

Each CSV file should contain the following columns:

- `framework`
- `control_id`
- `title`
- `description`
- `domain`
- `tags`

The `tags` column must use semicolon-separated values such as:

```text
access; identity; authentication
```

## How It Works

1. Load source and target control libraries from CSV.
2. Validate that each file contains the expected columns.
3. Normalize blank values and tag formatting.
4. Compare every source control to every target control.
5. Score the mapping based on shared tags.
6. Keep only mappings with at least one shared tag.
7. Identify source controls with no matches.
8. Print a terminal summary and write `output/report.md`.

Confidence scoring:

- `High`: 3 or more shared tags
- `Medium`: 2 shared tags
- `Low`: 1 shared tag

## How to Run

Make sure you have Python installed, then run:

```bash
python main.py
```

The project has already been tested successfully with Python `3.8.10`.

## How To Use This Project

### 1. Open the project folder

Open a terminal in the project root:

```bash
cd control-crosswalk
```

### 2. Review the input files

By default, the tool compares:

- `data/nist_csf.csv` as the source framework
- `data/iso27001.csv` as the target framework

Each CSV row must follow this structure:

```csv
framework,control_id,title,description,domain,tags
NIST CSF,PR.AC-01,Identity And Access Management,Manage identities and access,Protect,access; identity; authentication
```

Tips for good results:

- Keep the column names exactly the same
- Separate tags with semicolons
- Use consistent security terms across frameworks
- Prefer specific tags like `authentication`, `vulnerability`, or `incident`
- Avoid overly vague tags unless you want broader matching

### 3. Run the tool

From the project root, execute:

```bash
python main.py
```

### 4. Read the terminal output

The script prints:

- source and target framework names
- total source controls
- total target controls
- total mappings found
- total unmapped source controls
- each mapping with shared tags and confidence level

Example:

```text
Control Crosswalk Report
Source Framework: NIST CSF
Target Framework: ISO 27001

Summary
- Total source controls: 5
- Total target controls: 5
- Total mappings: 15
- Total gaps: 0
```

### 5. Open the Markdown report

After the script runs, open:

- `output/report.md`

The report includes:

- report title
- source and target framework names
- summary counts
- detailed mapping table
- gaps table

### 6. Use your own control libraries

To compare different frameworks:

1. Add your CSV files under `data/`
2. Keep the same required columns
3. Update the file paths in `main.py`
4. Run `python main.py` again

These lines in `main.py` control the input files:

```python
source_path = Path("data/nist_csf.csv")
target_path = Path("data/iso27001.csv")
```

You can change them to files such as:

```python
source_path = Path("data/cis_controls.csv")
target_path = Path("data/pci_dss.csv")
```

### 7. Understand the results

A mapping is created when a source control and target control share at least one tag.

Confidence levels mean:

- `High`: strong overlap, usually a good candidate mapping
- `Medium`: moderate overlap, useful for review
- `Low`: weak overlap, likely needs human validation

A gap means a source control did not match any target control using the current tags.

If you see too many low-confidence mappings or too many gaps:

- refine the tags in your CSV files
- use more specific keywords
- align naming across frameworks
- remove duplicate or noisy tags

## Sample Terminal Output

```text
Control Crosswalk Report
Source Framework: NIST CSF
Target Framework: ISO 27001

Summary
- Total source controls: 5
- Total target controls: 5
- Total mappings: 15
- Total gaps: 0

Mappings
- DE.CM-01 -> A.5.24 | shared tags: incident, logging, monitoring | confidence: High
- DE.CM-01 -> A.8.15 | shared tags: incident, logging, monitoring | confidence: High
- ID.AM-01 -> A.5.9 | shared tags: asset, inventory, risk | confidence: High
```

Actual results depend on the CSV content you provide.

## Output

After a successful run, the project generates:

- terminal summary output
- `output/report.md`

## Extending the Project

You can add more framework CSV files for:

- CIS Controls
- PCI DSS
- MITRE ATT&CK
- internal control catalogs
- custom policy libraries

As long as the input format stays consistent, the same workflow will work.

## Roadmap

- Add CLI arguments for selecting source and target files
- Add support for weighted keywords beyond tags
- Add fuzzy title and description matching
- Export JSON and CSV mapping results
- Add tests for loader, mapper, and reporting
- Add optional framework-to-framework batch comparison

## Security And Ethical Use

This project is intended for defensive cybersecurity, governance, risk, and compliance analysis. It helps analysts understand alignment and gaps across security frameworks. It should not be used to misrepresent compliance, automate audit conclusions without review, or make security claims without human validation.

## License

No license file is included by default. Add one that matches your intended usage before distribution.
