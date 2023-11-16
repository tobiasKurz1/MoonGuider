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
import time
import pandas as pd

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

def targetmarkers(target_x, target_y, target_radius, ref_x, ref_y, img, handover_value, overlay = True, scale = 1):
    
    if len(img.shape) == 2:
        img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

    img = cv.resize(img, None, fx=scale, fy=scale, interpolation= cv.INTER_LINEAR)
        
    (height, width) = img.shape[0:2]
    line_color = (0, 0, 255)  # Red in BGR format
    
    # Define the thickness of the lines
    line_thickness = 5
    
    if target_x is not None and ref_x is not None:
        
        print(f"Target at unscaled Coordinates: {target_x}, {target_y}")
        
        target_x = int(target_x * scale)
        target_y = int(target_y * scale)
        target_radius = int(target_radius * scale)
        ref_x = int(ref_x * scale)
        ref_y =int(ref_y * scale)
        
                
        # Draw deviation Arrow
        cv.arrowedLine(img, (ref_x, ref_y), (target_x, target_y), (0, 255, 0), line_thickness, tipLength=0.2)
    
        # Draw horizontal line
        cv.line(img, (target_x - target_radius, target_y), (target_x + target_radius, target_y), line_color, line_thickness)
    
        # Draw vertical line
        cv.line(img, (target_x, target_y - target_radius), (target_x, target_y + target_radius), line_color, line_thickness)
        
        #Draw the circle
        cv.circle(img, (target_x, target_y), target_radius, line_color, line_thickness)
        
    else:
        print("Target not found")
        
        cv.line(img, (0, 0), (width, height), line_color, line_thickness)
        cv.line(img, (0, height), (width, 0), line_color, line_thickness)
        
        cv.circle(img, (width // 2, height // 2), 120, line_color, line_thickness)
        cv.circle(img, (width // 2, height // 2), 160, line_color, line_thickness)

        
        #cv.putText(img, "Not Found", (center_x,center_y), cv.FONT_HERSHEY_SIMPLEX, 10, (0,0,255))
    
    if overlay:
        
        bar_text = f"Target at {target_x}, {target_y}. {handover_value}"
        
        # Define the height of the black bar (you can adjust this value)
        bar_height = int(height * 0.2)
    
        # Create a black bar
     
        bar = np.ones((bar_height, width, 3), dtype=np.uint8) * 255
    
        # Add the text to the black bar
        font = cv.FONT_HERSHEY_SIMPLEX
        textsize = bar_height/150
        print(f"text : {textsize}")
        text_size = cv.getTextSize(bar_text, font, textsize, 2)[0]
        text_position = ((width - text_size[0]) // 2, (bar_height + text_size[1]) // 2)
        cv.putText(bar, bar_text, text_position, font, 1, (0, 0, 0), 2, cv.LINE_AA)
        
        # Stack the black bar on top of the original image
        #img = np.vstack((img, bar))
        #img = np.concatenate((img, bar), axis=0)
        img[height-bar_height:height, 0:width] = bar
        
        
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
        return(None,None,None)  

def get_deviation(ref, target):
    
    if not None in (target[0], ref[0]):
        target = (int(target[0]), int(target[1]))
        dev = (target[0] - ref[0], target[1] - ref[1])
    else:
        dev = None
    return dev

def export(values, filename):
    
    data = pd.DataFrame({"Values":values})
    data.to_excel(f'{filename}.xlsx',sheet_name=f'{time.ctime()[0:10]}',index=False)
    
    print(f"Exported to Excelfile '{filename}.xlsx'")

    
