import os
import re
import time
import shutil
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pdfminer.high_level import extract_pages


def process_pdf(pdf_path, address_callback=None):
    try:
        reader = PdfReader(pdf_path)
        text = "".join(page.extract_text() or "" for page in reader.pages)

        no_address_needed = "NO ADDRESS NEEDED" in text

        patterns = {
            "New Address": r"New Address:\s*(.*)"
        }

        address_match = re.search(patterns["New Address"], text, re.IGNORECASE)
        new_address = address_match.group(1).strip() if address_match else ""

        if address_callback and new_address:
            new_address = address_callback(new_address)

        writer = PdfWriter()
        first_page = reader.pages[0]
        _overlay_address(writer, first_page, new_address, no_address_needed)

        for page in reader.pages[1:]:
            writer.add_page(page)

        with open(pdf_path, "wb") as f:
            writer.write(f)

        new_name = rename_pdf(pdf_path)
        return f"Processed and renamed: {new_name}"

    except Exception as e:
        return f"Error processing {pdf_path}: {e}"


def _overlay_address(writer, page, address, no_address_needed):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.setFont("Helvetica", 12)

    x, y = 400, 500
    if not no_address_needed:
        c.drawString(x, y, "Assigned Address:")
        c.drawString(x, y - 15, address)
    else:
        c.drawString(x, y, "NO ADDRESS NEEDED")

    c.save()
    packet.seek(0)
    overlay = PdfReader(packet)
    page.merge_page(overlay.pages[0])
    writer.add_page(page)


def rename_pdf(path):
    folder = os.path.dirname(path) or "."
    content = []
    for layout in extract_pages(path):
        content.extend(str(e) for e in layout)

    matches = re.findall(r'(LUP|CUP|NA)[- ]20\d{2}-\d+', str(content))
    if not matches:
        raise RuntimeError("Permit identifier not found")

    new_name = "_".join(matches) + ".pdf"
    new_path = os.path.join(folder, new_name)
    os.rename(path, new_path)
    return new_path


def scan_directory(folder, address_callback=None):
    processed = set()
    while True:
        for name in os.listdir(folder):
            path = os.path.join(folder, name)
            if name.startswith("Scan") and name.endswith(".pdf") and name not in processed:
                time.sleep(2)
                yield process_pdf(path, address_callback)
                processed.add(name)
            elif name.endswith(".pdf") and name[:3] in ("LUP", "CUP", "NA"):
                shutil.move(path, os.path.join(folder, "..", name))
        time.sleep(1)
