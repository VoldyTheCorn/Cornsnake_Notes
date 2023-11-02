# -*- coding: utf-8 -*-

import os
import pathlib
import shutil
import subprocess
import re

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

print("[Compressing videos]...",end='\n\n')


def get_video_resolution(video_file):
    command = f'Scripts\\ffmpeg.exe -i "{video_file}"'
    result = subprocess.run(command, shell=True, check=False, capture_output=True)
    decoded_stderr = result.stderr.decode('utf-8', 'ignore')
    lines = decoded_stderr.split('\n')
    for line in lines:
        m = re.search(r'Stream .* Video.* ([0-9]+x[0-9]+)', line)
        if m:
            return tuple(map(int, m.group(1).split('x')))

def compress_videos(video_file, output_file):
    width, height = get_video_resolution(video_file)

    if height < 720:
        scale = f'scale={width}:{height}'
    else:
        scale = f'scale={int(width/height*720/2)*2}:720'

    command = f'Scripts\\ffmpeg.exe -i "{video_file}" -c:v libx264 -crf 28 -vf "{scale}" -maxrate 4M -bufsize 2M -c:a aac "{output_file}" -loglevel error'

    subprocess.run(command, shell=True, check=True)

originals = os.listdir("videos_original_resolution")
compressed = os.listdir("videos")

for original in originals:
    input_file = os.path.join("videos_original_resolution", original)
    # print(get_video_resolution(input_file), original)
    if original not in compressed:
        output_file = os.path.join("videos", original)
        print("Re-encoding Video:", input_file, output_file)

        shutil.copy(input_file, 'temp.mp4')
        # 压缩视频
        compress_videos("temp.mp4", "temp_out.mp4")
        shutil.move("temp_out.mp4", output_file)
        os.remove('temp.mp4')