from bs4 import BeautifulSoup
from tqdm import tqdm
import os
import json
import re

folder_path = './model_html' 
files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]

file_rm_list = []

for i in tqdm(range(len(files)), desc = "Processing files"):
    fname_rm_dir = files[i].replace('./model_html\\', '')
    fname_rm_ext = fname_rm_dir.split('_Page_HTML.txt')[0]
    file_rm_list.append(fname_rm_ext)

for j in tqdm(range(0, len(files), 1)):
    with open(files[j], 'r', encoding='utf-8') as f:
        content = f.read() # 파일 내용 출력
    soup = BeautifulSoup(content, 'lxml')
    site_container = soup.find('div', id='site-container')

    folder_path = './model_contents/'

    file_path = folder_path + file_rm_list[j] + '.txt'
    if site_container:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(site_container))
    else:
        pass