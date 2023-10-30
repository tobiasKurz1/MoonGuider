# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 23:22:15 2023

@author: Tobias Kurz
"""

import cv2 as cv
import numpy as np
import os

folder = r"D:\Dropbox\_UNI\3. Semester\Semesterarbeit\Mondbilder\testset"

filename = "00.jpg"



img = cv.imread(os.path.join(folder, filename)) #get image file into python

cv.imshow(f'Before Size:{img.shape}',img)

original = img

img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.imshow('Gray',img)


img = cv.Canny(img, np.min(img), np.max(img))

cv.imshow("Canny", img)


blur = cv.blur(img,(8,8))

cv.imshow(f'Blurred Size:{blur.shape}',blur)


cv.waitKey(0)
cv.destroyAllWindows()