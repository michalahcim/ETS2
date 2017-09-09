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
#import win32api
from uczenie_getkeys import key_check
from alexnet import alexnet
from directkeys import PressKey,ReleaseKey, W, A, S, D
import random
import os


width = 80
height = 60

LR = 1e-3
EPOCHS = 8

MODEL_NAME = 'pyets2-volvo-{}-{}-{}-epochs.model'.format(LR, 'alexnet', EPOCHS)


def forward():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)

def left():
   
    PressKey(W)
    PressKey(A)
    ReleaseKey(S)
   
    ReleaseKey(D)
    time.sleep(0.05)
    ReleaseKey(A)

def right():
    PressKey(W)   
    PressKey(D)
    
    ReleaseKey(A)
    ReleaseKey(S)
    time.sleep(0.05)
    ReleaseKey(D)
    


model = alexnet(width, height, LR)
model.load(MODEL_NAME)

def main():
    print("start za 5 sek")
    time.sleep(5)
    print("start")
    #last_time = time.time()
    paused = False
    while(True):
        
        if not paused:
            screen =  grab_screen(region = (0,40,800,640))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen,(80,60))
            
            prediction = model.predict([screen.reshape(width,height,1)])[0]
            moves = list(np.around(prediction))
            print(moves, prediction)
            #print('Loop took {} seconds'.format(time.time()-last_time))
            #last_time = time.time()
            if moves == [1,0,0]:
                left()
            elif moves == [0,1,0]:
                forward()
            elif moves == [0,0,1]:
                right()
            
        keys = key_check()
        
        if 'S' in keys:
            if paused:
                paused = False
                time.sleep(5)
            else:
                print("pause")
                pause = True
                ReleaseKey(W)
                ReleaseKey(A)
                ReleaseKey(D)
                time.sleep(10)
       
        


main()