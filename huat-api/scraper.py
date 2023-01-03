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

# print(driver.title)

# Wait for the page to load and the JavaScript code to be executed
# wait = Selenium: : WebDriver: : Wait.new(timeout: 10)
# wait.until {driver.find_element(: tag_name, 'select')}

# Select the element with the event listener
# dropdownbox = driver.find_element(: tag_name, 'select')
# ddboptions = dropdownbox.find_elements(: tag_name, 'option')

print("Waiting..")
element_present = EC.presence_of_element_located((By.TAG_NAME, 'select'))
# dropdownbox = WebDriverWait(driver, timeout=10).until(driver.find_element(By.TAG_NAME, 'select'))
WebDriverWait(driver, timeout=10).until(element_present)
print("Wait Complete")
dropdownbox = driver.find_element(By.TAG_NAME, 'select')
ddboptions = dropdownbox.find_elements(By.TAG_NAME, 'option')

for option in ddboptions:
    print(option.get_attribute('querystring'))


driver.close()
