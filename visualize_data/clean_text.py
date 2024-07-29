import pandas as pd
import re
import unicodedata
import sqlite3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# download the NLTK stopwords
import nltk
nltk.download('stopwords')

# Connect to the SQLite database
sqliteConnection = sqlite3.connect(r'C:\Users\zaza2\canada_us_events.db')

# Execute a SQL query and load the results into a DataFrame
query = """
SELECT Title, Body
FROM mmiwg_related_articles 
WHERE Title IS NOT NULL
"""

df = pd.read_sql_query(query, sqliteConnection)

# Execute a SQL query and load the results into a DataFrame
query = """
SELECT full_events.AllNames
FROM mmiwg_related_articles
INNER JOIN full_events ON mmiwg_related_articles.Urls = full_events.DocumentIdentifier;
"""

all_names_df = pd.read_sql_query(query, sqliteConnection)


def basic_clean(string):
    '''
    This function takes in a string and
    returns the string normalized.
    '''
    string = unicodedata.normalize('NFC', string)
    string = string.lower()
    string = re.sub(r"[^\w\s]", "", string)

    # Tokenize the string into words
    tokens = word_tokenize(string)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # Join the filtered tokens back into a string
    return ' '.join(filtered_tokens)


def remove_extra_spaces(text):
    '''
    Removes extra spaces from the text.
    '''
    words = text.split()
    return ' '.join(words)


def replace_semicolons_with_spaces(input_string):
    return input_string.replace(";", " ")


def remove_numbers(input_string):
    return ''.join(char for char in input_string if not char.isdigit())


# Adjusted basic_clean function
def adjusted_basic_clean(string):
    '''
    Adjusted basic_clean function to ensure no unintended spaces are introduced.
    '''
    string = remove_numbers(string)
    string = unicodedata.normalize('NFC', string)
    string = string.lower()
    string = re.sub(r"[^\w\s]", "", string)
    return string


# Concatenate all titles and bodies into single strings
all_titles = ' '.join(df['Title'])

df['Body'].fillna('', inplace=True)
all_bodies = ' '.join(df['Body'])

all_names = ' '.join(all_names_df['AllNames'])

# Clean the concatenated strings
cleaned_titles = basic_clean(all_titles)
cleaned_bodies = basic_clean(all_bodies)
cleaned_all_names = basic_clean(remove_numbers(replace_semicolons_with_spaces(all_names)))

# Save the cleaned strings to .txt files
with open('data/aggregated_titles.txt', 'w', encoding='utf-8') as file:
    file.write(cleaned_titles)

with open('data/aggregated_bodies.txt', 'w', encoding='utf-8') as file:
    file.write(cleaned_bodies)

with open('data/all_names.txt', 'w', encoding='utf-8') as file:
    file.write(cleaned_all_names)

print("Done writing to files")


