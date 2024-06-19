import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Set global font properties
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Tahoma']

# Connect to the SQLite database
sqliteConnection = sqlite3.connect(r'C:\Users\zaza2\canada_us_events.db')

# Execute a SQL query and load the results into a DataFrame
query = """
SELECT DATE as Date, DocumentIdentifier as ArticleLink
FROM mmiwg_events
"""

df = pd.read_sql_query(query, sqliteConnection)


# function that extracts the domain from a URL
def extract_domain(url):
    return url.split('//')[-1].split('/')[0]


# Apply the function to the 'url' column to create a new 'domain' column
df['Domain'] = df['ArticleLink'].apply(extract_domain)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', None)
# print(df.head())

mmiwg_urls_df = pd.read_excel("data/mmiwg_urls.xlsx")

merged_data_df = pd.merge(df, mmiwg_urls_df[['url', 'title']], left_on='ArticleLink', right_on="url", how='left')

merged_data_df.rename(columns={'title':'Title'}, inplace=True)
merged_data_df.rename(columns={'ArticleLink':'Article Link'}, inplace=True)
merged_data_df.drop('url', axis=1, inplace=True)

# Remove '#' symbol from the 'Title' column, cause of seperator
merged_data_df['Title'] = merged_data_df['Title'].str.replace('#', '')

# Convert the DATE column to datetime format
merged_data_df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d%H%M%S')

print(merged_data_df.head())

merged_data_df.to_csv('data/article_link_info.csv', sep='#', index=False)

