# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 19:41:05 2023

@author: Tobias Kurz
"""

from picamera2 import Picamera2
import cv2 as cv
import time
import os


"""
anz = int(input("Anzahl der Bilder: "))

delay = int(input("Abstand zw. Aufnahmen (s): "))
dateiname = input("dateiname: ")
"""

prefix = input("File name prefix? (can also be none) ")
picam = Picamera2()

# Specify the folder path
folder_path = "pics"

# Check if the folder exists, and if not, create it
if not os.path.exists(folder_path):
    os.makedirs(folder_path)



camera_config = picam.create_video_configuration(
    main={'format': 'RGB888', "size":(4056, 3040)},
    buffer_count = 7,
    )
picam.configure(camera_config)

picam.start()
i = 0

while True:
    
    if input("Enter wenn bereit"): break
    

    time.sleep(1)
    img = picam.capture_array()
    
    
    #cv.namedWindow('Camera Output', cv.WINDOW_NORMAL)
    #cv.setWindowProperty('Camera Output',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
    #cv.imshow('Camera Output',img)
    
    image_path = os.path.join(folder_path, f'{prefix}{i}.png')
    cv.imwrite(image_path, img)
   
    i+=1
    
    #key = cv.waitKey(1)
    #if key != -1:
    #    break  

    

cv.destroyAllWindows()