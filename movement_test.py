import calc as clc 
import cv2 as cv
import cam_feed as cam
from picamera2 import Picamera2
import time
import relay_handling as relay

relay_pins = [18, 22, 17, 27]

buffer = clc.buffer(buffer_length = 4)

guide = relay.guide(relay_pins, margin = 1.5)

time.sleep(1)

picam = Picamera2()


#config = picam.create_video_configuration()
config = picam.create_still_configuration()
picam.configure(config)

picam.start()
    
#guide.setup()

testimg = picam.capture_array()
shape = testimg.shape

#Center Point of the Image in (X,Y) Coordinates
image_center = (int(shape[1]//2), int(shape[0]//2)) 

cv.namedWindow('Camera Output', cv.WINDOW_FULLSCREEN)
cv.setWindowProperty('Camera Output',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

(reference_x, reference_y) = image_center

# MAIN CAPTURE LOOP:

step = 10
    
i = 0
    
while True: 
    
    if i in range(step): 
        guide.activate(relay_pins[0])
        guide.deactivate(relay_pins[1])
        guide.deactivate(relay_pins[2])
        guide.deactivate(relay_pins[3])

    if i in range(step+1, step*2): 
        guide.deactivate(relay_pins[0])
        guide.activate(relay_pins[1])
        guide.deactivate(relay_pins[2])
        guide.deactivate(relay_pins[3])

    if i in range(step * 2 + 1, step * 3): 
        guide.deactivate(relay_pins[0])
        guide.deactivate(relay_pins[1])
        guide.activate(relay_pins[2])
        guide.deactivate(relay_pins[3])

    if i in range(step * 3 + 1, step * 4): 
        guide.deactivate(relay_pins[0])
        guide.deactivate(relay_pins[1])
        guide.deactivate(relay_pins[2])
        guide.activate(relay_pins[3])        
    
    i = i+1
    
    if i > step * 4: break


    
    org_image = picam.capture_array()
    
    processed = clc.preprocessing(org_image, threshold = 0, blur = 5)
     
    (target_x, target_y, target_radius) = clc.moonposition(processed, 1) # Testparameter, wird noch entfernt
    
    buffer.add(target_x, "target_x")
    buffer.add(target_y, "target_y")
    buffer.add(target_radius, "target_radius")    
        
    marked, deviation = clc.targetmarkers(
        buffer.average("target_x"),
        buffer.average("target_y"),
        buffer.average("target_radius"),
        reference_x,
        reference_y,
        processed,
        handover_value = f"Active relays: {guide.showactive()} {i%10:.2f}",
        overlay = True,
        scale = 1        
        )
    

    
    
       
    cv.imshow('Camera Output',marked) 
    
    key = cv.waitKey(1)
    
    if key != -1:
        break

    

cv.destroyAllWindows()
guide.stop()

        

