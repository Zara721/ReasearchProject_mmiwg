import sqlite3
from prettytable import PrettyTable

# Connect to the SQLite database
sqliteConnection = sqlite3.connect(r'C:\Users\zaza2\canada_us_events.db')

# Create a cursor object
cursor = sqliteConnection.cursor()

# Define and execute the query
query = """
SELECT Urls, DATE
FROM mmiwg_related_articles
WHERE TITLE IS NULL
"""

cursor.execute(query)

# Fetch all rows from the result set
results = cursor.fetchall()

# Create a PrettyTable instance
table = PrettyTable(['Document Identifier', "DATE"])

# Set the alignment of the table to LEFT
table.align = "l"

# Add headers
table.field_names = ['article_url', 'date']

# Add rows to the table
for row in results:
    table.add_row([row[0], row[1]])

# # Print the table
# print(table)

# Collect document identifiers (urls) into a list
document_identifiers = [row[0] for row in results]

# Print the list of document identifiers (urls)
print(len(document_identifiers))
print(document_identifiers)

# all_names = [row[1] for row in results]
# print(all_names)

# Close the connection to the SQLite database
sqliteConnection.close()

