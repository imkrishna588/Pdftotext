## Python Related Modules and Dependencies
import os
import sys
import re
import json
# import pdftotext
import pdfplumber
from time import sleep
## Project Related Modules and Dependencies

FILE = "smart.pdf"

## Global Variable
class SRCAttr:
    pass

class KEDL:
    """
    Tata Power Delhi Distribution LTD.
    """
    def __init__(self, extractor="PDF_TO_TEXT", working_folder="/Users/anilkumargupta/Documents/PyWithAnil/goscale/data", src_path=FILE):
        self.src_path = src_path
        self.extractor = extractor
        self.src_data = []
        self.working_folder = working_folder
        self.final_data = []
        self.words = []
        self.tables = []
        self.a_v = SRCAttr
        self.read_src_data()
    
    def read_src_data(self):
        """
        DOCString
        """
        if self.extractor=="PDF_TO_TEXT":
            self.with_pdftotext()
        else:
            self.with_pdfplumber()
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
                #self.get_header()
                self.words.extend(txt_pg.extract_words())
                self.tables.extend(txt_pg.extract_tables(table_settings={}))


    def get_header(self):
        # print (" ".join([w.get("text") for w in self.words[3:7]]))
        # print ('==================================================================================================')
        # print (self.words)
        # for i,j in enumerate(self.words):
        #     print (i,j)
        #import pdb;pdb.set_trace()
        #hd = self.words
        self.a_v.av1 = "USER_NAME", " ".join([w.get("text") for w in self.words[4:7]])
        self.a_v.av2 = "BILL_NO", " ".join([w.get("text") for w in self.words[793:794]])
        self.a_v.av3 = "BILL_DATE", " ".join([w.get("text") for w in self.words[99:100]])
        self.a_v.av4 = "BILLING_ADDRESS", " ".join([w.get("text") for w in self.words[22:36]])
        self.a_v.av5 = "SUPPLY_ADDRESS", " ".join([w.get("text") for w in self.words[99:100]])
        self.a_v.av6 = "MOBILE_NUMBER", " ".join([w.get("text") for w in self.words[99:100]])
        self.a_v.av7 = "EMAIL", " ".join([w.get("text") for w in self.words[99:100]])
        self.a_v.av8 = "SANCTIONED_LOAD", " ".join([w.get("text") for w in self.words[99:100]])
        self.a_v.av9 = "DISTRICT", " ".join([w.get("text") for w in self.words[99:100]])
        self.a_v.av10 = "ZONE","Val"  #TODO
        self.a_v.av11 = "MRU_NO","Val"  #TODO
        self.a_v.av12 = "WALKING_SEQUENCE","Val"  #TODO
        self.a_v.av13 = "PILLAR_N0","Val"  #TODO
        self.a_v.av14 = "CA_NO","Val"  #TODO
        self.a_v.av15 = "ENERGISATION_DATE","Val"  #TODO
        self.a_v.av16 = "SECURITY_DEPOSIT","Val"  #TODO
        self.a_v.av17 = "SLD_CHARGES","Val"  #TODO
        self.a_v.av18 = "CONNECTION_TYPE","Val"  #TODO
        self.a_v.av19 = "TARIFF_CATEGORY","Val"  #TODO
        self.a_v.av20 = "BILL_BASIS","Val"  #TODO
        self.a_v.av21 = "BILL_REMARK","Val"  #TODO
        self.a_v.av22 = "BILL_DATE","Val"  #TODO
        self.a_v.av23 = "BILL_NO","Val"  #TODO
        av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(1, 11)]
        self.final_data.extend(av_rows)
        #hd = self.words
        self.a_v.av1 = "USER_NAME", " ".join([w.get("text") for w in self.words[4:7]])
        self.a_v.av2 = "BILL_NO", " ".join([w.get("text") for w in self.words[793:794]])

    # def get_client(self):
    #     client = self.src_data
    #     self.a_v.av11 = "CLIENT_NAME", " ".join([w.get("text") for w in self.words[37:40]])
    #     self.a_v.av12 = "K_NO", " ".join([w.get("text") for w in self.words[207:208]])
    #     self.a_v.av13 = "src_attr", "Val" #TODO
    #     self.a_v.av14 = "src_attr", "Val" #TODO
    #     self.a_v.av15 = "src_attr", "Val" #TODO
    #     self.a_v.av16 = "src_attr", "Val" #TODO
    #     self.a_v.av17 = "src_attr", "Val" #TODO
    #     self.a_v.av18 = "src_attr", "Val" #TODO
    #     self.a_v.av19 = "src_attr", "Val" #TODO
    #     self.a_v.av20 = "src_attr","Val"  #TODO
    #     av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(11, 21)]
    #     self.final_data.extend(av_rows)

    # def get_subdivision(self):
    #     sb = self.src_data
    #     self.a_v.av21 = "DIVISION_CODE", " ".join([w.get("text") for w in self.words[41:42]])
    #     self.a_v.av22 = "src_attr", "Val" #TODO
    #     self.a_v.av23 = "src_attr", "Val" #TODO
    #     self.a_v.av24 = "src_attr", "Val" #TODO
    #     self.a_v.av25 = "src_attr", "Val" #TODO
    #     self.a_v.av26 = "src_attr", "Val" #TODO
    #     self.a_v.av27 = "src_attr", "Val" #TODO
    #     self.a_v.av28 = "src_attr", "Val" #TODO
    #     self.a_v.av29 = "src_attr", "Val" #TODO
    #     self.a_v.av30 = "src_attr","Val"  #TODO
    #     av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(21, 31)]
    #     self.final_data.extend(av_rows)

    # def get_due_details(self):
    #     due = self.src_data
    #     self.a_v.av41 = "DUE_DATE", " ".join([w.get("text") for w in self.words[226:227]])
    #     self.a_v.av42 = "DUE_AMT", " ".join([w.get("text") for w in self.words[233:234]])
    #     self.a_v.av43 = "AFTER_DUE_AMT", " ".join([w.get("text") for w in self.words[244:245]])
    #     self.a_v.av44 = "CURR_DUE_AMT",  " ".join([w.get("text") for w in self.words[244:245]])
    #     self.a_v.av45 = "TTL_CURR_DUE_AMT",  " ".join([w.get("text") for w in self.words[244:245]])
    #     self.a_v.av46 = "LATE_PENALITY_LAST_FY", "NA" #TODO
    #     self.a_v.av47 = "LATE_PENALITY_CURR_FY", "NA" #TODO
    #     self.a_v.av48 = "TTL_DUE_AMT",  " ".join([w.get("text") for w in self.words[244:245]])
    #     self.a_v.av49 = "TTL_CURR_DUE_AMT", " ".join([w.get("text") for w in self.words[244:245]])
    #     self.a_v.av50 = "TTL_ACTL_DUE_AMT","NA"  #TODO
    #     self.a_v.av51 = "AMT_PAYABLE", " ".join([w.get("text") for w in self.words[244:245]])
    #     av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(41, 52)]
    #     self.final_data.extend(av_rows)

    # def get_plan(self):
    #     p = self.src_data
    #     self.a_v.av1 = "src_attr", "Val" #TODO
    #     self.a_v.av2 = "src_attr", "Val" #TODO
    #     self.a_v.av3 = "src_attr", "Val" #TODO
    #     self.a_v.av4 = "src_attr", "Val" #TODO
    #     self.a_v.av5 = "src_attr", "Val" #TODO
    #     self.a_v.av6 = "src_attr", "Val" #TODO
    #     self.a_v.av7 = "src_attr", "Val" #TODO
    #     self.a_v.av8 = "src_attr", "Val" #TODO
    #     self.a_v.av9 = "src_attr", "Val" #TODO
    #     self.a_v.av10 = "src_attr","Val"  #TODO
    #     av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(51, 61)]
    #     self.final_data.extend(av_rows)

    # def get_meter_details(self):
    #     mtr = self.src_data
    #     self.a_v.av61 = "OP_READING_DATE", " ".join([w.get("text") for w in self.words[84:85]]).replace(":","")
    #     self.a_v.av62 = "CL_READING_DATE", " ".join([w.get("text") for w in self.words[84:85]]).replace(":", "")
    #     self.a_v.av63 = "MTR_NO", " ".join([w.get("text") for w in self.words[285:286]])
    #     self.a_v.av64 = "MF", " ".join([w.get("text") for w in self.words[286:287]])
    #     self.a_v.av65 = "OP_MTR_KWH", " ".join([w.get("text") for w in self.words[288:289]])
    #     self.a_v.av66 = "CL_MTR_KWH", " ".join([w.get("text") for w in self.words[289:290]])
    #     self.a_v.av67 = "DIFF_MTR_KWH", " ".join([w.get("text") for w in self.words[290:291]])
    #     self.a_v.av68 = "OP_MTR_KVAH", " ".join([w.get("text") for w in self.words[296:297]])
    #     self.a_v.av69 = "CL_MTR_KVAH", " ".join([w.get("text") for w in self.words[297:298]])
    #     self.a_v.av70 = "DIFF_MTR_JVAH", " ".join([w.get("text") for w in self.words[298:299]])
    #     av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(61, 71)]
    #     self.final_data.extend(av_rows)

    # def get_account(self):
    #     ac = self.src_data
    #     self.a_v.av1 = "src_attr", "Val" #TODO
    #     self.a_v.av2 = "src_attr", "Val" #TODO
    #     self.a_v.av3 = "src_attr", "Val" #TODO
    #     self.a_v.av4 = "src_attr", "Val" #TODO
    #     self.a_v.av5 = "src_attr", "Val" #TODO
    #     self.a_v.av6 = "src_attr", "Val" #TODO
    #     self.a_v.av7 = "src_attr", "Val" #TODO
    #     self.a_v.av8 = "src_attr", "Val" #TODO
    #     self.a_v.av9 = "src_attr", "Val" #TODO
    #     self.a_v.av10 = "src_attr","Val"  #TODO
    #     av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(71, 81)]
    #     self.final_data.extend(av_rows)

    # def get_last_payment_detail(self):
    #     due = self.src_data
    #     self.a_v.av81 = "LAST_PAYMENT_DATE", " ".join([w.get("text") for w in self.words[155:156]])
    #     self.a_v.av82 = "LAST_PAID_AMT", " ".join([w.get("text") for w in self.words[156:157]])
    #     self.a_v.av83 = "src_attr", "Val" #TODO
    #     self.a_v.av84 = "src_attr", "Val" #TODO
    #     self.a_v.av85 = "src_attr", "Val" #TODO
    #     self.a_v.av86 = "src_attr", "Val" #TODO
    #     self.a_v.av87 = "src_attr", "Val" #TODO
    #     self.a_v.av88 = "src_attr", "Val" #TODO
    #     self.a_v.av89 = "src_attr", "Val" #TODO
    #     self.a_v.av90 = "src_attr","Val"  #TODO
    #     av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(81, 91)]
    #     self.final_data.extend(av_rows)

    # def get_discom_payment_details(self):
    #     pay = self.src_data
    #     self.a_v.av1 = "src_attr", "Val" #TODO
    #     self.a_v.av2 = "src_attr", "Val" #TODO
    #     self.a_v.av3 = "src_attr", "Val" #TODO
    #     self.a_v.av4 = "src_attr", "Val" #TODO
    #     self.a_v.av5 = "src_attr", "Val" #TODO
    #     self.a_v.av6 = "src_attr", "Val" #TODO
    #     self.a_v.av7 = "src_attr", "Val" #TODO
    #     self.a_v.av8 = "src_attr", "Val" #TODO
    #     self.a_v.av9 = "src_attr", "Val" #TODO
    #     self.a_v.av10 = "src_attr","Val"  #TODO
    #     av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(91, 101)]
    #     self.final_data.extend(av_rows)

    # def get_allowed_service(self):
    #     svc = self.src_data
    #     self.a_v.av101 = "PAID_SECURITY_AMT",  " ".join([w.get("text") for w in self.words[326:327]])
    #     self.a_v.av102 = "SANCTIONED_LOAD", " ".join([w.get("text") for w in self.words[328:330]])
    #     self.a_v.av103 = "AVG_UNITS", " ".join([w.get("text") for w in self.words[332:333]])
    #     self.a_v.av104 = "PWR_FACTOR", " ".join([w.get("text") for w in self.words[360:361]])
    #     self.a_v.av105 = "src_attr", "Val" #TODO
    #     self.a_v.av106 = "src_attr", "Val" #TODO
    #     self.a_v.av107 = "src_attr", "Val" #TODO
    #     self.a_v.av108 = "src_attr", "Val" #TODO
    #     self.a_v.av109 = "src_attr", "Val" #TODO
    #     self.a_v.av110 = "src_attr","Val"  #TODO
    #     av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(101, 110)]
    #     self.final_data.extend(av_rows)

    # def get_particulars(self):
    #     prcls = self.src_data
    #     self.a_v.av1 = "src_attr", "Val" #TODO
    #     self.a_v.av2 = "src_attr", "Val" #TODO
    #     self.a_v.av3 = "src_attr", "Val" #TODO
    #     self.a_v.av4 = "src_attr", "Val" #TODO
    #     self.a_v.av5 = "src_attr", "Val" #TODO
    #     self.a_v.av6 = "src_attr", "Val" #TODO
    #     self.a_v.av7 = "src_attr", "Val" #TODO
    #     self.a_v.av8 = "src_attr", "Val" #TODO
    #     self.a_v.av9 = "src_attr", "Val" #TODO
    #     self.a_v.av10 = "src_attr","Val"  #TODO
    #     av_rows = [getattr(self.a_v, f"av{idx}") for idx in range(11, 21)]
    #     self.final_data.extend(av_rows)

    def main(self):
        self.get_header()
        # self.get_client()
        # self.get_subdivision()
        # self.get_due_details()
        # self.get_meter_details()
        # self.get_last_payment_detail()
        return self.final_data


## Usage
#discom = KEDL(extractor="PDF_TO_TEXT")
discom = KEDL(extractor="PLUMBER")
# discom.get_header()
# discom.get_client()
# print(discom.final_data)
discom.main()
print(discom.final_data)


# class KEDLMapper:
#     def __init__(self, mapper_keys=None, discom_data=None):
#         self.mapper_keys = mapper_keys
#         self.discom_data = discom_data
    
#     def mapper(self):
#         pass
    
