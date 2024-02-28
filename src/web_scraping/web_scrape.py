import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time



def well_scrape(api_number, well_name):

    service = Service(executable_path='/home/wendy/Desktop/geckodriver')
    driver = webdriver.Firefox(service=service)
    
    search_url = "https://www.drillingedge.com/search"
    driver.get(search_url)
    
    
    well_name = well_name.upper()
    
    search_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'api_no')))
    search_input.send_keys(api_number)
    search_input.send_keys(Keys.ENTER)
    
    new_page = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, well_name)))
    new_page.click()
    
    website_wait = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME, 'dropcap'))) 
    
    dropcaps = driver.find_elements(By.CLASS_NAME, 'dropcap')
    
    oil_produced = dropcaps[0].text
    gas_produced = dropcaps[1].text
    
    table = driver.find_elements(By.CLASS_NAME, 'skinny')
    
    info = []
    info.append(oil_produced)
    info.append(gas_produced)

    required_info = False
    
    for tr in table:
        cells = tr.find_elements(By.XPATH, './/th | .//td')
        for element in cells:
            
            if required_info == True:
                required_info = False
                info.append(element.text)
            
            if element.text == 'Well Status':
                required_info = True
            elif element.text == 'Well Type':
                required_info = True
            elif element.text == 'Closest City':
                required_info = True
            else:
                required_info = False
    
    driver.quit()

    return info

# api_number = '33-053-03944'
# well_name = 'Magnum 2-36-25H'

print(well_scrape('33-053-03944', 'Magnum 2-36-25H'))




















