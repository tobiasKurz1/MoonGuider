# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 21:59:14 2023

@author: Tobias Kurz
"""
import RPi.GPIO as GPIO
import time

    

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
        self.margin = margin
        self.active = [False, False, False, False]
        self.pulsed = [False, False]
        self.button_pin = button_pin
        self.mode_info = None
        
        self.sticky_buffer = sticky_buffer
        
        self.sbx = []
        self.sby = []
        
        self.active_deviation = (None, None)
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
        
            """ Use this if you want the sticky pulse to activate only when 
            every change is with increasing deviation:
                
            err_x = 0
            err_y = 0
            

            for i in range(1,len(self.sbx)):
                if self.sbx[i] > self.sbx[i-1]:
                    err_x = err_x + 1
                if self.sby[i] > self.sby[i-1]:
                    err_y = err_y + 1
            
            if err_x >= self.sticky_buffer - 1:
                self.pulse(0)
                self.pulse(1)
                self.sbx = []
                self.sby = []
                
            if err_y >= self.sticky_buffer - 1:
                self.pulse(2)
                self.pulse(3)
                self.sbx = []
                self.sby = []
            """         

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
    
    def activate(self, right = False, left = False, down = False, up = False):
        """ Activates the Pins which are set to True, deactivates the Rest """
         
        if right:
            GPIO.output(self.relay_pins[0], GPIO.LOW)
            self.active[0] = True
        else:
            GPIO.output(self.relay_pins[0], GPIO.HIGH)
            self.active[0] = False            
            
        if left:
            GPIO.output(self.relay_pins[1], GPIO.LOW)
            self.active[1] = True
        else:
            GPIO.output(self.relay_pins[1], GPIO.HIGH)
            self.active[1] = False
            
        if down:
            GPIO.output(self.relay_pins[2], GPIO.LOW)
            self.active[2] = True
        else:
            GPIO.output(self.relay_pins[2], GPIO.HIGH)
            self.active[2] = False
            
        if up:
            GPIO.output(self.relay_pins[3], GPIO.LOW)
            self.active[3] = True
        else:
            GPIO.output(self.relay_pins[3], GPIO.HIGH)
            self.active[3] = False
        
        self.log.add("Activity", [time.time, right, left, down, up])
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
    
    def to(self, deviation = (None, None)):
        self.active_deviation = deviation
        
        self.cloud_handling()
        
        if None in self.active_deviation:
            self.activate(False, False, False, False)                
            return
        
        else:
            xdev = self.active_deviation[0]
            ydev = self.active_deviation[1]
            
            if self.sticky_buffer: self.check_sticky(xdev, ydev)
            
            # Activate the pins in the direction of positive deviation, 
            # deactivate everything else
            
            # direction = (Right, Left, Down, Up)
            (right, left, down, up) = (xdev > self.margin,
                                       xdev < self.margin * -1,
                                       ydev > self.margin,
                                       ydev < self.margin * -1)
            
            self.activate(right,left,down,up)
            
        return
    
    def stop(self):
        self.activate()            
        GPIO.cleanup()
        return
  


          