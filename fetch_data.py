import sqlite3
import pandas as pd

# Connect to the SQLite database
sqliteConnection = sqlite3.connect(r'C:\Users\zaza2\canada_us_events.db')

# Create a cursor object
cursor = sqliteConnection.cursor()

# Define and execute the query
query = """
SELECT MIN(me.DocumentIdentifier) as DocumentIdentifier, me.Themes
FROM large_events me
WHERE (me.Counts LIKE '%KILL%' OR me.AllNames LIKE '%Murder&')
  AND me.Counts LIKE '%Canada%'
  AND (me.AllNames LIKE '%First Nation%' OR me.Counts LIKE '%Indigenous%' OR me.Themes LIKE '%INDIGENOUS%')
  AND me.DocumentIdentifier NOT LIKE '%covid%' AND me.DocumentIdentifier NOT LIKE '%corona%' AND me.THEMES NOT LIKE '%PANDEMIC%' AND me.THEMES NOT LIKE '%CORONAVIRUS%'
  AND me.DocumentIdentifier NOT LIKE '%pipeline%' AND me.THEMES NOT LIKE '%PIPELINE%'
  AND me.THEMES NOT LIKE 'EDUCATION%' AND me.THEMES NOT LIKE 'GENERAL_GOVERNMENT%' AND me.THEMES NOT LIKE 'GENERAL_HEALTH%' AND me.THEMES NOT LIKE 'MANMADE_DISASTER_IMPLIED%' AND me.THEMES NOT LIKE 'TAX_DISEASE%'
GROUP BY me.Themes;
"""

cursor.execute(query)

# Fetch all rows from the result set
results = cursor.fetchall()

# Convert the results to a DataFrame
df = pd.DataFrame(results, columns=['article_url', 'themes'])

df.to_csv('url_themes.csv', index=False)

# Close the connection to the SQLite database
sqliteConnection.close()


def parse_themes(themes):
    # Split the themes string by semicolon
    theme_list = themes.split(';')
    return theme_list


df['themes'] = df['themes'].apply(parse_themes)

# create a DataFrame with unique themes as columns
themes_df = pd.DataFrame(columns=df['themes'].explode().unique())

#  iterate over each row in the original DataFrame
for index, row in df.iterrows():
    for theme in row['themes']:
        # Set the value to 1 if the theme is present, else 0
        themes_df.loc[index, theme] = 1

# fill NaN values with 0 since some articles might not have certain themes
themes_df.fillna(0, inplace=True)

# save the new DataFrame to a CSV file
themes_df.to_csv('theme_frequency_table.csv', index=False)
