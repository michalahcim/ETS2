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
import pyautogui
import win32api
from directkeys import ReleaseKey, PressKey, W, A, S, D 


def prosto():
    ReleaseKey(A)
    ReleaseKey(D)
    #pyautogui.moveTo(x,y)
    #ctypes.windll.user32.mouse_event(0, x, y, 0,0)
    print("Prosto")

def lewo():
    PressKey(A)
    ReleaseKey(D)
    #pyautogui.moveTo(x,y)
    #pyautogui.moveRel(x-10,0)
    #x= x_st
    #x = x+1
    #ctypes.windll.user32.mouse_event(0, x, y, 0,0)
    #print(x)
    print("lewo")

def prawo():
    #pyautogui.moveTo(x,y)
    #pyautogui.moveRel(x+10,)
    PressKey(D)
    ReleaseKey(A)
    #x = x_st
    #x = x-1
    #ctypes.windll.user32.mouse_event(0, x, y, 0,0)
    print("prawo")
    
def stop():
    #ReleaseKey(A)
    #ReleaseKey(D)
    PressKey(S)

def draw_lines(img,lines):
    global zmniejsz #zeby wyswietlac tylko 2 linie z dodatniego lub ujemnego nachylenia
    global wieksz 
    zmniejsz = 0
    wieksz = 0
    kat = 15
    try:
        for line in lines:
            coords = line[0]
            a = (coords[3]-coords[1])/(coords[2]-coords[0])
            radian = np.arctan(a)
            stopnie = math.degrees(radian)
           # print(stopnie)
            if stopnie <= -(kat):   #to jest po to zeby nie wykrywalo horyzontu i linii poziomych
                if zmniejsz >=1:
                    break
                else:
                    zmniejsz = zmniejsz + 1
                    cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)#wyswietlanie lini
            elif stopnie >=kat:
                if wieksz >=1:
                    break
                else:
                    wieksz = wieksz + 1
                    cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)
    except:
        pass


def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY) #zamiana kolorow na grey
    processed_img = cv2.Canny(processed_img, threshold1=50, threshold2=100) #zamiana obrazu na takie kreski
    #vertices = np.array([[117,407],[150,0],[650,0],[683,407],], np.int32) #dla widoku z gory
    vertices = np.array([[0,640],[0,540],[160,310],[640,310],[800,540],[800,640]], np.int32) #dla widoku z maski
    

    processed_img = cv2.GaussianBlur(processed_img,(5,5),0) #dodanie blura zeby poprawic wykrywanie linii
    processed_img = roi(processed_img, [vertices])
   
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, 10,  150) #min_dlugosc, max_przerwa
    draw_lines(processed_img,lines)
    return processed_img


def roi(img, vertices): #ograniczanie pola obrazu
    #blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_ulong), ("y", ctypes.c_ulong)]

def cursorPos():
    point = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.pointer(point))
    return (point.x, point.y)

def main():
    last_time = time.time()
    while(True):
        screen =  np.array(ImageGrab.grab(bbox=(0,40, 800, 640)))
        new_screen = process_img(screen)
        print('Loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        cv2.imshow('window', new_screen)
        #cv2.imshow('window2', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        
        if wieksz and zmniejsz ==1:
            prosto()
        elif wieksz ==1:
            lewo()
        elif zmniejsz ==1:
            prawo()
        else:
            prosto()
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
print("start za 5 sek")

for i in range (0,5):
    time.sleep(1)
#x,y = 0,0

#x_st, y_st = x,y 
#ctypes.windll.user32.SetCursorPos(x, y)
#pyautogui.dragTo(400,400)
main()