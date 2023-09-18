# -*- coding: utf-8 -*-
import sys
import pathlib
import os
import time
import re
from bs4 import BeautifulSoup
import urllib.parse
from collections import OrderedDict

from bs4 import BeautifulSoup
import requests
import os

print("Confirming all images and links exist",end='\n\n')

BASE_URL = "https://f000.backblazeb2.com/file/voldy-public/"

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

lines = open("README.md", encoding='utf-8').readlines()
img_srcs = re.findall('<img src="([^"]*)"', "".join(lines))
for src in img_srcs:
    if not os.path.isfile(src):
        raise FileNotFoundError(f"File {src} not found")
    # print("Exist:", src)

# Read the HTML file
with open("index.html", "r", encoding='utf-8') as f:
    contents = f.read()

soup = BeautifulSoup(contents, 'html.parser')

for link in soup.find_all('a'):
    href = link.get('href')
    if not href:
        print(link)
    if href.endswith('.mp4'):
        # 删除base_url
        file_path = href.replace(BASE_URL, '')
        # 解码
        file_path = requests.utils.unquote(file_path)
        # 检查文件是否存在

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
        # print("Exist:", file_path)

# Find all 'a' elements where href attribute starts with '#'
a_elements = soup.find_all('a', href=lambda value: value and value.startswith('#'))

targets = OrderedDict()

for a in a_elements:
    # Remove '#' from href value and decode URI component
    target = urllib.parse.unquote(a['href'][1:])
    targets[a] = target

headers = []

for i in range(1, 7):
    header_objects = soup.find_all('h' + str(i))
    for header in header_objects:
        headers.append(header.get_text())

has_error = False
for key, value in targets.items():
    if value not in headers:
        print("Missing link target:", value)
        has_error = True

if has_error:
    print("Deal with the missing link tags above:")
else:
    print("All links exist")
