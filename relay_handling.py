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
    
    def setup(self):
        print("Setting up the Movement of the Guider")
        print("The program will now go through every direction.")
        print("Please input the number of the correspinding direction:")
        print("1 -> Right\n2 -> Left\n3 -> Up\n4 -> Down")
        new_pins = []
        
        for pin in self.relay_pins:
            GPIO.output(pin, GPIO.LOW)   
            temp = input("Moving...? ")
            GPIO.output(pin, GPIO.HIGH)
            print(f"Relay Pin {self.relay_pins[0]} set do direction {temp}")
            new_pins.append(int(temp))
        
        self.relay_pins = new_pins
        print("New Order of relay Pins is now: {new_pins}")
        
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
            