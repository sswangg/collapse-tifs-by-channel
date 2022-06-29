import cv2
from blend_modes import lighten_only
import numpy as np
import os
import shutil


def listdir_no_DS_Store(dir_path):
    return [d for d in os.listdir(dir_path) if d != '.DS_Store']


def process_images(folder, image_names):
    foreground_images = []
    image_names = sorted(image_names)
    # Import background image
    background_img_float = cv2.imread(f'folder_of_folders/{folder}/{image_names[0]}', -1).astype(float)
    if background_img_float.shape[2] != 4:
        background_img_float = np.dstack((background_img_float, np.full(background_img_float.shape[:2], float(255))))

    # Import foreground image
    for i in range(1, 21):
        foreground_img_float = cv2.imread(f'folder_of_folders/{folder}/{image_names[i]}', -1).astype(float)
        if foreground_img_float.shape[2] != 4:
            foreground_img_float = np.dstack((foreground_img_float, np.full(foreground_img_float.shape[:2], float(255))))
        foreground_images.append(foreground_img_float)

    # Blend images
    combined_img_float = background_img_float
    for i in range(20):
        try:
            combined_img_float = lighten_only(combined_img_float, foreground_images[i], 1)
        except TypeError:
            print(foreground_images[i])
    return cv2.convertScaleAbs(combined_img_float)


def split_images_by_name(image_names):
    split_images = {}
    for image_name in image_names:
        identifier = image_name.split("c")[0]
        if identifier not in split_images.keys():
            split_images[identifier] = [image_name]
        else:
            split_images[identifier].append(image_name)
    return split_images


def split_images_by_channel(image_names):
    split_images = {1: [],
                    2: [],
                    3: [],
                    4: []}
    for name in image_names:
        split_images[int(name[-8])].append(name)
    return split_images


image_folders = listdir_no_DS_Store('folder_of_folders')
image_list = [listdir_no_DS_Store(f'folder_of_folders/{folder}') for folder in image_folders]
images_by_folder = dict(zip(image_folders, image_list))

for folder in images_by_folder:
    output_dir = f'processed_images/{folder}'
    images = images_by_folder[folder]
    images_by_name = split_images_by_name(images)
    for key in images_by_name:
        images_by_channel = split_images_by_channel(images_by_name[key])
        images_by_name[key] = images_by_channel
    os.mkdir(output_dir)
    for key in images_by_name:
        os.mkdir(f'{output_dir}/{key}')
        for c in range(1, 5):
            processed_image = process_images(folder, images_by_name[key][c])
            cv2.imwrite(f'{output_dir}/{key}/c{c}.tif', processed_image)
    shutil.rmtree(f'folder_of_folders/{folder}', ignore_errors=True)
