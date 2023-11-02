# -*- coding: utf-8 -*-

import os
import pathlib
import urllib
from PIL import Image

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

from bs4 import BeautifulSoup

print("[Setting lazy loading and image heights]...",end='\n\n')

# Read the HTML file and parse it into a BeautifulSoup object
with open("index.html", "r",encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

for img in soup.find_all('img'):
    img['loading'] = 'lazy'
    if "Signal_" in img['src'] or "Icon_" in img['src']:
        continue
    html_img_width = int(img['width'])
    PIL_img = Image.open(urllib.parse.unquote(img['src']))
    width, height = PIL_img.size  # returns (width, height)
    html_img_height = round(height/width*html_img_width)
    img['height'] = str(html_img_height)

# Save the changes to the HTML file
with open("index.html", "w",encoding='utf-8') as f:
    f.write(str(soup))
