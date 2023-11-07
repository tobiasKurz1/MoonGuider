# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 22:44:20 2023

@author: Tobias Kurz
"""
import os
import cv2 as cv
import numpy as np
import dataloader as dl
from main import preprocessing, moonposition, get_deviation, targetmarkers



    

folder = r"D:\Dropbox\_UNI\3. Semester\Semesterarbeit\MoonGuider\Testpictures"

image_files = [f for f in os.listdir(folder) if f.endswith(('.jpg', '.png'))]

image_center = (image_files[0].shape[0]//2, image_files[0].shape[1]//2) #Center Point of the Image in (X,Y) Coordinates

for filename in image_files:
    
    print(f"\n### {filename} ###")
    
    image = cv.imread(os.path.join(folder, filename)) #get image file into python
    
    processed = preprocessing(image)
    
    target = moonposition(processed)
    
    deviation = get_deviation(image_center, target)
    print(f"Deviation: {deviation}")
    
    final = targetmarkers(target, image)
    #cv.imshow(f'Final Target with center at {target[0]}',final)
    dl.save_image(final, 'Final', 'Output')
    
        
                
        
    try:
        dl.output_images_in_grid('Output', 0.5)
        
    except:
        break
        
# cv.waitKey(0)
# cv.destroyAllWindows()
