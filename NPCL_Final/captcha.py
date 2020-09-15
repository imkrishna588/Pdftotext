#! /usr/bin/python3

import os,distro
import sys
import re
import cv2
import pytesseract
import shutil
from xvfbwrapper import Xvfb
from time import sleep
from PIL import Image, ImageEnhance
from io import BytesIO
from distutils.dir_util import copy_tree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common import exceptions as E
from datetime import  datetime
from dateutil.parser import parse
from subprocess import check_output
import urllib.request
from db import *
import threading
import __main__ as main


u1 = 'https://iwebapps.noidapower.com:8032/Ebill_download.aspx'
# u1='https://services.ecourts.gov.in/ecourtindiaHC/cases/case_no.php?state_cd=13&dist_cd=1&court_code=1&stateNm=Uttar%20Pradesh'
# u2='http://elegalix.allahabadhighcourt.in/elegalix/WebCaseSearch.do'
img='https://iwebapps.noidapower.com:8032/CaptchaImage.axd?guid=89f2f690-f4e3-4516-b184-7d2a912f9f37'
# path = os.getcwd()
# path=os.path.join(path)

def enable_download_in_headless_chrome(driver):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': os.path.abspath('save')}}
    command_result = driver.execute("send_command", params)

def fName(s):
    invalid_chars = r'\/:*?"<>|@,'
    filename = ''.join(c if not c in invalid_chars else '_' for c in s)
    filename = filename.replace(' ','_')
    return filename

def allahabadCases(account):
    # v1=Xvfb()
    # v1.start()
    caseData=[]
    status = {}
    if not os.path.isdir('save'):
        os.mkdir('save')
    else:
        shutil.rmtree('save')
        os.mkdir('save')
    options = webdriver.ChromeOptions()
    if 'ebian' in distro.linux_distribution()[0]:
        p1 = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],"download.default_directory": os.path.abspath('save'), "download.extensions_to_open": "applications/pdf"}

    elif 'buntu' in distro.linux_distribution()[0]:
        p1 =  {
        "download.default_directory": os.path.abspath('save'),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
        }
    options.add_experimental_option("prefs", p1)
    # options.add_argument('--headless')
    d1=webdriver.Chrome(options=options)
    # enable_download_in_headless_chrome(d1)
    
    # d1.get(u1)
    # sleep(3)
    def _chkOrders():
        try:
            _=WebDriverWait(d1,10).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
            msgTxt=_.text
            if 'not uploaded' in msgTxt.lower():
                return True
        except Exception:
            return False

    def _chkCaptcha():
        try:
            _=WebDriverWait(d1,10).until(EC.visibility_of_element_located((By.XPATH,'//*[text()="Captcha  code is invalid. "]')))
            return False
        except Exception:
            #print('Error2: {}'.format(Exception))
            return True
    
    def _refreshCaptcha():
        try:
            d1.refresh()
            # _.click()
        except Exception:
            # self.closeSite()
            return
    def _chkPage():
        try:
            sleep(5)
            _=WebDriverWait(d1,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'input[type="submit"][value="Submit"][name="submit"]')))
            return True
        except Exception:
            return False
    
    def _saveCaptcha(url):
        try:
            c1='window.open("'+url+'")'
            _=d1.execute_script(c1)
            d1.switch_to.window(d1.window_handles[-1])
            _=WebDriverWait(d1,60).until(EC.presence_of_element_located((By.TAG_NAME,'body')))
            _.screenshot('test1.png')
            d1.close()
            d1.switch_to.window(d1.window_handles[-1])
            # _cropImage(path)
        except Exception:
            #self.closeSite()
            return
    def image_modify(path):
        img = cv2.imread(path)
        img[:, :, (0, 1)] = 0
        cv2.imwrite('test2.png', img, [cv2.IMWRITE_png_QUALITY, 100])

    def resolve(path):
        try:
            # check_output(['convert', path, '-resample', '600', path])
            check_output(['convert', path, '-resample', '50', path])
            check_output(['convert', path, '-resample', '90', path])
            check_output(['convert', path, '-resample', '110', path])
            return pytesseract.image_to_string(Image.open(path))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def validCaptcha3(path):
        try:
            txt=resolve(path).replace(' ','')
            if txt:
                print ('row text : ',txt)
                if len(txt)!=5:
                    # refreshCaptcha()
                    return 000000
                else:
                    return txt
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            # self.refreshCaptcha()
            return 000000
        

    d1.get(u1)
    sleep(5)
    while True:
        d1.get(u1)
        sleep(5)
        p4=d1.find_element_by_id('ContentPlaceHolder1_txtConsumerNo')
        p4.clear()
        p4.send_keys(account)
        sleep(2)

        element = d1.find_element_by_css_selector('#ContentPlaceHolder1_catpchaDiv > div:nth-child(1) > div.padd-bottom10.padd-top10 > div > img')
        element.screenshot('captcha.png')

        image = 'captcha.png'
        txt = str(validCaptcha3(image))
        print ('final Captcha:',txt)
        p5=d1.find_element_by_id('ContentPlaceHolder1_txtCaptcha')
        p5.clear()
        p5.send_keys(txt)
        sleep(2)
        p6=d1.find_element_by_id('ContentPlaceHolder1_Button2')
        p6.click()
        sleep(5)
        print ('check : ',_chkCaptcha)
        if _chkCaptcha == False :
            continue
        elif _chkCaptcha == True:
            break
        # d1.find_element_by_xpath('//*[@id="ContentPlaceHolder1_userDetails"]/div[5]/a').click()
        d1.find_element_by_xpath('//*[@id="ContentPlaceHolder1_userDetails"]/div[5]/a').click()

def runMain():
    vAdd = []
    # lMain1=getMainTable()
    lMain1=[('2000002593')]
    print ('all Cases: ',len(lMain1))
    if lMain1 is None:
        return
    if len(lMain1) is 0:
        print('No data to process.')
        return
    for lMain in lMain1:
        try:
            lCaseData=allahabadCases(lMain)
        except Exception as e:
            print('Error6: {}'.format(e.__str__))
            continue
        if lCaseData is None:
            continue
        if len(lCaseData) is 0:
            continue
        

if __name__ == "__main__":
    while True:
        try:
            runMain()
            sleep(60)
        except KeyboardInterrupt:
            raise
            #sys.exit(0)
        except Exception as e:
            print(e.__str__())
            continue

