# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 22:51:37 2023

@author: Tobias Kurz
"""

from picamera2 import Picamera2
import time


def initialize():
    picam = Picamera2()
    #config = picam.create_still_configuration()
    #picam.configure(config)
    
    picam.start()
    
    time.sleep(1)
    
    return(picam)


    