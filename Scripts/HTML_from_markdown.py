# -*- coding: utf-8 -*-

import gh_md_to_html

lines = open("README.md", encoding='utf-8').readlines()

ret = ""
for start in range(0, len(lines), 2500):
    end = min(start + 2500, len(lines))
    print("Performing Github Style Markdown to HTML for line:", start, "-", end)
    section = lines[start:end]
    ret += gh_md_to_html.markdown_to_html_via_github_api("".join(section)) + '\n'

before = """<html>
 <head>
  <link rel="stylesheet" type="text/css" href="index.css">
  <meta charset="utf-8" content="text/html"/>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
 </head>
 <body>
  <div class="gist">
   <style class="formula-style">
    svg.gh-md-to-html-formula {
            fill: black;
        }
   </style>
   <div class="gist-file">
    <!-- This is the class that is responsible for the boxing! -->
    <div class="gist-data">
     <div class="js-gist-file-update-container js-task-list-container file-box">
      <div class="file" id="user-content-article-README">
       <div class="Box-body readme blob js-code-block-container p-5 p-xl-6" id="user-content-file-docker-image-pull-md-readme" style="margin-left: 40px; margin-right: 40px; margin-top: 20px; margin-bottom: 20px">
        <article class="markdown-body entry-content container-lg" itemprop="text">"""

after = "</article></div></div></div></div></div></div></body></html>"

with open("index.html", 'w', encoding="utf-8") as index_html:
    index_html.write(before + ret + after)

from bs4 import BeautifulSoup

# Read the HTML file
with open("index.html", "r",encoding='utf-8') as f:
    contents = f.read()

soup = BeautifulSoup(contents, 'html.parser')

for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
    text = tag.get_text(strip=True)
    anchor = tag.find('a')
    if anchor:
        anchor['href'] = '#' + text

# Write back to the file
with open("index.html", "w",encoding='utf-8') as f:
    f.write(str(soup))
