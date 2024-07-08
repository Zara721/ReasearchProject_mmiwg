import sqlite3
import pandas as pd

# Connect to the SQLite database
sqliteConnection = sqlite3.connect(r'C:\Users\zaza2\canada_us_events.db')

# Create a cursor object
cursor = sqliteConnection.cursor()

# Define SQL query
query = """
SELECT MIN(me.DocumentIdentifier) as DocumentIdentifier, MAX(me.Counts) as Counts
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
df = pd.DataFrame(results, columns=['article_url', 'counts'])

# Saving the DataFrame to a CSV file named 'url_counts.csv'
df.to_csv('../data/url_counts.csv', index=False)

# Close the connection to the SQLite database
sqliteConnection.close()

filename = '../project_data_files/frequency_tables/counts_frequency_table_v2.csv'


def parse_counts(counts):
    # Split the counts string by hash
    count_list = counts.split('#')
    return count_list


# Applying the parse_themes function to the 'counts' column of the DataFrame
df['counts'] = df['counts'].apply(parse_counts)

# create a DataFrame with unique counts as columns
counts_df = pd.DataFrame(columns=df['counts'].explode().unique())

#  iterate over each row in the original DataFrame
for index, row in df.iterrows():
    for count in row['counts']:
        # Set the value to 1 if the count is present
        counts_df.loc[index, count] = 1

# fill NaN values with 0 since some articles don't have certain counts
counts_df.fillna(0, inplace=True)

# Remove columns with numeric names
numeric_columns = [col for col in counts_df.columns if col.replace('.', '', 1).isnumeric()]
counts_df.drop(numeric_columns, axis=1, inplace=True)

# save the new DataFrame to a CSV file
counts_df.to_csv(filename, index=False)

# Reading the previously saved DataFrames
url_counts_df = pd.read_csv('../project_data_files/url_counts.csv')
count_frequency_df = pd.read_csv(filename)

# Concatenating the data frames so that the count_frequency_table has the article_url column
concatenated_df = pd.concat([count_frequency_df, url_counts_df['article_url']], axis=1)

# Overwriting the 'counts_frequency_table.csv' file, so it has the article_url column
concatenated_df.to_csv(filename, index=False)
