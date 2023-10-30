# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 19:01:12 2023

@author: Tobias Kurz
"""

def up(duration):
    # commands
    
    return

def down(duration):
    # commands
    
    return

def left(duration):
    # commands
    
    return

def right(duration):
    # commands
    
    return

import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for each relay
relay_pins = [17, 18, 22, 27]  # Example GPIO pins, adjust as per your wiring





# Set the relay pins as output
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)

try:
   
    # Turn on each relay for 1 second and then turn it off
    for pin in relay_pins:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(1)
except:
    pass

