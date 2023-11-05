# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 19:41:05 2023

@author: Tobias Kurz
"""

from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()

camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)
picam2.capture_file("test.jpg")