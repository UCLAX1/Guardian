from darknet import performDetect
import argparse
import cv2
import math
import numpy as np
import os
import pickle
import socket
import struct
import sys
import time
import zlib




def getLinkCoords(img):
    yolo_result = performDetect(img, configPath = "./cfg/yolov3-tiny.cfg", 
                                weightPath = "yolov3-tiny.weights", showImage= False, 
                                makeImageOnly = False, initOnly= False)

    # maybe default to -1, -1 to make it unambiguous?
    coords = [0, 0] # link's center x, y
    
    # extract coordinates from output
    # only works for showImage=False
    for detected in yolo_result:
        if detected[0] == 'person':
            coords[0] = detected[2][0]
            coords[1] = detected[2][1]
    
    return coords



def getLaserCoords(img):
    
    pixel_width  = 2560.0
    pixel_height = 1920.0
    pixel_margin = 10.0
    
    low_red_bounds  = np.array([230, 210, 225], dtype=np.uint8)
    high_red_bounds = np.array([255, 250, 255], dtype=np.uint8)
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
        return [0, 0]
    
    num_points = len(approx)
    sum_x = 0
    sum_y = 0
    
    for i in range(num_points):
        sum_x = sum_x + approx[i][0][0]
        sum_y = sum_y + approx[i][0][1]

    if num_points == 0:
        return [0, 0]
    
    coord_center = [sum_x / num_points, sum_y / num_points]
    return coord_center


def getLocations(img):
    link_coord = getLinkCoords(img)
    laser_coord = getLaserCoords(img)
    return "Position - Link: " + str(link_coord[0]) + "," + str(link_coord[1]) + ". Laser: " + str(laser_coord[0]) + "," + str(laser_coord[1])



HOST = '192.168.0.101'
CAMERA_PORT = 5000
CONTROLS_PORT = 5001

camera_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
controls_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Sockets created.')

camera_socket.bind((HOST, CAMERA_PORT))
controls_socket.bind((HOST, CONTROLS_PORT))
print('Socket binds complete.')

camera_socket.listen(10)
controls_socket.listen(10)
print('Sockets now listening.')

camera_conn, camera_addr = camera_socket.accept()
controls_conn, controls_addr = controls_socket.accept()


while True:
    img_str = ""
    while True:
        data = camera_conn.recv(1024)
        if "breakbreakbreakbreakbreak" in str(data):
            img_str += data.replace("breakbreakbreakbreakbreak", ""))
            break
        imgstr += data
    print("Received Image")
    
    # convert from string to opencv image
    # not 100% sure this works - ben
    nparr = np.fromstring(img_str, np.uint8)
    img = cv2.imdecode(nparr)
    
    location_data = getLocations(img)
    print(location_data)
    controls_conn.send(location_data)
    print("Sent Position Data")
    print(" ")


camera_conn.close()
controls_conn.close()
