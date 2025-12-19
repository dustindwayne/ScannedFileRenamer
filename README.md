# Scanned File Renamer

Rename permit PDFs using the permit number extracted from the first page of the file.

## Requirements

- Python 3.8+
- [`pypdf`](https://pypi.org/project/pypdf/)

Install dependencies:

```bash
pip install pypdf
```

## Usage

Provide the path to a permit PDF. The script will extract permit numbers matching `LUP/NA/FP/CUP-20XX-XXX` (or similar) from the first page, join multiple matches with underscores, and rename the file in place while preserving its original extension.

```bash
python scannedFileRenamer.py path/to/permit.pdf
```

If multiple permit numbers are found, the renamed file will combine them, e.g., `LUP-2024-001_CUP-2024-015.pdf`. If no permit number is found, the script will raise an error when attempting to rename; verify the PDF text content in that case.
