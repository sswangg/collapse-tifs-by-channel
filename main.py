import cv2
from blend_modes import lighten_only
import numpy as np

foreground_images = []

# Import background image
background_img_float = cv2.imread('fs image1c2z01.tif', -1).astype(float)
background_img_float = np.dstack((background_img_float, np.full(background_img_float.shape[:2], float(255))))

# Import foreground image
for i in range(20):
    num = str(i+2)
    if len(num) != 2:
        num = "0"+num
    foreground_img_float = cv2.imread(f'fs image1c2z{num}.tif', -1).astype(float)
    foreground_img_float = np.dstack((foreground_img_float, np.full(foreground_img_float.shape[:2], float(255))))
    foreground_images.append(foreground_img_float)

# Blend images
blended_img_float = background_img_float
for i in range(20):
    blended_img_float = lighten_only(blended_img_float, foreground_images[i], 1)

# Display blended image
dist1 = cv2.convertScaleAbs(blended_img_float)
cv2.imshow('window', dist1)
cv2.waitKey()  # Press a key to close window with the image.
