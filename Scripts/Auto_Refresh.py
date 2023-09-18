# -*- coding: utf-8 -*-

print("Setting auto refreshes.")

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

tags = soup.find_all(string=re.compile(r"Version: \d{8}-\d{4}"))

# Assign the id "version" to that object
for tag in tags:
    tag.parent['id'] = 'version'

check_update_interval = 7200 # in seconds

# Script to be inserted
script = """
<script>
  setInterval(function(){
    fetch('newest_version_number.txt')
      .then(response => response.text())
      .then(data => {
        var currentVersion = document.getElementById('version').textContent.match(/Version: (\d{8}-\d{4})/)[1];
        if (currentVersion != data.trim()) {
          console.log("New version found: " + currentVersion+" vs. "+ data.trim())
          location.reload();
        } else {
          console.log("Version check passed: " + currentVersion);
        }
      });
  }, """+str(check_update_interval*1000)+"""); // Check every hour
</script>
"""

# Append the script at the end of the body
soup.body.append(BeautifulSoup(script, 'html.parser'))

# Write back to the file
with open("index.html", "w",encoding='utf-8') as f:
    f.write(str(soup))
