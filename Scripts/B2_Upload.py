# -*- coding: utf-8 -*-

import os
import pathlib
import hashlib

from b2sdk.v1 import InMemoryAccountInfo
from b2sdk.v1 import B2Api
from B2_cloud_secret import application_key, application_key_id, bucket_name

parent_path = str(pathlib.Path(__file__).parent.parent.resolve())
os.chdir(parent_path)

upload_excludes = ["Voldy 栖地结构.psd","垫材显微照片：虫.psd"]  # These file will not be upload to backblaze

upload_base_files = ['index.css',"newest_version_number.txt", 'index.html', 'index_vertical.html']

print("Upload files to backblaze B2 cloud...",end='\n\n')

def calculate_md5(file_path):
    with open(file_path, 'rb') as file:
        md5_hash = hashlib.md5()
        while True:
            data = file.read(8192)  # Read the file in chunks of 8192 bytes
            if not data:
                break
            md5_hash.update(data)
    return md5_hash.hexdigest()


# Your local directory
local_dirs = ['images', 'videos']

info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account('production', application_key_id, application_key)
bucket = b2_api.get_bucket_by_name(bucket_name)

print("Bucket:",bucket)

for local_dir in local_dirs:
    print("Listing B2 folder:",local_dir)
    # Get list of files in the bucket
    bucket_files = {}  # {filename: MD5}
    for f in bucket.ls(folder_to_list=local_dir):
        f = f[0]
        bucket_files[f.file_name] = f.content_md5

    # Get list of files in the local directory
    local_filepaths = {}
    for f in os.listdir(local_dir):
        real_path = os.path.join(local_dir, f).replace('\\', '/')
        if os.path.isfile(real_path):
            local_filepaths[real_path] = calculate_md5(real_path)

    # Compare files and upload if necessary
    for file_path, md5 in local_filepaths.items():
        excluded = False
        for exclude_file in upload_excludes:
            if pathlib.Path(file_path).name.lower() == exclude_file.lower():
                excluded = True
                break
        if excluded:
            print("Excluded:", file_path, '\n')
            continue
        # If the file does not exist in the bucket or has been modified after the last upload
        if file_path not in bucket_files or md5 not in bucket_files.values():
            # Upload the file
            print(f'Uploading file: {file_path}', end="... ", flush=True)
            bucket.upload_local_file(
                local_file=file_path,
                file_name=file_path,
            )

            download_url = b2_api.get_download_url_for_file_name(bucket_name, file_path)
            print(f'Direct link: {download_url}')
            print()
        else:
            # print(f"File exist: {file_path}")
            # print()
            pass
        # print()

    # Compare files and delete if necessary
    for f in bucket.ls(folder_to_list=local_dir):
        f = f[0]
        if not os.path.isfile(f.file_name):
            input("Confirm delete " + f.file_name + ": ")
            bucket.delete_file_version(f.id_, f.file_name)
            print('Deleted')

for f in bucket.ls():
    f = f[0]
    if not os.path.isfile(f.file_name):
        input("Confirm delete " + f.file_name + ": ")
        bucket.delete_file_version(f.id_, f.file_name)
        print('Deleted')

print("------------\n")

download_url = None

for base_file in upload_base_files:
    if os.path.isfile(base_file):
        print('Uploading file: ' + base_file + "... ")
        bucket.upload_local_file(
            local_file=base_file,
            file_name=base_file,
        )
        download_url = b2_api.get_download_url_for_file_name(bucket_name, base_file)

print(f'Index.html direct link: {download_url}')
