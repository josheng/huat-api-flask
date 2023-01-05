from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import ipdb
import psycopg2

# set up headless chrome browser
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

URL = 'https://www.singaporepools.com.sg/en/product/pages/4d_results.aspx'

driver.get(URL)

# wait for js snippet to load
print("Waiting for element to load ⏳")
element_present = EC.presence_of_element_located((By.TAG_NAME, 'select'))
WebDriverWait(driver, timeout=10).until(element_present)
print("Element Loaded ✅")

# get query string from drop down box to scrap individual date results
dropdownbox = driver.find_element(By.TAG_NAME, 'select')
ddboptions = dropdownbox.find_elements(By.TAG_NAME, 'option')
queryarr = []
print("Saving query string 📝")
for query in ddboptions:
    queryarr.append(query.get_attribute('querystring'))

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


# Connect to the database
conn = psycopg2.connect(
    "host=localhost dbname=huat_api_flask")

# Create a cursor
cursor = conn.cursor()

print("Seeding data 🌱")
for querystring in queryarr:
    result_hash = scrap_result(querystring)
    print(f"Saving draw number {result_hash['draw_number']} ")
    cursor.execute(
        "INSERT INTO fourds (drawnumber, drawdate, first, second, third, starter, consolation) VALUES (%s,%s,%s,%s,%s,%s,%s)", (result_hash['draw_number'], result_hash['draw_date'], result_hash['first'], result_hash['second'], result_hash['third'], result_hash['starter'], result_hash['consolation']))
    # ipdb.set_trace()


print("Commit to database 🚀")
conn.commit()
# Close the cursor and connection
cursor.close()
conn.close()
driver.close()
print("Seeding complete! ✅")

# Run this 2 command to create db and table in psql
# CREATE DATABASE huat_api_flask
# CREATE TABLE fourds(id serial PRIMARY KEY,drawnumber varchar, drawdate date, first varchar, second varchar, third varchar, starter varchar, consolation varchar,created_at timestamptz DEFAULT NOW());
