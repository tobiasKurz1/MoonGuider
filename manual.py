import calc as clc 
import cv2 as cv
import cam_feed as cam
from picamera2 import Picamera2
import time
import relay_handling as relay
import keyboard
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = []
y1 = []
y2 = []

relay_pins = [18, 22, 17, 27]

buffer = clc.buffer(buffer_length = 2)

guide = relay.guide(relay_pins, margin = 1.5)

time.sleep(1)

picam = Picamera2()

picam.setup()

targetvalues = []
targetvalues.append(["Time", "target_x", "target_y", "Active Relays"])

#config = picam.create_video_configuration()
config = picam.create_still_configuration()
picam.configure(config)

picam.start()
    


testimg = picam.capture_array()
shape = testimg.shape

#Center Point of the Image in (X,Y) Coordinates
image_center = (int(shape[1]//2), int(shape[0]//2)) 

cv.namedWindow('Camera Output', cv.WINDOW_FULLSCREEN)
cv.setWindowProperty('Camera Output',cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

(reference_x, reference_y) = image_center

def animate(i, x, y1, y2):
    
    buff = 100
    
    x = x[-buff:]
    y1 = y1[-buff:]
    y2 = y2[-buff:]
    
    
    # Draw x and y lists
    ax.clear()
    ax.plot(x, y1, label="y1")
    ax.plot(x, y2, label="y2")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TEst')
    plt.ylabel('Values')
    plt.legend()

def on_key_event(e):
    if e.name == 'd':
        guide.activate(relay_pins[0])
        guide.deactivate(relay_pins[1])
        guide.deactivate(relay_pins[2])
        guide.deactivate(relay_pins[3])
    if e.name == 'a':
        guide.deactivate(relay_pins[0])
        guide.activate(relay_pins[1])
        guide.deactivate(relay_pins[2])
        guide.deactivate(relay_pins[3])
    if e.name == 'w':
        guide.deactivate(relay_pins[0])
        guide.deactivate(relay_pins[1])
        guide.activate(relay_pins[2])
        guide.deactivate(relay_pins[3])
    if e.name == 's':
        guide.deactivate(relay_pins[0])
        guide.deactivate(relay_pins[1])
        guide.deactivate(relay_pins[2])
        guide.activate(relay_pins[3])

# MAIN CAPTURE LOOP:
keyboard.on_press(on_key_event)  

ani = animation.FuncAnimation(fig, animate, fargs=(x, y1, y2), interval=500)

while True:  
    
   
    if keyboard.is_pressed('esc'):
        print("Escape key pressed. Exiting the loop.")
        break

    
    org_image = picam.capture_array()
    
    processed = clc.preprocessing(org_image, threshold = 0, blur = 5)
     
    (target_x, target_y, target_radius) = clc.moonposition(processed, 1) # Testparameter, wird noch entfernt
    
    
       
    buffer.add(target_x, "target_x")
    buffer.add(target_y, "target_y")
    buffer.add(target_radius, "target_radius")    
    
    x.append(time.ctime())
    y1.append(buffer.average("target_x"))
    y2.append(buffer.average("target_y"))
    
        
    targetvalues.append([str(time.time())[6:13],target_x, target_y, guide.showactive()])  
     

cv.destroyAllWindows()
guide.stop()

clc.export(targetvalues, "Log")   
keyboard.unhook_all()