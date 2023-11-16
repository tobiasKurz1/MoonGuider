# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 21:08:05 2023

@author: Tobias Kurz

This Python script offers functions for processing the Images taken by the Pi.
This includes preprocessing, detection of the moon and calculating deviations 
from the center. 

Functions:
- preprocessing(img, grey=True, threshold=0, blur=3): Preprocesses images by 
  converting to grayscale, applying threshold, and blurring.
- targetmarkers(target, img, shape): Marks moon position and deviation on the 
  image.
- moonposition(processed_img, param=1): Detects the largest circle 
  (e.g., the moon) in the processed image.
- get_deviation(center, target): Calculates deviation between the center 
  and target.

Ensure OpenCV (cv2) and NumPy are installed.

"""

import cv2 as cv
import numpy as np

def preprocessing(img, grey = True, threshold = 0, blur = 3):
        
    # Turn image into grey version (1 channel)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) if grey else img
    
    # Define Threshold value for brightest object
    th = threshold * np.min(img) if threshold else None
        
    # Remove unwanted stars or craters with threshold
    (_, img) = cv.threshold(img, int(th), 255, 0) if threshold else (None, img)
        
    # Blur to remove noise
    img = cv.blur(img,(int(blur), int(blur))) if blur else img
    
    return(img)

def targetmarkers(target, prev_center, img, shape):
    (width, height) = (shape[0], shape[1])
    line_color = (0, 0, 255)  # Red in BGR format
    
    # Define the thickness of the lines
    line_thickness = 5
    
    if target is not None and prev_center is not None:
        
        print(f"Target at {target}")
        center_x,  center_y, radius = target
        
        

        
        # Draw deviation Arrow
        cv.arrowedLine(img, prev_center, (center_x, center_y), (0, 255, 0), line_thickness, tipLength=0.2)
    
        # Draw horizontal line
        cv.line(img, (center_x - radius, center_y), (center_x + radius, center_y), line_color, line_thickness)
    
        # Draw vertical line
        cv.line(img, (center_x, center_y - radius), (center_x, center_y + radius), line_color, line_thickness)
        
        #Draw the circle
        cv.circle(img, (center_x, center_y), radius, line_color, line_thickness)
        
    else:
        print("Target not found")
        
        cv.line(img, (0, 0), (height, width), line_color, line_thickness)
        cv.line(img, (0, width), (height, 0), line_color, line_thickness)
        
        cv.circle(img, (height // 2, width // 2), 120, line_color, line_thickness)
        cv.circle(img, (height // 2, width // 2), 160, line_color, line_thickness)

        
        #cv.putText(img, "Not Found", (center_x,center_y), cv.FONT_HERSHEY_SIMPLEX, 10, (0,0,255))
    
    return(img)

def moonposition(processed_img, param = 1):
    
    circles = cv.HoughCircles(
        processed_img,       # Input image
        cv.HOUGH_GRADIENT,   # Detection method
        dp=param,                # Inverse ratio of the accumulator resolution to the image resolution
        minDist=50,          # Minimum distance between detected centers
        param1=100,          # Higher threshold for edge detection
        param2=30,           # Accumulator threshold for circle detection
        minRadius=120,        # Minimum circle radius
        maxRadius=160        # Maximum circle radius
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

def get_deviation(prev, current):
    
    if current is not None and prev is not None:
        current = (int(current[0]), int(current[1]))
        dev = (current[0] - prev[0], current[1] - prev[1])
    else:
        dev = None
    return dev

