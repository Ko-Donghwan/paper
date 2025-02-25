from bs4 import BeautifulSoup
from tqdm import tqdm
import os
from collections import Counter
import pandas as pd

# 폴더 리스트 정의
folder_paths = ['./model_contents']

# HTML 파일의 헤딩 텍스트 추출
headings_text_list = []

# 모든 폴더에 대해 작업 수행
for folder_path in folder_paths:
    print(f"Processing folder: {folder_path}")
    
    # 폴더 내 .txt 파일 목록 가져오기
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]

    file_rm_list = []

    # 파일 이름에서 확장자 제거 및 리스트에 추가
    for i in tqdm(range(len(files)), desc="Generating file_rm_list"):
        fname_rm_dir = files[i].replace(folder_path + os.sep, '')
        fname_rm_ext = fname_rm_dir.split('.txt')[0]
        file_rm_list.append(fname_rm_ext)

    for i in tqdm(range(len(files)), desc="Extracting headings"):
        with open(files[i], 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        for heading in headings:
            headings_text_list.append(heading.get_text(strip=True))

    # 결과 출력 (필요 시 파일 저장 추가)
    print(f"Processed {len(files)} files in folder {folder_path}.")
    print(f"File removal list: {file_rm_list}")
    print(f"Extracted {len(headings_text_list)} headings.")

    # dict 타입이 아닌 요소들만 필터링
filtered_keywords = [keyword for keyword in headings_text_list if not isinstance(keyword, dict)]

# Counter를 사용하여 빈도수 계산
keyword_counts = Counter(filtered_keywords)

top_keywords = keyword_counts.most_common()
formatted_output = [f"{key}:{count}" for key, count in top_keywords]

# 데이터 처리 함수
def split_and_process(data_list):
    processed_data = []
    for item in data_list:
        # [Optional] 제거
        cleaned_item = item.replace("[Optional]", "").replace("[optional]", "").strip()
        # 키와 값을 분리
        if ':' in cleaned_item:
            key, value = cleaned_item.rsplit(":", 1)
            # 'and'와 '&'로 연결된 항목 분리
            sub_keys = [k.strip() for k in key.replace("&", ",").replace(" and ", ",").split(",")]
            for sub_key in sub_keys:
                if sub_key:  # 빈 항목은 제외
                    # 키워드 공백 제거 및 소문자로 변환
                    processed_data.append(f"{sub_key.replace(' ', '').lower()}:{value.strip()}")
        else:
            processed_data.append(cleaned_item.replace(" ", "").lower())
    return processed_data

formatted_data = split_and_process(formatted_output)

# 키워드와 빈도수 추출
keywords_with_counts = []
for item in formatted_data:
    if ':' in item:  # ':'이 있는 경우만 처리
        parts = item.split(':', 1)  # ':'로 분리
        if parts[1].isdigit():  # 숫자인 경우만 처리
            keywords_with_counts.append((parts[0], int(parts[1])))

# Counter 생성
counter = Counter()
for keyword, count in keywords_with_counts:
    counter[keyword] += count

# 키워드와 빈도수 추출
keywords_with_counts = []
for item in formatted_data:
    if ':' in item:  # ':'이 있는 경우만 처리
        parts = item.split(':', 1)  # ':'로 분리
        if parts[1].isdigit():  # 숫자인 경우만 처리
            keywords_with_counts.append((parts[0], int(parts[1])))

# Counter 생성
counter = Counter()
for keyword, count in keywords_with_counts:
    counter[keyword] += count

# 데이터를 데이터프레임으로 변환
df = pd.DataFrame(counter.most_common(), columns=['Keyword', 'Frequency'])

# 엑셀에 저장
output_file = './model_frequency/kaggle_model_keyword_frequency.xlsx'
df.to_excel(output_file, index=False, sheet_name='Keyword Counts')

print(f"Keyword frequencies saved to '{output_file}'.")