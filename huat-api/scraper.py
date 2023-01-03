from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

URL = 'https://www.singaporepools.com.sg/en/product/pages/4d_results.aspx'

driver.get(URL)


print("Waiting..")
element_present = EC.presence_of_element_located((By.TAG_NAME, 'select'))
WebDriverWait(driver, timeout=10).until(element_present)
print("Wait Complete")
dropdownbox = driver.find_element(By.TAG_NAME, 'select')
ddboptions = dropdownbox.find_elements(By.TAG_NAME, 'option')

# for option in ddboptions:
#     print(option.get_attribute('querystring'))

topresult = ddboptions[0].get_attribute('querystring')
driver.get(URL + "?" + topresult)
print(driver.title)

driver.close()
