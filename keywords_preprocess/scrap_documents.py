import os
import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

# 데이터 로드
df = pd.read_csv('../ai_model_data/raw_data/model_06_15.csv')
model_name_list = list(df['id'])

# 폴더 생성
os.makedirs('./documents', exist_ok=True)

# 오류 및 모델 카드 없음 파일 경로 설정
error_file_path = './error_model.txt'
model_card_no_file_path = './model_card_no.txt'

def fetch_model_page(model_name):
    url = f'https://huggingface.co/{model_name}'
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        file_path = f'./documents/{model_name.replace("/", "_", 1)}.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
    
    except Exception:
        with open(error_file_path, 'a', encoding='utf-8') as error_file:
            error_file.write(f"{model_name}\n")
    
    # 서버 부하 방지를 위해 랜덤 대기 시간 추가 (0.5 ~ 1.5초)
    time.sleep(random.uniform(0.5, 1.5))

# 첫 500개 모델 실행 (tqdm 추가)
for model_name in tqdm(model_name_list[:500], desc="Fetching models"):
    fetch_model_page(model_name)