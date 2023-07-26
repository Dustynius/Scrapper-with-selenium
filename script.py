from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Remote(
    command_executor='http://hub:4444/wd/hub',
    options=chrome_options
)

client = MongoClient('mongodb://localhost:27017/')
db = client['mcs_assignment']
collection = db['quotes']

try:
    for page in range(10):
        for i in range(1, 11):
            quote_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[1]"
            author_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[2]/small"
            quote_element = driver.find_element(By.XPATH, quote_xpath)
            quote_text = quote_element.text
            author_element = driver.find_element(By.XPATH, author_xpath)
            author_name = author_element.text
            print("Quote:", quote_text)
            print("Author:", author_name)
            print()

            document = {
                'quote_id': page * 10 + i,
                'quote': quote_text,
                'author': author_name
            }
            collection.insert_one(document)

        try:
            next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
            next_button.click()
        except:
            print("No more pages available. Exiting loop.")
            break

finally:
    driver.quit()
