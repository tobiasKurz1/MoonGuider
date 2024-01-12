# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 21:08:05 2023

@author: Tobias Kurz

This Python script offers functions for processing the Images taken by the Pi.
This includes preprocessing, detection of the moon and calculating deviations 
from the center. 

Functions:
- preprocessing(img, grey=True, threshold=0, blur=3): Preprocesses images by 
  converting to grayscale, applying threshold, and blurring.
- targetmarkers(target, img, shape): Marks moon position and deviation on the 
  image.
- moonposition(processed_img, param=1): Detects the largest circle 
  (e.g., the moon) in the processed image.
- get_deviation(center, target): Calculates deviation between the center 
  and target.

Ensure OpenCV (cv2) and NumPy are installed.

"""

import cv2 as cv
import numpy as np
import time
import pandas as pd

class calculation:
    def __init__(self, config):
        self.grey = config.grey
        self.blur = config.blur
        self.threshold = config.threshold
        self.overlay = config.overlay
        self.input_scale = config.input_scale
        self.dp = config.dp
        self.param1 = config.param1
        self.param2 = config.param2
        self.in_scale = config.in_scale
        
        self.minRadius = 120
        self.maxRadius = 160
        


    def calculate_text_size(text, font, font_scale, thickness):
        return cv.getTextSize(text, font, font_scale, thickness)[0]
    
    def adjust_font_size(self, text, font, target_height, target_width, thickness, max_font_scale=5):
        current_font_scale = max_font_scale
        lines = text.split('\n')
    
        while current_font_scale > 0.1:
            text_size = self.calculate_text_size(text, font, current_font_scale, 2)
            total_text_height = text_size[1] * len(lines)
            max_width = max(self.calculate_text_size(line, font, current_font_scale, thickness)[0] for line in lines)
            if total_text_height <= target_height and max_width  <= target_width:
                return current_font_scale
            else:
                current_font_scale -= 0.1
        return current_font_scale
    
    def preprocessing(self, img):

        # Turn image into grey version (1 channel)
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) if self.grey else img
        
        # Define Threshold value for brightest object
        th = self.threshold * np.min(img) if self.threshold else None
            
        # Remove unwanted stars or craters with threshold
        (_, img) = cv.threshold(img, int(th), 255, 0) if self.threshold else (None, img)
            
        # Blur to remove noise
        img = cv.blur(img,(int(self.blur), int(self.blur))) if self.blur else img
        
        return(img)
    
    def targetmarkers(self,
                      target_x, 
                      target_y, 
                      target_radius, 
                      ref_x, 
                      ref_y, 
                      deviation, 
                      img, 
                      handover_value):
        
                
        if len(img.shape) == 2:
            img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    
        img = cv.resize(img, None, fx=self.out_scale, fy=self.out_scale, interpolation= cv.INTER_LINEAR)
        
        if img.shape[2] == 4:
            # Split the image into its channels
            channels = cv.split(img)
    
            # Keep only the first three channels (RGB)
            img = cv.merge(channels[:3])
            
        (height, width) = img.shape[0:2]
        line_color = (0, 0, 255)  # Red in BGR format
        
        # Define the thickness of the lines
        line_thickness = int(8 * self.out_scale) if int(8 * self.out_scale) >= 1 else 1
        
        if None in deviation: # No target is tracked
            
            cv.line(img, (0, 0), (width, height), line_color, line_thickness)
            cv.line(img, (0, height), (width, 0), line_color, line_thickness)
            
            cv.circle(img, (width // 2, height // 2), 
                      int(self.minRadius * self.out_scale), 
                      line_color, line_thickness)
            cv.circle(img, (width // 2, height // 2), 
                      int(self.maxRadius * self.out_scale), 
                      line_color, line_thickness)
            
        elif None in (target_x, target_y): 
            
            # Target is not found but deviation is generated through prediction
            # or last deviation
            scl_devx = int(deviation[0] * self.out_scale)
            scl_devy = int(deviation[1] * self.out_scale)
            try:
                scl_ref_x = int(ref_x * self.out_scale)
                scl_ref_y = int(ref_y * self.out_scale)
                
                # Draw deviation Arrow
                cv.arrowedLine(img, (scl_ref_x, scl_ref_y), 
                               (scl_ref_x + scl_devx, scl_ref_y + scl_devy), 
                               (0, 0, 255), 
                               line_thickness, 
                               tipLength=0.2)
            except: pass
        
        else:   # Both target and deviation are valid
        
            print(f"Target at unscaled Coordinates: {target_x}, {target_y}")
                  
            scl_target_x = int(target_x * self.out_scale)
            scl_target_y = int(target_y * self.out_scale)
            scl_target_radius = int(target_radius * self.out_scale)
            scl_ref_x = int(ref_x * self.out_scale)
            scl_ref_y =int(ref_y * self.out_scale)
            
            # Draw reference Point
            cv.line(img, (0, scl_ref_y), (width, scl_ref_y), line_color, line_thickness * 2)
            cv.line(img, (scl_ref_x, 0), (scl_ref_x, height), line_color, line_thickness * 2)
            
            # Draw deviation Arrow
            cv.arrowedLine(img, 
                           (scl_ref_x, scl_ref_y), 
                           (scl_target_x, scl_target_y), 
                           (0, 255, 0), 
                           line_thickness, 
                           tipLength=0.2)
        
            # Draw horizontal line
            cv.line(img, 
                    (scl_target_x - scl_target_radius, scl_target_y), 
                    (scl_target_x + scl_target_radius, scl_target_y), 
                    line_color, 
                    line_thickness)
        
            # Draw vertical line
            cv.line(img, 
                    (scl_target_x, scl_target_y - scl_target_radius), 
                    (scl_target_x, scl_target_y + scl_target_radius), 
                    line_color, 
                    line_thickness)
            
            #Draw the circle
            cv.circle(img, 
                      (scl_target_x, scl_target_y), 
                      scl_target_radius, 
                      line_color, 
                      line_thickness)
        
        if self.overlay:
            
            if None not in deviation:
                deviation = (f"{deviation[0]:.2f}", f"{deviation[1]:.2f}")
                
            if None not in (target_x, target_y):
                target_x = f"{target_x:.2f}"
                target_y = f"{target_y:.2f}"
            
            bar_text = f"Target at {target_x}, {target_y}; Deviation: {deviation[0]}, {deviation[1]};\n{handover_value}"
            
            # Define the height of the black bar (you can adjust this value)
            bar_height = int(height * 0.2)
        
            # Create a black bar
         
            bar = np.ones((bar_height, width, 3), dtype=np.uint8) * 255
        
            # Add the text to the black bar
            font = cv.FONT_HERSHEY_SIMPLEX      
            
            text_lines = bar_text.split('\n')
            max_font_scale = 10
            thickness = line_thickness
            
            # Adjust the font size to fit within the bar
            font_scale = self.adjust_font_size(bar_text, 
                                          font, 
                                          bar_height,
                                          width, 
                                          thickness, 
                                          max_font_scale)
    
            # Calculate starting position for the first line
            y_position = (bar_height - self.calculate_text_size(text_lines[0], font, font_scale, thickness)[1] 
                          * len(text_lines)) // 2
            print(f'y-position: {y_position}')
            print(f'font_scale: {font_scale}')
            # Draw each line of text
            for line in text_lines:
                text_position = ((width - self.calculate_text_size(line, font, font_scale, 2)[0]) // 2, y_position)
                cv.putText(bar, line, text_position, font, font_scale, (0, 0, 0), thickness, cv.LINE_AA)
                y_position += self.calculate_text_size(line, font, font_scale, thickness)[1]
    
    
         
            # Stack the black bar on top of the original image
            # If Moon would be under the bar at the bottom, put bar on top
            if target_x is None or deviation[0] is None:
                img[height-bar_height:height, 0:width] = bar         
            elif (scl_target_y + scl_target_radius) > (height - bar_height):
                    img[0:bar_height, 0:width] = bar   
            else:
                img[height-bar_height:height, 0:width]= bar 
            
            
        return(img)
    
    def moonposition(self, processed_img):
        
        circles = cv.HoughCircles(
            processed_img,       # Input image
            cv.HOUGH_GRADIENT,   # Detection method
            dp=self.dp,                # Inverse ratio of the accumulator resolution to the image resolution
            minDist=processed_img.shape[0],          # Minimum distance between detected centers
            param1 = self.param1,          # Higher threshold for edge detection
            param2 = self.param2,           # Accumulator threshold for circle detection
            minRadius = int(self.minRadius * self.in_scale) ,        # Minimum circle radius 120
            maxRadius= int(self.maxRadius * self.in_scale)        # Maximum circle radius 160
        )
    
        if circles is not None:
            circles = np.uint16(np.around(circles))
            
            circle = max(circles[0], key=lambda x: x[2]) #Filter out the biggest circle (moon)
            
            (center_x, center_y) = (circle[0], circle[1])
            radius = circle[2]
    
            num_circles = len(circles[0])
            print(f"Number of circles detected: {num_circles}. Marked largest radius.")
            return(center_x, center_y ,radius)
            
        else: 
            return(None,None,None)  
    
    def get_deviation(target, ref):
        if None in ref or None in target:
            return (None, None)
        
        else:    
            target = (float(target[0]), float(target[1]))
            dev = (target[0] - ref[0], target[1] - ref[1])
    
            return dev

class log:
    def __init__(self):
        self.sheets = {}
        
        self.sheets["Target"] = []
        self.sheets["Activity"] = []
        self.sheets["Configuration"] = []
        
    def add(self, sheetname, data):
        if sheetname not in self.sheets:
                raise ValueError(f"Sheet {sheetname} does not exist.")
        else: self.sheets[sheetname].append(data)
        return
            
    def get(self, sheetname):
        if sheetname not in self.sheets:
                raise ValueError(f"Sheet {sheetname} does not exist.")
        else: return self.sheets[sheetname]
            
    def export(self):
        filename = "log_" + time.strftime('%y-%m-%d_%H-%M', time.localtime())
        
        print(f"Nr. of Datapoints: {len(self.sheets['Target'])-1}")
        print(f"Config Profile: {self.sheets['Configuration'][0][0]}")
        temp = input("Save Logged data as ...? Press Enter for default 'log_Y-M-D_H-M.xlsx', type 'n' or 'no' to skip. ")
        if temp: 
            if temp in ["N","n","No","NO","nein","Nein","NEIN"]:
                print("Data has not been saved")
                return
            filename = temp
            
        note = input("Add a Note. Press enter when done.\n")
        
       
        self.sheets['Configuration'].append([f'{time.ctime()}',""])
        self.sheets['Configuration'].append(["NOTE", note + ""])    
        
        
        df1 = pd.DataFrame(self.sheets["Target"])
        df2 = pd.DataFrame(self.sheets["Activity"])
        df3 = pd.DataFrame(self.sheets["Configuration"])
 
        
        with pd.ExcelWriter(f"Logs/{filename}.xlsx", engine='openpyxl') as writer:
            df1.to_excel(writer, sheet_name='Target', index=False, header=False)
            df2.to_excel(writer, sheet_name='Activity', index=False, header=False)
            df3.to_excel(writer, sheet_name='Configuration', index=False, header=False)  
        print(f"Exported to Excelfile '{filename}.xlsx'")

    
class buffer:
    def __init__(self, buffer_length = 1):
        self.values = {}
        self.values['target_x'] = []
        self.values['target_y'] = []
        self.values['target_radius'] = []
        
        self.buffer_length = buffer_length


    def errorcheck(self, name = None):
        if name not in self.values:
                raise ValueError(f"Target '{name}' does not exist in the buffer.")
            
    def get_valid(self, name = "target_x"):
        temp = 0
        
        
        if name is not None:
            self.errorcheck(name)
            temp = len([value for value in self.values[name] if value is not None])
        
        return f"{temp} of {self.buffer_length}"
                
        
    def add(self, value, name=None):

        self.errorcheck(name)
                
        self.values[name].append(value)
                        
        if self.buffer_length is not None and len(self.values[name]) > self.buffer_length:
                self.values[name].pop(0)
                
    def average(self, name):
        
        self.errorcheck(name)
                 
        if not self.values[name]:
            return None
        temp =  list(filter(lambda x: x is not None, self.values[name]))
        
        return float(sum(temp) / len(temp)) if temp else None

