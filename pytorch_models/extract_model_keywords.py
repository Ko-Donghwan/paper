from bs4 import BeautifulSoup
from tqdm import tqdm
import os
import pandas as pd
from collections import Counter

folder_path = r'C:\Users\kodonghwan\Desktop\pytorch_models\documents'
files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')] 

file_list = []

for i in tqdm(range(len(files)), desc="Processing files"):
    fname = os.path.relpath(files[i], folder_path)
    file_list.append(fname)

headings_text_list = []

for i in tqdm(range(0, len(files)), desc="Extracting headings"):
    with open(files[i], 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    for heading in headings:
        headings_text_list.append(heading.get_text(strip=True))

filtered_keywords = [keyword for keyword in headings_text_list if isinstance(keyword, str)]

keyword_counts = Counter(filtered_keywords)

desc_keywords = keyword_counts.most_common()
formatted_output = [f"{key}:{count}" for key, count in desc_keywords]

data_list = [line.rsplit(":", 1) for line in formatted_output if len(line.rsplit(":", 1)) == 2]
df = pd.DataFrame(data_list, columns=["Keyword", "Frequency"])

df["Frequency"] = pd.to_numeric(df["Frequency"])

output_path = r'C:\Users\kodonghwan\Desktop\pytorch_models\pytorch_model_keyword_frequency.xlsx'
df.to_excel(output_path, index=False)