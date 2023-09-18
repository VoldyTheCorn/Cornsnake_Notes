# -*- coding: utf-8 -*-

import pathlib
import os
import cssutils

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

from bs4 import BeautifulSoup

html = open("index.html", encoding='utf-8').read()  # 这是你的HTML文档
soup = BeautifulSoup(html, 'html.parser')

from bs4 import BeautifulSoup

# Read the HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse the HTML content
soup = BeautifulSoup(content, 'html.parser')

# Get the elements
split_container = soup.find(id='split-container')
TOC_scroll_div = soup.find(id='TOC-scroll-div')
content_scroll_div = soup.find(id='content-scroll-div')


def style_to_dict(style_string):
    """
    "font-size: inherit; line-height: inherit; color: inherit" to dict
    :param style_string:
    :return:
    """
    ret = {}
    for i in style_string.strip().split(";"):
        i = i.strip()
        if not i:
            continue
        key, value = i.split(":")
        ret[key.strip()] = value.strip()
    return ret


def dict_to_style(style_dict: dict):
    ret = ""
    for key, value in style_dict.items():
        ret += f"{key}: {value}; "
    return ret


def remove_style_attr(bs4_object, attr):
    if not bs4_object.has_attr("style"):
        style_string = ""
    else:
        style_string = bs4_object['style']
    style_dict = style_to_dict(style_string)
    style_dict.pop(attr)
    return dict_to_style(style_dict)


def replace_style_attr(bs4_object, attr, new_value):
    if not bs4_object.has_attr("style"):
        style_string = ""
    else:
        style_string = bs4_object['style']
    style_dict = style_to_dict(style_string)
    style_dict[attr] = new_value
    bs4_object['style'] = dict_to_style(style_dict)


# Modify the elements' style
if 'style' in split_container.attrs:
    split_container['style'] = remove_style_attr(split_container, 'display')

# Modify the TOC_scroll_div's style
if 'style' in TOC_scroll_div.attrs:
    for attr in ['width', 'min-width', 'max-width', 'border-right']:
        TOC_scroll_div['style'] = remove_style_attr(TOC_scroll_div, attr)

# Modify the content_scroll_div's style
if 'style' in content_scroll_div.attrs:
    for attr in ['width', 'padding-left', 'padding-right']:
        content_scroll_div['style'] = remove_style_attr(content_scroll_div, attr)

# Modify TOC-list element's style
element = soup.find(id="TOC-list")
if element:
    replace_style_attr(element, "font-size", 'inherit')
    replace_style_attr(element, "line-height", 'inherit')
    replace_style_attr(element, "color", 'inherit')



# Find the target h1 element
target_h1_ret = soup.find_all('h1', align='middle')
for target_h1 in target_h1_ret:
    if target_h1.text.strip()=='玉米蛇宠物饲养询证指南':
        # Move the target h1 element to the beginning of its grandparent
        target_h1.extract()
        split_container.insert(0, target_h1)
        break

# Create a new h1 element and insert it after the target h1 element
new_h1 = soup.new_tag('h1')
new_h1.string = '目录'
target_h1.insert_after(new_h1)

# Move all children of the first li's ul to the parent ul and remove the first li
ul = soup.find(id='TOC-list')
first_li = ul.find('li')
inner_ul = first_li.find('ul')
children_to_move = list(inner_ul.children)
for child in children_to_move:
    ul.append(child)
first_li.decompose()

# Modify .gist-file element's style
gist_file = soup.find(class_="gist-file")
if gist_file:
    replace_style_attr(gist_file, "max-width", "900px")
    replace_style_attr(gist_file, "margin", "0 auto")

# Change color of all anchor tags
for link in soup.find_all('a'):
    replace_style_attr(link, "color", "#1A0DAB")

script_tags = soup.find_all('script')
for tag in script_tags:
    # If tag has 'src' attribute and 'index_vertical.html' is in 'src'
    if tag.string and 'index_vertical.html' in tag.string:
        # Replace 'index_vertical.html' with 'index.html'
        tag.string = tag.string.replace('index_vertical.html', 'index.html')\
                               .replace("window.innerWidth < window.innerHeight","window.innerWidth > window.innerHeight*1.1")
    if tag.string and 'Split(' in tag.string: # remove the Split control from the split div of the landscape version of html
        tag.string = ""


# 输出修改后的HTML文档
with open('index_vertical.html', 'w', encoding='utf-8') as output_file:
    output_file.write(str(soup))
