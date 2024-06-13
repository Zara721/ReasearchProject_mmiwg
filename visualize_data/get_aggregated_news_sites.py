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

domain_variations = {
    "www.ctvnews.ca": ["winnipeg.ctvnews.ca", "montreal.ctvnews.ca", "calgary.ctvnews.ca", "atlantic.ctvnews.ca",
                       "barrie.ctvnews.ca", "kitchener.ctvnews.ca", "bc.ctvnews.ca", "windsor.ctvnews.ca",
                       "ottawa.ctvnews.ca", "vancouverisland.ctvnews.ca"],
    "thestarphoenix.com": ["www.another-example.com", "www.thestarphoenix.com", "thestarphoenix.com:443"],
    "theturtleislandnews.com": ["www.theturtleislandnews.com"],
    "www.huffingtonpost.ca": ["quebec.huffingtonpost.ca", "www.huffingtonpost.com"],
    "leaderpost.com": ["leaderpost.com:443", "www.thestarphoenix.com", "thestarphoenix.com:443"],
    "news.nationalpost.com": ["nationalpost.com"],
    "vancouversun.com": ["www.vancouversun.com", "blogs.vancouversun.com", "vancouversun.com:443"],
    "montrealgazette.com": ["montrealgazette.com:443", "www.montrealgazette.com"],
    "theprovince.com": ["www.theprovince.com"],
    "ottawacitizen.com": ["ottawacitizen.com:443", "www.ottawacitizen.com"],
    "calgaryherald.com": ["www.calgaryherald.com"],
    "edmontonsun.com": ["www.edmontonsun.com"],
    "winnipegsun.com": ["www.winnipegsun.com"],
}

# Count occurrences of each domain
domain_counts = df['domain'].value_counts().reset_index()
domain_counts.columns = ['domain', 'count']

# Merge with domain_variations to aggregate counts
merged_counts = domain_counts.copy()
for main_domain, variations in domain_variations.items():
    merged_counts.loc[merged_counts['domain'] == main_domain, 'count'] += domain_counts.loc[domain_counts['domain'].isin(variations), 'count'].sum()

# Filter domains with counts higher than 10 and exclude variations
filtered_domains = merged_counts[(merged_counts['count'] > 10) & (~merged_counts['domain'].isin([var for sublist in domain_variations.values() for var in sublist]))]

# Sort the filtered domains by count in descending order
sorted_filtered_domains = filtered_domains.sort_values(by='count', ascending=False)

# Create a bar graph with domain names on the y-axis
fig, ax = plt.subplots(figsize=(12, 10), facecolor="#e3dccf")
ax.set_facecolor("#f5f2ed")

# Plot the bars horizontally
ax.barh(sorted_filtered_domains['domain'], sorted_filtered_domains['count'], color='#913d61')

# Label the y-axis with domain names
ax.set_yticks(sorted_filtered_domains['domain'])
ax.set_yticklabels(sorted_filtered_domains['domain'])

# Set the title and labels
ax.set_title('Aggregated Domain Name Counts')
ax.set_xlabel('Count')
ax.set_ylabel('Domain Names')

plt.tight_layout()  # Adjust layout to prevent labels from overlapping
plt.show()
