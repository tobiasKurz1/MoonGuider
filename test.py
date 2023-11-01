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




iterations = int(input("Iterations "))
fz = 1/int(input("Frequency in Hz "))
mode = str(input("Mode LUDR "))

on = [char for char in mode]

for i in range(iterations):
    print(i+1)
    for i in range(len(on)):
        if int(on[i]) == 1:
            GPIO.output(relay_pins[i], GPIO.LOW)   
    time.sleep(fz)
    for i in range(len(on)):
        if int(on[i]) == 1:
            GPIO.output(relay_pins[i], GPIO.HIGH)  
    time.sleep(fz)
    

"""
alles = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']
print("LUDR")
for test in alles:
    print(test)
    on = [char for char in test]
    try:
               
        for i in range(len(on)):
            if int(on[i]) == 1:
                GPIO.output(relay_pins[i], GPIO.LOW)   
        input()
        for i in range(len(on)):
            if int(on[i]) == 1:
                GPIO.output(relay_pins[i], GPIO.HIGH)       
        input()
    except:
        break
"""

GPIO.cleanup()






