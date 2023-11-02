# -*- coding: utf-8 -*-
print("Adding video players")

import subprocess
import os
import pathlib
import traceback
from PIL import Image

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

print("[Adding Video Players]...",end='\n\n')

MAXIMUM_WINDOW_HEIGHT = 500

from bs4 import BeautifulSoup

# Read the HTML file and parse it into a BeautifulSoup object
with open("index.html", "r",encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Add the script tag to the HTML file
script_tag = soup.new_tag("script", src="https://vjs.zencdn.net/7.8.4/video.js")
soup.body.append(script_tag)


# Add new info to head
new_info = """
<link href="https://vjs.zencdn.net/7.8.4/video-js.css" rel="stylesheet" />
<script src="https://vjs.zencdn.net/ie8/1.1.2/videojs-ie8.min.js"></script>
<style>
.video-js-container {
  display: flex;
  justify-content: center;
}

.vjs-big-play-button {
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%);
}

.video-js .vjs-control-bar {
  display: flex !important;
  opacity: 1 !important;
  visibility: visible !important;
}
</style>
"""
soup.head.append(BeautifulSoup(new_info, 'html.parser'))


# Find all the <p> tags and replace them
for p_tag in soup.find_all('p', {'align': 'center'}):
    a_tag = p_tag.find('a')
    img_tag = p_tag.find('img')

    # Continue if the href attribute in <a> tag doesn't end with .mp4 or the src attribute in <img> tag doesn't end with .jpg
    if not (a_tag and a_tag['href'].endswith('.mp4') and img_tag and img_tag['src'].endswith('.jpg')):
        continue

    p = p_tag
    video_link = p.a['href']
    img_filename = p.img['src']
    width = p.img['width']

    # Get the image filename without the play button
    img_filename = p_tag.img['src']
    filename_parts = img_filename.rsplit('.', 1)
    img_filename_no_playbutton = filename_parts[0] + '_no_playbutton.' + filename_parts[1]

    import urllib.parse
    img = Image.open(urllib.parse.unquote(img_filename))
    img_width, img_height =img.size
    # print(img_width,img_height)

    if int(width)/img_width*img_height>MAXIMUM_WINDOW_HEIGHT:
        width = round(MAXIMUM_WINDOW_HEIGHT/img_height*img_width)

    # Create the new tag
    new_div_tag = soup.new_tag("div", **{"class": "video-js-container"})
    new_tag_content = f"""
    <video class="video-js" controls preload="auto" width="{width}" poster="{img_filename_no_playbutton}" data-setup="{{}}">
        <source src="{video_link}" type='video/mp4'>
        <p class='vjs-no-js'>
        To view this video please enable JavaScript, and consider upgrading to a web browser that
        <a href="https://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a>
        </p>
    </video>
    <br>
    <p align="middle"><a href="{video_link}" style="color: rgb(26, 13, 171);"><img height="14" loading="lazy" src="images/Icon_Download.png" style="max-width: 100%;"></a></p>
    """

    new_tag_content = BeautifulSoup(new_tag_content, 'html.parser')
    new_div_tag.append(new_tag_content)


    p.replace_with(new_div_tag)

    new_div_tag.insert_before(BeautifulSoup("<br>", 'html.parser'))
    new_div_tag.insert_after(BeautifulSoup("<br>", 'html.parser'))

# Save the changes to the HTML file
with open("index.html", "w",encoding='utf-8') as f:
    f.write(str(soup))