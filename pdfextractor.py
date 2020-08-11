#! /usr/bin/python3

import os,distro
import sys
import re
import cv2
import json
import requests
import pytesseract
import numpy as np
import pandas as pd
import mysql.connector
import pymssql
import shutil
import urllib
import pdftotext
from time import sleep
from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
from distutils.dir_util import copy_tree
from smb.SMBConnection import SMBConnection
from xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common import exceptions as E
from datetime import datetime,timedelta
from dateutil.parser import parse
from tabula import read_pdf
import tabula


header = ['discom_name','bill_for','gst_number','bill_number','bill_date','bill_period','cin','website','email']
dict1 = {}
dict1 = { 'header': { },  
         'client': { }} 
file1 = open("abc.txt","r") 
a = file1.readlines()
txt1 = ''
for n,i in enumerate(a):
    txt1+=i.replace('                       ','</tr>')+'<tr={}>'.format(n)
    # txt1+=i
# print (txt1)
print ('****************************************************************************************')

c4 = re.compile('FOR(.*?)GST:', re.DOTALL)
v1 = c4.search(str(txt1), re.IGNORECASE).group(1).strip()
c5 = re.compile('GST:\s+(.*?)Bill', re.DOTALL)
v2 = c5.search(str(txt1), re.IGNORECASE).group(1).strip()
c6 = re.compile('Bill No.: (.*?)Bill Date', re.DOTALL)
v3 = c6.search(str(txt1), re.IGNORECASE).group(1).strip()
c7 = re.compile('Bill Date:(.*?)Bill Period', re.DOTALL)
v4 = c7.search(str(txt1), re.IGNORECASE).group(1).strip()
c8 = re.compile('Bill Period:(.*?)CIN:', re.DOTALL)
v5 = c8.search(str(txt1), re.IGNORECASE).group(1).strip()
c9 = re.compile('CIN:(.*?)Website:', re.DOTALL)
v6 = c9.search(str(txt1), re.IGNORECASE).group(1).strip()
c10 = re.compile('Website:(.*?)E-mail:', re.DOTALL)
v7 = c10.search(str(txt1), re.IGNORECASE).group(1).strip()
c11 = re.compile('E-mail:(.*?)\s{4}', re.DOTALL)
v8 = c11.search(str(txt1), re.IGNORECASE).group(1).strip()

######################## client #############################
comp_name = str(a[7]).strip()
d1 = re.compile('<tr=8>.*?</tr>.*?</tr></tr>.*?<tr=9>(.*?)</tr>', re.DOTALL)
a1 = d1.search(str(txt1), re.IGNORECASE).group(1).strip()
d2 = re.compile('<tr=12>.*?Phone -(.*?)</tr>', re.DOTALL)
a2 = d2.search(str(txt1), re.IGNORECASE).group(1).strip()
d3 = re.compile('<tr=12>.*?E-mail -(.*?)</tr>', re.DOTALL)
a3 = d3.search(str(txt1), re.IGNORECASE).group(1).strip()
################################ subdivision ########################
d4 = re.compile('<tr=7></tr>.*?</tr>(.*?)<tr=8>', re.DOTALL)
a4 = d4.search(str(txt1), re.IGNORECASE).group(1).strip()
d5 = re.compile('<tr=10></tr></tr>(.*?)<tr=11>', re.DOTALL)
a5 = d5.search(str(txt1), re.IGNORECASE).group(1).strip().replace('\n','')
d6 = re.compile('<tr=11></tr></tr>(.*?)</tr></tr>', re.DOTALL)
a6 = d6.search(str(txt1), re.IGNORECASE).group(1).strip()
combo = a5 +' '+a6 
d7 = re.compile('Office Code:(.*?)<tr=13>', re.DOTALL)
a7 = d7.search(str(txt1), re.IGNORECASE).group(1).strip()
########################## complaint_center ################################
d8 = re.compile('<tr=11></tr></tr>.*?</tr></tr>(.*?)<tr=12>', re.DOTALL)
a8 = d8.search(str(txt1), re.IGNORECASE).group(1).strip()
d9 = re.compile('<tr=13>.*?</tr></tr></tr></tr>(.*?)<tr=14>', re.DOTALL)
a9 = d9.search(str(txt1), re.IGNORECASE).group(1).strip()
combo2 = a8+','+a9
########################### due_details ######################################
d10 = re.compile('<tr=17>(.*?)</tr>', re.DOTALL)
a10 = d10.search(str(txt1), re.IGNORECASE).group(1).strip()
d11 = re.compile('<tr=21>(.*?)<tr=22>', re.DOTALL)
a11 = d11.search(str(txt1), re.IGNORECASE).group(1).strip()
d12 = re.compile('Due Date Amount:(.*?)<tr=47>', re.DOTALL)
a12 = d12.search(str(txt1), re.IGNORECASE).group(1).strip()
d13 = re.compile('Amt after Due Date:(.*?)<tr=48>', re.DOTALL)
a13 = d13.search(str(txt1), re.IGNORECASE).group(1).strip()
########################### plan #######################################
d14 = re.compile('Due Date</tr></tr>(.*?)<tr=20>', re.DOTALL)
a14 = d14.search(str(txt1), re.IGNORECASE).group(1).strip()
a14 = a14.split('      ')
d15 = re.compile('<tr=22></tr></tr></tr>(.*?)Consumer Status', re.DOTALL)
a15 = d15.search(str(txt1), re.IGNORECASE).group(1).strip()
d16 = re.compile('Total Amt. after Due Date:</tr>.*?</tr>(.*?)<tr=25>', re.DOTALL)
a16 = d16.search(str(txt1), re.IGNORECASE).group(1).strip()
a16 = a16.split('      ')
############################### meter_reading ##############################################
d17 = re.compile('Current Reading Date.*?:(.*?)<tr=16>', re.DOTALL)
a17 = d17.search(str(txt1), re.IGNORECASE).group(1).strip()
d18 = re.compile('Previous Reading Date.*?:(.*?)<tr=19>', re.DOTALL)
a18 = d18.search(str(txt1), re.IGNORECASE).group(1).strip()
d19 = re.compile('Consumption.*?:(.*?)<tr=21>', re.DOTALL)
a19 = d19.search(str(txt1), re.IGNORECASE).group(1).strip()
d20 = re.compile('Trans. Loss.*?:(.*?)<tr=23>', re.DOTALL)
a20 = d20.search(str(txt1), re.IGNORECASE).group(1).strip()
d21 = re.compile('<tr=25></tr></tr></tr></tr></tr></tr>.*?:(.*?)<tr=26>', re.DOTALL)
a21 = d21.search(str(txt1), re.IGNORECASE).group(1).strip()
################################### account ##################################################
d22 = re.compile('<tr=29></tr></tr></tr></tr>(.*?)<tr=30>', re.DOTALL)
a22 = d22.search(str(txt1), re.IGNORECASE).group(1).strip()
d23 = re.compile('<tr=29></tr></tr></tr></tr>(.*?)<tr=30>', re.DOTALL)
a23 = d23.search(str(txt1), re.IGNORECASE).group(1).strip()
################################# last_payment_detail #######################################
d24 = re.compile('<tr=32></tr></tr></tr></tr>(.*?)<tr=33>', re.DOTALL)
a24 = d24.search(str(txt1), re.IGNORECASE).group(1).strip()
a24 = str(a24).split('      ')
############################## discom_payment #######################################
d25 = re.compile(' BENEFICIARY NAME(.*?)<tr=36>', re.DOTALL)
a25 = d25.search(str(txt1), re.IGNORECASE).group(1).strip()
d26 = re.compile('A/C NO.</tr>(.*?)<tr=37>', re.DOTALL)
a26 = d26.search(str(txt1), re.IGNORECASE).group(1).strip()
d27 = re.compile('IFSC CODE</tr>(.*?)<tr=38>', re.DOTALL)
a27 = d27.search(str(txt1), re.IGNORECASE).group(1).strip()
d28 = re.compile('BANK BRANCH(.*?)<tr=39>', re.DOTALL)
a28 = d28.search(str(txt1), re.IGNORECASE).group(1).strip()
############################## meter_reading_detail part 1 ##################################
d29 = re.compile('<tr=53>(.*?)<tr=54>', re.DOTALL)
a29 = d29.search(str(txt1), re.IGNORECASE).group(1).strip()
a29 = a29.split('      ')
############################## meter_reading_detail part 2 ##################################
d30 = re.compile('<tr=54>(.*?)<tr=55>', re.DOTALL)
a30 = d30.search(str(txt1), re.IGNORECASE).group(1).strip()
a30 = a30.split('      ')
############################## meter_reading_detail part 3 ##################################
d31 = re.compile('<tr=55>(.*?)<tr=56>', re.DOTALL)
a31 = d31.search(str(txt1), re.IGNORECASE).group(1).strip()
a31 = a31.split('      ')
############################ allowed_service ##############################
d32 = re.compile('<tr=59>(.*?)<tr=65>', re.DOTALL)
a32 = d32.search(str(txt1), re.IGNORECASE).group(1).strip()
a32 = a32.split('     ')
################################ particulars ###########################################
d33 = re.compile('</tr> Bill Amount(.*?)<tr=82>', re.DOTALL)
a33 = d33.search(str(txt1), re.IGNORECASE).group(1).strip()
# print (a33)
a33 = a33.split('.            ')
part = []
for i in a33:
    part2=[]
    for p,j in enumerate(i.split('\n')):
        part2.append(j)
    part.append(part2)
part3=[]
for t1 in part:
    if len(t1)>=1:
        for t2 in t1:
            t2 = re.sub('<tr.*?>|</tr>|    ','',str(t2)).strip()
            part3.append(t2)
    else:
        pass
last=[]
for t4 in part3:
    t4 = re.sub('^\d{1,2}.','',str(t4)).strip()
    t4 = re.sub(r'\s{1,}\d+$', '', t4)
    if t4.startswith('Power Factor') or t4.startswith('Shunt Capacitor') or t4.startswith('Unauthorized Consumption'):
        # t4=re.split("\d{2,}\s*\(....", t4)
        t4=re.split("\d{2,}\s*\(....", t4)
        for k2 in t4:
            last.append(k2)
    last.append(t4)
print (last)
print (len(last))




        # for v,t in enumerate(j):
        #     print (v,t)
        # if len(j) >1:
        #     for t in j:
        #         part2.append(t)
        # else:
        #     for t in j

        






#     part.append(part2)
# print ('final data = = = = = =',len(part))
# d34 = re.compile('<tr=.*?>.*?\d{1,2}.(.*?)\s{11}\d{1,5}.', re.DOTALL)
# a34 = d34.findall(str(a33), re.IGNORECASE)
# # print (a34)
# for i in a34:
#     print (i)





# dict1['header']={'discom_name':a[0],'bill_for':v1}

#     # c4 = re.compile('<tbody>(.*?)</tbody>', re.DOTALL)
#     # v1 = c4.search(str(i), re.IGNORECASE).group(1)
# print (dict1)
file1.close()










# df = read_pdf('KOT074.pdf')
# print (df[])
# df[1].to_csv('file2.csv', header=True, index=True) 






# path = 'KOT074.pdf'
# df = tabula.read_pdf(path, pages = '2', multiple_tables = True, output_format='json')
# for i in df:
#     print (i)
#     # for j in i:
#     #     print (j)




# dict1 = {}
# with open('KOT074.pdf','rb') as f:
#     pdf=pdftotext.PDF(f)
#     for j in pdf:
#         print (j)
        
        # json_data = json.dumps(j, indent=10)
       



        # l2=str(j).split('\n')
        # print (l2)
        # l1=[]
        # for k in l2:
        #     name = re.sub('\s{2,5}','<tr>',k)
        #     name = re.sub('<tr>{1,}','>',name)
        #     name = re.sub('>>','',name)
        #     if name.startswith('>'):
        #         l1.append(name)
        # print (l1)


        #     # l3 = k.split('\n')
        #     for l in k:
        #         print (l)
        #         # name = re.sub('^\s*','',l)
        #         # print (name)
        #         # print ('*****************************************')
