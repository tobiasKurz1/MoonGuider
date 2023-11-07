# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 22:51:37 2023

@author: Tobias Kurz
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
    
    print("Set camera in right Position and press any key when ready")
    
    
    testimg = picam.capture_array()
    shape = testimg.shape
    
    print(f'Shape: {shape}')


    cv.namedWindow('Camera Feed', cv.WINDOW_FULLSCREEN)
    cv.setWindowProperty('Camera Feed',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
        
    
    while True:
        img = picam.capture_array()
        
        cv.imshow('Camera Feed',img)
        
        key = cv.waitKey(1)
        
        if key != -1:
            cv.destroyWindow('Camera Feed')
            picam.stop()
                        
            return()
        

        
        
    