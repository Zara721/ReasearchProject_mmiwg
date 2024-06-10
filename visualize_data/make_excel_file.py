import pandas as pd
import openpyxl

# Read JSON data into a DataFrame
df = pd.read_json(r'C:\Users\zaza2\PycharmProjects\ReasearchProject\data\url_data\url_data.json',  lines=True)

# Create an Excel file with the DataFrame
df.to_excel('mmiwg_urls.xlsx', index=False)
