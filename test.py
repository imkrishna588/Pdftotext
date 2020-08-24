## Python Related Modules and Dependencies
import os
import sys
import re
import json
import pdfplumber

# def with_pdfplumber(src_path):
#     with pdfplumber.open(src_path) as pdf:
#         list1 =[]
#         words =[]
#         tables=[]
#         for txt_pg in pdf.pages:
#             list1.append(txt_pg)
#             # self.get_header()
#             words.extend(txt_pg.extract_words())
#             tables.extend(txt_pg.extract_tables(table_settings={}))
#         print (list1)
#         print (words)
#         # print (tables)

# path = 'smart.pdf'
# with_pdfplumber(path)

with pdfplumber.open('smart.pdf') as pdf:
    for txt_pg in pdf.pages:
        text1 = txt_pg.extract_text()
        try:
            with open ("text.html", "a") as output:
                file1 = text1.replace("\n", "<br>")
                output.write(file1)
        except:
            pass

with open("text.html") as file1:
#     with open ("text.html", "a") as output:
        file1 = file1.read()
        v0 = re.search('DUPLICATE BILL(.*?)<br>',str(file1), re.IGNORECASE).group(1)
        print (v0)