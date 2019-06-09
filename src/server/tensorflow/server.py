from detection import Detection
from multiprocessing import Process
import argparse
import base64
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

HOST = '192.168.0.101'
#HOST = 'localhost'
CAMERA_PORT = 5000
CONTROLS_PORT = 5001
WEB_PORT = 5002

def setup():
    
    global camera_conn, camera_addr, controls_conn, controls_addr, web_conn, web_addr
    
    camera_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    controls_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    web_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Sockets created.')
    
    camera_socket.bind((HOST, CAMERA_PORT))
    controls_socket.bind((HOST, CONTROLS_PORT))
    web_socket.bind((HOST, WEB_PORT))
    print('Socket binds complete.')
    
    camera_socket.listen(10)
    controls_socket.listen(10)
    web_socket.listen(10)
    print('Sockets now listening.')
    
    camera_conn, camera_addr = camera_socket.accept()
    controls_conn, controls_addr = controls_socket.accept()
    web_conn, web_addr = web_socket.accept()
    
    d = Detection()


def getLinkCoords(d, img):
    d = Detection()
    link_coord = d.run(img)
    return link_coord


def getLaserCoords(img):
    
    #pixel_width  = 1920.0
    #pixel_height = 1440.0
    pixel_width  = 960.0
    pixel_height = 720.0
    pixel_margin = 10.0
    
    cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    low_red_bounds  = np.array([215, 215, 215], dtype=np.uint8)
    high_red_bounds = np.array([255, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(img, low_red_bounds, high_red_bounds)
    
    isolated_red_output = img.copy()
    isolated_red_output[np.where(mask==0)] = 0
    
    gray_image = cv2.cvtColor(isolated_red_output, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray_image,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
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


def getLocations(d, img):
    link_coord = getLinkCoords(d, img)
    laser_coord = getLaserCoords(img)
    loc_data1 = "Position - Link: " + str(link_coord[0]) + "," + str(link_coord[1]) + ". Laser: " + str(laser_coord[0]) + "," + str(laser_coord[1])
    loc_data2 = "Coords - " + str(link_coord[0]) + "," + str(link_coord[1]) + "," + str(laser_coord[0]) + "," + str(laser_coord[1])
    return loc_data1, loc_data2


def runMOVEprocess():
    
    while True:
        motion_data = web_conn.recv(1024)
        motion_data = motion_data.split("clean")[0]
        if "ON" in motion_data:
            input_data = "cleanMotion - ON"
            print(input_data.replace("clean",""))
            controls_conn.send(input_data)
        elif "OFF" in motion_data:
            input_data = "cleanMotion - OFF"
            print(input_data.replace("clean",""))
            controls_conn.send(input_data)
        else:
            input_data_list = motion_data.split(",")
        
            if input_data_list[1] == "":
                input_data_list[1] = "0"
            if input_data_list[2] == "":
                input_data_list[2] = "0"
            if input_data_list[4] == "":
                input_data_list[4] = "0"
        
            bt = int(input_data_list[1])
            dist = int(input_data_list[2])
            theta = int(input_data_list[4])
        
            if "R" in input_data_list[0]:
                bt = bt * -1
            if "R" in input_data_list[3]:
                theta = theta * -1
        
            input_data = "cleanMotion - Body_Turn: " + str(bt) + ", Distance: " + str(dist) + ", Theta:" + str(theta)
            print(input_data.replace("clean",""))
            controls_conn.send(input_data)


def runCAMprocess():
    d = Detection()
    
    while True:

        img_str = ""
        while True:
            data = camera_conn.recv(1024)
            img_str += data
            if "breakbreakbreak" in str(data):
                break
        print("Received Image")


        received_file = 'received_image.jpg'
        resized_file = 'resized_image.jpg'
    
        decoded_img = base64.b64decode(img_str.replace("breakbreakbreak", "")  + "===")
    
        with open(received_file, 'wb') as f:
            f.write(decoded_img)
        img = cv2.imread(received_file)

        #resize_img = cv2.resize(img, (1280, 960))
        resize_img = cv2.resize(img, (960, 720))
        cv2.imwrite(resized_file, resize_img)

        b64_str = ""
        with open(resized_file, "rb") as imageFile:
            b64_str = base64.b64encode(imageFile.read())
        b64_str = b64_str + "breakbreakbreak"
        num_chunks = len(b64_str)/1024
        for i in range(0, num_chunks - 1):
            web_conn.send(b64_str[1024*i : 1024*(i + 1)])
        web_conn.send(b64_str[1024 * (num_chunks - 1) : ])
        print("Sent Image to Dashboard")

        location_data1, location_data2 = getLocations(d, img)
        controls_conn.send("clean" + location_data1)
        print(location_data1)
        camera_conn.send(location_data1)
        web_conn.send(location_data2)
        print("Sent Position Data to Pi 3 and Dashboard")
        print(" ")


def cleanup():
    camera_conn.close()
    controls_conn.close()
    web_conn.close()


def main():
    setup()
    p1 = Process(target = runMOVEprocess)
    p1.start()
    p2 = Process(target = runCAMprocess)
    p2.start()
    cleanup()


if __name__=='__main__':
    main()
