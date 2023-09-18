# -*- coding: utf-8 -*-

import os
import pathlib

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

from bs4 import BeautifulSoup

# Read the HTML file and parse it into a BeautifulSoup object
with open("index.html", "r",encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

for img in soup.find_all('img'):
    img['loading'] = 'lazy'

# Save the changes to the HTML file
with open("index.html", "w",encoding='utf-8') as f:
    f.write(str(soup))
