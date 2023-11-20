# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 19:01:12 2023

@author: Tobias Kurz
"""

import RPi.GPIO as GPIO
import time

# Define the GPIO pins for each relay
relay_pins = [27, 17, 22, 18]

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the relay pins as output and default off
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def up(duration=1, pins=relay_pins):
    """
    Activate relay for specified duration.

    :param duration: Duration in seconds to keep the relay activated (default: 1)
    :param pins: List of relay pins (default: relay_pins)
    """
    pin = pins[1]  # Get correct relay pin from provided list
    GPIO.output(pin, GPIO.LOW)  # Activate relay
    time.sleep(duration)  # Wait for specified duration
    GPIO.output(pin, GPIO.HIGH)  # Deactivate relay
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


# Prompt for the number of iterations, frequency in Hz, and mode (Left, Up, Down, Right)
iterations = input("Iterations (press enter for general test): ")

if iterations:
    iterations = int(iterations)
    fz = 1 / float(input("Frequency in Hz: "))
    mode = input("Mode (RLDU): ")
    
    # Convert input to list of characters
    on = [char for char in mode]
    
    # Loop for the specified number of iterations
    for i in range(iterations):
        print(i + 1)  # Print the current iteration number
    
        # Activate the specified relays based on the mode
        for i in range(len(on)):
            if int(on[i]) == 1:
                GPIO.output(relay_pins[i], GPIO.LOW)
    
        # Pause for the specified time (frequency)
        time.sleep(fz / 2)
    
        # Deactivate the relays based on the mode
        for i in range(len(on)):
            if int(on[i]) == 1:
                GPIO.output(relay_pins[i], GPIO.HIGH)
    
        # Pause for the specified time (frequency)
        time.sleep(fz / 2)
    
    
        
    
else:

    # Try every possible combination of activations. Press Enter in between.
    
    alles = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']
    print("Testing every possible combination...")
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


GPIO.cleanup()






