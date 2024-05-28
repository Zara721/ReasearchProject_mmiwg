import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

'''
Sources:
https://www.youtube.com/watch?v=iNlZ3IU5Ffw
'''

df = pd.read_csv('../data/theme_frequency_table.csv', index_col='article_url')

# since the data only holds binary values no need to standardize the data
# scaler = StandardScaler()
# df[['KILL_T', 'TAX_ETHNICITY_INDIGENOUS_T']] = scaler.fit_transform(df[['KILL', 'TAX_ETHNICITY_INDIGENOUS']])


# function that works out optimum number of clusters
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

# optimise_k_means(df, 12)


kmeans = KMeans(n_clusters=7)
kmeans.fit(df)
df['kmeans_7'] = kmeans.labels_

# pd.set_option('display.max_columns', None)
# pd.set_option('max_colwidth', None)
# # print(df['kmeans_3'])
# print(df['kmeans_7'].head(50))

# plt.scatter(x=df['KILL'], y=df['TAX_ETHNICITY_INDIGENOUS'], c=df['kmeans_7'])
# plt.xlim(-0.1, 7)
# plt.ylim(-0.1, 7)
# plt.show()

x = np.array([0, 1, 2, 3, 4, 5, 6])
y = []

counts = df['kmeans_7'].value_counts()

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

# plt.bar(x, y)
# # plt.xlabel('Cluster Groups')
# # plt.ylabel('Articles')
# # plt.title('Cluster Distribution')
# # plt.show()

# Sort the DataFrame by the 'kmeans' column in ascending order
sorted_df = df[['kmeans_7']].sort_values(by='kmeans_7', ascending=True)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', None)
print(sorted_df)