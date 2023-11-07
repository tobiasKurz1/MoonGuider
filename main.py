# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 22:44:20 2023

@author: Tobias Kurz
"""
import os
import calc as clc 
import cv2 as cv
import numpy as np
import cam_feed as cam
from picamera2 import Picamera2
import time



picam = Picamera2()

cam.setup(picam)

config = picam.create_still_configuration()
picam.configure(config)

picam.start()
    

testimg = picam.capture_array()
shape = testimg.shape

image_center = (shape[0]//2, shape[1]//2) #Center Point of the Image in (X,Y) Coordinates


cv.namedWindow('Camera Output', cv.WINDOW_FULLSCREEN)
cv.setWindowProperty('Camera Output',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)


# MAIN CAPTURE LOOP:
    
while True:
    start_frame = time.time()
    
    image = picam.capture_array()
    
    image = clc.preprocessing(image,threshold=False)
    
    target = clc.moonposition(image)
    
    deviation = clc.get_deviation(image_center, target)
    print(f"Deviation: {deviation}")
    
    final = clc.targetmarkers(target, image, shape)
    
    cv.imshow('Camera Output',final)
    
    end_frame = time.time()
    
    duration = end_frame - start_frame
    
    print(f"Effective framerate of {1/duration:.2f} fps")
    
    key = cv.waitKey(1)
    
    if key != -1:
        break
    
    

        
# cv.waitKey(0)
# cv.destroyAllWindows()
