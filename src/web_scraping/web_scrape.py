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
import pandas as pd



def well_scrape(api_number, well_name):

	print('------------------------------------------------------------------')
	print('Now scraping {} API: {}'.format(well_name, api_number))
	service = Service(executable_path='/home/wendy/Desktop/geckodriver')
	driver = webdriver.Firefox(service=service)

	search_url = "https://www.drillingedge.com/search"
	driver.get(search_url)

	well_name = well_name.upper().strip()
	search_input = WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.NAME, 'api_no')))
	search_input.send_keys(api_number)
	search_input.send_keys(Keys.ENTER)

	new_page = WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.LINK_TEXT, well_name)))
	new_page.click()
	info = []

	try:
		website_wait = WebDriverWait(driver,35).until(EC.presence_of_element_located((By.CLASS_NAME, 'dropcap'))) 
		dropcaps = driver.find_elements(By.CLASS_NAME, 'dropcap')

		oil_produced = dropcaps[0].text
		gas_produced = dropcaps[1].text

		info.append(oil_produced)
		info.append(gas_produced)
	except:
		print('{} with api number {} does not have info on oil and gas produced.'.format(well_name, api_number))
		info.append("")
		info.append("")

	table = driver.find_elements(By.CLASS_NAME, 'skinny')

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


#api_number = '33-053-03944'
#well_name = 'Magnum 2-36-25H'

api_well_df = pd.read_csv('api_well.csv')
api_well_df = api_well_df.drop(api_well_df.columns[1], axis = 1)
well_web_info = []

for i in range(len(api_well_df)):
	well_web_info.append(well_scrape(api_well_df.iloc[i,0], api_well_df.iloc[i,1]))

well_web_df = pd.DataFrame(well_web_info, columns = ['Barrels of Oil Produced', 'MCF of Gas Produced', 
													'Well Status', 'Well Type', 'Closest City'])

print(well_web_df.head())
well_web_df.to_csv('web_info.csv')




#print(well_scrape('33-053-06027', 'KLINE FEDERAL 5300 41-18 11T2'))


