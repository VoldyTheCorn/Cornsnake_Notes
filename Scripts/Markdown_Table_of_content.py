# -*- coding: utf-8 -*-
import re


def generate_toc(read_filename, write_filename):
    with open(read_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    toc = []
    for line in lines:
        if re.match('^#+ ', line):
            count = line.count('#')
            title = line.replace('#', '').strip()
            if title in ["玉米蛇宠物饲养询证指南", '目录']:
                continue
            link = title.replace(' ', '-')
            if title.strip():
                toc.append(' ' * (count - 1) * 2 + '- [' + title + '](#' + link + ')')

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