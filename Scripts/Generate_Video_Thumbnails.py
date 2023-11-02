# -*- coding: utf-8 -*-

# import sys
# import pathlib
# parent_path = str(pathlib.Path(__file__).parent.resolve())
# sys.path.insert(0,parent_path)

import subprocess
import os
import pathlib
import traceback

from PIL import Image

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

print("[Generate video thumbnails]...",end='\n\n')

# Specify the folder path
folder_path = 'videos'

# Get all the files from the folder
files = os.listdir(folder_path)

# Filter out the MP4 files
mp4_files = [file for file in files if file.endswith('.mp4')]

# Loop through each MP4 file
for mp4_file in mp4_files:
    output_jpg = os.path.join(folder_path, mp4_file[:-4] + '.jpg')
    output_jpg_no_playbutton = os.path.join(folder_path, mp4_file[:-4] + '_no_playbutton.jpg')
    if os.path.isfile(output_jpg) and os.path.isfile(output_jpg_no_playbutton):
        continue

    print(mp4_file)

    duration = subprocess.check_output('Scripts/ffprobe.exe -loglevel error -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "'+ os.path.join("videos",mp4_file)+'"')
    display_ratio = subprocess.check_output('Scripts/ffprobe.exe -loglevel error -v error -select_streams v:0 -show_entries stream=display_aspect_ratio -of default=noprint_wrappers=1:nokey=1 "'+ os.path.join("videos",mp4_file)+'"')
    duration = float(duration.decode('utf-8').strip())
    display_ratio = display_ratio.decode('utf-8').strip().split(':')
    try:
        display_ratio = int(display_ratio[0])/int(display_ratio[1])
    except ValueError as e:
        print(e)
        traceback.print_exc()
        display_ratio = input("Display ratio error, manual input (width/height, accept python expression): ")
        display_ratio = eval(display_ratio)

    middle_frame_temp = os.path.join("Scripts",'Thumbnail.temp.png')
    if os.path.isfile(middle_frame_temp):
        os.remove(middle_frame_temp)
    subprocess.call(["Scripts/ffmpeg.exe", "-loglevel", "error", "-ss", str(duration/2), "-i", os.path.join("videos",mp4_file), "-vframes", "1",middle_frame_temp])

    original_image = Image.open(middle_frame_temp)
    width, height = original_image.size

    # calculate the target size maintaining the aspect ratio
    if width/height > display_ratio:
        target_height = int(width/display_ratio)
        target_size = (width, target_height)
    else:
        target_width = int(display_ratio * height)
        target_size = (target_width, height)

    # resize the image
    resized_image = original_image.resize(target_size, Image.LANCZOS)

    pil_image = resized_image

    pil_image.save(output_jpg_no_playbutton)

    ########## Add a play symbol to it ########

    # Open both images
    play_button = Image.open('images/Play_Symbol.png')
    # Resize imageA to be 1/5 the size of the shorter edge of imageB
    shorter_edge = min(pil_image.size)
    new_size = int(shorter_edge / 4)
    play_button = play_button.resize((new_size, new_size))

    # Calculate the position where imageA should be pasted onto imageB
    paste_position = ((pil_image.size[0] - play_button.size[0]) // 2,
                      (pil_image.size[1] - play_button.size[1]) // 2)

    # Paste imageA onto imageB and save the result
    pil_image.paste(play_button, paste_position, play_button)

    # Save the image using the PIL library
    pil_image.save(output_jpg)

    if os.path.isfile(middle_frame_temp):
        os.remove(middle_frame_temp)