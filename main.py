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
import relay_handling as relay

duration = 1

targetvalues = []
targetvalues.append(["Time", "target_x", "target_y", "target_radius", "x_deviation"," y_deviation", "Active Relays"])

buffer = clc.buffer(buffer_length = 6)

guide = relay.guide(relay_pins = [18, 22, 27, 17], margin = 1.5)

time.sleep(1)

picam = Picamera2()

cam.setup(picam)

#config = picam.create_video_configuration()
config = picam.create_still_configuration()
picam.configure(config)

picam.start()
    
#guide.setup()

testimg = picam.capture_array()
shape = testimg.shape

#Center Point of the Image in (X,Y) Coordinates
image_center = (int(shape[1]//2), int(shape[0]//2)) 

cv.namedWindow('Camera Output', cv.WINDOW_FULLSCREEN)
cv.setWindowProperty('Camera Output',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

(reference_x, reference_y) = image_center

# MAIN CAPTURE LOOP:
    
while True:
    start_frame = time.time()
    
    org_image = picam.capture_array()
    
    processed = clc.preprocessing(org_image, threshold = 0, blur = 5)
    
    (target_x, target_y, target_radius) = clc.moonposition(processed, 1) # Testparameter, wird noch entfernt
    
    buffer.add(target_x, "target_x")
    buffer.add(target_y, "target_y")
    buffer.add(target_radius, "target_radius")    
    
    
    
    marked, deviation = clc.targetmarkers(
        buffer.average("target_x"),
        buffer.average("target_y"),
        buffer.average("target_radius"),
        reference_x,
        reference_y,
        processed,
        handover_value = f"Effective framerate of {1/duration:.2f} fps, active relays: {guide.showactive()}",
        overlay = True,
        scale = 1        
        )
    targetvalues.append([str(time.time())[6:13],target_x, target_y, deviation[0], deviation[1], target_radius, guide.showactive()])  
    guide.to(deviation)
    
    """ Commented Because guiding to image center
    if target_x is not None:
        reference_x = buffer.average("target_x")
        reference_y = buffer.average("target_y")
    else:
        reference_x = None
        reference_y = None
    """   

    
    cv.imshow('Camera Output',marked)
    
    end_frame = time.time()
    
    duration = end_frame - start_frame
    

    
    
    key = cv.waitKey(1)
    
    if key != -1:
        break

    

cv.destroyAllWindows()
guide.stop()

clc.export(targetvalues, "Log")   

        

