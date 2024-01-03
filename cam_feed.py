# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 22:51:37 2023

@author: Tobias Kurz

This Python script utilizes the 'picamera2' library to initialize and set up 
the Pi-Camera for capturing images.

Functions:
- initialize(): Initializes the camera using 'Picamera2' and returns the 
  camera instance.
- setup(picam): Provides full-screen image of camera in high-refreshrate mode
  for the user to set up and focus the camera. Waits for user input before 
  exiting.

Ensure the 'picamera2' library is installed to run this script.
"""

from picamera2 import Picamera2
import time
import cv2 as cv


def initialize():
    picam = Picamera2()
    #config = picam.create_still_configuration()
    #picam.configure(config)
    
    picam.start()
    
    time.sleep(1)
    
    return(picam)

def setup(picam):
    
    config = picam.create_video_configuration()
    picam.configure(config)

    picam.start()
    
    time.sleep(1)
    
    print("Set camera in right Position and press any key when ready")
    
    
    testimg = picam.capture_array()
    shape = testimg.shape
    
    print(f'Shape: {shape}')

    
    while True:
        cv.namedWindow('Camera Feed', cv.WINDOW_FULLSCREEN)
        cv.setWindowProperty('Camera Feed',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
        img = picam.capture_array()
        
        cv.imshow('Camera Feed',img)
        
        key = cv.waitKey(1)
        
        if key != -1:
            cv.destroyWindow('Camera Feed')
            picam.stop()
                        
            return()
        

        
        
    