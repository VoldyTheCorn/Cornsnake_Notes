# -*- coding: utf-8 -*-

import os
import pathlib

# Backblaze link 的前缀是 https://f000.backblazeb2.com/file/voldy-public/
# TODO: index.html修正非标题的链接
# TODO: index.html增加标题和图标

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)
print('Current directory:', parent_path)

input("Will process and upload the generated index.html to public internet.\n\n\nVerify you don't have unsaved changes. Press Enter to confirm: ")

print()

import Process_References

import Markdown_Table_of_content

import HTML_from_markdown

import Navigation

import Link_Coloring

import Compress_video_original_resolution

import Generate_Video_Thumbnails

import Set_HTML_Icon_and_Title

import Reference_info_click_function

import Auto_Refresh

import In_Text_Links

import Verify_Images_Videos_And_Links # needs to be performed before Add_Video_Player

import Add_Video_Player

import Compress_Images

import Set_Lazy_Loading_and_Image_Height

import Generate_Vertical_Webpage

import Add_Back_to_Top_Button_to_Vertical

import B2_Upload