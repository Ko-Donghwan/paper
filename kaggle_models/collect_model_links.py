import selenium
import time
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://www.kaggle.com/models?query=&task=&lang=&id=&datatype=&framework=&license=&size=&fine-tunable=&minUsabilityRating=&publisher=")

model_address_list = []

i = 0

while i< 642:
    j = 1
    for j in range(1, 13, 1):
        try:
            model_address_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="site-content"]/div[2]/div/div[6]/div/div/div/ul[1]/li[{j}]/div/a'))
            )
            model_address = model_address_element.get_attribute('href')
            model_address_list.append(model_address)
        except Exception as e:
            print(f"Error finding element {j}: {e}")

    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div[2]/div/div[6]/div/div/div/ul[2]/li[11]/button'))
        )
        driver.execute_script("arguments[0].click();", button)
    except Exception as e:
        print(f"Error clicking button: {e}")

    i += 1

# Save the list contents to a text file
with open('./kaggle_model_sources2.txt', 'w', encoding='utf-8') as file:
    for model_address in model_address_list:
        file.write(model_address + '\n')