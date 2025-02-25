import selenium
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from httpcore import TimeoutException
from tqdm import tqdm
import random

with open('./kaggle_model_sources.txt', 'r', encoding='utf-8') as file:
    content = file.read()

model_address_list = content.splitlines()

driver = webdriver.Chrome()

start_index = 3046 + 1215 + 948
end_index = 7608


for i in tqdm(range(start_index, end_index)):
    driver.get(model_address_list[i])
    
    # JavaScript를 이용해 페이지 끝까지 스크롤 (Python에서 실행)
    scroll_pause = random.uniform(2, 5)  # 2초에서 5초 사이의 랜덤한 대기 시간
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause)  # 스크롤 후 대기 시간

    # JavaScript를 통해 페이지 전체 HTML 가져오기
    try:
        # JavaScript로 전체 페이지의 HTML을 추출
        page_HTML = driver.execute_script(
            "return document.documentElement.outerHTML;"
        )

        # 모델 이름을 URL에서 추출
        model_name = model_address_list[i].replace('https://www.kaggle.com/models/', '').replace('/', '_', 1)
        
        # 인덱스를 파일 이름에 추가하여 고유한 파일 이름 생성
        file_name = f'./model_html/{model_name}_Page_HTML.txt'
        
        # 파일로 HTML 내용 저장
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(page_HTML)

    except Exception as e:
        print(f"Error: {str(e)}. Could not retrieve the page content for index {i}.")

    # 3초에서 7초 사이의 랜덤한 대기 시간
    random_sleep = random.uniform(3, 7)
    time.sleep(random_sleep)

# 최종 드라이버 종료
driver.quit()