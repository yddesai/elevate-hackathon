import os 
import requests 
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

COURT_URL = "https://portal.scscourt.org/dashboard"

bearer_token = ""

def open_browser():
    options = Options()

    options.headless = False  
    driver = webdriver.Firefox(options=options)

    # Add authorization token as a cookie
    driver.get(COURT_URL)
    driver.add_cookie({
        'name': 'Authorization',
        'value': f'Bearer {bearer_token}',
        'domain': 'portal.scscourt.org',
        'path': '/'
    })

    time.sleep(4)  # Waiting for page to load

    # traverse all cases for fl cases
    fl_cases = [_ for _ in range(1, 2101)]

    for case in fl_cases:        
        # reload browser
        driver.refresh()
        time.sleep(2)
        
        case_number  = '{:06d}'.format(case)
        case_code = '23FL' + str(case_number)
        print(f'case number is {case_code}')
        
        case_number_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "search-input"))
)
        case_number_input.clear()  # Clear any existing value in the input field
        case_number_input.send_keys(case_code)
 
        case_number_input.send_keys(Keys.ENTER)
        time.sleep(2)
        
    # Close the browser
    driver.quit()

if __name__ == "__main__":
    open_browser()
