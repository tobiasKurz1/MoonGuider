# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 22:44:20 2023

@author: Tobias Kurz

This Python script serves as the main file that integrates functions 
from 'calc' and 'cam_feed' to capture and process images from the camera using 
the 'picamera2' library. It calculates the deviation of a celestial target 
(e.g., the moon) from the center of the image and visually marks the target's 
position and deviation on the camera feed.

Key Components:
- Initializes the camera and sets up the camera feed.
- Captures images and performs preprocessing using the 'calc' module.
- Calculates the target's position and deviation.
- Displays the camera feed with target markings.

Ensure 'picamera2', 'cv2' (OpenCV), 'calc', and 'cam_feed' modules are 
available to run this script.
"""

import calc as clc 
import cv2 as cv
import cam_feed as cam
from picamera2 import Picamera2
import time
import relay_handling_TP as relay
import config_loader as load

log = clc.log()

config = load.configuration(log)



log.add('Target',["Time", "target_x", "target_y", "target_x_average", "target_y_average", 
                  "x_deviation", " y_deviation"])



duration = 1
press_counter = 0
avrg_target_x = None
avrg_target_y = None


buffer = clc.buffer(config.buffer_length)

guide = relay.guide(log, config)
    

def perform_relay_test():
    deviations = []

    while True:
        cv.namedWindow('Camera Output', cv.WINDOW_NORMAL)
        cv.setWindowProperty('Camera Output',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
        
        org_image = picam.capture_array()
        processed = clc.preprocessing(org_image, config)
        
        (target_x, target_y, _) = clc.moonposition(processed, config)
                
        marked = clc.targetmarkers(
            target_x,
            target_y,
            _,
            target_x,
            target_y,
            (0,0),
            org_image,
            config,
            handover_value = "Press any key to skip relay test.\nPress Button if correct stationary Target is found.")
                
        cv.imshow('Camera Output',marked)
        key = cv.waitKey(1)
        
        if key != -1:
            return
        
        if guide.button_is_pressed():
            cv.destroyAllWindows()
            print("Relay Testing in Progress...\nThis will take 40s")
            time.sleep(1)
            break
    
    
    for pin, direction in zip(guide.relay_pins, ["right","left","down","up"]):
        org_image = picam.capture_array()
        processed = clc.preprocessing(org_image, config)
        
        (target_x, target_y, _) = clc.moonposition(processed, config)

    
    
    for pin, direction in zip(guide.relay_pins, ["right","left","down","up"]):
        org_image = picam.capture_array()
        processed = clc.preprocessing(org_image, config)
        
        (target_x, target_y, _) = clc.moonposition(processed)
        
        print(f"Testing pin {pin} ({direction})...")
        
        guide.activate_pin(pin)
        time.sleep(10)
        guide.activate()
        
        org_image = picam.capture_array()
        processed = clc.preprocessing(org_image, config)
        (x, y, _) = clc.moonposition(processed, config)
        deviation = clc.get_deviation((x, y), (target_x, target_y))
        deviations.append(deviation)
        print(f"Detected deviation: {deviation}")
        
    input("\nPress Enter to continue")
    

    time.sleep(1)
    return


picam = Picamera2()

if config.show_cam_feed: cam.setup(picam)

#camera_config = picam.create_video_configuration()
#camera_config = picam.create_still_configuration()
camera_config = picam.create_video_configuration(
    main={'format': 'RGB888', "size": config.image_size},
    buffer_count = config.image_buffer,
    )


picam.configure(camera_config)

picam.start()
    
testimg = picam.capture_array()
shape = testimg.shape

if config.do_relay_test: perform_relay_test()

#Center Point of the Image in (X,Y) Coordinates
image_center = (int(shape[1]//2), int(shape[0]//2)) 

(reference_x, reference_y) = image_center

start_time = time.time()
# MAIN CAPTURE LOOP:
    
while True:
    cv.namedWindow('Camera Output', cv.WINDOW_NORMAL)
    cv.setWindowProperty('Camera Output',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
    
    start_frame = time.time()
    
    org_image = picam.capture_array()
    
    processed = clc.preprocessing(org_image, config)
    
    (target_x, target_y, target_radius) = clc.moonposition(processed, config)
    
    if not None in (target_x, target_y):
        if max(abs(target_x - avrg_target_x), abs(target_y - avrg_target_y)) > 100:
            (target_x, target_y, target_radius) = (None, None, None)
    
    buffer.add(target_x, "target_x")
    buffer.add(target_y, "target_y")
    buffer.add(target_radius, "target_radius")    
    
    avrg_target_x = buffer.average("target_x")
    avrg_target_y = buffer.average("target_y")
    
    if guide.button_is_pressed() and not None in (avrg_target_x, avrg_target_y):
        (reference_x, reference_y) = (avrg_target_x, avrg_target_y)
        press_counter += 1
        if press_counter >= 2:
            (reference_x, reference_y) = image_center            
    else:
        press_counter = 0
    
    deviation = clc.get_deviation((avrg_target_x, avrg_target_y), (reference_x, reference_y))  
  
    guide.to(deviation)
    
    log.add("Target", [time.time(), target_x, target_y, avrg_target_x, avrg_target_y,
                       deviation[0], deviation[1]])
    
    marked = clc.targetmarkers(
        avrg_target_x,
        avrg_target_y,
        buffer.average("target_radius"),
        reference_x,
        reference_y,
        guide.active_deviation,
        org_image,
        config,
        handover_value = f"{1/duration:.2f} FpS, active relays: {guide.showactive()},\nValid target positions: {buffer.get_valid()}, {int(time.time()-start_time)}")
    
    
    cv.imshow('Camera Output',marked)
    
    end_frame = time.time()
    
    duration = end_frame - start_frame
         
    key = cv.waitKey(1)
    
    if key != -1:
        break
    
    if time.time()-start_time > 60 * 5 : #nach 5 min abbrechen ####################################################### test
        break

cv.destroyAllWindows()
guide.stop()



if config.export_to_excel: log.export()   

        

        
    

