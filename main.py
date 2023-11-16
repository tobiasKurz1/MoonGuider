# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 22:44:20 2023

@author: Tobias Kurz

This Python script serves as the main file that integrates functions 
from 'calc' and 'cam_feed' to capture and process images from the camera using 
the 'picamera2' library. It calculates the deviation of a celestial target 
(e.g., the moon) from the center of the image and visually marks the target's 
position and deviation on the camera feed.

Key Components:
- Initializes the camera and sets up the camera feed.
- Captures images and performs preprocessing using the 'calc' module.
- Calculates the target's position and deviation.
- Displays the camera feed with target markings.

Ensure 'picamera2', 'cv2' (OpenCV), 'calc', and 'cam_feed' modules are 
available to run this script.
"""

import calc as clc 
import cv2 as cv
import cam_feed as cam
from picamera2 import Picamera2
import time

duration = 1

targetvalues = (["Time", "target_x", "target_y", "target_radius"])

picam = Picamera2()

cam.setup(picam)


config = picam.create_still_configuration()
picam.configure(config)

picam.start()
    

testimg = picam.capture_array()
shape = testimg.shape

#Center Point of the Image in (X,Y) Coordinates
image_center = (int(shape[0]//2), int(shape[1]//2)) 

cv.namedWindow('Camera Output', cv.WINDOW_FULLSCREEN)
cv.setWindowProperty('Camera Output',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

(reference_x, reference_y) = image_center

# MAIN CAPTURE LOOP:
    
while True:
    start_frame = time.time()
    
    org_image = picam.capture_array()
    
    processed = clc.preprocessing(org_image, threshold = 0, blur = 5)
    
    (target_x, target_y, target_radius) = clc.moonposition(processed, 1) # Testparameter, wird noch entfernt
    
    targetvalues.append([str(time.time())[6:13],target_x, target_y, target_radius])
    
    marked = clc.targetmarkers(
        target_x,
        target_y,
        target_radius,
        reference_x,
        reference_y,
        processed,
        handover_value = f"Effective framerate of {1/duration:.2f} fps",
        overlay = True,
        scale = 1        
        )
    
    if target_x is not None:
        reference_x = target_x
        reference_y = target_y
    else:
        reference_x = None
        reference_y = None
        

    
    cv.imshow('Camera Output',marked)
    
    end_frame = time.time()
    
    duration = end_frame - start_frame
    
    
    key = cv.waitKey(1)
    
    if key != -1:
        break
    
clc.export(targetvalues, "Log")   

        
# cv.waitKey(0)
# cv.destroyAllWindows()
