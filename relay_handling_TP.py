# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 22:41:42 2024

@author: Tobias Kurz
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 21:59:14 2023

@author: Tobias Kurz
"""
import RPi.GPIO as GPIO
import time
import threading





class guide:
    def __init__(self, 
                 log,
                 relay_pins = [19, 13, 6, 26], 
                 button_pin = 16, 
                 margin = 0, 
                 sticky_buffer = 0, 
                 cloud_mode = None, 
                 record_buffer = 20, 
                 rotate = 0):
        
        self.log = log
        self.log.add('Activity',["Time", "Duration", "Direction"])
        
        self.active_deviation = (None, None)
        self.margin = margin
        self.active = [False, False, False, False]
        
        self.stop_threads = False
        # Create a lock for thread synchronization
        self.gpio_lock = threading.Lock()
        self.log_lock = threading.Lock()
        self.active_lock = threading.Lock()
        self.active_deviation_lock = threading.Lock()

        # Create a thread for relay activation
        self.activate_thread_ra = threading.Thread(target=self.activate_ra, daemon = True)        
        self.activate_thread_dec = threading.Thread(target=self.activate_dec, daemon = True)




        self.pulsed = [False, False]
        self.button_pin = button_pin
        self.mode_info = None
        
        self.sticky_buffer = sticky_buffer
        
        self.sbx = []
        self.sby = []
        

        
        self.last_deviation = (None, None)
        self.deviation_records = [(0,0)]
        
        self.record_buffer = record_buffer
        

        # Pin order is RIGHT, LEFT, DOWN, UP
        self.relay_pins = relay_pins
    
        if rotate == 90:
            self.relay_pins = [relay_pins[3], relay_pins[2], relay_pins[0], relay_pins[1]]
        elif rotate == 180:
            self.relay_pins = [relay_pins[1], relay_pins[0], relay_pins[3], relay_pins[2]]
        elif rotate == 270:
            self.relay_pins = [relay_pins[2], relay_pins[3], relay_pins[1], relay_pins[0]]
        else:
            if rotate != 0:
                raise ValueError("Only camera rotations of 0, 90, 180 or 270 Degree supported.")
            
                 
        if cloud_mode == "guide_last" or cloud_mode == "repeat":
            self.cloud_mode = cloud_mode
        else:
            self.cloud_mode = None
            
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
               
        for pin in self.relay_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
        
        for pin in self.relay_pins:
            self.pulse(pin, 1)
                
    def to(self, deviation = (None, None)):

        self.active_deviation = deviation
        
        
                
        
        if not self.activate_thread_ra.is_alive():
            self.activate_thread_ra = threading.Thread(target=self.activate_ra, daemon = True)
            self.activate_thread_ra.start()
        if not self.activate_thread_dec.is_alive():
            self.activate_thread_dec = threading.Thread(target=self.activate_dec, daemon = True)
            self.activate_thread_dec.start()
        #self.cloud_handling()
        

        #####
             
        return
          
    
    def activate_ra(self): # left right
        if not self.stop_threads:
            ad = self.active_deviation
            margin = self.margin
            if not None in ad:
                    xdev = ad[0]              
                    if abs(xdev) <= margin: pass
                    else:
                        (right, left) = (xdev > margin, xdev < margin * -1)
                                                   
                        # calculate pulse time
                        temp = (abs(xdev)-margin) * 0.2
                        duration = temp if temp < 3 else 3
                        
                        with self.active_lock:
                             self.active[0] = right
                             self.active[1] = left
                        
                        direction = 'right' if right else 'left'
                        
                        with self.log_lock:
                            self.log.add('Activity',[time.time(), duration, direction])
                           
                        self.switch_pin_on([right, left, False, False])   
                        time.sleep(duration)
                        self.switch_pin_off([right, left, False, False])

                    
                         
    def activate_dec(self): # up down
        if not self.stop_threads:
            ad = self.active_deviation
            margin = self.margin
            if not None in ad:
                ydev = ad[1]
                if abs(ydev) <= margin: pass
                else:    
                    (down, up) = (ydev > margin, ydev < margin * -1)
                                                   
                    # calculate pulse time
                    temp = (abs(ydev)-margin) * 0.2
                    duration = temp if temp < 3 else 3
                    
                    with self.active_lock:
                         self.active[2] = down
                         self.active[3] = up
                         
                    direction = 'down' if down else 'up'  
                    
                    with self.log_lock:
                        self.log.add('Activity',[time.time(), duration, direction])
                    
                    self.switch_pin_on([False, False, down, up])
                    time.sleep(duration)
                    self.switch_pin_off([False, False, down, up])
                    

    
    
    def switch_pin_on(self, directions = ['Right', 'Left', 'Down', 'Up']):
        with self.gpio_lock:
            for pin, direction in zip(self.relay_pins, directions):
                if direction: GPIO.output(pin, GPIO.LOW)
        return
    
    def switch_pin_off(self, directions = ['Right', 'Left', 'Down', 'Up']):
        with self.gpio_lock:
            for pin, direction in zip(self.relay_pins, directions):
                if direction: GPIO.output(pin, GPIO.HIGH)
        return
        
        
        
    def button_is_pressed(self):
        return GPIO.input(self.button_pin) == GPIO.LOW
    
    def check_sticky(self, xdev, ydev):
        self.pulsed = [False, False]  
        
        if not self.mode_info == "Active Guiding":
            return
        
        if None in (xdev, ydev):
            return
        
        self.sbx.append(abs(xdev))
        self.sby.append(abs(ydev))
        
             
        if len(self.sbx) > self.sticky_buffer:
            self.sbx.pop(0)
        if len(self.sby) > self.sticky_buffer:
            self.sby.pop(0)
        

            if (self.sbx[0] < self.sbx[-1]) and (len(self.sbx) == self.sticky_buffer) and (max(self.sbx) > 10):
                self.pulse(self.relay_pins[0])
                self.pulse(self.relay_pins[1])
                self.sbx = []
                self.pulsed[0] = True
                                
            if (self.sby[0] < self.sby[-1]) and (len(self.sby) == self.sticky_buffer) and (max(self.sby) > 10):
                self.pulse(self.relay_pins[2])
                self.pulse(self.relay_pins[3])
                self.sbx = []
                self.pulsed[1] = True
                
            
        return
    
    
    def pulse(self, pin, count = 1):
        for i in range(count):
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.1)
                        
        return
    
    def activate_pin(self, pin):
        GPIO.output(pin, GPIO.LOW)
        return
    
    
    def showactive(self):
        act = []
        
        if self.active[0]:
            act.append("Right")
        if self.active[1]:
            act.append("Left")
        if self.active[2]:
            act.append("Down")
        if self.active[3]:
            act.append("Up")
            
        if self.pulsed[0]:
            act.append("X-Sticky")
        if self.pulsed[1]:
            act.append("Y-Sticky")
            
        act.append(self.mode_info)
            
        return(act)
    
    def cloud_handling(self):
        
        if not None in self.active_deviation:
            
            self.record(self.active_deviation)
            self.last_deviation = self.active_deviation
            self.mode_info = "Active Guiding"
                        
            return
        
        else: 
            if self.cloud_mode == "guide_last" and not None in self.last_deviation :
                self.mode_info = f"Guiding to last valid deviation {self.last_deviation}"
                self.active_deviation = self.last_deviation
                return
                
            elif self.cloud_mode == "repeat":
                self.mode_info = f"Repeating last {len(self.deviation_records)} deviations"
                
                #cycle through list:
                self.active_deviation = self.deviation_records[0]
                self.deviation_records.append(self.deviation_records[0])
                self.deviation_records.pop(0)
                return
 
            else:
                self.mode_info = "Guiding paused"     
        
        return
    
    def record(self, deviation):
       
        self.deviation_records.append(deviation)
        
        if len(self.deviation_records) > self.record_buffer:
            self.deviation_records.pop(0)
        return
    
    
    
    def stop(self):
        
        self.stop_threads = True
        self.activate_thread_ra.join()
        self.activate_thread_dec.join()
        
        self.switch_pin_off([True, True, True, True])
         
        GPIO.cleanup()
        return
  


          