from pypdf import PdfReader
import re
import sys
import os

def extract_permit_number(permit):
    reader = PdfReader(permit)
    page = reader.pages[0]
    text = page.extract_text()
    permitnumber = re.findall(r'(?:LUP|NA|FP|CUP){1,2}[- ]20\d{2}-\d{2,3}',str(text))
    rename_permit(permitnumber)

def rename_permit(newName):
    filename = '_'.join([i for i in newName])
    print(filename)    
    os.rename(os.path.join(directory,permit), os.path.join(directory, filename))  

if __name__ == "__main__":
    permit = sys.argv[1]
    filetype = os.path.splitext(permit)
    directory = os.path.dirname(permit)
    print(directory)
    extract_permit_number(permit)
