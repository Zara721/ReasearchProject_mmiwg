import sqlite3
from prettytable import PrettyTable

# Connect to the SQLite database
sqliteConnection = sqlite3.connect(r'C:\Users\zaza2\canada_us_events.db')

# Create a cursor object
cursor = sqliteConnection.cursor()

# Define and execute the query
query = """
SELECT me.DocumentIdentifier, me.Counts
FROM medium_events me
JOIN (
    SELECT DISTINCT GCAM
    FROM medium_events
    WHERE Counts LIKE '%KILL%' AND Counts LIKE '%Canada%' AND AllNames LIKE '%Indigenous%'
) AS unique_gcam ON me.GCAM = unique_gcam.GCAM;
"""
cursor.execute(query)

# Fetch all rows from the result set
results = cursor.fetchall()

# Create a PrettyTable instance
table = PrettyTable(['Document Identifier', 'Counts'])

# Set the alignment of the table to LEFT
table.align = "l"

# Add headers
table.field_names = ['Document Identifier', 'Counts']

# Add rows to the table
for row in results:
    table.add_row([row[0], row[1]])

# Print the table
print(table)

# Close the connection to the SQLite database
sqliteConnection.close()


