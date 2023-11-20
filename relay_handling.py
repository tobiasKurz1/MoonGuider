# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 21:59:14 2023

@author: Tobias Kurz
"""
import RPi.GPIO as GPIO

class guide:
    def __init__(self, relay_pins = [27, 17, 22, 18]):
        self.relay_pins = relay_pins
        GPIO.setmode(GPIO.BCM)
        
        for pin in self.relay_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
        
    def to(self, deviation = (None, None)):
        
        if None in deviation:
            return
        
        else:
            xdev = deviation[0]
            ydev = deviation[1]
            # Activate the pins in the direction of positive deviation, 
            # deactivate everything else
            
            # direction = (Right, Left, Down, Up)
            direction = (xdev > 0,
                         xdev < 0,
                         ydev > 0,
                         ydev < 0)
            
            for i in range(len(direction)):
                if direction[i] ==  True:
                    GPIO.output(self.relay_pins[i], GPIO.LOW)
                    print("RLDU Relay {i} activated")
                else:
                    GPIO.output(self.relay_pins[i], GPIO.HIGH)
                    print("RLDU Relay {i} deactivated")
        
        return