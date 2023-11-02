# -*- coding: utf-8 -*-

import os
import shutil
from PIL import Image
import pathlib

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

print("[Compressing Images]...",end='\n\n')

# Path to the images directory
images_dir = "images"

# Path to the backup directory
backup_dir = "images_original_resolution"

# Create the backup directory if it does not exist
os.makedirs(backup_dir, exist_ok=True)

files = os.listdir(images_dir)
i = 0
# Loop through all files in the images directory
while i < len(files):
    filename = files[i]
    i += 1
    # Full path to the current file
    filepath = os.path.join(images_dir, filename)

    # Only process images (PNG and JPG files)
    if filename.lower().endswith(('.png', '.jpg')) and os.path.getsize(filepath) > 1 * 1024 * 1024:

        print(filename)

        # Backup the original file
        if not os.path.isfile(os.path.join(backup_dir, filename)):
            shutil.copy2(filepath, backup_dir)

        # Open the image file
        img = Image.open(filepath)

        # If the file is a PNG, convert it to JPG
        if filename.lower().endswith('.png'):
            # Remove the file extension from the filename
            filename_without_ext = os.path.splitext(filename)[0]

            # Save the image in JPG format with the same filename
            img.convert('RGB').save(os.path.join(images_dir, filename_without_ext + '.jpg'))

            # Remove the original PNG file
            os.remove(filepath)

            files.append(filename_without_ext + '.jpg')

        # If the file is a JPG, resize it
        elif filename.lower().endswith('.jpg'):
            # Calculate the ratio of the target size to the current size
            ratio = (os.path.getsize(filepath) / (1 * 1024 * 1024) * 1.05) ** 0.5

            # Calculate the new dimensions
            new_width = int(img.width / ratio)
            new_height = int(img.height / ratio)

            print(img.width, img.height, new_width, new_height)

            # Resize the image
            img = img.resize((new_width, new_height))

            # Save the resized image
            img.save(filepath)

            files.append(filename)