"""
Sources:
https://medium.com/@m3redithw/wordclouds-with-python-c287887acc8b
https://github.com/m3redithw/data-science-visualizations/blob/main/WordClouds/prepare.py
"""

import pandas as pd
import re
import unicodedata


def basic_clean(string):
    '''
    This function takes in a string and
    returns the string normalized.
    '''
    string = unicodedata.normalize('NFC', string)
    string = string.lower()
    string = re.sub(r"[^\w\s]", "", string)
    return string


def remove_extra_spaces(text):
    '''
    Removes extra spaces from the text.
    '''
    # Split the text into words, keeping spaces intact
    words = text.split()
    # Join the words back together without extra spaces
    return ' '.join(words)


# Adjusted basic_clean function
def adjusted_basic_clean(string):
    '''
    Adjusted basic_clean function to ensure no unintended spaces are introduced.
    '''
    string = unicodedata.normalize('NFC', string)
    string = string.lower()
    string = re.sub(r"[^\w\s]", "", string)
    return string


def clean_title_from_excel(file_path):
    """
    Reads an Excel file, extracts the 'title' column, concatenates all titles into a single string,
    and cleans the string using the provided cleaning functions.
    """
    # read the Excel file and extract the 'title' column
    df = pd.read_excel(file_path)
    titles = df['title'].tolist()  # Convert the 'title' column to a list

    # concatenate all titles into a single string
    concatenated_titles = ' '.join(str(title) for title in titles)

    # clean the concatenated string
    cleaned_string = adjusted_basic_clean(concatenated_titles)
    cleaned_string = remove_extra_spaces(cleaned_string)

    return cleaned_string


def clean_body_from_excel(file_path):
    """
    Reads an Excel file, extracts the 'body' column, concatenates all bodies into a single string,
    and cleans the string using the provided cleaning functions.
    """
    # read the Excel file and extract the 'title' column
    df = pd.read_excel(file_path)
    bodies = df['body'].tolist()  # Convert the 'title' column to a list

    # concatenate all bodies into a single string
    concatenated_bodies = ' '.join(str(body) for body in bodies)

    # clean the concatenated string
    cleaned_string = adjusted_basic_clean(concatenated_bodies)
    cleaned_string = remove_extra_spaces(cleaned_string)

    return cleaned_string


file_path = r'C:\Users\zaza2\PycharmProjects\ReasearchProject\visualize_data\mmiwg_urls.xlsx'
cleaned_text = clean_body_from_excel(file_path)
print(cleaned_text)

# Open the file in write mode ('w')
with open('data/output.txt', 'w', encoding='utf-8') as file:
    # Write a string to the file
    file.write(cleaned_text)
