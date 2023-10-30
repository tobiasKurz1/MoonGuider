# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 00:02:38 2023

@author: Tobias Kurz
"""

import os
import cv2 as cv
import numpy as np

def save_image(image, filename, folder):
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
        cv.putText(grid, label, (x_start + 10, y_end - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the grid
    cv.imshow('Output', grid)
    cv.waitKey(0)
    cv.destroyAllWindows()
