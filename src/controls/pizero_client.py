import base64
import cv2
import io
import math
import os
import picamera
import pickle
import socket
import struct
import time
import zlib


link_x, link_y, laser_x, laser_y = 0, 0, 0, 0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.101', 5000))
#connection = client_socket.makefile('wb')

camera = picamera.PiCamera()
#camera.resolution = (2560, 1920)
camera.resolution = (1280, 960)
camera.vflip = True
camera.hflip = True
camera.start_preview()
time.sleep(2)
camera.stop_preview()


# Sample Position Input would look like "Position - Link: 152,156. Laser: 142,138"

def updatePosition(pos_data):

    global link_x, link_y, laser_x, laser_y

    pos_data = pos_data[11:]

    link_data = pos_data.split(". ")[0]
    link_coords = link_data.split(": ")[1]
    link_x = int(link_coords.split(",")[0])
    link_y = int(link_coords.split(",")[1])

    laser_data = pos_data.split(". ")[1]
    laser_coords = laser_data.split(": ")[1]
    laser_x = int(laser_coords.split(",")[0])
    laser_y = int(laser_coords.split(",")[1])

    
def convertToB64(file):
    b64_str = ""
    with open(file, "rb") as imageFile:
        b64_str = base64.b64encode(imageFile.read())
    return b64_str


while True:

    file = "image.jpg"
    camera.capture(file)
    
    file_str = convertToB64(file)
    file_str = file_str + "breakbreakbreak"

    num_chunks = len(file_str)/1024
    for i in range(0, num_chunks - 1):
        client_socket.send(file_str[1024*i : 1024*(i + 1)])
    client_socket.send(file_str[1024 * (num_chunks - 1) : ])
    print("Image sent.")
    time.sleep(0.25)

    """
    message = client_socket.recv(1024)
    updatePosition(message)
    print("Position Data:", link_x, link_y, laser_x, laser_y)
    """

    
client_socket.close()
    
    
