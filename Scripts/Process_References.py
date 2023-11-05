# -*- coding: utf-8 -*-

import sys
import pathlib
import os
import time

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

import re
import datetime
import urllib


print("[Processing references]...",end='\n\n')

# Open your markdown file
with open('README_original_ref_infos.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Get current date and time
now = datetime.datetime.now()
new_version = now.strftime("%Y%m%d-%H%M")

# Use regex to find the version number and replace it
content = re.sub(r'Version: \{.*\}', f'Version: {new_version}', content)

# Write the new version number to newest_version_number.txt
with open('newest_version_number.txt', 'w') as file:
    file.write(new_version)

content = content.replace("{green}",'<img src="images/Signal_Light_Green.png" height=15 />')
content = content.replace("{yellow}",'<img src="images/Signal_Light_Yellow.png" height=15 />')
content = content.replace("{red}",'<img src="images/Signal_Light_Red.png" height=15 />')
content = content.replace("{finished}",'<img src="images/Signal_Finished.png" height=15 />')

# {作者姓名，采访视频以被才放人为准，这个框可以用#做注释，不显示在最后文档中}{引文信息}{引文链接}{附件链接,可以没有}{翻译链接,可以没有}{证据级别1~5或I~V，可以没有}
pattern = r'{(.*?)}{(.*?)}{(.*?)}(?:{(.*?)}){0,1}(?:{(.*?)}){0,1}(?:{(.*?)}){0,1}'

missing_attach = False

# Function to convert each match
def convert(match):
    global missing_attach

    cores_author = match.group(1)
    # 可以用#做注释
    if "#" in cores_author:
        cores_author, _, _ = cores_author.rpartition('#')

    ref_info = match.group(2)
    ref_link = match.group(3)
    attach_link = match.group(4)
    translation_link = match.group(5)
    evidence_level = match.group(6)

    year = 0
    re_ret = re.findall(r"\D(\d{4})\D", ref_info)
    if not re_ret:
        re_ret = re.findall(r"\D*(\d{4})\D*", ref_info)
    if re_ret:
        re_ret = [int(x) for x in re_ret if 1900 <= int(x) <= time.localtime().tm_year]
        if len(re_ret)==1:
            year = re_ret[0]

    ret = "（"
    if ref_link:
        ret += f'<a href="{ref_link}">'
    if cores_author:
        ret += cores_author
    else:
        ret += f"【FILL_REF_AUTHOR: {ref_info}】"
    ret += ", "+str(year) if year else ""
    if ref_link:
        ret+='</a>'
    if attach_link:
        ret += f'&nbsp;<a href="{urllib.parse.quote(attach_link)}"><img src="images/Icon_Download.png" height=14 /></a>'
        if not os.path.isfile(urllib.parse.unquote(attach_link)):
            print("Missing attachment file:", match.group(0), "File:", attach_link)
            missing_attach = True
    if translation_link:
        ret += f'&nbsp;<a href="{translation_link}"><img src="images/Icon_Translation.png" height=14 /></a>'
    ret += f'&nbsp;<img src="images/Icon_Info.png" height=14 title="{ref_info}" />'
    ret += "）"
    evidence_levels = ["I", "II", "III", "IV", "V"]
    if evidence_level:
        if evidence_level.isdigit():
            evidence_level = evidence_levels[int(evidence_level) - 1]
        ret += f"<sup>{evidence_level}</sup>&nbsp;"
    return ret


# Apply the conversion to the content
new_content = re.sub(pattern, convert, content)

if missing_attach:
    input("Deal with the missing attachment files, and reboot the process.")

# Write the result back to the file
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)
