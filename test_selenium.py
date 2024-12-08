from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

opts = FirefoxOptions()
opts.add_argument("--headless")
driver = webdriver.Firefox(options=opts)
driver.get("http://www.usamega.com/powerball/results")
elem = driver.find_element(
    By.XPATH, '/html/body/div[1]/main/div[4]/table/thead/tr/td[1]')
print(f'Text output - {str(elem.text)}')

elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
