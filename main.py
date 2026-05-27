import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", False)

# Remove the 'navigator.webdriver' flag
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# (Optional) Add a custom User-Agent to mimic a real browser
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

url = "https://angoemprego.com/vagas-de-emprego/"
driver = webdriver.Chrome(options=options)
driver.get(url)

xpaths = {
 'Logo'            :"./div/div[1]/a/img",
 'Role'            :"./div/div[2]/a/div/h3",
 'Company'         :"./div/div/div/div",
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