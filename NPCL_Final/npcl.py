## Python Related Modules and Dependencies
import os
import sys
import re
import json
import pandas as pd
from time import sleep
import uuid
import datetime
## Project Related Modules and Dependencies
from .base import BaseExtractor, SRCAttr
from payu.mappers.base_mapper import BaseMapper
TODAY = datetime.datetime.today().strftime("%Y_%m_%d")

class KEDL(BaseExtractor):
    """
    Kota Electric Distribution LTD.
    """
    def __init__(self, extractor="PDF_TO_TEXT", working_folder=None, src_path=None):
        self.src_path = src_path
        self.working_folder = "{}{}{}".format(working_folder, os.sep, TODAY)
        if not os.path.exists(self.working_folder):
            os.makedirs(self.working_folder)
        self.extractor = extractor
        self.src_data = ''
        self.working_file_path = "{}{}{}.html".format(self.working_folder,os.sep, str(uuid.uuid4()))
        self.dest_file_path = "{}{}{}.csv"
        self.final_data = []
        self.words = []
        self.tables = []
        self.a_v = SRCAttr()
        self.read_src_data()        
    
    def get_header(self):
        hd = self.src_data
        self.a_v.av1 = "DISCOM_NAME", 'Noida Power Company Limited'
        self.a_v.av2 = "CONN_NO", re.search('(.*?)\s+',str(hd), re.IGNORECASE).group(1).strip()
        self.a_v.av3 = "BILL_NO", re.search('V<br>.*?<br>(.*?)<br',str(hd), re.IGNORECASE).group(1).strip()
        self.a_v.av4 = "BILL_DATE", re.search('<br>.*?<br>(.*?)<br',str(hd), re.IGNORECASE).group(1).strip()
        self.a_v.av5 = "BOOK_NO", "NA"
        self.a_v.av6 = "K_NO", "NA"
        self.a_v.av7 = "DISCONN_DATE", re.search('V<br>(.*?)<br',str(hd), re.IGNORECASE).group(1).strip()
        self.a_v.av8 = "DIVISION_CODE", "NA"
        self.a_v.av9 = "AMT_PAYABLE", re.search('<br>Total Amount  Rs. (.*?)<br',str(hd), re.IGNORECASE).group(1).strip()
        self.a_v.av10 = "BILLING_ADD", re.search('<br>.*?<br>.*?<br>.*?<br>.*?<br>(.*?)\s+',str(hd), re.IGNORECASE).group(1).strip()+' '+re.search('<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>(.*?)<br',str(file1), re.IGNORECASE).group(1).strip()

        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(1, 11)]
        ## Outputfile nanme
        self.dest_file_path = "{}{}{}.csv".format(self.working_folder,os.sep, self.a_v.av3[1])
        self.final_data.extend(av_rows)

    def get_due_details(self):
        due = self.src_data
        self.a_v.av11 = "DUE_DATE", re.search('<br>Connection Status:\s+.*?\s+(.*?)<br',str(due), re.IGNORECASE).group(1).strip() 
        self.a_v.av12 = "DUE_AMT", re.search('<br>Total Amount  Rs. (.*?)<br',str(due), re.IGNORECASE).group(1).strip() 
        self.a_v.av13 = "AFTER_DUE_AMT", re.search('KVA\s+(.*?)<br',str(due), re.IGNORECASE).group(1).strip() 
        self.a_v.av14 = "CURR_DUE_AMT", re.search('<br>Total Amount  Rs. (.*?)<br',str(due), re.IGNORECASE).group(1).strip() 
        self.a_v.av15 = "ARREAR_AMT",  "NA"
        self.a_v.av16 = "ADJUSTMENT", "NA"
        self.a_v.av17 = "TTL_CURR_DUE_AMT", re.search('<br>Total Amount  Rs. (.*?)<br',str(due), re.IGNORECASE).group(1).strip() 
        self.a_v.av18 = "TTL_DUE_AMT", re.search('<br>Total Amount  Rs. (.*?)<br',str(due), re.IGNORECASE).group(1).strip() 
        self.a_v.av19 = "AMT_AS_PER_BILL",  re.search('<br>Total Amount  Rs. (.*?)<br',str(due), re.IGNORECASE).group(1).strip() 
        self.a_v.av20 = "TTL_ACTL_DUE_AMT",  re.search('<br>Total Amount  Rs. (.*?)<br',str(due), re.IGNORECASE).group(1).strip() 
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(11, 21)]
        self.final_data.extend(av_rows)

    def get_charges(self):
        chrg = self.src_data
        self.a_v.av21 = "AMT_MIN_CHRG", "NA"
        self.a_v.av22 = "CAP_CHRG", "NA"
        self.a_v.av23 = "REG_SURCHRG_1", "NA"
        self.a_v.av24 = "REG_SURCHRG_2", "NA"
        self.a_v.av25 = "MISC_CHRG", "NA"
        self.a_v.av26 = "FCA_CHRG", "NA"
        self.a_v.av27 = "GREEN_ENRGY", "NA"
        self.a_v.av28 = "VLTG_SURCHRG", "NA"
        self.a_v.av29 = "MAINTENANCE_CHRG","NA"
        self.a_v.av30 = "ADD_ENRGY_CHRG", "NA"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(21, 31)]
        self.final_data.extend(av_rows)
        pay = self.src_data
        self.a_v.av31 = "REBATEES", "NA"
        self.a_v.av32 = "EXCESS_LOAD", "NA"
        self.a_v.av33 = "CON_SPLY_SURCHRG", "NA"
        self.a_v.av34 = "IT_METERING_SURCHRG", "NA"
        self.a_v.av35 = "DISH_CHQ", "NA"
        self.a_v.av36 = "DEBIT", "NA"
        self.a_v.av37 = "CREDIT", "NA"
        self.a_v.av38 = "TEMP_PAYMENT", "NA"
        self.a_v.av39 = "RND_TTL_AMT", re.search('<br>Rounding amount  Rs. (.*?)<br',str(pay), re.IGNORECASE).group(1).strip()
        self.a_v.av40 = "MF", re.search('br>Total Amount.*?<br>.*?<br>.*?<br>.*?<br>(.*?)<br>',str(pay), re.IGNORECASE).group(1).strip().split(' ')[3]
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(31, 41)]
        self.final_data.extend(av_rows)
    
    def get_payment_detail(self):
        last_pay = self.src_data
        self.a_v.av41 = "LAST_PAYMENT_DATE", re.search('V<br>.*?<br>.*?<br>.*?<br>.*?<br>(.*?)<br',str(last_pay), re.IGNORECASE).group(1).strip()
        self.a_v.av42 = "LAST_PAID_AMT", re.search('Actual (.*?)<br',str(last_pay), re.IGNORECASE).group(1).strip()
        self.a_v.av43 = "LATE_PENALITY_LAST_FY", "NA" #
        self.a_v.av44 = "LATE_PENALITY_CURR_FY", "NA" #
        self.a_v.av45 = "PAYABLE_TO","NA"
        self.a_v.av46 = "PAYABLE_AT", "NA"
        self.a_v.av47 = "ARR_CURR_FY", "NA"
        self.a_v.av48 = "ARR_LAST_FY", "NA"
        self.a_v.av49 = "TTL_ARREAR", "NA"
        self.a_v.av50 = "EXCEEDING_DMND", "NA"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(41, 51)]
        self.final_data.extend(av_rows)

    def get_meter_details(self):
        mtr = self.src_data
        self.a_v.av51 = "MTR_NO", re.search('br>Total Amount.*?<br>.*?<br>.*?<br>.*?<br>\s+(.*?)\s+',str(mtr), re.IGNORECASE).group(1).strip().replace('<br>','')
        self.a_v.av52 = "OP_READING_DATE", re.search('<br>Total Amount  Rs. .*?<br>.*?<br>.*?<br>(.*?)<br',str(mtr), re.IGNORECASE).group(1).strip().replace('<br>','').split(' ')[1]
        self.a_v.av53 = "CL_READING_DATE", re.search('<br>Total Amount  Rs. .*?<br>.*?<br>.*?<br>(.*?)<br',str(mtr), re.IGNORECASE).group(1).strip().replace('<br>','').split(' ')[0]
        self.a_v.av54 = "OP_MTR_KWH", re.search('br>Total Amount.*?<br>.*?<br>.*?<br>.*?<br>(.*?)<br>',str(mtr), re.IGNORECASE).group(1).strip().split(' ')[1]
        self.a_v.av55 = "CL_MTR_KWH", re.search('br>Total Amount.*?<br>.*?<br>.*?<br>.*?<br>(.*?)<br>',str(mtr), re.IGNORECASE).group(1).strip().split(' ')[0]
        self.a_v.av56 = "DIFF_MTR_KWH", re.search('br>Total Amount.*?<br>.*?<br>.*?<br>.*?<br>(.*?)<br>',str(mtr), re.IGNORECASE).group(1).strip().split(' ')[2]
        self.a_v.av57 = "OP_MTR_KVAH", "NA"
        self.a_v.av58 = "CL_MTR_KVAH", "NA"
        self.a_v.av59 = "DIFF_MTR_KVAH", "NA"
        self.a_v.av60 = "BILLED_UNIT", re.search('br>Total Amount.*?<br>.*?<br>.*?<br>.*?<br>(.*?)<br>',str(mtr), re.IGNORECASE).group(1).strip().split(' ')[2]
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(51, 61)]
        self.final_data.extend(av_rows)

    def get_particulars_61_70(self):
        prcls = self.src_data
        self.a_v.av61 = "FIXED_CHARGES", re.search('Fixed Charges  Rs. (.*?)<br',str(prcls), re.IGNORECASE).group(1).strip() 
        self.a_v.av62 = "UNIT_RATE1", re.search('Fixed Charges  Rs.*?<br>.*?<br>(.*?)<br',str(prcls), re.IGNORECASE).group(1).strip().split(' ')[1] 
        self.a_v.av63 = "UNIT_CONSUMED1", re.search('Fixed Charges  Rs.*?<br>.*?<br>(.*?)<br',str(prcls), re.IGNORECASE).group(1).strip().split(' ')[0] 
        self.a_v.av64 = "UNIT_CHARGE1", re.search('Fixed Charges  Rs.*?<br>.*?<br>(.*?)<br',str(prcls), re.IGNORECASE).group(1).strip().split(' ')[2] 
        self.a_v.av65 = "UNIT_RATE2",re.search('Fixed Charges  Rs.*?<br>.*?<br>.*?<br>.*?<br>(.*?)<br',str(prcls), re.IGNORECASE).group(1).strip().split(' ')[1] 
        self.a_v.av66 = "UNIT_CONSUMED2", re.search('Fixed Charges  Rs.*?<br>.*?<br>.*?<br>.*?<br>(.*?)<br',str(prcls), re.IGNORECASE).group(1).strip().split(' ')[0] 
        self.a_v.av67 = "UNIT_CHARGE2", re.search('Fixed Charges  Rs.*?<br>.*?<br>.*?<br>.*?<br>(.*?)<br',str(prcls), re.IGNORECASE).group(1).strip().split(' ')[2] 
        self.a_v.av68 = "UNIT_RATE3", "NA"
        self.a_v.av69 = "UNIT_CONSUMED3", "NA"
        self.a_v.av70 = "UNIT_CHARGE3", "NA"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(61, 71)]
        self.final_data.extend(av_rows)
     
    def get_particulars_71_82(self):
        prcls = self.src_data
        self.a_v.av71 = "UNIT_RATE4", "NA"
        self.a_v.av72 = "UNIT_CONSUMED4", "NA"
        self.a_v.av73 = "UNIT_CHARGE4", "NA"
        self.a_v.av74 = "UNIT_RATE5", "NA"
        self.a_v.av75 = "UNIT_CONSUMED5", "NA"
        self.a_v.av76 = "UNIT_CHARGE5", "NA"
        self.a_v.av77 = "UNIT_RATE6", "NA"
        self.a_v.av78 = "UNIT_CONSUMED6", "NA"
        self.a_v.av79 = "UNIT_CHARGE6", "NA"
        self.a_v.av80 = "UNIT_RATE7", "NA"
        self.a_v.av81 = "UNIT_CONSUMED7", "NA"
        self.a_v.av82 = "UNIT_CHARGE7", "NA"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(71, 83)]
        self.final_data.extend(av_rows)
    
    def get_other_details83_90(self):
        others = self.src_data
        self.a_v.av83 = "OTHER_PENALTIES", "NA"
        self.a_v.av84 = "THEFT_MANI", "NA"
        self.a_v.av85 = "TTL_MONTH", "NA"
        self.a_v.av86 = "PICKED_FROM", "NA"
        self.a_v.av87 = "REMARK1", "NA"
        self.a_v.av88 = "ELEC_TAX_LAST_FY", "NA"
        self.a_v.av89 = "ELEC_TAX_CURR_FY", "NA"
        self.a_v.av90 = "RECEIPT_NO", "NA"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(83, 91)]
        self.final_data.extend(av_rows)
    
    def get_allowed_service(self):
        svc = self.src_data
        self.a_v.av91 = "PAID_SECURITY_AMT",  re.search('<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>(.*?)<br',str(svc), re.IGNORECASE).group(1).strip() 
        test = re.search('<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>.*?<br>(.*?)<br',str(svc), re.IGNORECASE).group(1).strip().split()[5:7]
        fin = test[0]+' '+test[1]
        self.a_v.av92 = "SANCTIONED_LOAD", fin
        self.a_v.av93 = "AVG_UNITS", "NA"
        self.a_v.av94 = "PWR_FACTOR", "NA"
        self.a_v.av95 = "INTS_ON_SEC", "NA"
        self.a_v.av96 = "ADDITIONAL_SEC", "NA"
        self.a_v.av97 = "SUPPLY_TYPE", "NA"
        self.a_v.av98 = "TEMP_DEPOSIT", "NA"
        self.a_v.av99 = "RECORD_DEMAND",re.search('<br>\d{10}\s+(.*?)<br',str(svc), re.IGNORECASE).group(1).strip()
        self.a_v.av100 = "BILL_BASIS", "NA"
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(91, 101)]
        self.final_data.extend(av_rows)
    
    def get_mapped_data(self):
        mapper = BaseMapper
        mapped_data = [(mapper.__dict__.get(k),k, v) for k, v in self.a_v.__dict__.values()]
        return mapped_data
    
    def main(self):
        self.get_header()
        self.get_due_details()
        self.get_charges()
        self.get_discom_payment_details()
        self.get_meter_details()
        self.get_payment_detail()
        self.get_particulars_61_70()
        self.get_particulars_71_82()
        self.get_other_details83_90()
        self.get_allowed_service()
        mapped_data = self.get_mapped_data()
        df = pd.DataFrame(mapped_data)
        df.to_csv(discom.dest_file_path)
        ## Remove Tmp files
        os.remove(self.working_file_path)
        return mapped_data


## Usage
if __name__ == '__main__':
    working_folder = "/home/server/Documents/anil_sir"
    FILE = "/home/server/Documents/anil_sir/KOT074 - Kamlesh Mohpal.pdf"
    discom = KEDL(extractor="PLUMBER_HTML", working_folder=working_folder, src_path=FILE)
    data = discom.main()