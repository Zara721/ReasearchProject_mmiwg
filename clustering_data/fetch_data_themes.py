import sqlite3
import pandas as pd

# Connect to the SQLite database
sqliteConnection = sqlite3.connect(r'C:\Users\zaza2\canada_us_events.db')

# Create a cursor object
cursor = sqliteConnection.cursor()

# Define SQL query
query = """
SELECT MIN(me.DocumentIdentifier) as DocumentIdentifier, me.Themes
FROM large_events me
WHERE (me.Counts LIKE '%KILL%' OR me.AllNames LIKE '%Murder&')
  AND me.Counts LIKE '%Canada%'
  AND (me.AllNames LIKE '%First Nation%' OR me.AllNames LIKE '%Indigenous%' OR me.Counts LIKE '%Indigenous%' OR me.Themes LIKE '%INDIGENOUS%')
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
df = pd.DataFrame(results, columns=['article_url', 'themes'])

# Saving the DataFrame to a CSV file named 'url_themes.csv'
df.to_csv('../data/url_themes.csv', index=False)

# Close the connection to the SQLite database
sqliteConnection.close()

filename = '../data/theme_frequency_table.csv'


def parse_themes(themes):
    # Split the themes string by semicolon
    theme_list = themes.split(';')

    # # Filter the list to keep only entries that contain the string "TAX_FNCACT"
    # filtered_theme_list = [theme for theme in theme_list if "TAX_FNCACT" in theme]
    return theme_list


# Applying the parse_themes function to the 'themes' column of the DataFrame
df['themes'] = df['themes'].apply(parse_themes)

# create a DataFrame with unique themes as columns
themes_df = pd.DataFrame(columns=df['themes'].explode().unique())

#  iterate over each row in the original DataFrame
for index, row in df.iterrows():
    for theme in row['themes']:
        # Set the value to 1 if the theme is present
        themes_df.loc[index, theme] = 1

# fill NaN values with 0 since some articles don't have certain themes
themes_df.fillna(0, inplace=True)

# save the new DataFrame to a CSV file
themes_df.to_csv(filename, index=False)

# Reading the previously saved DataFrames
url_themes_df = pd.read_csv('../data/url_themes.csv')
theme_frequency_df = pd.read_csv(filename)

# Concatenating the data frames so that the theme_frequency_table has the article_url column
concatenated_df = pd.concat([theme_frequency_df, url_themes_df['article_url']], axis=1)

# Overwriting the 'theme_frequency_table.csv' file, so it has the article_url column
concatenated_df.to_csv(filename, index=False)


