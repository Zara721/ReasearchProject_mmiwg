import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

'''
Sources:
https://www.youtube.com/watch?v=iNlZ3IU5Ffw
https://www.w3schools.com/python/matplotlib_intro.asp
https://builtin.com/data-science/pandas-show-all-columns
'''

df = pd.read_csv('../project_data_files/frequency_tables/counts_frequency_table_v2.csv', index_col='article_url')


def optimise_k_means(data, max_k):
    means = []
    inertias = []

    for k in range(1, max_k):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(data)

        means.append(k)
        inertias.append(kmeans.inertia_)

    # generate elbow plot
    # fig = plt.subplot(10, 5)
    plt.plot(means, inertias, 'o-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.grid(True)
    plt.show()


optimise_k_means(df, 10)

kmeans = KMeans(n_clusters=5)
kmeans.fit(df)
kmeans_colname = 'kmeans_5'
df[kmeans_colname] = kmeans.labels_

x = np.array([0, 1, 2, 3, 4, 5, 6, 7])
y = []

counts = df[kmeans_colname].value_counts()

# Iterate over x and append the count for each number in x to y
for num in x:
    if num in counts.index:
        y.append(counts[num])
    else:
        # Handle cases where a number in x does not appear in 'kmeans_7'
        y.append(0)  # Or handle differently based on your requirements

# Convert y to a NumPy array
y = np.array(y)

print(counts)

# Sort the DataFrame by the 'kmeans' column in ascending order
sorted_df = df[[kmeans_colname]].sort_values(by=kmeans_colname, ascending=True)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', None)
print(sorted_df)
