# -*- coding: utf-8 -*-
"""
Captures a predefined number of images in rapid succession

Output is folder of images
"""

from picamera2 import Picamera2
import cv2 as cv
import time
import os


anz = int(input("Anzahl "))
picam = Picamera2()

# Specify the folder path
folder_path = "pics"

# Check if the folder exists, and if not, create it
if not os.path.exists(folder_path):
    os.makedirs(folder_path)


# Picam Configuration
camera_config = picam.create_video_configuration(
    main={'format': 'RGB888', "size": (4056, 3040)},
    buffer_count=7,
)
picam.configure(camera_config)

picam.start()


# Loop for displaying image
while True:
    img = picam.capture_array()
    cv.namedWindow('Camera Output', cv.WINDOW_NORMAL)
    cv.setWindowProperty('Camera Output', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.imshow('Camera Output', img)
    key = cv.waitKey(1)
    if key != -1:
        break

time.sleep(1)
cv.destroyAllWindows()

# Capturing and saving images
for i in range(anz):
    img = picam.capture_array()
    print(f"Bild {i} aufgenommen.")

    image_path = os.path.join(folder_path, f'{i}.png')
    cv.imwrite(image_path, img)


cv.destroyAllWindows()
