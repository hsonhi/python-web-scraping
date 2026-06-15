import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# Configuration
URL = "https://angoemprego.com/vagas-de-emprego/" #This project uses a popular job listing website called AngoEmprego.
OUTPUT_FILE = "joblist.xlsx"
JOBS_TO_SCRAPE = 15
SCROLL_PAUSE_TIME = 0.2
WAIT_TIMEOUT = 10

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# XPath definitions
XPATHS = {
    'Logo': "./div/div[1]/a/img",
    'Role': "./div/div[2]/a/div/h3",
    'Company': "./div/div[3]/div/h4",  # More specific XPath
    # 'Location': "./div[4]/div/div[2]",
    # 'Source': "./div[4]/div/div[3]",
    # 'Posted': "./div[4]/div/div[4]/div[1]",
    # 'Full / Part Time': "./div[4]/div/div[4]/div[2]",
}

def setup_driver():
    """Initialize and configure the Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    return webdriver.Chrome(options=options)

def wait_for_jobs(driver):
    """Wait for job listings to load."""
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@class="job_listings"]/li'))
        )
        logger.info("Job listings loaded successfully")
    except TimeoutException:
        logger.error("Timeout waiting for job listings to load")
        raise

def extract_job_data(li, xpaths):
    """Extract job data from a list item element."""
    job_data = {}
    for key, xpath in xpaths.items():
        try:
            element = li.find_element(By.XPATH, xpath)
            job_data[key] = element.get_attribute('src' if key == 'Logo' else 'innerHTML')
        except NoSuchElementException:
            logger.warning(f"Could not find {key} for job listing")
            job_data[key] = '*missing data*'
    return job_data

def scrape_jobs(driver, num_jobs):
    """Scrape job listings from the website."""
    data = {key: [] for key in XPATHS}
    jobs_done = 0
    
    try:
        while jobs_done < num_jobs:
            lis = driver.find_elements(By.XPATH, '//*[@class="job_listings"]/li')
            
            # Check if we've reached the available jobs
            if jobs_done >= len(lis):
                logger.warning(f"Only {len(lis)} jobs available, but {num_jobs} requested")
                break
            
            for li in lis[jobs_done:]:
                if jobs_done >= num_jobs:
                    break
                
                try:
                    # Scroll to the job listing
                    driver.execute_script('arguments[0].scrollIntoView({block: "center", behavior: "smooth"});', li)
                    time.sleep(SCROLL_PAUSE_TIME)
                    
                    # Extract data
                    job_data = extract_job_data(li, XPATHS)
                    for key, value in job_data.items():
                        data[key].append(value)
                    
                    jobs_done += 1
                    logger.info(f"Scraped {jobs_done}/{num_jobs} jobs")
                    
                except Exception as e:
                    logger.error(f"Error processing job listing: {e}")
                    continue
    
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        raise
    
    return data

def main():
    """Main execution function."""
    driver = None
    try:
        logger.info(f"Starting web scraper for {URL}")
        driver = setup_driver()
        driver.get(URL)
        
        wait_for_jobs(driver)
        data = scrape_jobs(driver, JOBS_TO_SCRAPE)
        
        # Save to Excel
        df = pd.DataFrame(data)
        df.to_excel(OUTPUT_FILE, index=False)
        logger.info(f"Data saved to {OUTPUT_FILE} ({len(df)} rows)")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
    
    finally:
        if driver:
            driver.quit()
            logger.info("WebDriver closed")

if __name__ == "__main__":
    main()