import calc as clc 
import cv2 as cv
import cam_feed as cam
from picamera2 import Picamera2
import time
import relay_handling as relay


step = int(input("Nr. of steps per direction: "))
s = float(step)
i = 1

rounds = int(input("Nr. of Rounds: "))
r = float(rounds)


relay_pins = [19, 13, 6, 26]

buffer = clc.buffer(buffer_length = 2)

guide = relay.guide(relay_pins, margin = 1.5)

time.sleep(1)

picam = Picamera2()


targetvalues = []
targetvalues.append(["Time", "target_x", "target_y", "deviation_x", "deviation_y", "Active Relays"])

#config = picam.create_video_configuration()
config = picam.create_still_configuration()
picam.configure(config)

picam.start()
    

testimg = picam.capture_array()
shape = testimg.shape

#Center Point of the Image in (X,Y) Coordinates
image_center = (int(shape[1]//2), int(shape[0]//2)) 

(reference_x, reference_y) = image_center

# MAIN CAPTURE LOOP:
    
while True: 
    cv.namedWindow('Camera Output', cv.WINDOW_NORMAL)
    cv.setWindowProperty('Camera Output',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
    
    if i in range(step+1, step*2): 
        guide.activate(right=True)

    if i in range(step * 2 + 1, step * 3): 
        guide.activate(left=True)

    if i in range(step * 3 + 1, step * 4): 
        guide.activate(down=True)

    if i in range(step * 4 + 1, step * 5): 
        guide.activate(up=True)       
    
    
    if i > step * 5: 
        i = 1
        guide.activate()  
        rounds = rounds - 1
        if rounds <= 0:
            break
    
   
    prozent = (((r-rounds)*5*s + i) / (s * 5 * r)) *100

    i = i+1

    
    org_image = picam.capture_array()
    
    processed = clc.preprocessing(org_image, threshold = 0, blur = 5)
     
    (target_x, target_y, target_radius) = clc.moonposition(processed) # Testparameter, wird noch entfernt
    
    
       
    buffer.add(target_x, "target_x")
    buffer.add(target_y, "target_y")
    buffer.add(target_radius, "target_radius")    
    deviation = clc.get_deviation((target_x, target_y), (reference_x, reference_y))
    
    marked = clc.targetmarkers(
        buffer.average("target_x"),
        buffer.average("target_y"),
        buffer.average("target_radius"),
        reference_x,
        reference_y,
        (0,0),
        processed,
        handover_value = f"Active relays: {guide.showactive()}    {i-1} / {step*5}; rounds left:{rounds-1}; {prozent:.1f}%",
        overlay = True,
        scale = 1        
        )
    
    targetvalues.append([str(time.time())[6:13],target_x, target_y, deviation[0], deviation[1], guide.showactive()])  
    
    
       
    cv.imshow('Camera Output',marked) 
    
    key = cv.waitKey(1)
    
    if key != -1:
        break

    

cv.destroyAllWindows()
guide.stop()

clc.export(targetvalues, "Log")   

