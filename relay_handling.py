# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 21:59:14 2023

@author: Tobias Kurz
"""
import RPi.GPIO as GPIO
import time

class guide:
    def __init__(self, relay_pins = [27, 17, 22, 18], margin = 0, sticky_buffer = 6):
        
        # Pin order is RIGHT, LEFT, DOWN, UP
        
        self.relay_pins = relay_pins
        self.margin = margin
        self.active = ["","","",""]
        
        self.sticky_buffer = sticky_buffer
        
        self.sbx = []
        self.sby = []
        
        
        
        print(f"Activation Margin set to {margin} px")
        GPIO.setmode(GPIO.BCM)
        
        for pin in self.relay_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
    
    def check_sticky(self, xdev, ydev):
        
        self.sbx.append(abs(xdev))
        self.sby.append(abs(ydev))
                        
        if len(self.sbx) > self.sticky_buffer:
            self.sbx.pop(0)
            self.sby.pop(0)
        
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
                
        return
    
    
    def pulse(self, pin, count = 3):
        for i in range(count):
            GPIO.output(self.relay_pins[pin], GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(self.relay_pins[pin], GPIO.HIGH)
            time.sleep(0.1)
                        
        return
    
    def activate(self, pin):
        try:
            GPIO.output(pin, GPIO.LOW)
            for i in range(len(self.relay_pins)):
                if self.relay_pins[i] == pin:
                    self.active[i] = True
        except:
            raise ValueError(f"Unable to activate relay on pin {pin}")
        return  
    
    def deactivate(self, pin):
        try:
            GPIO.output(pin, GPIO.HIGH)
            for i in range(len(self.relay_pins)):
                if self.relay_pins[i] == pin:
                    self.active[i] = False
        except:
            raise ValueError(f"Unable to deactivate relay on pin {pin}")
        return   

    
    def showactive(self):
        act = []
        
        if self.active[0]:
            act.append("Right")
        if self.active[1]:
            act.append("Left")
        if self.active[3]:
            act.append("Up")
        if self.active[2]:
            act.append("Down")
            
        return(act)
        
    
    def to(self, deviation = (None, None)):
        
        if None in deviation:
            for pin in self.relay_pins:
                GPIO.output(pin, GPIO.HIGH)
            self.active = (False, False, False, False)                
            return
        
        else:
            xdev = deviation[0]
            ydev = deviation[1]
            
            self.check_sticky(xdev, ydev)
            
            # Activate the pins in the direction of positive deviation, 
            # deactivate everything else
            
            # direction = (Right, Left, Down, Up)
            self.active = (xdev > self.margin,
                         xdev < self.margin * -1,
                         ydev > self.margin,
                         ydev < self.margin * -1)
            
            for i in range(len(self.active)):
                if self.active[i] ==  True:
                    GPIO.output(self.relay_pins[i], GPIO.LOW)
                    
                else:
                    GPIO.output(self.relay_pins[i], GPIO.HIGH)
        return
    
    def stop(self):
        for pin in self.relay_pins:
            GPIO.output(pin, GPIO.HIGH)
            
        GPIO.cleanup()
        return
            