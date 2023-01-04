from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import ipdb

# set up headless chrome browser
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

URL = 'https://www.singaporepools.com.sg/en/product/pages/4d_results.aspx'

driver.get(URL)

# wait for js snippet to load
print("Waiting..")
element_present = EC.presence_of_element_located((By.TAG_NAME, 'select'))
WebDriverWait(driver, timeout=10).until(element_present)
print("Element Found")

# get query string from drop down box to scrap individual date results
dropdownbox = driver.find_element(By.TAG_NAME, 'select')
ddboptions = dropdownbox.find_elements(By.TAG_NAME, 'option')

def scrap_result(query):
    # individual result page
    driver.get(URL + "?" + query)

    # draw date and draw number
    info_element = driver.find_element(By.CSS_SELECTOR, '.table.table-striped.orange-header thead')
    draw_date = info_element.find_element(By.CSS_SELECTOR, '.drawDate').text
    draw_number = info_element.find_element(By.CSS_SELECTOR, '.drawNumber').text.split()[-1]

    # scrap the top 3 prize into array
    top_three = []
    top_prize = driver.find_element(By.CSS_SELECTOR, ".table.table-striped.orange-header tbody").text.split()
    top_three.extend([top_prize[2], top_prize[5], top_prize[8]])

    # starter numbers
    starter = []
    starters_element = driver.find_element(By.CSS_SELECTOR, '.tbodyStarterPrizes').text.split()
    starter.extend(starters_element)

    # consolation numbers
    consolation = []
    consolation_element = driver.find_element(By.CSS_SELECTOR, '.tbodyConsolationPrizes').text.split()
    consolation.extend(consolation_element)

    return {'draw_date': draw_date, 'draw_number': draw_number, 'first': top_three[0], 'second': top_three[1], 'third': top_three[2], 'starter': starter, 'consolation': consolation}


for option in ddboptions:
    result_hash = scrap_result(option.get_attribute('querystring'))
    ipdb.set_trace()

driver.close()
