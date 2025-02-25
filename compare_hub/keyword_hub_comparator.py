import pandas as pd

def load_excel_files(file_paths):
    """Load multiple Excel files into separate DataFrames."""
    return [pd.read_excel(file) for file in file_paths]

def merge_dataframes(dfs, labels):
    """Merge multiple DataFrames on the 'Keyword' column with outer join."""
    merged_df = dfs[0]
    for df, label in zip(dfs[1:], labels[1:]):
        merged_df = merged_df.merge(df, on='Keyword', how='outer', suffixes=('', f'_{label}'))
    return merged_df

def filter_keywords_by_threshold(df, threshold=1000):
    """Filter keywords based on a frequency threshold."""
    df['Total_Frequency'] = df.iloc[:, 1:].sum(axis=1)
    return df[df['Total_Frequency'] >= threshold]

# File paths
file_paths = [
    '../data/model_keywords_with_counts.xlsx',
    '../data/kaggle_keywords_with_counts.xlsx',
    '../data/pytorch_keywords_with_counts.xlsx'
]

# Load data
huggingface_df, kaggle_df, pytorch_df = load_excel_files(file_paths)

# Merge data
merged_df = merge_dataframes([kaggle_df, pytorch_df, huggingface_df], ['kaggle', 'pytorch', 'huggingface'])
merged_df = merged_df.fillna(0).rename(columns={"Frequency": "Frequency_huggingface"})

# Filter and save
above_1000_df = filter_keywords_by_threshold(merged_df, threshold=1000)
above_1000_df.to_excel("../results/filtered_keywords_1000.xlsx", index=False)
