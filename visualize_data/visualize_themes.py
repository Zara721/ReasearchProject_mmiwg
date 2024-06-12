import pandas as pd
import matplotlib.pyplot as plt

file_path = 'data/article_themes_frequency_chart.csv'
df = pd.read_csv(file_path)

# Calculate the sum of each column
sum_row = df.sum()

# Create a DataFrame for the sum row
sum_df = pd.DataFrame(sum_row).T

# Rename the index of the sum DataFrame to 'total'
sum_df.index = ['total']

# Concatenate the original DataFrame with the sum DataFrame
df_final = pd.concat([df, sum_df])

# Calculate the top 30 values from the total row
top_30_totals = df_final.loc['total'].nlargest(30)

print(df)

# Set figure size for the plot
plt.figure(figsize=(12, 10), facecolor="#e3dccf")

plt.axes().set_facecolor("#f5f2ed")

# Plot the bar chart with the top 30 totals and their counts
plt.barh(top_30_totals.index, top_30_totals.values, color='#3d6391')

# Customize the plot
plt.xlabel('Number of Articles', fontsize=12)
plt.ylabel('Theme')
plt.title('Top 30 Themes Across Articles', fontsize=20, pad=20)
plt.gca().invert_yaxis()  # Invert y-axis so higher counts are at the top

plt.show()
