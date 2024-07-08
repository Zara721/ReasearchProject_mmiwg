import sqlite3
import pandas as pd
import re

# Connect to the SQLite database
sqliteConnection = sqlite3.connect(r'C:\Users\zaza2\canada_us_events.db')

# Create a cursor object
cursor = sqliteConnection.cursor()

# Define SQL query
query = """
SELECT MIN(me.DocumentIdentifier) as DocumentIdentifier, MAX(me.AllNames) as AllNames
FROM large_events me
WHERE (me.Counts LIKE '%KILL%' OR me.AllNames LIKE '%Murder&')
  AND me.Counts LIKE '%Canada%'
  AND (me.AllNames LIKE '%First Nation%' OR me.AllNames LIKE '%Indigenous%' OR me.Counts LIKE '%Indigenous%') AND me.Themes LIKE '%INDIGENOUS%'
  AND me.DocumentIdentifier NOT LIKE '%covid%' AND me.DocumentIdentifier NOT LIKE '%corona%' AND me.Themes NOT LIKE '%PANDEMIC%' AND me.THEMES NOT LIKE '%CORONAVIRUS%'
  AND me.DocumentIdentifier NOT LIKE '%pipeline%' AND me.Themes NOT LIKE '%PIPELINE%'
  AND me.Themes NOT LIKE '%SUICIDE%' AND me.Themes NOT LIKE '%MENTAL_HEALTH%' AND me.Themes NOT LIKE '%ILLEGAL_DRUGS%'
  AND me.Themes NOT LIKE 'EDUCATION%' AND me.Themes NOT LIKE 'GENERAL_GOVERNMENT%' AND me.Themes NOT LIKE 'GENERAL_HEALTH%' AND me.Themes NOT LIKE 'MANMADE_DISASTER_IMPLIED%' AND me.Themes NOT LIKE 'TAX_DISEASE%'
GROUP BY me.Themes
"""
# Executing the query
cursor.execute(query)

# Fetch all rows from the result set
results = cursor.fetchall()

# Convert the results to a DataFrame
df = pd.DataFrame(results, columns=['article_url', 'all_names'])

# Saving the DataFrame to a CSV file named 'url_all_names.csv'
df.to_csv('../data/url_all_names.csv', index=False)

# Close the connection to the SQLite database
sqliteConnection.close()

filename = '../project_data_files/frequency_tables/all_names_frequency_table.csv'


def parse_all_names(all_names):
    # Split the all_names string by semicolon
    all_names_list = all_names.split(';')

    # Remove all numbers and non-letter characters from each name
    cleaned_names_list = []
    for names in all_names_list:
        cleaned_name = re.sub(r'[^a-zA-Z]', '', names)
        cleaned_names_list.append(cleaned_name)

    return cleaned_names_list


# Applying the parse_themes function to the 'all_names' column of the DataFrame
df['all_names'] = df['all_names'].apply(parse_all_names)

# create a DataFrame with unique all_names as columns
all_names_df = pd.DataFrame(columns=df['all_names'].explode().unique())

#  iterate over each row in the original DataFrame
for index, row in df.iterrows():
    for name in row['all_names']:
        # Set the value to 1 if the name is present
        all_names_df.loc[index, name] = 1

# fill NaN values with 0 since some articles don't have certain names
all_names_df.fillna(0, inplace=True)

# save the new DataFrame to a CSV file
all_names_df.to_csv(filename, index=False)

# Reading the previously saved DataFrames
url_all_names_df = pd.read_csv('../project_data_files/url_all_names.csv')
all_names_frequency_df = pd.read_csv(filename)

# Concatenating the data frames so that the all_names_frequency_table has the article_url column
concatenated_df = pd.concat([all_names_frequency_df, url_all_names_df['article_url']], axis=1)

# Overwriting the 'all_names_frequency_table.csv' file, so it has the article_url column
concatenated_df.to_csv(filename, index=False)


