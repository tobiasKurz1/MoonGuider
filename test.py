# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 19:01:12 2023

@author: Tobias Kurz
"""

import RPi.GPIO as GPIO
import time

# Define the GPIO pins for each relay
relay_pins = [17, 18, 22, 27]

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the relay pins as output
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def up(duration=1, pins=relay_pins):
    pin = pins[1]
    GPIO.output(pin, GPIO.LOW)
    time.sleep(duration)
    GPIO.output(pin, GPIO.HIGH) 
    return()

def down(duration=1, pins=relay_pins):
    pin = pins[2]
    GPIO.output(pin, GPIO.LOW)
    time.sleep(duration)
    GPIO.output(pin, GPIO.HIGH) 
    return()

def left(duration=1, pins=relay_pins):
    pin = pins[0]
    GPIO.output(pin, GPIO.LOW)
    time.sleep(duration)
    GPIO.output(pin, GPIO.HIGH)
    return()

def right(duration=1, pins=relay_pins):
    pin = pins[3]
    GPIO.output(pin, GPIO.LOW)
    time.sleep(duration)
    GPIO.output(pin, GPIO.HIGH)
    return()


up()
left()
down()
right()


GPIO.cleanup()






