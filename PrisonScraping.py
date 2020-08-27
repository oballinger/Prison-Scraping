from selenium import webdriver;
from selenium.webdriver.support.ui import Select;
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
import time
import os
from os import listdir
import glob
import pandas as pd
import csv
import sys
import os
import glob
import csv
import sys
import numpy as np
import pandas as pd
import xlrd
from pathlib import Path
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from itertools import product
from fuzzywuzzy.fuzz import ratio
from openpyxl import Workbook
import collections
import datetime
import urllib.request
import requests
import time
from bs4 import BeautifulSoup, SoupStrainer
from googlesearch import search 
import textract
import signal
import re
from fuzzywuzzy import process
from itertools import product
from fuzzywuzzy.fuzz import ratio
from fuzzywuzzy import fuzz

#from webdriver_manager.chrome import ChromeDriverManager


# ----------- Configuration ------------- # 

# Replace this with the path you would like the raw .xlsx files to download to before concatenation 

directory="/Users/ollieballinger/downloads/"

# 
gender="men"


driver_path= "/Users/ollieballinger/.wdm/drivers/chromedriver/mac64/84.0.4147.30/chromedriver"
names=pd.read_csv(directory+"BOP_Names.csv")
output=pd.read_csv(directory+"output.csv")


# 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0',
    'From': 'huey.newton@ACAB.com' 
}

url="https://www.bop.gov/inmateloc/"
root="/html/body/div[1]/div[1]/section/div/div[2]/"
name_tab=root+"ul/li[2]/a"


driver = webdriver.Chrome(executable_path=driver_path)

driver.get(url)
driver.find_element_by_xpath(name_tab).click()
first=driver.find_element_by_xpath(root+"div[2]/form/table[1]/tbody/tr/td[1]/table/tbody/tr[2]/td[1]/input")
last=driver.find_element_by_xpath(root+"div[2]/form/table[1]/tbody/tr/td[1]/table/tbody/tr[2]/td[3]/input")

def search(firstname,lastname):
	first.clear()
	last.clear()
	first.send_keys(firstname)
	last.send_keys(lastname)
	driver.find_element_by_xpath(root+"div[2]/form/table[2]/tbody/tr/td[3]/button").click()

def handler(signum, frame):
	print("Forever is over!")
	raise Exception("end of time")

def loop_forever():
	while 1:
		print("sec")
		time.sleep(1)

signal.signal(signal.SIGALRM, handler)


index_1=output.at[len(output)-1,'lastname_index']
index_2=output.at[len(output)-1,'firstname_index']

for i in range(len(names)):
	for i in range(len(names)):
		df=pd.DataFrame()
		index_1=index_1+1

		print(index_2, index_1)
		try:
			apellido=names.at[index_1,'lastname']
			men=names.at[index_2,'men']
			women=names.at[index_2,'women']
			try:
				if gender=='men':
					search(men, apellido)
					print(men, apellido)
				else:
					search(women, apellido)

				#while True:
				try:
					element=EC.visibility_of_element_located((By.XPATH, '//*[contains(@id,"inmateTable")]//tr'))
					wait=WebDriverWait(driver, 10)
					wait.until(element)

				except Exception:break

				for table in driver.find_elements_by_xpath('//*[contains(@id,"inmateTable")]//tr'):
					data = [item.text for item in table.find_elements_by_xpath(".//*[self::td or self::th]")]
					df=df.append([data])
					print(data)

				df.columns=df.iloc[0]
				df.reset_index(inplace=True)
				df=df[1:]
				df['firstname_index']=index_2
				df['lastname_index']=index_1
				output=output.append(df)
				output.to_csv(directory+"output.csv",index=None)
			except:
				pass
		except:
				pass

	index_2=index_2+1
	index_1=-1
	



driver.quit()
quit()

