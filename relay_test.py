# -*- coding: utf-8 -*-
"""
This code is used to test if a connected relay works properly and the wiring is correct
Activate single or multiple relays, then the program exits

Takes some input from the user

Utilizes GPIO and time
"""

import RPi.GPIO as GPIO
import time

# Define the GPIO pins for each relay
relay_pins = [19, 13, 6, 26]

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the relay pins as output and default off
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

# Prompt for the number of iterations, frequency in Hz, and mode (Left, Up, Down, Right)
# If nothing is entered, every possible combination will be tested out
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

    alles = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111',
             '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']
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
