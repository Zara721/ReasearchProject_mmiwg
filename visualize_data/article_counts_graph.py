import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Set global font properties
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Tahoma']

# Connect to the SQLite database
sqliteConnection = sqlite3.connect(r'C:\Users\zaza2\canada_us_events.db')

# Execute a SQL query and load the results into a DataFrame
query = """
SELECT Date, COUNT(*) as article_count 
FROM mmiwg_related_articles
GROUP BY Date;
"""
df = pd.read_sql_query(query, sqliteConnection)

# Convert the Date column to Datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d%H%M%S')

# Extract the year from the Date column and set it as a new column
df['year'] = df['Date'].dt.year

# Group by year and count the number of articles per year
df_yearly = df.groupby('year')['article_count'].sum().reset_index()

# Sort the DataFrame by year
df_yearly.sort_values(by='year', inplace=True)

# Close the connection
sqliteConnection.close()

# Create a list of years from 2015 to 2024
years = list(range(2015, 2025))

# Plot a bar chart of the article counts per year with manual x-ticks
plt.figure(figsize=(10, 6), facecolor="#e3dccf")
plt.axes().set_facecolor("#f5f2ed")
plt.bar(years, df_yearly['article_count'], color='#3d8a91')
plt.title('MMIWG Articles Counts (2015-2024)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Article Count', fontsize=12)
plt.xticks(years, rotation=45, ha='right')  # Manually set x-ticks and labels
plt.tight_layout()  # Ensures labels do not overlap
plt.show()
