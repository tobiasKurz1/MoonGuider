# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 22:44:20 2023

@author: Tobias Kurz

This Python script processes a series of images stored in 'Testpictures' to test
parameters for the live capture.

Key Components:
- Preprocesses images
- Calculates the target's position and deviation from the center
- Displays a grid of processed images with labels for comparison.
- Allows the user to interactively change threshold, blur, and parameter values 
  during image processing. Repeats image if parameters are changed.


"""

#WIIIIILLLLDDDD

import os
import cv2 as cv
import numpy as np
import calc as clc
import time


folder = r"Testpictures"

def preprocessing(img, grey = True, threshold = 0, blur = 3):
    
        
    # Turn image into grey version (1 channel)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) if grey else img
    
    save_image(img, "1_Grey")
    
    
    print(f'Min Value: {np.min(img)}')
    print(f'Max Value: {np.max(img)}')
    
    # Define Threshold value for brightest object
    th = threshold if threshold else None
        
    # Remove unwanted stars or craters with threshold
    (_, img) = cv.threshold(img, int(th), 255, 0) if threshold else (None, img)
        
    save_image(img, "2_Threshold")
    
    # Blur to remove noise
    img = cv.blur(img,(int(blur), int(blur))) if blur else img
    
    save_image(img, "3_Blur")
    
    return(img)

def save_image(image, filename, folder = "Output"):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Define the file path
    file_path = os.path.join(folder, filename + ".jpg")

    # Save the image to the specified path
    cv.imwrite(file_path, image)
    
def output_images_in_grid(folder, scale_factor=1.0):
    # Get a list of image filenames in the folder
    image_files = [f for f in os.listdir(folder) if f.endswith(('.jpg', '.png'))]

    if not image_files:
        print("No image files found in the folder.")
        return

    # Load the images into an array and get the dimensions of the first image
    first_image = cv.imread(os.path.join(folder, image_files[0]))
    cell_height, cell_width, _ = first_image.shape

    # Define the grid dimensions (2x2 square)
    num_images = len(image_files)
    num_cols = 2
    num_rows = 2

    if num_images < 4:
        print("Insufficient images to create a 2x2 grid.")
        return

    # Calculate the size of the grid
    grid_height = int(cell_height * num_rows * scale_factor)
    grid_width = int(cell_width * num_cols * scale_factor)

    # Create an empty canvas for the grid
    grid = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)

    # Arrange images in the grid (2x2 square) with the specified scaling
    for i in range(4):
        y_start = int((i // num_cols) * cell_height * scale_factor)
        y_end = int(y_start + cell_height * scale_factor)
        x_start = int((i % num_cols) * cell_width * scale_factor)
        x_end = int(x_start + cell_width * scale_factor)
        image = cv.imread(os.path.join(folder, image_files[i]))
        image = cv.resize(image, (x_end - x_start, y_end - y_start))
        grid[y_start:y_end, x_start:x_end] = image

        # Draw the file name as a label on the image
        label = os.path.splitext(image_files[i])[0]  # Extract the file name without extension
        cv.putText(grid, label, (x_start + 10, y_end - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display the grid
    cv.imshow('Output', grid)
    cv.waitKey(0)

    
    return

    


threshold = 0
blur= 3

param = 1


image_files = [f for f in os.listdir(folder) if f.endswith(('.jpg', '.png'))]

first_img = cv.imread(os.path.join(folder, image_files[0]))

# Center Point of the Image in (X,Y) Coordinates for initialization
prev_center = (int(first_img.shape[0]//2), int(first_img.shape[1]//2))

i = 0
while i < len(image_files): 
    
    print(f"\n### {image_files[i]} ###")
    
    # get image file into python
    image = cv.imread(os.path.join(folder, image_files[i])) 
        
    processed = preprocessing(image, threshold = threshold, blur = blur)
    
    target = clc.moonposition(processed, param)
       
    # sammeln der kommandos, nicht der position
    #motion_buffer.append((time.time(),target))
    
    deviation = clc.get_deviation(prev_center, target)
    print(f"Deviation from previous: {deviation}")
    
    final = clc.targetmarkers(target,prev_center, image, processed.shape)
    
    prev_center = target[0:2]
    #cv.imshow(f'Final Target with center at {target[0]}',final)
    save_image(final, 'Final')
    
        
    try:
        output_images_in_grid('Output', 0.1)
        """ change = 0
        temp = input(f"Change Threshold from {threshold}?: ")
        if temp: 
            threshold = float(temp)
            change = 1
        temp = input(f"Change Blur from {blur}?: ")   
        if temp: 
            blur = int(temp)
            change = 1
        temp = input(f"Change Param from {param}?: ")   
        if temp: 
            param = int(temp)
            change = 1
        
        if not(change):
            i = i+1      
        """
        i = i+1
    except:
        cv.destroyAllWindows()
        break
cv.destroyAllWindows()
# cv.waitKey(0)
# cv.destroyAllWindows()
