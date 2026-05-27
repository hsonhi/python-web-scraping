# Source - https://stackoverflow.com/q/75473465
# Posted by Richard T Vetticad
# Retrieved 2026-05-24, License - CC BY-SA 4.0

#imports
import pandas as pd
import numpy as np
from serpapi import GoogleSearch
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", False)
#
#options = webdriver.ChromeOptions()

# Remove the 'navigator.webdriver' flag
options.add_argument("--disable-blink-features=AutomationControlled")
#
#options.add_argument("user-data-dir=C:\\Users\\PC\\AppData\\Local\\Google\\Chrome\\User Data")
#options.add_argument("profile-directory=Default")
#
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# (Optional) Add a custom User-Agent to mimic a real browser
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

#using selenium to launch and scroll through the Google Jobs page
url = "https://angoemprego.com/vagas-de-emprego/"
driver = webdriver.Chrome(options=options)
driver.get(url)
joblist =[]



# Source - https://stackoverflow.com/a/75486908
# Posted by sound wave, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-27, License - CC BY-SA 4.0

# import libraries...
# load webpage...


xpaths = {
 #'Logo'            :"./div[1]//img",
 #'Role'            :"./div[2]",
 'Company'         :"./div/div[2]/a/div/h3",
 #'Location'        :"./div[4]/div/div[2]",
 #'Source'          :"./div[4]/div/div[3]",
 #'Posted'          :"./div[4]/div/div[4]/div[1]",
 #'Full / Part Time':"./div[4]/div/div[4]/div[2]",
}
data = {key:[] for key in xpaths}
jobs_to_do = 2
jobs_done = 0

while jobs_done < jobs_to_do:
    lis = driver.find_elements(By.XPATH, '//*[@class="job_listings"]/li')
    
    for li in lis[jobs_done:]:
        driver.execute_script('arguments[0].scrollIntoView({block: "center", behavior: "smooth"});', li)
        
        for key in xpaths:
            try:
                t = li.find_element(By.XPATH, xpaths[key]).get_attribute('src' if key=='Logo' else 'innerHTML')
            except NoSuchElementException:
                t = '*missing data*'
            data[key].append(t)
        
        jobs_done += 1
        print(f'{jobs_done=}', end='\r')
        time.sleep(.2)
pd.DataFrame(data).to_excel('google_jobs.xlsx', index=False)