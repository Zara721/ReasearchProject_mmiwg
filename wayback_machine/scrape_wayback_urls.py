import os
import json
import re

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import re
from bs4 import BeautifulSoup


def extract_url_from_script(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all('script', {'type': 'text/javascript'})

    for script_tag in script_tags:
        # Check if the script tag contains the __wm.wombat function call
        if "__wm.wombat" in script_tag.text:
            # Regular expression to match the URL within the __wm.wombat function call
            match = re.search(r"__wm\.wombat\(\"(.*?)\"", script_tag.text)

            if match:
                return match.group(1)  # Return the matched URL
            else:
                return None
    return None


# Function to launch Playwright and scrape data
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract title
    title = soup.find('title').text if soup.find('title') else "No Title Found"

    # Extract body content
    body = soup.body.text if soup.body else "No Body Content Found"

    # Extract URL from script tag
    url = extract_url_from_script(html_content)
    print(url)

    return {"url": url, "title": title, "body": body}


dir_path = os.path.join("downloads_waybackMachine", "downloads_waybackMachine")

# Initialize an empty list to hold the scraped data
data_list = []

folder_path = "downloads_waybackMachine/downloads_waybackMachine"

for filename in os.listdir(folder_path):
    # Correctly construct the file path using direct string concatenation
    file_path = folder_path + "\\" + filename
    # print(filename)
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    html_content = file.read()
            except UnicodeDecodeError:
                print(f"Failed to decode file: {file_path}")
                continue
        # Scrape data and append to the list
        data = parse_html(html_content)
        data_list.append(data)

# Save the data to a JSON file
with open('output_files/wayback_article_content.json', 'w', encoding='utf-8') as outfile:
    json.dump(data_list, outfile, indent=4)

print("Data successfully saved to wayback_article_content.json")
