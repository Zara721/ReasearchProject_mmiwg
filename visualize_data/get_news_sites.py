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
SELECT DocumentIdentifier as url
FROM mmiwg_events
"""
df = pd.read_sql_query(query, sqliteConnection)

# Define a function to extract the domain from a URL
def extract_domain(url):
    return url.split('//')[-1].split('/')[0]

# Apply the function to the 'url' column to create a new 'domain' column
df['domain'] = df['url'].apply(extract_domain)

# Filter domains with counts higher than 15
domain_counts = df['domain'].value_counts()
filtered_domains = domain_counts[domain_counts > 10]

# Create a bar graph with domain names on the y-axis
fig, ax = plt.subplots(figsize=(12, 10), facecolor="#e3dccf")
ax.set_facecolor("#f5f2ed")

# Plot the bars horizontally
ax.barh(filtered_domains.index, filtered_domains.values, color='#913d61')

# Label the y-axis with domain names
ax.set_yticks(filtered_domains.index)
ax.set_yticklabels(filtered_domains.index)

# Set the title and labels
ax.set_title('Domain Name Counts')
ax.set_xlabel('Count')
ax.set_ylabel('Domain Names')

plt.tight_layout()  # Adjust layout to prevent labels from overlapping
plt.show()
