import argparse, textwrap
import os
import time

import numpy as np
import leg

from adafruit_servokit import ServoKit

import socket

link_x, link_y, laser_x, laser_y = 0, 0, 0, 0
head_turn = False
init_body_turn, travel_distance, theta = 0, 0, 0

# Movement state globals
MOVE_FORWARD = False
MOVE_BACKWARD = False
TURN_LEFT = False
TURN_RIGHT = False

orientation_back = False
current_position = 0.0
current_angle = 0

kit1 = ServoKit(channels=16,address=0x40)
kit2 = ServoKit(channels=16,address=0x41)

# Prameters for the legs
FIRST_SEG_LEN = 0
SECOND_SEG_LEN = 0
THIRD_SEG_LEN = 0
num_legs = 6

x_offset = 0
y_radius = 0
z_radius = 0
y_offset = 0
z_offset = 0

base_locs = []
base_angs = []

positions = []

legs = []
angs = []

# Turret parameters
L0 = 82.5
R0 = 77.5

L = L0
R = R0

laser_pos = 0

R_CW = np.array([[np.cos(45*np.pi/180), -np.sin(45*np.pi/180)], [np.sin(45*np.pi/180), np.cos(45*np.pi/180)]])



def resetData():
    global link_x, link_y, laser_x, laser_y
    global head_turn, init_body_turn, travel_distance, theta
    link_x = 0
    link_y = 0
    laser_x = 0
    laser_y = 0
    init_body_turn = 0
    travel_distance = 0
    theta = 0



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
    

# Sample Motion Input would look like "Motion - Body_Turn: -12, Distance: 7, Theta: 45" or "Motion - ON" or "Motion - OFF"

def updateMotion(motion_data):

    global head_turn, init_body_turn, travel_distance, theta

    motion_data = motion_data[9:]
    if "ON" in motion_data:
        head_turn = True
    elif "OFF" in motion_data:
        head_turn = False
    else:
        motion_data = motion_data.replace(" ", "")
        data_list = motion_data.split(",")
        init_body_turn = float(data_list[0].split(":")[1])
        travel_distance = float(data_list[1].split(":")[1])
        theta = int(data_list[2].split(":")[1])
  

def parse_arguments():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    # segment lengths are cm
    parser.add_argument("--seg1_len",dest="seg1_len",type=float,default=3.9,help="length of 1st seg (cloest to body)")
    parser.add_argument("--seg2_len",dest="seg2_len",type=float,default=7.75,help="length of 2nd seg (middle)")
    parser.add_argument("--seg3_len",dest="seg3_len",type=float,default=12.8,help="length of 3rd seg (farthest from body)")

    parser.add_argument("--x_offset",dest="x_offset",type=float,default=10)
    parser.add_argument("--y_radius",dest="y_radius",type=float,default=4)
    parser.add_argument("--z_radius",dest="z_radius",type=float,default=5)
    parser.add_argument("--y_offset",dest="y_offset",type=float,default=0)
    parser.add_argument("--z_offset",dest="z_offset",type=float,default=-16)

    parser.add_argument("--z_offset_heights",dest="z_offset_heights",type=list,default=[0,0,0,0,0,0])

    return parser.parse_args()

# Used for printing the angle of every joint
def print_angs(num_legs,angs):
    for i in range(num_legs):
        print("Leg ",i)
        print(angs[i])
    print("")

# Used for updating the servo angles through the servo hat
def update_angs(num_legs,angs):
    '''
    for (i) in range(num_legs):
        kit.servo[3*i+0].angle = angs[i][0]
        kit.servo[3*i+1].angle = angs[i][1]
        kit.servo[3*i+2].angle = angs[i][2]+90
    '''
    hat_map = [1,1,1,2,2,2]
    pin_map =[[0,1,2],[3,4,5],[6,7,8],[7,8,9],[10,11,12],[13,14,15]]

    for i in range(0,num_legs):
        #angs[5][1] =  angs[5][1] - 5
        if (hat_map[i] == 1):
            
            for p,s in zip(pin_map[i],[0,1,2]):
                if (s==2):
                    kit1.servo[p].angle = angs[i][s]+90
                else:
                    kit1.servo[p].angle = angs[i][s]
        else:
            for p,s in zip(pin_map[i],[0,1,2]):
                if (s==2):
                    kit2.servo[p].angle = angs[i][s]+90
                else:
                    kit2.servo[p].angle = angs[i][s]

def init_legs(args):
    global x_offset, y_radius, z_radius, y_offset, z_offset, base_locs, base_angs, positions, legs, num_legs, angs

    FIRST_SEG_LEN = args.seg1_len
    SECOND_SEG_LEN = args.seg2_len
    THIRD_SEG_LEN = args.seg3_len

    x_offset = args.x_offset
    y_radius = args.y_radius
    z_radius = args.z_radius
    y_offset = args.y_offset
    z_offset = args.z_offset

    z_offset_heights = args.z_offset_heights

    base_locs = []
    base_angs = []
    angle_inc = 2*np.pi/num_legs
    for i in range(num_legs):
        base_angs.append(i*angle_inc)
        base_locs.append([1*np.cos(base_angs[i]),-1*np.sin(base_angs[i]),0])

    k = 19;
    num_points = k;
    for t in range(0,8):
        positions.append([x_offset,  y_radius*np.cos(-1*t/(8-1)*np.pi/2-np.pi/2)+y_offset,  z_offset])
    for t in range(0,3):
        positions.append([x_offset,  y_radius*np.cos(-1*t/(3-1)*np.pi-np.pi)+y_offset,  z_radius*np.sin(-1*t/(5-1)*np.pi-np.pi)+z_offset])
    for t in range(0,8):
        positions.append([x_offset,  y_radius*np.cos(-1*t/(8-1)*np.pi/2)+y_offset,  z_offset])

    legs = []
    for (i,b_loc,b_ang) in zip(range(num_legs),base_locs,base_angs):
        if i%2 == 1:
            if num_legs == 6:
                step_offset = 0.5
            else:
                step_offset = 0
        else:
            step_offset = 0
        legs.append(leg.leg(num_segs=3,lens=[FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN],base_location=b_loc,base_angle=b_ang,positions=positions,forward_angle=b_ang,leg_ID=i,step_offset=step_offset,z_offset_height=z_offset_heights[i]))

    angs = []
    for l in legs:
        angs.append(l.get_angles_deg(mode='servo')+90)
    print_angs(num_legs,angs)
    update_angs(num_legs,angs)
    print("First leg path: after init")
    print(legs[0].positions)
    print("First leg forward angle: after init")
    print(legs[0].forward_angle)

def init_laser():
    set_laser_servos(L0,R0)


def move(init_body_turn, travel_distance, theta):
    global current_position, legs, num_legs, angs, orientation_back

    # Set movement state base on input string values
    if current_position < travel_distance and np.abs(current_position-travel_distance) > 1e0:
        MOVE_FORWARD = True
        MOVE_BACKWARD = False
    elif current_position > travel_distance and np.abs(current_position-travel_distance) > 1e0:
        MOVE_FORWARD = False
        MOVE_BACKWARD = True
    else:
        MOVE_FORWARD = False
        MOVE_BACKWARD = False
        current_position = 0

    if theta < 0:
        print("Turning right")
    elif theta > 0:
        print("Turning left")

    for (l,i) in zip(legs,range(num_legs)):
        l.turn(theta*np.pi/180)

    if MOVE_FORWARD:
        if not orientation_back:
            for (l,i) in zip(legs,range(num_legs)):
                l.step()
        else:
            for (l,i) in zip(legs,range(num_legs)):
                l.reverse()
                l.step()
            orientation_back = False
        current_position = current_position + 5/19*3/2
    elif MOVE_BACKWARD:
        if not orientation_back:
            for (l,i) in zip(legs,range(num_legs)):
                l.reverse()
                l.step()
            orientation_back = True
        else:
            for (l,i) in zip(legs,range(num_legs)):
                l.step()
        current_position = current_position - 5/19*3/2

    for (l,k) in zip(legs,range(num_legs)):
        angs[k] = l.get_angles_deg(mode='servo')+90
        
    update_angs(num_legs,angs)
    return ((not MOVE_FORWARD) and (not MOVE_BACKWARD))
    

def set_laser_servos(ang1,ang2):
    kit1.servo[14].angle = ang1
    kit1.servo[15].angle = ang2

def move_laser(link_x, link_y, laser_x, laser_y):
    global L, R, laser_err

    laser_err = [link_x-50, link_y-50]
    laser_err = np.matmul(R_CW,laser_err)

    screen_dim = 100
    dR = -laser_err[0]/screen_dim*(105-50)
    dL = -laser_err[1]/screen_dim*(105-60)

    R = R0 + dR
    L = L0 + dL

    edge = False

    if R >= 105:
        R = 105
        edge = True
    elif R <= 50:
        R = 50
        edge = True
    if L >= 105:
        L = 105
        edge = True
    elif L <= 60:
        L = 60
        edge = True

    print("L: ",L)
    print("R: ",R)
    set_laser_servos(L,R)
    return True


def client_program():
    
    host = "192.168.0.101"
    port = 5001

    client_socket = socket.socket()
    client_socket.connect((host, port))

    while True:
        message = client_socket.recv(1024).decode()
        print(message)
        if (message[0:8] == "Position"):
            updatePosition(message)
        elif (message[0:6] == "Motion"):
            updateMotion(message)
            
        print("Position Data:", link_x, link_y, laser_x, laser_y)
        print("Motion Data:", head_turn, init_body_turn, travel_distance, theta)
        start_time = time.time()
        if head_turn:
            kit1.continuous_servo[13].throttle = 0.15
        else:
            kit1.continuous_servo[13].throttle = 0.05
        while True:
            move_legs_result = move(init_body_turn, travel_distance, theta)
            move_laser_result = move_laser(link_x, link_y, laser_x, laser_y)
            if (move_legs_result && move_laser_result):
               break
        """
        print("First leg path: after data")
        print(legs[0].positions)
        print("First leg forward angle: after data")
        print(legs[0].forward_angle)
        """
        resetData()
    client_socket.close() 


def laser_proc():



if __name__ == '__main__':

    args = parse_arguments()

    init_legs(args)

    init_laser()

    client_program()
