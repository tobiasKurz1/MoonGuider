# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 15:07:41 2024

@author: Tobias Kurz
"""

import configparser
import sys


class configuration:
    def __init__(self, log):
        
        self.log = log
        self.config = configparser.ConfigParser()
        
        try:
            self.config.read('config.ini')
        except:
            raise ValueError("Config File not Found!")
          
        sections = self.config.sections()
        
        if len(sections) > 1:
            print("Multiple Configurations Found:")
            for i in range(len(sections)):
                print(f"{i}: {sections[i]}")
            print(f"{len(sections)}: EXIT")
            while True:
                temp = input("Which Configuration do you want to use? Enter Number: ")
                try:
                    temp = int(temp)
                    self.profile = sections[temp]
                    break
                except:
                    if temp == len(sections): print("Exiting..."), sys.exit()
                    print("Wrong input.")
        else:
            self.profile = sections[0]
        
              
        print(f"Profile '{self.profile}' loaded.")
        
        ### Guider ###
        self.relay_pins       = [int(self.config[self.profile]['pin_right']),
                                 int(self.config[self.profile]['pin_left']),
                                 int(self.config[self.profile]['pin_down']),
                                 int(self.config[self.profile]['pin_up'])]  
        self.button_pin       = int(self.config[self.profile]['button_pin']) 
        self.margin           = float(self.config[self.profile]['margin'])  
        self.sticky_buffer    = int(self.config[self.profile]['sticky_buffer']) 
        if self.config[self.profile]['cloud_mode'] == 'None': self.cloud_mode = None
        else: self.cloud_mode = self.config[self.profile]['cloud_mode']
        self.record_buffer    = int(self.config[self.profile]['record_buffer'])
        self.rotate           = int(self.config[self.profile]['rotate'])
               
        ### Camera ###
        self.image_scale      = float(self.config[self.profile]['image_scale'])
        self.image_size       = (int(int(self.config[self.profile]['image_width']) 
                                         * self.image_scale),
                                 int(int(self.config[self.profile]['image_height']) 
                                         * self.image_scale))
        self.image_buffer     = int(self.config[self.profile]['image_buffer'])
        
        ### Image Processing and Moon Detection ###
        self.threshold        = int(self.config[self.profile]['threshold'])
        self.grey             = eval(self.config[self.profile]['grey'])
        self.blur             = int(self.config[self.profile]['blur'])
        self.param1		      = int(self.config[self.profile]['param1'])
        self.param2		      = int(self.config[self.profile]['param2'])
        self.dp 		      = int(self.config[self.profile]['dp'])
                
        ### General ###
        self.buffer_length   = int(self.config[self.profile]['buffer_length'])
        self.overlay         = eval(self.config[self.profile]['overlay'])
        self.scale           = float(self.config[self.profile]['scale'])
        self.show_cam_feed   = eval(self.config[self.profile]['show_cam_feed'])
        self.do_relay_test   = eval(self.config[self.profile]['do_relay_test'])
        self.export_to_excel = eval(self.config[self.profile]['export_to_excel'])
       
        
        
    def get_config(self):
        temp = []
        temp.append([self.profile, ""])
        for key in self.config[self.profile]:
            temp.append([key, self.config[self.profile][key]])
        return temp
         
    def log_config(self):
        
        self.log.add([self.profile, ""])
        for key in self.config[self.profile]:
            self.log.add("Configuration",[key, self.config[self.profile][key]])




