#!/usr/bin/env python3

#program napisany z poradnikiem
#https://www.youtube.com/watch?v=ks4MPfMq8aQ&list=PLQVvvaa0QuDeETZEOy4VdocT7TOjfSA8a
#jednak nie jest to kopia 1:1

import numpy as np
from PIL import ImageGrab
import cv2
import time
import ctypes
import math
from grabscreen import grab_screen
import win32api
from uczenie_getkeys import key_check

import os


def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array

    [A,W,D] boolean values.
    '''
    output = [0,0,0]
    
    if 'A' in keys:
        output[0] = 1
    elif 'D' in keys:
        output[2] = 1
    else:
        output[1] = 1
    return output

file_name = "training_data.npy"

if os.path.isfile(file_name):
    print("File exists")
    training_data = list(np.load(file_name))
else:
    print("Starting fresh")
    training_data = []
    


def main():
    print("start za 5 sek")
    time.sleep(5)
    
    #last_time = time.time()
    while(True):
        screen =  grab_screen(region = (0,40,800,640))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen,(80,60))
        keys = key_check()
        output = keys_to_output(keys)
        training_data.append([screen, output])
        #print('Loop took {} seconds'.format(time.time()-last_time))
        #last_time = time.time()
        
        if len(training_data)%500 ==0:
            print(len(training_data))
            np.save(file_name, training_data)
       
        


main()