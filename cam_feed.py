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

def setup(picam2):
    print("Set camera in right Position and press any key when ready")
    
    
    testimg = picam2.capture_array()
    shape = testimg.shape
    
    print(f'Shape: {shape}')


    cv.namedWindow('Camera Feed', cv.WINDOW_NORMAL)
    cv.resizeWindow('Camera Feed', shape[0], shape[1])
    
    
    while True:
        img = picam2.capture_array()
        
        cv.imshow('Camera Feed',img)
        
        key = cv.waitKey(1)
        
        if key != -1:
            cv.destroyWindow('Camera Feed')
                        
            return()
        

        
        
    