# -*- coding: utf-8 -*-

import sys
import pathlib
import os
import time

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

print("Adding reference info function")

from bs4 import BeautifulSoup
import re

# Read the HTML file
with open("index.html", "r",encoding='utf-8') as f:
    contents = f.read()

soup = BeautifulSoup(contents, 'html.parser')

imgs = soup.find_all('img', {'src': "images/Icon_Info.png"})

for img in imgs:
    if img.parent.name == 'a':
        img.parent.replace_with(img)

# Script to be inserted
script = """
<script>
window.addEventListener('load', function() {
    var imgs = document.querySelectorAll('img[src="images/Icon_Info.png"]');
    for (var i = 0; i < imgs.length; i++)
    {
        imgs[i].addEventListener('click', function (e)
        {
            e.preventDefault();
            e.stopPropagation();

            var title = this.title;
            navigator.clipboard.writeText(title).then(function ()
                                                      {
                                                          console.log('Copying to clipboard was successful!');
                                                      }, function (err)
                                                      {
                                                          console.error('Could not copy text: ', err);
                                                      });

            var img = this;
            var parent = this.parentNode;
            var grandparent = parent.parentNode;
            var span = document.createElement('span');
            span.textContent = '已复制引文信息到剪切板。';
            span.style.display = 'inline-block';  // add this line

            parent.replaceChild(span, img);
            setTimeout(function ()
                       {
                           parent.replaceChild(img, span);
                       }, 3000);
        });
    }
});
</script>
"""

# Append the script at the end of the body
soup.body.append(BeautifulSoup(script, 'html.parser'))

# Write back to the file
with open("index.html", "w",encoding='utf-8') as f:
    f.write(str(soup))
