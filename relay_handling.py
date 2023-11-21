# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 21:59:14 2023

@author: Tobias Kurz
"""
import RPi.GPIO as GPIO

class guide:
    def __init__(self, relay_pins = [27, 17, 22, 18], margin = 0):
        self.relay_pins = relay_pins
        self.margin = margin
        self.active = ["","","",""]
        
        print(f"Activation Margin set to {margin} px")
        GPIO.setmode(GPIO.BCM)
        
        for pin in self.relay_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
    
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
        if self.active[2]:
            act.append("Up")
        if self.active[3]:
            act.append("Down")
            
        return(act)
        
    
    def to(self, deviation = (None, None)):
        
        if None in deviation:
            return
        
        else:
            xdev = deviation[0]
            ydev = deviation[1]
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
            