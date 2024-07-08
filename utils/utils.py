import pandas as pd
import re


def parse_line_as_dict(line):
    """Parses a line of text representing a JSON-like object and returns a dictionary."""
    data = {}
    patterns = {
        "url": r'"url": "(.+?)"',
        "title": r'"title": "(.+?)"',
        "body": r'"body": "(.+?)"'
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, line)
        if match:
            data[key] = match.group(1)
    return data


def read_text_file(filepath):
    """Reads a text file and parses each line as a JSON-like object."""
    data = []
    with open(filepath, 'r') as file:
        for line in file:
            data.append(parse_line_as_dict(line))
    return data


def create_dataframe_from_json(data_list):
    """Creates a DataFrame from a list of dictionaries."""
    df = pd.DataFrame(data_list)
    df.columns = ['url', 'title', 'body']
    return df


def write_to_excel(df, filename):
    """Writes a DataFrame to an Excel file."""
    df.to_excel(filename, index=False)


def write_urls_to_txt(data_list, filename):
    """Writes a list of URLs to a text file."""
    with open(filename, 'w') as outfile:
        for url in data_list:
            outfile.write(str(url) + '\n')


def remove_repeat_urls(all_urls, repeat_urls):
    # Iterate over all_urls and remove items that are in repeat_set
    for url in list(all_urls):  # Convert to list to avoid modifying during iteration
        if url in repeat_urls:
            all_urls.remove(url)

    return all_urls
