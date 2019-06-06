"""
./drive_sim_servos.py
Jingbin Huang
UCLA ASME X1 Robotics 2018-2019

Combines simulation and servo driver script.

Can use internal hard coded paths or external path file.

Use argument "--help" to see usage information

Examples:

python3 drive_sim_servos.py --seg1_len 1.7 --seg2_len 1 --seg3_len 2.25 --mode servo --path_source external --path_data data.txt --wait_time 0.001
Drives servos for a leg with specified segment lengths, using path data from an external file named "data.txt". Sleeps controller for 0.001 seconds between each data point.

python3 drive_sim_servos.py --seg1_len 1.7 --seg2_len 1 --seg3_len 2.25 --mode sim --path_source internal --path_data ellipse
Simulates movement for a leg with specified segment lengths, using internally coded "ellipse" path. 


"""

import argparse, textwrap
import os
import time
import keyboard

import numpy as np
import leg

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d.proj3d as proj3d
import matplotlib.animation as animation

from adafruit_servokit import ServoKit

import path_scaling as ps


kit1 = ServoKit(channels=16,address=0x40)
kit2 = ServoKit(channels=16,address=0x41)

clear_msg = "clear"

if os.name == 'nt':
    clear_msg = "cls"
elif os.name == 'posix':
    clear_msg = "clear"

z_offset_heights = [0,0,0,0,0,0]

# Keyboard state dictionary 
ks = {
    "forward_key": 'up',
    "backward_key": 'down',
    "left_key": 'left',
    "right_key": 'right',
    "stateForward": False,
    "stateLeft": False,
    "stateBackward": False,
    "stateRight": False,
    "prev_stateForward": False,
    "prev_stateLeft": False,
    "prev_stateBackward": False,
    "prev_stateRight": False,
    "orientationBack": False,
    "left_time": 0,
    "left_time_dif": 0,
    "left_waiting": False,
    "right_time": 0,
    "right_time_dif": 0,
    "right_waiting": False,
    "turning_ang_per_int": 2*np.pi/180,
    "update_interval": 0.1,
}

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

    parser.add_argument("--forward_key",dest="forward_key",type=str,default="up")
    parser.add_argument("--backward_key",dest="backward_key",type=str,default="down")
    parser.add_argument("--left_key",dest="left_key",type=str,default="left")
    parser.add_argument("--right_key",dest="right_key",type=str,default="right")
    parser.add_argument("--turn_angle",dest="turn_angle",type=float,default=2/180*np.pi)
    parser.add_argument("--turn_interval",dest="turn_interval",type=float,default=0.1)
    parser.add_argument("--x_offset",dest="x_offset",type=float,default=10)
    parser.add_argument("--y_radius",dest="y_radius",type=float,default=4)
    parser.add_argument("--z_radius",dest="z_radius",type=float,default=5)
    parser.add_argument("--y_offset",dest="y_offset",type=float,default=0)
    parser.add_argument("--z_offset",dest="z_offset",type=float,default=-16)

    return parser.parse_args()

# Used for simulation animation
def update_legs(num, legs, lines, texts, ax, positions,ks):
    # Keyboard code below
    # Using arrows keys instead because matplotlib hotkeys

    if (keyboard.is_pressed(ks["forward_key"])):
        ks["stateForward"] = True
    else:
        ks["stateForward"] = False
    if (keyboard.is_pressed(ks["backward_key"])):
        ks["stateBackward"] = True
    else:
        ks["stateBackward"] = False
    if (keyboard.is_pressed(ks["left_key"])):
        ks["stateLeft"] = True
    else:
        ks["stateLeft"] = False
    if (keyboard.is_pressed(ks["right_key"])):
        ks["stateRight"] = True
    else:
        ks["stateRight"] = False

    if ks["stateLeft"]==True:
        if ks["left_time_dif"] > ks["update_interval"] or ks["left_waiting"] == False:
            for (l,i) in zip(legs,range(num_legs)):
                l.turn(ks["turning_ang_per_int"]) #positive is CW
            ks["left_time"] = time.time()
            ks["left_time_dif"] = 0
            ks["left_waiting"] = True
        else:
            ks["left_time_dif"] = time.time() - ks["left_time"]

    if ks["stateRight"]==True:
        if ks["right_time_dif"] > ks["update_interval"] or ks["right_waiting"] == False:
            for (l,i) in zip(legs,range(num_legs)):
                l.turn(-1*ks["turning_ang_per_int"]) #positive is CW
            ks["right_time"] = time.time()
            ks["right_time_dif"] = 0
            ks["right_waiting"] = True
        else:
            ks["right_time_dif"] = time.time() - ks["right_time"]

    if ks["stateForward"]==True:
        if ks["orientationBack"]==False:
            for (l,i) in zip(legs,range(num_legs)):
                l.step()
        else:
            for (l,i) in zip(legs,range(num_legs)):
                l.reverse()
                l.step()
            ks["orientationBack"]=False
    elif ks["stateBackward"]==True:
        if ks["orientationBack"]==False:
            for (l,i) in zip(legs,range(num_legs)):
                l.reverse()
                l.step()
            ks["orientationBack"]=True
        else:
            for (l,i) in zip(legs,range(num_legs)):
                l.step()

    if ks["prev_stateLeft"]==True and ks["stateLeft"]==False:
        ks["left_waiting"] = False
    
    if ks["prev_stateRight"]==True and ks["stateRight"]==False:
        ks["right_waiting"] = False

    ks["prev_stateForward"] = ks["stateForward"]
    ks["prev_stateBackward"] = ks["stateBackward"]
    ks["prev_stateLeft"] = ks["stateLeft"]
    ks["prev_stateRight"] = ks["stateRight"]
    
    os.system(clear_msg)
    print("Step count: ", legs[0].step_count)
    print("Forward angle: ", legs[0].forward_angle/np.pi*180)

    # Keyboard code above

    for (l,i) in zip(legs,range(num_legs)):
        endpoints[i] = np.array(l.get_3D_endpoints())
    
    endpointsT = []
    for i in range(num_legs):
        endpointsT.append(np.transpose(endpoints[i]))

    for (sub_lines,sub_endpointsT,i) in zip(lines,endpointsT,range(num_legs)):
        for line,ind in zip(sub_lines,range(3)):
            line.set_data(sub_endpointsT[0:2,ind:ind+2])
            line.set_3d_properties(sub_endpointsT[2,ind:ind+2])
    
    angs = []
    for l in legs:
        angs.append(l.get_angles_deg(mode='servo'))

    for (sub_texts,sub_angs,i) in zip(texts,angs,range(num_legs)):
        for text,ang,pos in zip(sub_texts,sub_angs,endpoints[i][0:3]):
            x,y,_ = proj3d.proj_transform(pos[0],pos[1],pos[2], ax.get_proj())
            text.set_position((x,y))
            text.set_text('%.1f'%(ang))

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

    ks["forward_key"] = args.forward_key
    ks["backward_key"] = args.backward_key
    ks["left_key"] = args.left_key
    ks["right_key"] = args.right_key
    ks["turning_ang_per_int"] = args.turn_angle
    ks["update_interval"] = args.turn_interval

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
            k = 17;
            num_points = k;
            #theta = np.arccos((x_pos*TOT_LEN-FIRST_SEG_LEN)/(SECOND_SEG_LEN+THIRD_SEG_LEN));
            #radius = (SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(theta);
            for t in range(0,7):
                positions.append([x_offset,  y_radius*np.cos(-1*t/(8-1)*np.pi/2-np.pi/2)+y_offset,  z_offset])
            for t in range(0,3):
                positions.append([x_offset,  y_radius*np.cos(-1*t/(3-1)*np.pi-np.pi)+y_offset,  z_radius*np.sin(-1*t/(5-1)*np.pi-np.pi)+z_offset])
            for t in range(0,7):
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
        legs.append(leg.leg(num_segs=3,lens=[FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN],base_location=b_loc,base_angle=b_ang,positions=positions,forward_angle=b_ang,leg_ID=i,step_offset=step_offset,z_offset_height=z_offset_heights[i]))

    if (mode == "sim"):
        endpoints = []
        for l in legs:
            print(l)
            endpoints.append(np.array(l.get_3D_endpoints()))
            print(np.array(l.get_3D_endpoints()))
        print(endpoints)

        # Attaching 3D axis to the figure
        fig = plt.figure()
        ax = p3.Axes3D(fig)

        lines = []
        for i in range(num_legs):
            lines.append([ax.plot(endpoints[i][0:2,0],endpoints[i][0:2,1],endpoints[i][0:2,2],'-',linewidth=5,color=(0.5,0.5,1))[0],ax.plot(endpoints[i][1:3,0],endpoints[i][1:3,1],endpoints[i][1:3,2],'-',linewidth=5,color=(1,0.5,0.5))[0],ax.plot(endpoints[i][2:4,0],endpoints[i][2:4,1],endpoints[i][2:4,2],'-',linewidth=5,color=(0.5,1,0.5))[0]])
        print(lines)

        texts = []
        for i in range(num_legs):
            texts.append([ax.text2D(endpoints[i][0,0],endpoints[i][0,1],"test",color='black',fontsize=15,weight='bold'),ax.text2D(endpoints[i][1,0],endpoints[i][1,1],"test",color='black',fontsize=15,weight='bold'),ax.text2D(endpoints[i][3,0],endpoints[i][3,1],"test",color='black',fontsize=15,weight='bold')])
        print(texts)

        # Setting the axes properties
        ax.set_xlim3d([-1*(TOT_LEN), 1*(TOT_LEN)])
        ax.set_xlabel('X')

        ax.set_ylim3d([-1*(TOT_LEN), 1*(TOT_LEN)])
        ax.set_ylabel('Y')

        ax.set_zlim3d([-1*(TOT_LEN), 1*(TOT_LEN)])
        ax.set_zlabel('Z')

        # Creating the Animation object
        line_ani = animation.FuncAnimation(fig, update_legs, 400, fargs=(legs, lines, texts, ax, positions, ks),
                                      interval=1, blit=False)

        plt.show()

    elif (mode == "servo"):
        angs = []
        for l in legs:
            angs.append(l.get_angles_deg(mode='servo')+90)
        print_angs(num_legs,angs)
        update_angs(num_legs,angs)
        print(angs)

        while True:
            try:
                # Keyboard code below
                # Using arrows keys instead because matplotlib hotkeys

                if (keyboard.is_pressed(ks["forward_key"])):
                    ks["stateForward"] = True
                else:
                    ks["stateForward"] = False
                if (keyboard.is_pressed(ks["backward_key"])):
                    ks["stateBackward"] = True
                else:
                    ks["stateBackward"] = False
                if (keyboard.is_pressed(ks["left_key"])):
                    ks["stateLeft"] = True
                else:
                    ks["stateLeft"] = False
                if (keyboard.is_pressed(ks["right_key"])):
                    ks["stateRight"] = True
                else:
                    ks["stateRight"] = False

                if ks["stateLeft"]==True:
                    if ks["left_time_dif"] > ks["update_interval"] or ks["left_waiting"] == False:
                        for (l,i) in zip(legs,range(num_legs)):
                            l.turn(ks["turning_ang_per_int"]) #positive is CW
                        ks["left_time"] = time.time()
                        ks["left_time_dif"] = 0
                        ks["left_waiting"] = True
                    else:
                        ks["left_time_dif"] = time.time() - ks["left_time"]

                if ks["stateRight"]==True:
                    if ks["right_time_dif"] > ks["update_interval"] or ks["right_waiting"] == False:
                        for (l,i) in zip(legs,range(num_legs)):
                            l.turn(-1*ks["turning_ang_per_int"]) #positive is CW
                        ks["right_time"] = time.time()
                        ks["right_time_dif"] = 0
                        ks["right_waiting"] = True
                    else:
                        ks["right_time_dif"] = time.time() - ks["right_time"]

                if ks["stateForward"]==True:
                    if ks["orientationBack"]==False:
                        for (l,i) in zip(legs,range(num_legs)):
                            l.step()
                    else:
                        for (l,i) in zip(legs,range(num_legs)):
                            l.reverse()
                            l.step()
                        ks["orientationBack"]=False
                elif ks["stateBackward"]==True:
                    if ks["orientationBack"]==False:
                        for (l,i) in zip(legs,range(num_legs)):
                            l.reverse()
                            l.step()
                        ks["orientationBack"]=True
                    else:
                        for (l,i) in zip(legs,range(num_legs)):
                            l.step()

                if ks["prev_stateLeft"]==True and ks["stateLeft"]==False:
                    ks["left_waiting"] = False
                
                if ks["prev_stateRight"]==True and ks["stateRight"]==False:
                    ks["right_waiting"] = False

                ks["prev_stateForward"] = ks["stateForward"]
                ks["prev_stateBackward"] = ks["stateBackward"]
                ks["prev_stateLeft"] = ks["stateLeft"]
                ks["prev_stateRight"] = ks["stateRight"]

                for (l,k) in zip(legs,range(num_legs)):
                    angs[k] = l.get_angles_deg(mode='servo')+90
                    
                update_angs(num_legs,angs)
                os.system(clear_msg)
                print("Step count: ", legs[0].step_count)
                print("Forward angle: ", legs[0].forward_angle/np.pi*180)
                print_angs(num_legs,angs)
                time.sleep(wait_time)

            except KeyboardInterrupt:
                exit()

    else:
        print("Unrecognized mode: ", mode)
        quit()

