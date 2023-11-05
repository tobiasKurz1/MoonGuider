# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 19:41:05 2023

@author: Tobias Kurz
"""

from picamera2 import Picamera2, Preview
import cv2 as cv
import time

framerate = float(input("Framerate: "))
frames = int(input("Anzahl Frames: "))

picam2 = Picamera2()
picam2.start()

time.sleep(1)

testimg = picam2.capture_array()


cv.namedWindow('Camera Output', cv.WINDOW_NORMAL)
cv.resizeWindow('Camera Output', testimg.shape[0], testimg.shape[1])

for nummer in range(frames):
    
    img = picam2.capture_array()
    
    cv.putText(img,nummer)
    
    cv.imshow('Camera Output',img)
    
    key = cv.waitKey(int(1000/framerate))
    
    if key != -1:
        break
    
    time.sleep(1/framerate)


    
cv.destroyAllWindows()