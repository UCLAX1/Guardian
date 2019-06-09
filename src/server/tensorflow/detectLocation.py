from detection import Detection
import argparse
import cv2
import math
import numpy as np
import os
import sys
import time


def getLaserCoords(img):
    
    pixel_width  = 2560.0
    pixel_height = 1920.0
    pixel_margin = 10.0
    
    cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    low_red_bounds  = np.array([215, 215, 215], dtype=np.uint8)
    high_red_bounds = np.array([255, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(img, low_red_bounds, high_red_bounds)
    
    isolated_red_output = img.copy()
    isolated_red_output[np.where(mask==0)] = 0

    gray_image = cv2.cvtColor(isolated_red_output, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray_image,127,255,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    maxArea = 0
    for c in contours:
        _,_,w,h = cv2.boundingRect(c)
        if w < 1.5 * h and h < 1.5 * w and cv2.contourArea(c) < 12000:
            if cv2.contourArea(c) > maxArea:
                maxArea = cv2.contourArea(c)
    
    for c in contours:
        if maxArea == cv2.contourArea(c):
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                return [cX, cY]

    return [-1, -1]



def parseInput():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-i", "--image", help = "Path to Image")
    args = vars(arg_parse.parse_args())
    img = cv2.imread(args["image"])
    return img



def main():
    
    img = parseInput()
    d = Detection()
    link_coord = d.run(img)
    laser_coord = getLaserCoords(img)
    print("Link Coordinates", link_coord)
    print("Laser Coordinates", laser_coord)



if __name__ == '__main__':
    main()
