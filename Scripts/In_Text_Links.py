# -*- coding: utf-8 -*-

import sys
import pathlib
import os
import time

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

from bs4 import BeautifulSoup
import re
import urllib.parse

print("[Processing in-text Links]...",end='\n\n')

# Read the HTML file
with open("index.html", "r",encoding='utf-8') as f:
    contents = f.read()

soup = BeautifulSoup(contents, 'html.parser')



# Find all 'a' elements where href attribute starts with '#'
a_elements = soup.find_all('a', href=lambda value: value and value.startswith('#'))

for a in a_elements:
    # Remove '#' from href value and decode URI component
    target = urllib.parse.unquote(a['href'][1:])

    # Assign JavaScript function "scrollToElementInText(event,target)"
    # BeautifulSoup can't really handle JavaScript, you would need to use a different tool for that
    # Here, we are simply adding a 'onclick' attribute with the JavaScript function
    a['onclick'] = f"scrollToElementInText(event,'{target}')"


# Script to be inserted
script = """
<script>function scrollToElementInText(event, target_text)
{
    console.log(target_text)
    event.preventDefault();

    var scroll_div = document.getElementById("content-scroll-div");

    for (let i = 1; i <= 6; i++)
    {
        var headers = scroll_div.querySelectorAll('h' + i);
        headers.forEach(header =>
                        {
                            if (header.innerText === target_text)
                            {
                                if (scroll_div.scrollHeight > scroll_div.clientHeight)
                                {
                                    console.log(scroll_div)
                                    console.log(header.offsetTop - header.offsetHeight - 20)
                                    scroll_div.scrollTop = header.offsetTop - header.offsetHeight - 20;
                                }
                                else // for cellphone layout
                                {
                                    console.log(document.getElementsByClassName("gist-data")[0])
                                    console.log(header.offsetTop - header.offsetHeight - 20)
                                    document.getElementsByClassName("gist-data")[0].scrollTop = header.offsetTop - header.offsetHeight - 20;
                                }
                            }
                        });
    }
}
</script>
"""

# Append the script at the end of the body
soup.body.append(BeautifulSoup(script, 'html.parser'))

# Write back to the file
with open("index.html", "w",encoding='utf-8') as f:
    f.write(str(soup))
