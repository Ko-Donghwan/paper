import os
from tqdm import tqdm
from bs4 import BeautifulSoup

folder_path = "./documents"
txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

for i in tqdm(range(0, len(txt_files), 1)):
    file_path = os.path.join(folder_path, txt_files[i])
    
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 모델 본문
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 본문 섹션 추출
    model_card = soup.find_all('div', 'model-card-content') 

    if model_card:  # 섹션이 존재하는 경우에만 처리
        model_name = txt_files[i].replace('.txt', '')
        model_name_replace = model_name.replace('/', '_', 1)
        section_file_path = f"./contents/{model_name_replace}.txt"  # 파일 이름에 _side_section 추가

        # 섹션의 텍스트 내용만 파일에 저장
        with open(section_file_path, 'w', encoding='utf-8') as section_file:
            section_file.write(str(model_card[0]))