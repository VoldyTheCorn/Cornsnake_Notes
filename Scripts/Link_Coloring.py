# -*- coding: utf-8 -*-

import sys
import pathlib
import os
import time

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)
from bs4 import BeautifulSoup
import re

# Read the HTML file
with open("index.html", "r",encoding='utf-8') as f:
    contents = f.read()

soup = BeautifulSoup(contents, 'html.parser')

# Script to be inserted
script = """<script>

// Select all anchor tags on the page
var links = document.querySelectorAll('a');

// Iterate over each link
for (var i = 0; i < links.length; i++)
{
    var link = links[i];

    // Check if the link is not a child of the element with id 'TOC-list'
    if (!document.getElementById('TOC-list').contains(link))
    {
        // Change the color of the link
        link.style.color = '#1A0DAB';
    }
}
        
</script>
"""

# Append the script at the end of the body
soup.body.append(BeautifulSoup(script, 'html.parser'))

# Write back to the file
with open("index.html", "w",encoding='utf-8') as f:
    f.write(str(soup))
