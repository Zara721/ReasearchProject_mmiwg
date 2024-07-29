import sqlite3
import pandas as pd

# Currently, the database mmiwg_related_articles has 4613 total entries, 3087 have titles and body
# Read the Excel file
excel_file_path = r'wayback_machine/output_files/urls_output.xlsx'
df = pd.read_excel(excel_file_path)

# Connect to the SQLite database
sqliteConnection = sqlite3.connect(r'C:\Users\zaza2\canada_us_events.db')
cursor = sqliteConnection.cursor()

# Access the table with mmiwg events
table_name = 'mmiwg_related_articles'

# Iterate through URLs and update the database
for index, row in df.iterrows():
    url = row['url']
    title = row['title']
    body = row['body']

    # Check if the URL exists in the database
    cursor.execute(f"SELECT * FROM {table_name} WHERE Urls=?", (url,))
    result = cursor.fetchone()

    if result:
        # Update the existing record
        cursor.execute(f"""
            UPDATE {table_name}
            SET title=?, body=? 
            WHERE Urls=?
        """, (title, body, url))
    else:
        # Insert a new record if not found
        cursor.execute(f"""
            INSERT INTO {table_name} (Urls, title, body)
            VALUES (?, ?, ?)
        """, (url, title, body))

# Commit the changes and close the connection
sqliteConnection.commit()
sqliteConnection.close()

