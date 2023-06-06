#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: autofisher.py
# Author: Joshua Zeng
# Date: June 5th, 2023
# Version: 1.0.0
# Description: D2 Autofisher

import numpy as np
import cv2
from mss import mss
import ctypes
from PIL import Image

def getScreenSize():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize

if __name__ == "__main__":
    #TODO: Add args

    monitor_height = 1080
    monitor_width = 1920
    window_height = int(monitor_height/2)
    window_width = int(monitor_height/2)

    bounding_box = {'top': int(monitor_height/2),
                    'left': int(monitor_width/2-window_width/2),
                    'width': window_width,
                    'height': window_height}
    debug = False
    sct = mss()

    while True:
        sct_img = np.array(sct.grab(bounding_box))

        # Visuals
        if not debug:
            cv2.imshow('Capture Screen', sct_img)
        else:
            #TODO: Add other visual w/ stats here
            break

        # Key Actions
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
        elif (cv2.waitKey(1) & 0xFF) == ord('p'):
            debug=True
