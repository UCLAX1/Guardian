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


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.101', 5000))

camera = picamera.PiCamera()
camera.resolution = (960, 720)
camera.vflip = True
camera.hflip = True
camera.start_preview()
time.sleep(2)
camera.stop_preview()

    
def convertToB64(file):
    b64_str = ""
    with open(file, "rb") as imageFile:
        b64_str = base64.b64encode(imageFile.read())
    return b64_str


while True:

    file = "image.jpg"
    camera.capture(file)
    
    file_str = convertToB64(file)
    file_str = file_str + "breakbreakbreak==="

    num_chunks = len(file_str)/1024
    for i in range(0, num_chunks - 1):
        client_socket.send(file_str[1024*i : 1024*(i + 1)])
    client_socket.send(file_str[1024 * (num_chunks - 1) : ])
    print("Image sent.")
    time.sleep(0.25)

    
client_socket.close()
    
    
