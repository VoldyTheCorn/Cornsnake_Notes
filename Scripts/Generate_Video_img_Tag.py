# -*- coding: utf-8 -*-


import pathlib
import os

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

def addToClipBoard(text):
    import pyperclip
    pyperclip.copy(text)


import pathlib
def filename_name(file_path):
    path = pathlib.Path(file_path)
    return path.name

def replace_last_append(file_path, new_append: str):
    """
    Parameters:
        new_append: Can be with or without the . in the front
    """
    path = pathlib.Path(file_path)
    new_append = "." + new_append if not new_append.startswith(".") else new_append
    return str(path.with_suffix(new_append))

while True:
    filename = input("Full path (Ctrl+Shift+C) of the mp4/png file: ")
    filename = filename.strip('"')
    if not filename:
        continue

    if filename.lower().endswith('mp4'):
        name = filename_name(filename)
        jpg_name =replace_last_append(name,'jpg')
        ret = f'<p align="center"><a href="https://f000.backblazeb2.com/file/voldy-public/videos/{name}">' \
              f'<img src="videos/{jpg_name}" width=603 /></a></p>'
    else:
        if not os.path.isfile(filename):
            filename = os.path.join("images",filename)
        if os.path.getsize(filename) > 1 * 1024 * 1024:
            ret = f'<p align="center"><img src="images/{replace_last_append(filename_name(filename),"jpg")}" width=603/></p>'
        else:
            ret = f'<p align="center"><img src="images/{filename_name(filename)}" width=603/></p>'

    print(ret)
    addToClipBoard(ret)