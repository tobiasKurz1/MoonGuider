# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 21:59:14 2023

@author: Tobias Kurz
"""
import RPi.GPIO as GPIO

class guide:
    def __init__(self, relay_pins = [17, 18, 22, 27]):
        self.relay_pins = relay_pins
        GPIO.setmode(GPIO.BCM)
        
        for pin in self.relay_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
        
    def to(self, deviation= (None, None)):
        if None in self.deviation:
            return
        
        else:
            #Activate the pins in the 
            pass
        
        return