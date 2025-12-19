from pypdf import PdfReader
import re
import sys
import os

def extract_permit_number(permit):
    reader = PdfReader(permit)
    page = reader.pages[0]
    text = page.extract_text()
    permitnumber = re.findall(r'(?:LUP|NA|FP|CUP){1,2}[- ]20\d{2}-\d{2,3}',str(text))
    rename_permit(permit, permitnumber)

def rename_permit(permit_path, matched_names):
    filename = '_'.join([i for i in matched_names])
    print(filename)    
    directory = os.path.dirname(permit_path)
    original_extension = os.path.splitext(permit_path)[1]
    os.rename(permit_path, os.path.join(directory, filename + original_extension))  

if __name__ == "__main__":
    permit = sys.argv[1]
    extract_permit_number(permit)

# python scannedFileRenamer.py <pdf file here>
