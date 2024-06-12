import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/article_themes_date.csv')

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H%M%S')

# Convert the 'date' column to datetime and extract the year
df['year'] = df['date'].dt.year

# Drop the original 'date' column
df.drop(columns=['date'], inplace=True)

# Set the index to the 'year' column
df.set_index('year', inplace=True)

# List of themes to exclude
themes_to_exclude = ['TAX_FNCACT', 'AFFECT', 'Unnamed: 101', 'TAX_ETHNICITY', 'CRISISLEX_CRISISLEXREC']


# Function to find the top 10 themes for a given year
def top_10_themes(year):
    # Filter rows for the given year
    filtered_df = df.loc[year]

    # Select all columns except those representing excluded themes
    filtered_columns = filtered_df.columns.difference(themes_to_exclude)

    # Filter the DataFrame to only include selected columns
    filtered_df = filtered_df.loc[:, filtered_columns]

    # Count occurrences of each remaining theme
    theme_counts = filtered_df.sum()

    # Sort themes by count and select the top 10
    top_10 = theme_counts.sort_values(ascending=False).head(10)

    return top_10


# Define the year ranges for each figure
year_ranges = [(2015, 2018), (2019, 2022), (2023, 2024)]

# Create three figures with subplots arranged in grids with two columns each
figs = []
for start_year, end_year in year_ranges:
    num_years = end_year - start_year + 1
    num_rows = num_years // 2 + (num_years % 2)
    fig, axs = plt.subplots(num_rows, 2, figsize=(20, 10), facecolor="#e3dccf")
    figs.append((fig, axs))
    axs = axs.flatten()

    # Iterate over the years and plot the top 10 themes for each year
    for i, year in enumerate(range(start_year, end_year+1)):
        top_10 = top_10_themes(year)
        axs[i].bar(top_10.index, top_10.values, width=0.7, color='#3d6391')
        axs[i].set_title(f'Top 10 Themes for Year {year}', fontsize=10)
        axs[i].set_facecolor("#f5f2ed")
        # axs[i].set_xlabel('Themes', fontsize=8)
        # axs[i].set_ylabel('Occurrences', fontsize=8)

        # Rotate the x-axis labels
        axs[i].set_xticklabels(axs[i].get_xticklabels(), rotation=45, ha='right')
        axs[i].tick_params(axis='both', length=0)

    # Adjust layout to fit subplots properly
    plt.tight_layout()
    plt.show()

# Display the figures
for fig, _ in figs:
    plt.sca(fig)  # Switch to the current figure
    plt.draw()  # Redraw the figure
