# PermitFlow Automator

PermitFlow Automator is a local automation tool designed to eliminate manual file renaming and data extraction during permit-related data entry workflows.

It continuously watches a scan directory, extracts permit metadata directly from newly scanned PDFs, verifies addresses when required, writes assigned address information back into the PDF, renames the file according to official permit conventions, and logs extracted data for reference.

The goal is not AI interpretation, but deterministic removal of repetitive clerical steps.

---

## Problem Statement

Scanned permit PDFs typically arrive with generic filenames (e.g. `Scan001.pdf`).  
Before they can be filed or processed, each document must be:

- Opened manually
- Inspected for permit identifiers
- Verified for assigned address accuracy
- Renamed to a strict naming convention
- Logged externally

This process is repetitive, time-consuming, and error-prone at scale.

---

## What This Tool Does

### Automated Pipeline

1. **Directory Watching**
   - Continuously monitors a folder for newly scanned PDF files.
   - Ignores already-processed permit files.

2. **PDF Data Extraction**
   - Extracts permit-related fields directly from PDF text:
     - Permit number
     - Applicant name
     - Phone number
     - Mailing address
     - Assigned / new address
   - Detects `NO ADDRESS NEEDED` cases automatically.

3. **Address Verification**
   - Prompts for confirmation only when an address is detected.
   - Allows immediate correction before committing changes.

4. **PDF Modification**
   - Writes the assigned address visibly onto the first page of the PDF.
   - Ensures downstream clarity without reopening the document.

5. **Deterministic File Renaming**
   - Renames files based on extracted permit identifiers:
     - `LUP-YYYY-###`
     - `CUP-YYYY-###`
     - `NA-YYYY-###`
   - Supports multiple identifiers when present.

6. **Audit Logging**
   - Appends extracted fields to `extracted_info.txt`.

7. **Directory Hygiene**
   - Moves completed permit files out of the scan directory automatically.

---

## Why This Exists

This tool removes:
- Repetitive decision-making
- Manual transcription errors
- Constant context switching during data entry

It replaces them with a predictable, auditable workflow that runs locally and requires no cloud services.

---

## Requirements

- Python 3.9+
- PyQt5
- PyPDF2
- pdfminer.six
- reportlab

---

## Usage

### GUI Mode
```bash
python gui.py
```
