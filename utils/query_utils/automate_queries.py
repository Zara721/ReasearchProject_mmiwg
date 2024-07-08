import sqlite3
from prettytable import PrettyTable

# Connect to the SQLite database
sqliteConnection = sqlite3.connect(r'C:\Users\zaza2\canada_us_events.db')

# Create a cursor object
cursor = sqliteConnection.cursor()

kewords = ["Tina Fontaine", "Robert", "Pickton"]

where_clause = ""

# Check if there are any keywords to filter by
if kewords:
    # Start the WHERE clause with the first condition
    where_clause = "WHERE AllNames LIKE '%{}%'".format(kewords[0])

    for keyword in kewords[1:]:
        where_clause += " OR AllNames LIKE '%{}%'".format(keyword)

# Define and execute the query
query = f"""
SELECT * 
FROM full_events
{where_clause}
GROUP BY AllNames
"""
print(query)

# cursor.execute(query)
#
# # Fetch all rows from the result set
# results = cursor.fetchall()
