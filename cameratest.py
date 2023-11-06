# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 19:41:05 2023

@author: Tobias Kurz
"""

from picamera2 import Picamera2, Preview
import cv2 as cv
import time
import cam_feed as cam

anz = int(input("Anzahl der Bilder: "))

delay = int(input("Abstand zw. Aufnahmen (s): "))
dateiname = input("dateiname: ")

picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)

picam2.start()

cam.setup(picam2)


testimg = picam2.capture_array()
shape = testimg.shape
print("Aufnahme beginnt!")

cv.namedWindow('Camera Feed', cv.WINDOW_NORMAL)
cv.resizeWindow('Camera Feed', shape[0]//4, shape[1]//4)
        


for nr in range(anz):
    print(f'{nr+1}/{anz}')
    picam2.capture_file(f'{dateiname}{nr}.jpg')
    image = picam2.capture_array()
    
    cv.imshow('Camera Feed',image)
    
    key = cv.waitKey(1)
    
    if key != -1:
        cv.destroyWindow('Camera Feed')
                    
        break
    
    
    time.sleep(delay)


"""
framerate = float(input("Framerate: "))
frames = int(input("Anzahl Frames: "))

picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

time.sleep(1)

testimg = picam2.capture_array()
shape = testimg.shape


cv.namedWindow('Camera Output', cv.WINDOW_NORMAL)
cv.resizeWindow('Camera Output', shape[0], shape[1])

start = time.time()

for nummer in range(frames):

    
    img = picam2.capture_array()
    
    end = time.time()
    
    cv.putText(img, f'{nummer+1}', (shape[0]//2, shape[1]//2), cv.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 2, cv.LINE_AA)
    
    time.sleep(1/framerate)
    
    cv.imshow('Camera Output',img)
    
    end = time.time()
    
    key = cv.waitKey(1)
    
    if key != -1:
        break
    


duration = end - start

print(f'Shape: {shape}')

print(f"Time elapsed: {duration:.2f} seconds\nThis is a effective framerate of {frames/duration:.2f} fps")
    
cv.destroyAllWindows()"""