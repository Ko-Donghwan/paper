import pandas as pd
import re
from collections import Counter, defaultdict

def load_model_data(file_path, sheet_name='Sheet1'):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return dict(zip(df['Field'][0:], df['Value'][0:]))

def remove_emojis(text):
    emoji_pattern = re.compile(
        "[\U00010000-\U0010FFFF]|"  # 이모티콘 (U+1F600 ~ U+1F64F 등)
        "[\u2600-\u26FF]|"         # 기호 (U+2600 ~ U+26FF)
        "[\u2700-\u27BF]"          # 기호 (U+2700 ~ U+27BF)
        "+", flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def split_and_process(data_list):
    processed_data = []
    for item in data_list:
        cleaned_item = item.replace("[Optional]", "").replace("[optional]", "").strip()
        cleaned_item = remove_emojis(cleaned_item)
        if len(cleaned_item.split()) >= 4:
            continue
        sub_keys = [k.strip() for k in cleaned_item.replace("&", ",").replace(" and ", ",").split(",")]
        processed_data.extend(k.replace(' ', '').lower() for k in sub_keys if k)
    return processed_data

def count_keywords(keyword_list):
    type_count = defaultdict(int)
    for item in keyword_list:
        type_count[type(item)] += 1
    str_items = [item for item in keyword_list if isinstance(item, str)]
    processed_data = split_and_process(str_items)
    keyword_counts = Counter(processed_data)
    return keyword_counts.most_common()

def save_to_excel(data, output_file, sheet_name='Keyword Counts'):
    df = pd.DataFrame(data, columns=['Keyword', 'Frequency'])
    df.to_excel(output_file, index=False, sheet_name=sheet_name)
    print(f"Keyword frequencies saved to '{output_file}'.")

if __name__ == "__main__":

    input_file = './Model_Keyword_Frequency2.xlsx'
    output_file = '../compare_hub/data/huggingface_keywords1.xlsx'
    model_dict = load_model_data(input_file)
    keyword_list = [key for key, count in model_dict.items() for _ in range(count)]
    keyword_counts = count_keywords(keyword_list)
    save_to_excel(keyword_counts, output_file)
