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
    background_img_float = np.dstack((background_img_float, np.full(background_img_float.shape[:2], float(255))))

    # Import foreground image
    for i in range(1, 21):
        try:
            foreground_img_float = cv2.imread(f'folder_of_folders/{folder}/{image_names[i]}', -1).astype(float)
        except:
            print(f'folder_of_folders/{folder}/{i}')
        foreground_img_float = np.dstack((foreground_img_float, np.full(foreground_img_float.shape[:2], float(255))))
        foreground_images.append(foreground_img_float)

    # Blend images
    blended_img_float = background_img_float
    for i in range(20):
        blended_img_float = lighten_only(blended_img_float, foreground_images[i], 1)

    # Display blended image
    return cv2.convertScaleAbs(blended_img_float)


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
    os.mkdir(output_dir)
    images = images_by_folder[folder]
    split_images = split_images_by_channel(images)
    for c in range(1, 5):
        processed_image = process_images(folder, split_images[c])
        cv2.imwrite(f'{output_dir}/c{c}.tif', processed_image)
    shutil.rmtree(f'folder_of_folders/{folder}', ignore_errors=True)
