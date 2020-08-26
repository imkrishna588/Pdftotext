## Python Related Modules and Dependencies
import os
import sys
import re
import json
import pdftotext
import pdfplumber
from time import sleep
## Project Related Modules and Dependencies

FILE = "/Users/anilkumargupta/Documents/PyWithAnil/goscale/data/TataDDL_Sample1.pdf"

## Global Variable
class SRCAttr:
    pass

class TataDDL:
    """
    Tata Power Delhi Distribution LTD.
    """
    def __init__(self, extractor="PDF_TO_TEXT", working_folder="/Users/anilkumargupta/Documents/PyWithAnil/goscale/data", src_path=FILE):
        self.src_path = src_path
        self.extractor = extractor
        self.src_data = ''
        self.working_folder = working_folder
        self.working_file_path =  "/Users/anilkumargupta/Documents/PyWithAnil/goscale/data/tatadll.html"
        self.final_data = []
        self.words = []
        self.tables = []
        self.a_v = SRCAttr
        self.read_src_data()        
    
    def read_src_data(self):
        """
        DOCString
        """
        if self.extractor=="PDF_TOTEXT":
            self.with_pdftotext()
        elif self.extractor=="PLUMBER_HTML":
            self.with_pdfplumber_html()
        elif self.extractor=="PLUMBER":
            self.with_pdfplumber()
        else:
            pass
        return self.src_data

    def with_pdftotext(self):
        with open(self.src_path,'rb') as f:
            pdf = pdftotext.PDF(f)
            for txt_ln in pdf:
                self.src_data.append(txt_ln)   
    
    def with_pdfplumber(self):
        with pdfplumber.open(self.src_path) as pdf:
            for txt_pg in pdf.pages:
                self.src_data.append(txt_pg)
    
    def with_pdfplumber_html(self):
        with pdfplumber.open(self.src_path) as pdf:
            html_file = open (self.working_file_path, "a")
            for txt_pg in pdf.pages:
                import pdb;pdb.set_trace()
                text = txt_pg.extract_text()
                if text:
                    html_txt = text.replace("\n", "<br>")
                    html_file.write(html_txt)
            html_file.close()

    def get_header(self):
        hd = self.src_data
        self.a_v.av1 = "DISCOM_NAME", re.search('(.*?)<br>',str(hd), re.IGNORECASE).group(1)
        self.a_v.av2 = "CONN_NO", "Val"
        self.a_v.av3 = "BILL_NO", re.search('Bill No.:(.*?)Bill Date:',str(hd), re.IGNORECASE).group(1).strip()
        self.a_v.av4 = "BILL_DATE", re.search('Bill Date:(.*?)Bill Period',str(hd), re.IGNORECASE).group(1).strip()
        self.a_v.av6 = "BOOK_NO", "Val" #TODO
        self.a_v.av7 = "K_NO", re.search('K. No.:(.*?)Bill No.:',str(hd), re.IGNORECASE).group(1).strip()
        self.a_v.av8 = "DISCONN_DATE", "Val" #TODO
        self.a_v.av9 = "BILLING_ADD", re.search('immediate assistance call.*?\d{6}(.*?)<br>',str(hd), re.IGNORECASE).group(1)+' '+re.search('immediate assistance call.*?\d{6}.*?<br>(.*?)<br>',str(hd), re.IGNORECASE).group(1)+' '+re.search('immediate assistance call.*?\d{6}.*?<br>.*?<br>.*?<br>(.*?)<br>',str(hd), re.IGNORECASE).group(1)
        self.a_v.av10 = "DIVISION_CODE", "Val" #TODO
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(1, 11)]
        self.final_data.extend(av_rows)

    def get_due_details(self):
        due = self.src_data
        self.a_v.av11 = "DUE_DATE", re.search('<br>Due Date.*?<br>.*?<br>(.*?)Consumption',str(file1), re.IGNORECASE).group(1).strip()
        self.a_v.av12 = "DUE_AMT", re.search('Due Date Amount:(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        self.a_v.av13 = "ADJUSTMENT", "Val"
        self.a_v.av14 = "CURR_DUE_AMT",  re.search('Due Date Amount:(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        self.a_v.av15 = "ARREAR_AMT",  "Val"
        self.a_v.av16 = "TTL_CURR_DUE_AMT", re.search('Due Date Amount:(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        self.a_v.av18 = "TTL_DUE_AMT", re.search('Due Date Amount:(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        self.a_v.av19 = "TTL_CURR_DUE_AMT", re.search('Amt after Due Date:(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        self.a_v.av20 = "TTL_ACTL_DUE_AMT", re.search('Amt after Due Date:(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        self.a_v.av21 = "AMT_PAYABLE", re.search('Amt after Due Date:(.*?)<br>',str(file1), re.IGNORECASE).group(1).strip()
        self.a_v.av22 = "AFTER_DUE_AMT", "NA"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(11, 23)]
        self.final_data.extend(av_rows)

# done from here
    def get_charges(self):
        chrg = self.src_data
        self.a_v.av6 = "AMT_MIN_CHRG", "Val" #TODO
        self.a_v.av1 = "CAP_CHRG", "Val" #TODO
        self.a_v.av2 = "REG_SURCHRG_1", "Val" #TODO
        self.a_v.av3 = "REG_SURCHRG_2", "Val" #TODO
        self.a_v.av4 = "MISC_CHRG", "Val" #TODO
        self.a_v.av5 = "REBATEES", "Val" #TODO
        self.a_v.av7 = "FCA_CHRG", "Val" #TODO
        self.a_v.av8 = "GREEN_ENRGY", "Val" #TODO
        self.a_v.av9 = "VLTG_SURCHRG", "Val" #TODO
        self.a_v.av10 = "MAINTENANCE_CHRG","Val"  #TODO
        self.a_v.av10 = "ADD_ENRGY_CHRG", "Val"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(51, 61)]
        self.final_data.extend(av_rows)
    
    def get_discom_payment_details(self):
        pay = self.src_data
        self.a_v.av1 = "EXCESS_LOAD", "Val" #TODO
        self.a_v.av2 = "CON_SPLY_SURCHRG", "Val" #TODO
        self.a_v.av3 = "IT_METERING_SURCHRG", "Val" #TODO
        self.a_v.av4 = "DISH_CHQ", "Val" #TODO
        self.a_v.av5 = "DEBIT", "Val" #TODO
        self.a_v.av6 = "CREDIT", "Val" #TODO
        self.a_v.av7 = "TEMP_PAYMENT", "Val" #TODO
        self.a_v.av8 = "RND_TTL_AMT", "Val" #TODO
        self.a_v.av9 = "src_attr", "Val" #TODO
        self.a_v.av10 = "src_attr","Val"  #TODO
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(91, 101)]
        self.final_data.extend(av_rows)

    def get_meter_details(self):
        mtr = self.src_data
        self.a_v.av61 = "OP_READING_DATE", re.search('Bill Period.*?to(.*?)<br>',str(mtr), re.IGNORECASE).group(1).strip('.| ')
        self.a_v.av62 = "CL_READING_DATE", re.search('Bill Period(.*?)to',str(mtr), re.IGNORECASE).group(1).strip('.| ')
        self.a_v.av63 = "MTR_NO", re.search('Bill No.*?No(.*?),MF',str(mtr), re.IGNORECASE).group(1).strip('.| ')
        self.a_v.av64 = "MF", re.search('MF=(.*?)<br>',str(mtr), re.IGNORECASE).group(1).strip('.| ')
        self.a_v.av65 = "OP_MTR_KWH", re.search('<br>KWH(.*?)<br>',str(mtr), re.IGNORECASE).group(1).strip('.| ').split()[-2]
        self.a_v.av66 = "CL_MTR_KWH", re.search('<br>KWH(.*?)<br>',str(mtr), re.IGNORECASE).group(1).strip('.| ').split()[-3]
        self.a_v.av67 = "DIFF_MTR_KWH", re.search('<br>KWH(.*?)<br>',str(mtr), re.IGNORECASE).group(1).strip('.| ').split()[-1]
        self.a_v.av68 = "OP_MTR_KVAH", "Val"
        self.a_v.av69 = "CL_MTR_KVAH", "Val"
        self.a_v.av70 = "DIFF_MTR_KVAH", "Val"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(61, 71)]
        self.final_data.extend(av_rows)

    def get_last_payment_detail(self):
        last_pay = self.src_data
        self.a_v.av81 = "LAST_PAYMENT_DATE", re.search('received on\s+(.*?)\s+',str(last_pay), re.IGNORECASE).group(1).strip('.| ')
        self.a_v.av82 = "LAST_PAID_AMT", re.search('Last payment of RS(.*?)received',str(last_pay), re.IGNORECASE).group(1).strip('.| ')
        self.a_v.av53 = "LATE_PENALITY_LAST_FY", "NA" #TODO
        self.a_v.av54 = "LATE_PENALITY_CURR_FY", "NA" #TODO

        self.a_v.av83 = "PAYABLE_TO", "Val" #TODO
        self.a_v.av84 = "PAYABLE_AT", "Val" #TODO
        self.a_v.av85 = "src_attr", "Val" #TODO
        self.a_v.av86 = "src_attr", "Val" #TODO
        self.a_v.av87 = "src_attr", "Val" #TODO
        self.a_v.av88 = "src_attr", "Val" #TODO
        self.a_v.av89 = "src_attr", "Val" #TODO
        self.a_v.av90 = "src_attr","Val"  #TODO
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(81, 91)]
        self.final_data.extend(av_rows)


    def get_allowed_service(self):
        svc = self.src_data
        self.a_v.av25 = "PAID_SECURITY_AMT",  re.search('Security Deposit(.*?)<br>',str(svc), re.IGNORECASE).group(1).strip()
        sanctioned = re.search('Sanctioned Load (.*?)CA No',str(svc), re.IGNORECASE).group(1)
        self.a_v.av26 = "SANCTIONED_LOAD", float(re.search(r'\d+', sanctioned).group(0))
        self.a_v.av103 = "AVG_UNITS", "Val"
        self.a_v.av104 = "PWR_FACTOR", "Val"
        self.a_v.av6 = "INTS_ON_SEC", "Val" #TODO
        self.a_v.av7 = "ADDITIONAL_SEC", "Val" #TODO
        self.a_v.av8 = "SUPPLY_TYPE", "Val" #TODO
        self.a_v.av9 = "TEMP_DEPOSIT", "Val" #TODO
        self.a_v.av10 = "RECORD_DEMAND","Val"  #TODO
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(11, 21)]
        self.final_data.extend(av_rows)

    def get_particulars_61_70(self):
        prcls = self.src_data
        self.a_v.av61 = "FIXED_CHARGES", re.search('Fixed Charges(.*?)<br>',str(prcls), re.IGNORECASE).group(1).strip()
        self.a_v.av62 = "UNIT_RATE1", re.search('<br>WhatsApp.*?\d{10}(.*?)<br>',str(prcls), re.IGNORECASE).group(1).strip('.| ').split()[2]
        self.a_v.av63 = "UNIT_CONSUMED1", re.search('<br>WhatsApp.*?\d{10}(.*?)<br>',str(prcls), re.IGNORECASE).group(1).strip('.| ').split()[0]
        self.a_v.av64 = "UNIT_CHARGE1", re.search('<br>WhatsApp.*?\d{10}(.*?)<br>',str(prcls), re.IGNORECASE).group(1).strip('.| ').split()[3]
        self.a_v.av65 = "UNIT_RATE2", "Val"
        self.a_v.av66 = "UNIT_CONSUMED2", "Val"
        self.a_v.av67 = "UNIT_CHARGE2", "Val"
        self.a_v.av68 = "UNIT_RATE3", "Val"
        self.a_v.av69 = "UNIT_CONSUMED3", "Val"
        self.a_v.av70 = "UNIT_CHARGE3", "Val"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(71, 81)]
        self.final_data.extend(av_rows)
     
    def get_particulars_71_82(self):
        prcls = self.src_data
        self.a_v.av71 = "UNIT_RATE4", "Val"
        self.a_v.av72 = "UNIT_CONSUMED4", "Val"
        self.a_v.av73 = "UNIT_CHARGE4", "Val"
        self.a_v.av74 = "UNIT_RATE5", "Val"
        self.a_v.av75 = "UNIT_CONSUMED5", "Val"
        self.a_v.av76 = "UNIT_CHARGE5", "Val"
        self.a_v.av77 = "UNIT_RATE6", "Val"
        self.a_v.av78 = "UNIT_CONSUMED6", "Val"
        self.a_v.av79 = "UNIT_CHARGE6", "Val"
        self.a_v.av80 = "UNIT_RATE7", "Val"
        self.a_v.av81 = "UNIT_CONSUMED7", "Val"
        self.a_v.av82 = "UNIT_CHARGE7", "Val"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(81, 93)]
        self.final_data.extend(av_rows)
    
    def get_other_details83_90(self):
        others = self.src_data
        self.a_v.av83 = "OTHER_PENALTIES", "Val"
        self.a_v.av84 = "THEFT_MANI", "Val"
        self.a_v.av85 = "TTL_MONTH", "Val"
        self.a_v.av86 = "PICKED_FROM", "Val"
        self.a_v.av87 = "REMARK1", "Val"
        self.a_v.av88 = "ELEC_TAX_LAST_FY", "Val"
        self.a_v.av89 = "ELEC_TAX_CURR_FY", "Val"
        self.a_v.av90 = "RECEIPT_NO", "Val"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(83, 91)]
        self.final_data.extend(av_rows)
    
    def get_other_details91_100(self):
        others = self.src_data
        self.a_v.av91 = "ARR_CURR_FY", "Val"
        self.a_v.av92 = "ARR_LAST_FY", "Val"
        self.a_v.av93 = "TTL_ARREAR", "Val"
        self.a_v.av92 = "EXCEEDING_DMND", "Val"

        self.a_v.av92 = "BILL_BASIS", "Val"
        self.a_v.av92 = "ARR_CURR_FY", "Val"
        self.a_v.av92 = "ARR_CURR_FY", "Val"
        self.a_v.av92 = "ARR_CURR_FY", "Val"
        self.a_v.av92 = "ARR_CURR_FY", "Val"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(83, 91)]
        self.final_data.extend(av_rows)
    
    def main(self):
        self.get_header()
        self.get_client()
        # self.get_subdivision()
        self.get_due_details()
        self.get_meter_details()
        self.get_last_payment_detail()
        self.get_allowed_service()
        self.get_particulars()
        return self.final_data


## Usage
discom = TataDDL(extractor="PLUMBER_HTML")
# discom.get_header()
# discom.get_client()
# print(discom.final_data)
discom.main()
print(discom.final_data)

