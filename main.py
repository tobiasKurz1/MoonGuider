# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 22:44:20 2023

@author: Tobias Kurz
"""
import os
import cv2 as cv
import numpy as np
import dataloader as dl
import cam_feed as cam
from picamera2 import Picamera2
import time



def preprocessing(img):
        
    # Turn image into grey version (1 channel)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # Define Threshold value for brightest object
    th = 2 * np.min(img)
        
    # Remove unwanted stars or craters with threshold
    _, img = cv.threshold(img, int(th), 255, 0)    
        
    # Blur to remove noise
    img = cv.blur(img,(3,3))
    
    return(img)

def targetmarkers(target, img, shape):
    (width, height) = (shape[0], shape[1])
    if target is not None:
        
        print(f"Target at {target[0:2]}")
        center_x,  center_y, radius = target
        
        
        line_color = (0, 0, 0)  # Red in BGR format
        
        # Define the thickness of the lines
        line_thickness = 5
        
        # Draw deviation Arrow
        cv.arrowedLine(img, (width //2, height //2), (center_x, center_y), (0, 255, 0), line_thickness, tipLength=0.2)
    
        # Draw horizontal line
        cv.line(img, (center_x - 10, center_y), (center_x + 10, center_y), line_color, line_thickness)
    
        # Draw vertical line
        cv.line(img, (center_x, center_y - 10), (center_x, center_y + 10), line_color, line_thickness)
        
        #Draw the circle
        cv.circle(img, (center_x, center_y), radius, line_color, line_thickness)
        
    else:
        print("Target not found")
        
        center_x = width // 2
        center_y = height // 2
        
        cv.putText(img, "Not Found", (center_x,center_y), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
    
    return(img)

def moonposition(processed_img):
    
    circles = cv.HoughCircles(
        processed_img,       # Input image
        cv.HOUGH_GRADIENT,   # Detection method
        dp=1,                # Inverse ratio of the accumulator resolution to the image resolution
        minDist=50,          # Minimum distance between detected centers
        param1=100,          # Higher threshold for edge detection
        param2=30,           # Accumulator threshold for circle detection
        minRadius=10,        # Minimum circle radius
        maxRadius=800        # Maximum circle radius
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        
        circle = max(circles[0], key=lambda x: x[2]) #Filter out the biggest circle (moon)
        
        (center_x, center_y) = (circle[0], circle[1])
        radius = circle[2]

        num_circles = len(circles[0])
        print(f"Number of circles detected: {num_circles}. Marked largest radius.")
        return(center_x, center_y ,radius)
        
    else: 
        return(None)  

def get_deviation(center, target):
    
    if target is not None:
        dev = (target[0] - center[0], target[1] - center[1])
    else:
        dev = None
    return dev
    

picam = Picamera2()

config = picam.create_still_configuration()
picam.configure(config)

picam.start()
    

testimg = picam.capture_array()
shape = testimg.shape

image_center = (shape[0]//2, shape[1]//2) #Center Point of the Image in (X,Y) Coordinates



cam.setup(picam)



cv.namedWindow('Camera Output', cv.WINDOW_NORMAL)
#cv.resizeWindow('Camera Output', shape[0], shape[1])

# MAIN CAPTURE LOOP:
    
while True:
    start_frame = time.time()
    
    image = picam.capture_array()
    
    image = preprocessing(image)
    
    target = moonposition(image)
    
    deviation = get_deviation(image_center, target)
    print(f"Deviation: {deviation}")
    
    final = targetmarkers(target, image, shape)
    
    cv.imshow('Camera Output',final)
    
    end_frame = time.time()
    
    duration = end_frame - start_frame
    
    print(f"Effective framerate of {1/duration:.2f} fps")
    
    key = cv.waitKey(1)
    
    if key != -1:
        break
    
    

        
# cv.waitKey(0)
# cv.destroyAllWindows()
