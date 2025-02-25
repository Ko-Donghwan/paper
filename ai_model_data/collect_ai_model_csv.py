from huggingface_hub import HfApi
import pandas as pd
from tqdm import tqdm
import ast
from datetime import datetime

now = datetime.now()
output_csv_file = f'../raw_data/Model_{now.month:02d}_{now.day:02d}.csv'

api = HfApi()
models_data = list(tqdm(api.list_models(full=True), desc="Fetching model metadata"))

df = pd.DataFrame(models_data).drop(columns=['siblings', 'sha', 'mask_token', 'card_data', 'widget_data', 'model_index', 'config', 'transformers_info', 'spaces', 'safetensors'], errors='ignore')

df[['arxiv', 'dataset', 'region', 'license']] = ''

def process_tags(tags):
    tag_map = {key: None for key in ['arxiv:', 'dataset:', 'region:', 'license:']}
    new_tags = []
    
    for tag in tags:
        lower_tag = tag.lower()
        for key in tag_map:
            if lower_tag.startswith(key):
                tag_map[key] = tag
                break
        else:
            new_tags.append(tag)
    
    return tuple(tag_map.values()) + (new_tags,)

df.loc[:, ['arxiv', 'dataset', 'region', 'license', 'tags']] = df['tags'].apply(lambda tags: process_tags(ast.literal_eval(tags) if isinstance(tags, str) else tags)).apply(pd.Series)
df.to_csv(output_csv_file, index=False)