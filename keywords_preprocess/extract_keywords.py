from bs4 import BeautifulSoup
from tqdm import tqdm
import os
from collections import Counter
import pandas as pd

folder_path = './contents'
headings_count = {}

files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]

for file_path in tqdm(files, desc="Extracting headings"):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    for heading in headings:
        text = heading.get_text(strip=True)
        if text in headings_count:
            headings_count[text] += 1
        else:
            headings_count[text] = 1

headings_df = pd.DataFrame(list(headings_count.items()), columns=['Field', 'Value'])
headings_df.sort_values(by='Value', ascending=False, inplace=True)
headings_df.to_excel('./Model_Keyword_Frequency.xlsx', index=False)