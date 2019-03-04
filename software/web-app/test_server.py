import argparse
import base64
import cv2
import math
import numpy as np
import os
import socket
import sys
import time


def convertToB64(file):
    b64_str = ""
    with open(file, "rb") as imageFile:
        b64_str = base64.b64encode(imageFile.read())
    return b64_str


def parseInput():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-i", "--image", help = "Path to Image")
    args = vars(arg_parse.parse_args())
    return args["image"]

s = socket.socket()
host = 'localhost'
port = 5000

s.bind((host, port))
s.listen(5)

c, addr = s.accept()

file = parseInput()
file_str = convertToB64(file)

file_str = file_str + b"breakbreakbreak"

num_chunks = math.ceil(len(file_str)/1024)

for i in range(0, num_chunks - 1):
    c.send(file_str[1024*i : 1024*(i + 1)])
c.send(file_str[1024 * (num_chunks - 1) : ])


return_data = c.recv(1024)
print(return_data)

c.close()
