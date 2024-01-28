# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 22:44:20 2023

@author: Tobias Kurz

This Python script serves as the main file that integrates functions
from 'calc' and 'cam_feed' to capture and process images from the camera using
the 'picamera2' library. It calculates the deviation of a celestial target
(e.g., the moon) from the center of the image and visually marks the target's
position and deviation on the camera feed.

Key Components:
- Initializes the camera and sets up the camera feed.
- Captures images and performs preprocessing using the 'calc' module.
- Calculates the target's position and deviation.
- Displays the camera feed with target markings.

Ensure 'picamera2', 'cv2' (OpenCV), 'calc', and 'cam_feed' modules are
available to run this script.
"""

import calc
import cv2 as cv
from picamera2 import Picamera2
import time
import relay_handling as relay
import config_loader as load


# Initialize outside classes
log = calc.log()
config = load.configuration(log)
clc = calc.calculation(config)

# Set header for data logging
log.add('Target', ["Time", "target_x", "target_y", "target_x_average", "target_y_average",
                   "x_deviation", " y_deviation"])


duration = 1
start_press = 0
error_accumulator = 0
error_limit = 5
avrg_target_x = None
avrg_target_y = None


buffer = calc.buffer(config.buffer_length)

guide = relay.guide(log, config)


def perform_relay_test():
    deviations = []

    while True:
        cv.namedWindow('Camera Output', cv.WINDOW_NORMAL)
        cv.setWindowProperty(
            'Camera Output', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

        org_image = picam.capture_array()
        processed = clc.preprocessing(org_image)

        (target_x, target_y, _) = clc.moonposition(processed)

        marked = clc.targetmarkers(
            target_x,
            target_y,
            _,
            target_x,
            target_y,
            (0, 0),
            org_image,
            "Press any key to skip relay test.\nPress Button if correct Target is found."
        )

        cv.imshow('Camera Output', marked)
        key = cv.waitKey(1)

        if key != -1:
            return

        if guide.button_is_pressed():
            cv.destroyAllWindows()
            print("Relay Testing in Progress...\nThis will take 40s")
            time.sleep(1)
            break

    org_image = picam.capture_array()
    processed = clc.preprocessing(org_image)

    (target_x, target_y, _) = clc.moonposition(processed)

    for pin, direction in zip(guide.relay_pins, ["right", "left", "down", "up"]):
        org_image = picam.capture_array()
        processed = clc.preprocessing(org_image)

        (target_x, target_y, _) = clc.moonposition(processed)

        print(f"Testing pin {pin} ({direction})...")

        guide.pulse(pin, 5, 2, 0.2)

        org_image = picam.capture_array()
        processed = clc.preprocessing(org_image)
        (x, y, _) = clc.moonposition(processed)
        deviation = clc.get_deviation((x, y), (target_x, target_y))
        deviations.append(deviation)
        print(f"Detected deviation: {deviation}")

    print("\nPress Button to continue")
    while True:
        if guide.button_is_pressed():
            break

    return


def lock_moon_size():
    handover_value = "Press any key to skip.\nPress Button to lock current moon size"

    while True:
        cv.namedWindow('Camera Output', cv.WINDOW_NORMAL)
        cv.setWindowProperty(
            'Camera Output', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

        org_image = picam.capture_array()
        processed = clc.preprocessing(org_image)

        (target_x, target_y, target_radius) = clc.moonposition(processed)

        marked = clc.targetmarkers(
            target_x,
            target_y,
            target_radius,
            target_x,
            target_y,
            (0, 0),
            org_image,
            handover_value
        )

        handover_value = "Press any key to skip.\nPress Button to lock current moon size"
        cv.imshow('Camera Output', marked)
        key = cv.waitKey(1)
        if key != -1:
            return

        if guide.button_is_pressed():
            if target_radius:
                start = time.time()
                while time.time() < start + 5:
                    cv.namedWindow('Camera Output', cv.WINDOW_NORMAL)
                    cv.setWindowProperty(
                        'Camera Output', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
                    time_left = start + 5 - time.time()
                    marked = clc.targetmarkers(
                        target_x,
                        target_y,
                        target_radius,
                        target_x,
                        target_y,
                        (0, 0),
                        org_image,
                        f"Lock radius at {target_radius} pixels? Press Button\n{time_left:.2f}"
                    )
                    cv.imshow('Camera Output', marked)
                    key = cv.waitKey(1)
                    if key != -1:
                        return
                    if guide.button_is_pressed() and time_left < 4:
                        clc.minRadius = target_radius - 10
                        clc.maxRadius = target_radius + 10
                        print(f"Radius locked at {target_radius} +- 10 pixels")
                        return
            else:
                handover_value = "Target not found, try again."

    return


def setup(picam):

    config = picam.create_video_configuration()
    picam.configure(config)

    picam.start()

    time.sleep(1)

    print("Set camera in right Position and press any key when ready")

    testimg = picam.capture_array()
    shape = testimg.shape

    print(f'Shape: {shape}')

    while True:
        cv.namedWindow('Camera Feed', cv.WINDOW_NORMAL)
        cv.setWindowProperty(
            'Camera Feed', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        img = picam.capture_array()

        cv.imshow('Camera Feed', img)

        key = cv.waitKey(1)

        if key != -1 or guide.button_is_pressed():
            cv.destroyWindow('Camera Feed')
            picam.stop()

            return


picam = Picamera2()

if config.show_cam_feed:
    setup(picam)

camera_config = picam.create_video_configuration(
    main={'format': 'RGB888', "size": config.image_size},
    buffer_count=config.image_buffer,
)

picam.configure(camera_config)

picam.start()

testimg = picam.capture_array()
shape = testimg.shape

if config.do_relay_test:
    perform_relay_test()

lock_moon_size()


# Center Point of the Image in (X,Y) Coordinates
image_center = (int(shape[1]//2), int(shape[0]//2))

(reference_x, reference_y) = image_center

start_time = time.time()

# MAIN CAPTURE LOOP:
while True:
    cv.namedWindow('Camera Output', cv.WINDOW_NORMAL)
    cv.setWindowProperty(
        'Camera Output', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

    start_frame = time.time()

    org_image = picam.capture_array()

    processed = clc.preprocessing(org_image)

    (target_x, target_y, target_radius) = clc.moonposition(processed)

    # Check for deviation between target positions of more than 100 pixels
    # If so, an improper target is assumed
    dev_to_last = clc.get_deviation(
        (target_x, target_y), (avrg_target_x, avrg_target_y))
    if None not in dev_to_last:
        if max(dev_to_last) > 100:
            (target_x, target_y, target_radius) = (None, None, None)

    # Check for failed target acquisition and clear averaging buffer when
    # Target is not acquired three times in a row
    if None in (target_x, target_y, target_radius):
        error_accumulator += 1
        if error_accumulator >= error_limit:
            error_accumulator = error_limit
            buffer.clear_all()
    else:
        error_accumulator = 0

    # Add targets to buffer for averaging
    buffer.add(target_x, "target_x")
    buffer.add(target_y, "target_y")
    buffer.add(target_radius, "target_radius")

    # Save Current average target for 100 pixel deviation check in next iteration
    avrg_target_x = buffer.average("target_x")
    avrg_target_y = buffer.average("target_y")

    # Calculate Moon deviation from desired location
    deviation = clc.get_deviation((avrg_target_x, avrg_target_y), (reference_x, reference_y))

    # Add telemetry to log for analysis and later export
    log.add("Target", [time.time(), target_x, target_y, avrg_target_x, avrg_target_y,
                       deviation[0], deviation[1]])

    # Compute guiding signal from deviation
    guide.to(deviation)
    relay_info = guide.showactive()
    # Join info text for display
    infotext = (
        f"{1/duration:.2f} FpS, Active Relays: {relay_info[0:-1]}, Mode: {relay_info[-1]}\n"
        f"Buffer: {buffer.get_valid()}, EA: {error_accumulator}/{error_limit},"
        f"Runtime: {int(time.time()-start_time)} s")

    # Generate output image with target markings and information
    marked = clc.targetmarkers(
        avrg_target_x,
        avrg_target_y,
        buffer.average("target_radius"),
        reference_x,
        reference_y,
        guide.active_deviation,
        org_image,
        infotext
    )

    # Show generated image
    cv.imshow('Camera Output', marked)

    # Routine for setting reference point with button press
    if guide.button_is_pressed():
        # Set current target position as reference
        if None not in (avrg_target_x, avrg_target_y):
            (reference_x, reference_y) = (avrg_target_x, avrg_target_y)
            buffer.clear_all()
        # Begin timer to check for long press
        if start_press == 0:
            start_press = time.time()
        # Handle longer button press
        else:
            duration_press = time.time()-start_press
            # Over 2 seconds: set center as reference point
            if duration_press > 2 and duration_press < 5:
                (reference_x, reference_y) = image_center
                buffer.clear_all()
            # 5 second press terminates the guider
            elif duration_press >= 5:
                break
    else:
        start_press = 0

    end_frame = time.time()

    duration = end_frame - start_frame

    key = cv.waitKey(1)

    if key != -1:
        break

    # if time.time()-start_time > 60 * 5 : #nach 5 min abbrechen ####################################################### test
    #    break

cv.destroyAllWindows()
guide.stop()
print("Guider stopped.")

# Export to Excel
if config.export_to_excel:
    log.export()
