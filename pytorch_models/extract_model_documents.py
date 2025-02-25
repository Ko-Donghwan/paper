import time
import random
from tqdm import tqdm
from selenium import webdriver
import os

if not os.path.exists('./documents'):
    os.makedirs('./documents')

with open('pytorch_model_sources.txt', 'r', encoding='utf-8') as f:
    content = f.read()

model_address_list = content.splitlines()

driver = webdriver.Chrome()

start_index = 0
end_index = len(model_address_list)

def save_html_to_file(model_address, page_html):
    model_name = model_address.replace('https://pytorch.org/hub/', '').replace('/', '', 1)
    
    model_name = model_name.replace(':', '').replace('?', '').replace('<', '').replace('>', '')
    
    file_name = f'./documents/{model_name}.txt'
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(page_html)

for i in tqdm(range(start_index, end_index)):
    driver.get(model_address_list[i])
    
    scroll_pause = random.uniform(2, 5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause)

    page_HTML = driver.execute_script("return document.documentElement.outerHTML;") # 페이지 추출
    save_html_to_file(model_address_list[i], page_HTML)

    random_sleep = random.uniform(3, 7)
    time.sleep(random_sleep)

driver.quit()