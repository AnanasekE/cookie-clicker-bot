import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://x-kom.pl")

button = driver.find_element(By.XPATH, "//button[@data-name='AcceptPermissionButton']")
button.click()



time.sleep(500)