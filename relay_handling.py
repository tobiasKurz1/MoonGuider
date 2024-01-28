# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 22:41:42 2024

@author: Tobias Kurz
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 21:59:14 2023

@author: Tobias Kurz
"""




import RPi.GPIO as GPIO
import time
import threading
class guide:
    def __init__(self, log, config):

        self.active_deviation = (None, None)
        self.active = [False, False, False, False]
        self.mode_info = None
        self.deviation_records = [(0, 0)]
        self.sbx = []
        self.sby = []

        # Add logging
        self.log = log
        self.log.add('Activity', ["Time", "Duration", "Direction"])

        # Get settings and parameters from config
        self.pulse_multiplier = config.pulse_multiplier
        self.margin = config.margin
        self.button_pin = config.button_pin
        self.record_buffer = config.record_buffer
        rotate = config.rotate
        self.cloud_mode = config.cloud_mode
        # Pin order is RIGHT, LEFT, DOWN, UP ; -RA, +RA, -DEC, +DEC
        relay_pins = config.relay_pins

        # Create a locks for thread synchronization
        self.gpio_lock = threading.Lock()
        self.log_lock = threading.Lock()
        self.active_lock = threading.Lock()
        self.active_deviation_lock = threading.Lock()

        # Create threads for relay activation
        self.activate_thread_ra = threading.Thread(target=self.activate_ra, daemon=True)
        self.activate_thread_dec = threading.Thread(target=self.activate_dec, daemon=True)

        # Rearrange relay pins to compensate for rotated setup
        if rotate == 90:
            self.relay_pins = [relay_pins[3], relay_pins[2], relay_pins[0], relay_pins[1]]
        elif rotate == 180:
            self.relay_pins = [relay_pins[1], relay_pins[0], relay_pins[3], relay_pins[2]]
        elif rotate == 270:
            self.relay_pins = [relay_pins[2], relay_pins[3], relay_pins[1], relay_pins[0]]
        else:
            self.relay_pins = relay_pins
            if rotate != 0:
                raise ValueError("Only camera rotations of 0, 90, 180 or 270 Degree supported.")

        # Errorcheck cloudmode
        if self.cloud_mode not in (None, "repeat", "Repeat"):
            raise ValueError("Cloud mode not correctly specified.")

        # Initialize Raspberry Pi GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for pin in self.relay_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)

        # Pulse every relay once
        for pin in self.relay_pins:
            self.pulse(pin, 1)

    def to(self, deviation=(None, None)):

        # Check if no target is found, deviation is none, therefore cloud mode will take over
        # Using self.active_deviation as basis for relay activation
        if None in deviation:
            self.active_deviation = self.cloud_handling()
        else:
            # Check if contact has been regained after being in repeat mode
            if self.mode_info == "Repeat":
                self.deviation_records = []

            self.mode_info = "Active"
            self.active_deviation = deviation
            self.record(deviation)

        # Start threads for relay activation for each axis if not already active
        if not self.activate_thread_ra.is_alive():
            self.activate_thread_ra = threading.Thread(target=self.activate_ra, daemon=True)
            self.activate_thread_ra.start()
        if not self.activate_thread_dec.is_alive():
            self.activate_thread_dec = threading.Thread(target=self.activate_dec, daemon=True)
            self.activate_thread_dec.start()

        return

    def cloud_handling(self):
        # If cloud mode is set to None, set deviation to 0 to turn off relays
        if self.cloud_mode is None:
            self.mode_info = "Inactive"
            return (0, 0)
        # Repeat previous signals by cycling through recording
        else:
            self.mode_info = "Repeat"
            temp = self.deviation_records[0]
            self.deviation_records.pop(0)
            self.deviation_records.append(temp)
            return temp

        return

    def record(self, deviation):
        self.deviation_records.append(deviation)
        if len(self.deviation_records) > self.record_buffer:
            self.deviation_records.pop(0)
        return

    def activate_ra(self):  # left right
        ad = self.active_deviation
        margin = self.margin

        xdev = ad[0]
        if abs(xdev) <= margin:
            pass
        else:
            (right, left) = (xdev > margin, xdev < margin * -1)

            # calculate pulse time
            temp = (abs(xdev)) * self.pulse_multiplier
            duration = temp if temp < 3 else 3

            with self.active_lock:
                self.active[0] = right
                self.active[1] = left

            direction = 'right' if right else 'left'

            with self.log_lock:
                self.log.add('Activity', [time.time(), duration, direction])

            self.switch_pin_on([right, left, False, False])
            time.sleep(duration)
            self.switch_pin_off([right, left, False, False])
            with self.active_lock:
                self.active[0] = 0
                self.active[1] = 0

    def activate_dec(self):  # up down
        ad = self.active_deviation
        margin = self.margin

        ydev = ad[1]
        if abs(ydev) <= margin:
            pass
        else:
            (down, up) = (ydev > margin, ydev < margin * -1)

            # calculate pulse time
            temp = (abs(ydev)) * self.pulse_multiplier
            duration = temp if temp < 3 else 3

            with self.active_lock:
                self.active[2] = down
                self.active[3] = up

            direction = 'down' if down else 'up'

            with self.log_lock:
                self.log.add('Activity', [time.time(), duration, direction])

            self.switch_pin_on([False, False, down, up])
            time.sleep(duration)
            self.switch_pin_off([False, False, down, up])
            with self.active_lock:
                self.active[2] = 0
                self.active[3] = 0

    def switch_pin_on(self, directions=['Right', 'Left', 'Down', 'Up']):
        with self.gpio_lock:
            for pin, direction in zip(self.relay_pins, directions):
                if direction:
                    GPIO.output(pin, GPIO.LOW)
        return

    def switch_pin_off(self, directions=['Right', 'Left', 'Down', 'Up']):
        with self.gpio_lock:
            for pin, direction in zip(self.relay_pins, directions):
                if direction:
                    GPIO.output(pin, GPIO.HIGH)
        return

    def button_is_pressed(self):
        return GPIO.input(self.button_pin) == GPIO.LOW

    def pulse(self, pin, count=1, uptime=0.1, downtime=0.1):
        for i in range(count):
            GPIO.output(pin, GPIO.LOW)
            time.sleep(uptime)
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(downtime)

        return

    def showactive(self):
        act = []

        if self.active[0]:
            act.append("-RA")
        if self.active[1]:
            act.append("+RA")
        if self.active[2]:
            act.append("-DEC")
        if self.active[3]:
            act.append("+DEC")

        act.append(self.mode_info)

        return(act)

    def stop(self):
        print("Waiting for threads to finish...")
        self.activate_thread_ra.join()
        self.activate_thread_dec.join()

        self.switch_pin_off([True, True, True, True])

        GPIO.cleanup()
        return
