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
SELECT MIN(me.DocumentIdentifier) as DocumentIdentifier, MAX(me.Counts) as Counts, me.Themes
FROM large_events me
WHERE (me.Counts LIKE '%KILL%' OR me.AllNames LIKE '%Murder&')
  AND me.Counts LIKE '%Canada%'
  AND (me.AllNames LIKE '%First Nation%' OR me.Counts LIKE '%Indigenous%' OR me.Themes LIKE '%INDIGENOUS%')
  AND me.DocumentIdentifier NOT LIKE '%covid%' AND me.DocumentIdentifier NOT LIKE '%corona%' AND me.Themes NOT LIKE '%PANDEMIC%' AND me.THEMES NOT LIKE '%CORONAVIRUS%'
  AND me.DocumentIdentifier NOT LIKE '%pipeline%' AND me.Themes NOT LIKE '%PIPELINE%'
  AND me.Themes NOT LIKE 'EDUCATION%' AND me.Themes NOT LIKE 'GENERAL_GOVERNMENT%' AND me.Themes NOT LIKE 'GENERAL_HEALTH%' AND me.Themes NOT LIKE 'MANMADE_DISASTER_IMPLIED%' AND me.Themes NOT LIKE 'TAX_DISEASE%'
GROUP BY me.Themes;
"""

cursor.execute(query)

# Fetch all rows from the result set
results = cursor.fetchall()

# Create a PrettyTable instance
table = PrettyTable(['Document Identifier', 'Counts', 'Themes'])

# Set the alignment of the table to LEFT
table.align = "l"

# Add headers
table.field_names = ['Document Identifier', 'Counts', 'Themes']

# Add rows to the table
for row in results:
    table.add_row([row[0], row[1], row[2]])

# Print the table
print(table)

# Collect document identifiers (urls) into a list
document_identifiers = [row[0] for row in results]

# Print the list of document identifiers (urls)
print(document_identifiers)

# Close the connection to the SQLite database
sqliteConnection.close()


