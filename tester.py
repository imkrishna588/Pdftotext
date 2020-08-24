#! /usr/bin/python3

# import PyPDF2 as pypdf


# import PyPDF2
# import collections
# import json
# import pdftotext

# pdf_file = open('smart.pdf', 'rb')
# read_pdf = PyPDF2.PdfFileReader(pdf_file)
# number_of_pages = read_pdf.getNumPages()
# c = collections.Counter(range(number_of_pages))
# for i in c:
#    page = read_pdf.getPage(i)
#    page_content = page.extractText()
#    print (page_content)



# with open("smart.pdf", "rb") as f:
#     pdf = pdftotext.PDF(f)
#     for line in pdf:
#         # print (line)
#         command, description = line.strip().split(None, 1)
#         print (command,description)
#         print ('*******************************************')
    
# #     with open("stringJson.txt", "wb") as fout:
#         json.dump(pdf, fout, indent=1)

import pdfplumber
import pandas as pd
import re
import ast
import json
import pdfkit


# with pdfplumber.open("D:/pdffile/testing/smart.pdf") as pdf:
#     first_page = pdf.pages[0]
#     print(first_page.chars[0])

pdf = pdfplumber.open("D:/pdffile/testing/smart.pdf")
page = pdf.pages[0]
page = page.extract_text()
with open('test.txt','w') as fin:
    fin.write(page)

with open("test.txt") as file1:
    with open ("text.html", "w") as output:
        file1 = file1.read()
        file1 = file1.replace("\n", "<br>")
        output.write(file1)
        
        # #os.startfile("text.txt")
# #os.startfile("text.html")
# pdfkit.from_file("text.html", "output.pdf")


# df5 = pd.DataFrame(page.extract_table())
# print (df5)
# df5.to_csv('hello.csv')