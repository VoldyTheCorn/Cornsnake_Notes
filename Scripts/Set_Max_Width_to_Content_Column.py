# -*- coding: utf-8 -*-
import pathlib
import os
import copy
parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

from bs4 import BeautifulSoup

print("[Set Max Width to Content Column]...",end='\n\n')

html = open("index.html", encoding='utf-8').read()  # 这是你的HTML文档
soup = BeautifulSoup(html, 'html.parser')

# Locate the div with id 'content-scroll-div'
content_scroll_div = soup.find('div', {'id': 'content-scroll-div'})

# Create a new div with the desired style
new_div_style = (
    'max-width: 800px; '
    'margin-left: auto; '
    'margin-right: auto; '
    'border-left: 1px solid #D0D7DE; '
    'border-right: 1px solid #D0D7DE; '
    'padding-left: 30px; '
    'padding-right: 30px;'
)
new_div = soup.new_tag('div', style=new_div_style)

# Move all children of content-scroll-div into new_div
for child in copy.copy(list(content_scroll_div.contents)):
    new_div.append(child)

# Clear the existing content and insert the new div
content_scroll_div.clear()
content_scroll_div.append(new_div)

# Save the changes to the HTML file
with open("index.html", "w",encoding='utf-8') as f:
    f.write(str(soup))
