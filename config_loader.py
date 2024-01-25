# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 15:07:41 2024

@author: Tobias Kurz
"""

import configparser
import sys


class configuration:
    def __init__(self, log):
        
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
        self.relay_pins       = [int(self.config[self.profile]['pin_ra_down']),
                                 int(self.config[self.profile]['pin_ra_up']),
                                 int(self.config[self.profile]['pin_dec_down']),
                                 int(self.config[self.profile]['pin_dec_up'])]  
        self.button_pin       = int(self.config[self.profile]['button_pin']) 
        self.margin           = float(self.config[self.profile]['margin']) 
        self.pulse_multiplier = float(self.config[self.profile]['pulse_multiplier'])
        self.sticky_buffer    = int(self.config[self.profile]['sticky_buffer']) 
        if self.config[self.profile]['cloud_mode'] == 'None': self.cloud_mode = None
        else: self.cloud_mode = self.config[self.profile]['cloud_mode']
        self.record_buffer    = int(self.config[self.profile]['record_buffer'])
        self.rotate           = int(self.config[self.profile]['rotate'])
               
        ### Camera ###
        self.in_scale         = float(self.config[self.profile]['in_scale'])
        self.image_size       = (int(int(self.config[self.profile]['image_width']) 
                                         * self.in_scale),
                                 int(int(self.config[self.profile]['image_height']) 
                                         * self.in_scale))
        self.image_buffer     = int(self.config[self.profile]['image_buffer'])
        
        ### Image Processing and Moon Detection ###
        
        self.blur             = int(self.config[self.profile]['blur'])
        self.param1		      = int(self.config[self.profile]['param1'])
        self.param2		      = int(self.config[self.profile]['param2'])
        self.dp 		      = int(self.config[self.profile]['dp'])
                
        ### General ###
        self.buffer_length   = int(self.config[self.profile]['buffer_length'])
        self.overlay         = eval(self.config[self.profile]['overlay'])
        self.out_scale       = float(self.config[self.profile]['out_scale'])
        self.show_cam_feed   = eval(self.config[self.profile]['show_cam_feed'])
        self.do_relay_test   = eval(self.config[self.profile]['do_relay_test'])
        self.export_to_excel = eval(self.config[self.profile]['export_to_excel'])
       
        # Log Config to excel
        log.add("Configuration", [self.profile, ""])
        for key in self.config[self.profile]:
            log.add("Configuration",[key, self.config[self.profile][key]])
            
        
    def get_config(self):
        temp = []
        temp.append([self.profile, ""])
        for key in self.config[self.profile]:
            temp.append([key, self.config[self.profile][key]])
        return temp
                
        




