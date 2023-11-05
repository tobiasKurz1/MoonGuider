# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 19:41:05 2023

@author: Tobias Kurz
"""

from picamera2 import Picamera2, Preview
import cv2 as cv
import time


picam2 = Picamera2()
picam2.start()

time.sleep(1)


for nummer in range(5):
    
    img = picam2.capture_array()
    
    cv.imshow(f'Bild {nummer}',img)
    
    time.sleep(1)

cv.waitKey(0)
cv.destroyAllWindows()