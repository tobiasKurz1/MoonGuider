# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 19:41:05 2023

@author: Tobias Kurz
"""

from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()

picam2.start_and_capture_file("test.jpg")