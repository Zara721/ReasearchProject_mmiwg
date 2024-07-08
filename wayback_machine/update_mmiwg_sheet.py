import json
import pandas as pd

mmiwg_data_df = pd.read_excel('../visualize_data/data/mmiwg_urls.xlsx', engine='openpyxl')
print(mmiwg_data_df.head())

# Load JSON data from file
with open('output_files/wayback_article_content.json', 'r') as file:
    data = json.load(file)

# Convert JSON data to DataFrame
new_articles_df = pd.DataFrame(data)

# Drop rows where 'url' is null
new_articles_df.dropna(subset=['url'], inplace=True)

print(new_articles_df.head())

# Append JSON data to existing DataFrame
combined_df = pd.concat([mmiwg_data_df, new_articles_df], ignore_index=True)

# Write combined DataFrame to Excel file
combined_df.to_excel('../visualize_data/data/updated_mmiwg_urls.xlsx', index=False, engine='openpyxl')

