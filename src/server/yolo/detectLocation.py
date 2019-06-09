from darknet import performDetect
import argparse
import cv2
import math
import numpy as np
import os
import sys
import time



def getLinkCoords(img):
    yolo_result = performDetect(img, configPath = "./yolo-link.cfg",
                                weightPath = "./yolo-link_final.weights",
                                metaPath = "./link.data",
                                showImage = False,
                                makeImageOnly = False, initOnly = False)
        
    coords = [-1, -1]

    for detected in yolo_result:
        if detected[0] == 'link':
            coords[0] = int(detected[2][0])
            coords[1] = int(detected[2][1])

    return coords


def getLaserCoords(img):
    
    pixel_width  = 2560.0
    pixel_height = 1920.0
    pixel_margin = 10.0
    
    low_red_bounds  = np.array([230, 200, 225], dtype=np.uint8)
    high_red_bounds = np.array([255, 240, 255], dtype=np.uint8)
    mask = cv2.inRange(img, low_red_bounds, high_red_bounds)
    
    isolated_red_output = img.copy()
    isolated_red_output[np.where(mask==0)] = 0
    
    corners = np.array([[[pixel_margin, pixel_margin]],[[pixel_margin, pixel_height + pixel_margin]],[[pixel_width + pixel_margin, pixel_height + pixel_margin]],[[pixel_width + pixel_margin, pixel_margin]],])
    
    point_dest = np.array(corners, np.float32)
    
    gray = cv2.cvtColor(isolated_red_output, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 1, 10, 120)
    
    edges  = cv2.Canny(gray, 10, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    _, contours, h = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    approxCheck = False
    
    for contour in contours:
        if cv2.contourArea(contour) > 200 :
            arc_len = cv2.arcLength(contour, True)
            approxCheck = True
            approx = cv2.approxPolyDP(contour, 0.1 * arc_len, True)
            if (len(approx) == 4):
                point_src = np.array(approx, np.float32)
                h, status = cv2.findHomography(point_src, point_dest)
                out = cv2.warpPerspective(isolated_red_output, h, (int(pixel_width + pixel_margin * 2), int(pixel_height + pixel_margin * 2)))
                cv2.drawContours(isolated_red_output, [approx], -1, (0, 200, 0), 2)
                break
            else : pass

    if approxCheck == False:
        return [-1, -1]
    
    num_points = len(approx)
    sum_x = 0
    sum_y = 0
    
    for i in range(num_points):
        sum_x = sum_x + approx[i][0][0]
        sum_y = sum_y + approx[i][0][1]
    
    if num_points == 0:
        return [-1, -1]
    
    coord_center = [sum_x / num_points, sum_y / num_points]
    return coord_center



def parseInput():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-i", "--image", help = "Path to Image")
    args = vars(arg_parse.parse_args())
    img = cv2.imread(args["image"])
    return img



def main():
    
    img = parseInput()
    link_coord = getLinkCoords(img)
    laser_coord = getLaserCoords(img)
    print("Link Coordinates", link_coord)
    print("Laser Coordinates", laser_coord)



if __name__ == '__main__':
    main()
