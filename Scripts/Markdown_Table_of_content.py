# -*- coding: utf-8 -*-
import re
import pathlib
import os

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

print("[Generating TOC of markdown file]...", end='\n\n')


def generate_toc(read_filename, write_filename):
    with open(read_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    toc = []
    titles = []
    for line in lines:
        if re.match('^#+ ', line):
            count = line.count('#')
            if count > 3:
                continue
            title = line.replace('#', '').strip()
            if title in ["玉米蛇宠物饲养询证指南", '目录']:
                continue
            link = title.replace(' ', '-')
            if title.strip():
                if count<2:
                    toc.append(' ' * (count - 1) * 2 + '- [**' + title + '**](#' + link + ')')
                else:
                    toc.append(' ' * (count - 1) * 2 + '- [' + title + '](#' + link + ')')
            titles.append(title)

    titles = ["".join([x for x in title if ('a' <= x <= 'z') or ('A' <= x <= 'Z') or ('0' <= x <= '9') or ('\u4e00' <= x <= '\u9fff')])
              for title in titles]

    has_dup = False
    for i, title1 in enumerate(titles):
        for title2 in titles[i + 1:]:
            if title1 == title2:
                print("Duplicated title", title1 + ".")
                has_dup = True

    if has_dup:
        input("Deal with the duplicated title and reboot the program.")

    start_marker = '[//]: # (Start of Automatic Table of Content)\n'
    end_marker = '[//]: # (End of Automatic Table of Content)\n'

    if start_marker in lines and end_marker in lines:
        start_index = lines.index(start_marker)
        end_index = lines.index(end_marker)
        lines = lines[:start_index + 1] + toc + ["", ""] + lines[end_index:]

    with open(write_filename, 'w', encoding='utf-8') as file:
        file.writelines([line.strip('\n') + '\n' for line in lines])


generate_toc('README_original_ref_infos.md', 'README_original_ref_infos.md')
generate_toc('README.md', 'README.md')
