
import os
import pathlib

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

from bs4 import BeautifulSoup

# Read the HTML file
with open("index.html", 'r', encoding='utf-8') as f:
    contents = f.read()

soup = BeautifulSoup(contents, 'lxml')

# Find the favicon link tag
favicon_link = soup.find("link", rel="icon")
if favicon_link is None:
    favicon_link = soup.find("link", rel="shortcut icon")

# If the favicon link tag doesn't exist, create a new one
if favicon_link is None:
    favicon_link = soup.new_tag("link", rel="icon", href="images/Icon.png")
    # Add it to the head tag
    soup.head.append(favicon_link)
else:
    # Otherwise, just change the href to the path of your .png
    favicon_link['href'] = "images/Icon.png"

# Find the title tag
title_tag = soup.title

# Set the new title
if title_tag is not None:
    title_tag.string.replace_with("玉米蛇宠物饲养询证指南")
else:
    new_title = soup.new_tag("title")
    new_title.string = "玉米蛇宠物饲养询证指南"
    # Append it to the head
    soup.head.append(new_title)

# Write the modified HTML back to the file
with open("index.html", 'w', encoding='utf-8') as f:
    f.write(str(soup))
