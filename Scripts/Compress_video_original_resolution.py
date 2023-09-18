# -*- coding: utf-8 -*-

import os
import pathlib
import shutil
import subprocess

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

print("Compress videos from videos_original_resolution to videos...",end='\n\n')

def compress_videos(video_file, output_file):
    # 使用ffmpeg压缩视频
    command = f'Scripts\\ffmpeg.exe -i "{video_file}" -c:v libx264 -crf 28 -vf "scale=-2y:720" -maxrate 4M -bufsize 2M -c:a aac "{output_file}" -loglevel error'
    subprocess.run(command, shell=True, check=True)


originals = os.listdir("videos_original_resolution")
compressed = os.listdir("videos")

for original in originals:
    if original not in compressed:
        input_file = os.path.join("videos_original_resolution", original)
        output_file = os.path.join("videos", original)
        print("Re-encoding Video:", input_file, output_file)

        shutil.copy(input_file, 'temp.mp4')
        # 压缩视频
        compress_videos("temp.mp4", "temp_out.mp4")
        shutil.move("temp_out.mp4", output_file)
        os.remove('temp.mp4')