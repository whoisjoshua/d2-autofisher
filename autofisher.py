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
import ctypes
import argparse
from mss import mss
from PIL import Image
from datetime import datetime


def getScreenSize():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize

def displayStats(img, prompts,
                 coords=[10, 35],
                 font=cv2.FONT_HERSHEY_SIMPLEX,
                 font_size=0.8,
                 color=(0, 0, 255),
                 thickness=2):
    offset = coords[1]
    #img_height, img_width, img_channels = img.shape
    for idx, key in enumerate(prompts):
        coords = tuple([coords[0], offset])
        #offset += int(img_height / len(prompts))
        offset += 35
        text = "{0}: {1}".format(key, prompts[key])
        # print("[DEBUG] Text coords: {0} {1}", type(coords), coords)
        #print("[DEBUG] Text: {0}", text)
        img = cv2.putText(img, text, coords, font, font_size, color, thickness, cv2.LINE_AA)
    return img


if __name__ == "__main__":
    # TODO: Add args (auto-detect monitor size)
    parser = argparse.ArgumentParser()

    monitor_height = 1080
    monitor_width = 1920
    window_height = int(monitor_height / 2)
    window_width = int(monitor_height / 2)

    bounding_box = {'top': int(monitor_height / 2),
                    'left': int(monitor_width / 2 - window_width / 2),
                    'width': window_width,
                    'height': window_height}
    sct = mss()

    # Debug fields
    show_filter = False
    debug = False
    debug_prompts = {
        "Command Registered": "None",
        "Detected Target": "None",
        "Positives": 0,
        "SS Delay": 0,
        "SS Window": 0,
    }

    while True:
        sct_img = np.array(sct.grab(bounding_box))
        sct_img_gray = cv2.cvtColor(sct_img, cv2.COLOR_BGR2GRAY)

        # sct_img_blur = cv2.medianBlur(sct_img_gray, 3)
        # sct_img_thresh = cv2.threshold(sct_img_blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        k_size = 3
        kernel = np.ones((k_size, k_size), np.uint8)
        sct_img_dilated = cv2.dilate(sct_img_gray, kernel, iterations=1)

        gs_border = 3
        sct_img_gaussian = cv2.GaussianBlur(sct_img_dilated, (0, 0), gs_border)
        sct_img_weight = cv2.addWeighted(sct_img_gray, 0.9, sct_img_gaussian, 1.7, 0)

        # Visuals
        if not show_filter:
            if debug:
                sct_img = displayStats(sct_img, debug_prompts)
            cv2.imshow('Capture Screen', sct_img)
        else:
            if debug:
                sct_img_weight = displayStats(sct_img_weight, debug_prompts)
            cv2.imshow('Capture Screen (Filtered)', sct_img_weight)

        # Key Actions
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
        elif (cv2.waitKey(1) & 0xFF) == ord('o'):
            if debug:
                debug_prompts["Command Registered"] = "Debug Mode (o)"
            cv2.destroyAllWindows()
            debug = not debug
            print("[INFO] Toggled \"debug\" mode.")
        elif (cv2.waitKey(1) & 0xFF) == ord('i'):
            if debug:
                debug_prompts["Command Registered"] = "Show Filter (i)"
            cv2.destroyAllWindows()
            show_filter = not show_filter
            print("[INFO] Toggled \"show_filter\" mode.")
        elif (cv2.waitKey(1) & 0xFF) == ord('p'):
            if debug:
                debug_prompts["Command Registered"] = "Screenshot (p)"
            date = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            cv2.imwrite(".\\screenshots\\SS_{}.png".format(date), sct_img)
            cv2.imwrite(".\\screenshots\\SS_filtered_{}.png".format(date), sct_img_weight)
            print("[INFO] Screenshot created: SS_{}.png".format(date))
            print("[INFO] Screenshot created: SS_filtered_{}.png".format(date))

