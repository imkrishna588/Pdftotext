## Python Related Modules and Dependencies
import os
import sys
import re
import json
# import pdfplumber

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

# with pdfplumber.open('smart.pdf') as pdf:
#     for txt_pg in pdf.pages:
#         text1 = txt_pg.extract_text()
#         try:
#             with open ("text.html", "a") as output:
#                 file1 = text1.replace("\n", "<br>")
#                 output.write(file1)
#         except:
#             pass

with open("text.html") as file1:
#     with open ("text.html", "a") as output:
        file1 = file1.read()
        dup_bill = re.search('DUPLICATE BILL(.*?)<br>',str(file1), re.IGNORECASE).group(1)
        name = re.search('Name:(.*?)Sanctioned',str(file1), re.IGNORECASE).group(1).strip()
        bill_no = re.search('Bill No.*?(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        bill_date = re.search('Bill Date(.*?)<br',str(file1), re.IGNORECASE).group(1).strip()
        bill_address = re.search('Billing Address:(.*?)Security Deposit',str(file1), re.IGNORECASE).group(1).strip() + ' '+re.search('Billing Address:.*?<br>(.*?)Power Factor',str(file1), re.IGNORECASE).group(1).strip() 
        supp_address = re.search('Supply Address:(.*?)Zone',str(file1), re.IGNORECASE).group(1).strip()+' '+ re.search('Supply Address:.*?<br>(.*?)MRU No',str(file1), re.IGNORECASE).group(1).strip()
        mobile = re.search('Mobile/Tel No.(.*?)Pole',str(file1), re.IGNORECASE).group(1).strip()
        email = re.search('E-mail(.*?)Bill No',str(file1), re.IGNORECASE).group(1).strip()
        sanctioned = re.search('Sanctioned Load (.*?)CA No',str(file1), re.IGNORECASE).group(1)
        sanctioned = float(re.search(r'\d+', sanctioned).group(0))
        district = re.search('District(.*?)Connection Type',str(file1), re.IGNORECASE).group(1).strip()
        zone = re.search('Zone(.*?)Tariff Category',str(file1), re.IGNORECASE).group(1).strip()
        mru_no = re.search('MRU No(.*?)Bill Basis',str(file1), re.IGNORECASE).group(1).strip('.| ')
        walking_seq = re.search('Walking Sequence(.*?)Bill Remark',str(file1), re.IGNORECASE).group(1).strip()
        pole = re.search('Pole/Pillar No(.*?)Bill Date',str(file1), re.IGNORECASE).group(1).strip('.| ')
        ca_num = re.search('CA No(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        energisation_date = re.search('Energisation Date(.*?)<br',str(file1), re.IGNORECASE).group(1).strip()
        security_dep = re.search('Security Deposit(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        connect_type = re.search('Connection Type(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        tariff_cat = re.search('Tariff Category(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        bill_basis = re.search('Bill Basis(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        bill_remark = re.search('Bill Remark(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        ppac = re.search('PPAC On Fixed  Charges(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        ppac_energy_charge = re.search('PPAC On Energy  Charges(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        ppac_fixed_charge = re.search('PPAC On Fixed Charges(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        diff_ppac_energy_charge = re.search('Differential  PPAC On Energy  Charges(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        ppac_energy_charge = re.search('PPAC On Energy  Charges(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        on_fixed_charge = re.search('On Fixed  Charge @8%(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        on_energy_charge = re.search('On Energy Charges @8%(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        on_fixed_charge2 = re.search('Pension Trust Surcharge.*?On Fixed Charge(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        on_energy_charge2 = re.search('Pension Trust Surcharge.*?On Fixed Charge.*?On Energy charge(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        electricity_tax = re.search('Electricity Tax  @5% ......(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        net_current_demand = re.search('Electricity Tax.*?<br>(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        variable = re.search('Electricity Tax.*?<br>.*?<br>(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ').split()
        total_payble_amount = variable[-1]
        adujustment_amount = variable[-2]
        bill_period_from_date = re.search('Bill Period(.*?)to',str(file1), re.IGNORECASE).group(1).strip('.| ')
        bill_period_to_date = re.search('Bill Period.*?to(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        consider_days = re.search('considering Days:(.*?)Month',str(file1), re.IGNORECASE).group(1).strip('.| ')
        months = re.search('Month:(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        phase_status = re.search('Status.*?:OK(.*?)\s+\d+',str(file1), re.IGNORECASE).group(1).strip(',| ')
        due_date = re.search('Status.*?:OK.*?\s+\d(.*?)<br',str(file1), re.IGNORECASE).group(1).strip(',| ')
        reading_num = re.search('Bill No.*?No(.*?),MF',str(file1), re.IGNORECASE).group(1).strip('.| ')
        mf = re.search('MF=(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        variable2 = re.search('<br>KWH(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ').split()
        current_month_units = variable2[-3]
        last_month_units = variable2[-2]
        consumed_unit = variable2[-1]
        mdi_kw = re.search('<br>MDI KW(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        company_name = re.search('<br>for(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')
        # ca_num = re.search('CA No(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip('.| ')





        print (company_name)
        
        dup_bill = re.search('DUPLICATE BILL(.*?)<br>',str(file1), re.IGNORECASE).group(1)
        dup_bill = re.search('DUPLICATE BILL(.*?)<br>',str(file1), re.IGNORECASE).group(1)
        