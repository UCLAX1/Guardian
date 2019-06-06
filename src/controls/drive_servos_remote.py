"""
./drive_sim_servos.py
Jingbin Huang
UCLA ASME X1 Robotics 2018-2019

Use argument "--help" to see usage information

"""

import argparse, textwrap
import os
import time

import numpy as np
import leg

from adafruit_servokit import ServoKit

import path_scaling as ps

import socket

link_x, link_y, laser_x, laser_y = 0, 0, 0, 0
head_turn, init_body_turn, travel_distance, theta = 0, 0, 0, 0

# Movement state globals
MOVE_FORWARD = False
MOVE_BACKWARD = False
TURN_LEFT = False
TURN_RIGHT = False

kit1 = ServoKit(channels=16,address=0x40)
kit2 = ServoKit(channels=16,address=0x41)

clear_msg = "clear"

if os.name == 'nt':
    clear_msg = "cls"
elif os.name == 'posix':
    clear_msg = "clear"


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


def updateMotion(motion_data):
    
    global head_turn, init_body_turn, travel_distance, theta
    
    motion_data = motion_data[9:]
    motion_data = motion_data.replace(" ", "")
    data_list = motion_data.split(",")
    
    head_turn = float(data_list[0].split(":")[1])
    init_body_turn = float(data_list[1].split(":")[1])
    travel_distance = float(data_list[2].split(":")[1])
    theta = float(data_list[3].split(":")[1])


def parse_arguments():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    # segment lengths are cm
    parser.add_argument("--seg1_len",dest="seg1_len",type=float,default=3.9,help="length of 1st seg (cloest to body)")
    parser.add_argument("--seg2_len",dest="seg2_len",type=float,default=7.75,help="length of 2nd seg (middle)")
    parser.add_argument("--seg3_len",dest="seg3_len",type=float,default=12.8,help="length of 3rd seg (farthest from body)")
    parser.add_argument("--mode",dest="mode",type=str,default="sim",help="sim | servo")
    parser.add_argument("--path_source",dest="path_source",type=str,default="internal",help=textwrap.dedent("""\
            internal: use in script paths.
            external: use path from external file.
            """))
    parser.add_argument("--path_data",dest="path_data",type=str,default="reset",help=textwrap.dedent("""\
            reset: all servo angles 0.
            ellipse: elliptical crawl path.
            semicircle.
            file name: used when path source is external.
            """))
    parser.add_argument("--wait_time",dest="wait_time",type=float,default=0,help="force sleep time between each data point")
    parser.add_argument("--num_legs",dest="num_legs",type=int,default=6,help="number of legs")

    parser.add_argument("--turn_angle",dest="turn_angle",type=float,default=2/180*np.pi)
    parser.add_argument("--turn_interval",dest="turn_interval",type=float,default=0.1)
    parser.add_argument("--x_offset",dest="x_offset",type=float,default=12)
    parser.add_argument("--y_radius",dest="y_radius",type=float,default=5)
    parser.add_argument("--z_radius",dest="z_radius",type=float,default=5)
    parser.add_argument("--y_offset",dest="y_offset",type=float,default=0)
    parser.add_argument("--z_offset",dest="z_offset",type=float,default=-15)

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
        angs[5][1] =  angs[5][1] - 5
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
    

# Main code
if __name__ == '__main__':
    # Parse command line arguments
    args = parse_arguments()
    # Segment lengths
    FIRST_SEG_LEN = args.seg1_len
    SECOND_SEG_LEN = args.seg2_len
    THIRD_SEG_LEN = args.seg3_len
    # Sim or servo
    mode = args.mode
    # Path
    path_source = args.path_source
    path_data = args.path_data

    wait_time = args.wait_time
    num_legs = args.num_legs

    TOT_LEN = FIRST_SEG_LEN + SECOND_SEG_LEN + THIRD_SEG_LEN;
    SECOND_THIRD_LEN = SECOND_SEG_LEN + THIRD_SEG_LEN;

    x_offset = args.x_offset
    y_radius = args.y_radius
    z_radius = args.z_radius
    y_offset = args.y_offset
    z_offset = args.z_offset

    base_locs = []
    base_angs = []
    angle_inc = 2*np.pi/num_legs
    for i in range(num_legs):
        base_angs.append(i*angle_inc)
        base_locs.append([1*np.cos(base_angs[i]),-1*np.sin(base_angs[i]),0])

    positions = []

    if (path_source == "internal"):
        # Set all joints to 0
        if (path_data == "reset"):
            num_points = 10
            for t in range(10):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN,0,0])        
        elif (path_data == "ellipse"):
            k = 25;
            num_points = k;
            theta = np.arccos((x_pos*TOT_LEN-FIRST_SEG_LEN)/(SECOND_SEG_LEN+THIRD_SEG_LEN));
            radius = (SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(theta);
            for t in range(k):
                positions.append([TOT_LEN*x_pos,  y_scale*radius*np.cos(-1*t/(k-1)*2*np.pi-np.pi/2)+y_offset*y_scale*radius,  z_scale*radius*np.sin(t/(k-1)*2*np.pi-np.pi/2)+z_offset*z_scale*radius])
        elif (path_data == "semicircle"):
            k = 19;
            num_points = k;
            #theta = np.arccos((x_pos*TOT_LEN-FIRST_SEG_LEN)/(SECOND_SEG_LEN+THIRD_SEG_LEN));
            #radius = (SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(theta);
            for t in range(0,8):
                positions.append([x_offset,  y_radius*np.cos(-1*t/(8-1)*np.pi/2-np.pi/2)+y_offset,  z_offset])
            for t in range(0,3):
                positions.append([x_offset,  y_radius*np.cos(-1*t/(3-1)*np.pi-np.pi)+y_offset,  z_radius*np.sin(-1*t/(5-1)*np.pi-np.pi)+z_offset])
            for t in range(0,8):
                positions.append([x_offset,  y_radius*np.cos(-1*t/(8-1)*np.pi/2)+y_offset,  z_offset])
        else:
            print("Unrecognized internal data: ", path_data)
            quit()

    elif (path_source == "external"):
        positions = np.genfromtxt(path_data, delimiter=",")
        positions = ps.scale_path(positions,FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN,x=x_pos,y_scale=y_scale,z_scale=z_scale,y_offset=y_offset,z_offset=z_offset)
        num_points = positions.shape[0]
    else:
        print("Unrecognized path source: ", path_source)
        quit()

    legs = []
    for (i,b_loc,b_ang) in zip(range(num_legs),base_locs,base_angs):
        if i%2 == 1:
            if num_legs == 6:
                step_offset = 0.5
            else:
                step_offset = 0
        else:
            step_offset = 0
        legs.append(leg.leg(num_segs=3,lens=[FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN],base_location=b_loc,base_angle=b_ang,positions=positions,forward_angle=b_ang,leg_ID=i,step_offset=step_offset))


    angs = []
    for l in legs:
        angs.append(l.get_angles_deg(mode='servo')+90)
    print_angs(num_legs,angs)
    update_angs(num_legs,angs)
    print(angs)

    orientation_back = False
    current_position = 0.0
    current_angle = 0

    while True:
        try:
            # Parse input string
            inp_str = "50,0"
            data = inp_str.split(",")
            distance = float(data[0])
            angle = int(data[1])

            # Set movement state base on input string values
            if current_position < distance and np.abs(current_position-distance) > 1e-4:
                MOVE_FORWARD = True
                MOVE_BACKWARD = False
            elif current_position > distance and np.abs(current_position-distance) > 1e-4:
                MOVE_FORWARD = False
                MOVE_BACKWARD = True
            else:
                MOVE_FORWARD = False
                MOVE_BACKWARD = False
            if current_angle > angle and np.abs(current_position-distance) > 1e-4:
                TURN_LEFT = True
                TURN_RIGHT = False
            elif current_angle < angle and np.abs(current_position-distance) > 1e-4:
                TURN_LEFT = False
                TURN_RIGHT = True
            else:
                TURN_LEFT = False
                TURN_RIGHT = False


            if MOVE_FORWARD:
                if not orientation_back:
                    for (l,i) in zip(legs,range(num_legs)):
                        l.step()
                else:
                    for (l,i) in zip(legs,range(num_legs)):
                        l.reverse()
                        l.step()
                    orientation_back = False
            elif MOVE_BACKWARD:
                if  not orientation_back:
                    for (l,i) in zip(legs,range(num_legs)):
                        l.reverse()
                        l.step()
                    orientation_back = True

            if TURN_RIGHT:
                for (l,i) in zip(legs,range(num_legs)):
                    l.turn(-1*(current_angle-angle))
                    current_angle = angle 
            else:
                for (l,i) in zip(legs,range(num_legs)):
                    l.turn(1*(current_angle-angle)) 
                    current_angle = angle

            for (l,k) in zip(legs,range(num_legs)):
                angs[k] = l.get_angles_deg(mode='servo')+90
                
            update_angs(num_legs,angs)
            os.system(clear_msg)
            print("Step count: ", legs[0].step_count)
            print("Forward angle: ", legs[0].forward_angle/np.pi*180)
            print_angs(num_legs,angs)
            if not orientation_back:
            	current_position = current_position + 5/19
            else:
                current_position = current_position - 5/19
            time.sleep(wait_time)

        except KeyboardInterrupt:
            exit()

