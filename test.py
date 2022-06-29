import os
import re


def listdir_no_DS_Store(dir_path):
    return [d for d in os.listdir(dir_path) if d != '.DS_Store']


image_folders = listdir_no_DS_Store('folder_of_folders')
images = [listdir_no_DS_Store(f'folder_of_folders/{folder}') for folder in image_folders]

for i in images:
    for image_name in i:
        print(image_name.split("c")[0])
