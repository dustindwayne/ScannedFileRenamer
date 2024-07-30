import sys, re, os
from pdfminer.high_level import extract_pages
pgs = []
def nameme(fnpdf):
    for page_layout in extract_pages(fnpdf):
        for element in page_layout:
            pgs.append(element)
    #the regex is looking for LUP,NA,FP and returns all that it finds
    filename_to_save_as = re.findall('[LUP,NA,FP]{2,3}[-, ]202[0-9]{1}-[0-9]{2,3}',str(pgs))
    print(filename_to_save_as)
    if len(filename_to_save_as) > 1:
        fiName = filename_to_save_as[0] + "_" + filename_to_save_as[1] + ".pdf"
        fiName[::4].replace('-',' ')
        os.rename(fnpdf, str(fiName))
    else:
        fiName = filename_to_save_as[0] + ".pdf"
        fiName[:4].replace('-',' ')
        os.rename(fnpdf, str(fiName))  

#this is so it can process multiple files at once
for i in sys.argv[1:]:
    nameme(i)  
    pgs = []
