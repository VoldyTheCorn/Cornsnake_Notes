
### TODO

import subprocess
import os
import pathlib
import traceback

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

from bs4 import BeautifulSoup

# Read the HTML file and parse it into a BeautifulSoup object
with open("index.html", "r",encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Find the list by its id
toc_list = soup.find('ul', {'id': 'TOC-list'})

# Function to recursively add symbols
def add_symbols(ul_element, level=1):
    for li in ul_element.find_all('li', recursive=False):
        # Add symbol if the level > 3
        if level > 3:
            li.string = '📁 ' + li.get_text()

        # Look for nested ul elements
        for nested_ul in li.find_all('ul', recursive=False):
            add_symbols(nested_ul, level + 1)

# Start the recursion
add_symbols(toc_list)

# Save the changes to the HTML file
with open("index2.html", "w",encoding='utf-8') as f:
    f.write(str(soup))