from pymongo import MongoClient
from selenium import webdriver # 1004 수정
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import re
import time
import pprint
import math
import json
from json import dumps
import sys


driver_path = "./chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument('window-size=1920,1080')
driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)

driver.get("https://open.assembly.go.kr/portal/assm/search/memberSchPage.do")
# driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div/div[3]/form/fieldset/div/input").send_keys("유승민")
# driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div/div[3]/form/fieldset/button").click()
# time.sleep(2)
# driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/section[1]/div[1]/div[3]/div/div/ul/li[2]/a").click()
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# img_src = soup.find('#main_pack > section.sc_new.cs_common_module.case_normal._au_people_content_wrap.color_99 > div.cm_content_wrap > div.cm_content_area._cm_content_area_profile > div > div.detail_info > a > img:href')
# carrer = soup.find("#mflick > div > div > dl > div:nth-child(1)") 
# Awards = soup.find('#mflick > div > div > dl > div:nth-child(1)')



print(img_src)  



