import sqlite3

import numpy as np
import pandas as pd
from prettytable import PrettyTable

# Connect to the SQLite database
sqliteConnection = sqlite3.connect(r'C:\Users\zaza2\canada_us_events.db')

# Create a cursor object
cursor = sqliteConnection.cursor()

# Define and execute the query
query = """
SELECT DocumentIdentifier, DATE, AllNames 
FROM mmiwg_events
ORDER BY Themes;
"""

"""
SELECT DocumentIdentifier, DATE, Locations 
FROM small_test_data
ORDER BY DATE
"""


cursor.execute(query)

# Fetch all rows from the result set
results = cursor.fetchall()

# Create a PrettyTable instance
table = PrettyTable(['Document Identifier', 'Counts', 'Themes'])

# Set the alignment of the table to LEFT
table.align = "l"

# Add headers
table.field_names = ['article_url', 'themes', '-_-']

# Add rows to the table
for row in results:
    table.add_row([row[0], row[1], row[2]])

# # Print the table
# print(table)

# Collect document identifiers (urls) into a list
document_identifiers = [row[0] for row in results]

# Print the list of document identifiers (urls)
print(document_identifiers)

# Close the connection to the SQLite database
sqliteConnection.close()

