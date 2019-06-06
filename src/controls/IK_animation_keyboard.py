import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d.proj3d as proj3d
import matplotlib.animation as animation

import argparse
import os

import time
import keyboard

import leg
import path_scaling as ps

clear_msg = "clear"

if os.name == 'nt':
    clear_msg = "cls"
elif os.name == 'posix':
    clear_msg = "clear"


# Leg parameters
num_legs = 6
base_locs = []
base_angs = []
angle_inc = 2*np.pi/num_legs
base_radius = 2
for i in range(num_legs):
    base_angs.append(i*angle_inc)
    base_locs.append([base_radius*np.cos(base_angs[i]),-base_radius*np.sin(base_angs[i]),0])


keyboard_states = {
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

'''
keyboard_states = collections.namedtuple('keyboard_states', 
    'stateForward stateLeft stateBackward stateRight prev_stateForward prev_stateLeft prev_stateBackward prev_stateRight orientationBack left_time left_time_dif left_waiting right_time right_time_dif right_waiting update_interval turning_ang_per_int')

ks = keyboard_states(stateForward=False,stateLeft=False,stateBackward=False,stateRight=False,prev_stateForward=False,prev_stateLeft=False,
                     prev_stateBackward=False,prev_stateRight=False,orientationBack=False,
                     left_time=0,left_time_dif=0,left_waiting=0,right_time=0,right_time_dif=0,right_waiting=0,update_interval=0,turning_ang_per_int=0)
'''

def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("--path_data",dest="path_data",type=str,default="data.txt")
    parser.add_argument("--forward_key",dest="forward_key",type=str,default="up")
    parser.add_argument("--backward_key",dest="backward_key",type=str,default="down")
    parser.add_argument("--left_key",dest="left_key",type=str,default="left")
    parser.add_argument("--right_key",dest="right_key",type=str,default="right")
    parser.add_argument("--turn_angle",dest="turn_angle",type=float,default=2/180*np.pi)
    parser.add_argument("--turn_interval",dest="turn_interval",type=float,default=0.1)
    parser.add_argument("--x_offset",dest="x_offset",type=float,default=12)
    parser.add_argument("--y_radius",dest="y_radius",type=float,default=5)
    parser.add_argument("--z_radius",dest="z_radius",type=float,default=5)
    parser.add_argument("--y_offset",dest="y_offset",type=float,default=0)
    parser.add_argument("--z_offset",dest="z_offset",type=float,default=-15)

    return parser.parse_args()

def update_legs(num, legs, lines, texts, ax, positions,ks):
    '''
    if (num == 0):
        print("Animation reset")
    '''
    # Keyboard code below
    # Using arrows keys instead because matplotlib hotkeys

    if (keyboard.is_pressed(ks["forward_key"])):
        ks["stateForward"] = True
    else:
        ks["stateForward"] = False
    if (keyboard.is_pressed(ks["left_key"])):
        ks["stateLeft"] = True
    else:
        ks["stateLeft"] = False
    if (keyboard.is_pressed(ks["backward_key"])):
        ks["stateBackward"] = True
    else:
        ks["stateBackward"] = False
    if (keyboard.is_pressed(ks["right_key"])):
        ks["stateRight"] = True
    else:
        ks["stateRight"] = False

    if ks["stateLeft"]==True:
        #print("hold a leg")
        if ks["left_time_dif"] > ks["update_interval"] or ks["left_waiting"] == False:
            #print("Turn 10 deg CCW")
            for (l,i) in zip(legs,range(num_legs)):
                l.turn(ks["turning_ang_per_int"]) #positive is CW
            ks["left_time"] = time.time()
            ks["left_time_dif"] = 0
            ks["left_waiting"] = True
        else:
            ks["left_time_dif"] = time.time() - ks["left_time"]

    if ks["stateRight"]==True:
        #print("hold d leg")
        if ks["right_time_dif"] > ks["update_interval"] or ks["right_waiting"] == False:
            #print("Turn 10 deg CW")
            for (l,i) in zip(legs,range(num_legs)):
                l.turn(-1*ks["turning_ang_per_int"]) #positive is CW
            ks["right_time"] = time.time()
            ks["right_time_dif"] = 0
            ks["right_waiting"] = True
        else:
            ks["right_time_dif"] = time.time() - ks["right_time"]

    if ks["stateForward"]==True:
        #print("hold w leg")
        if ks["orientationBack"]==False:
            for (l,i) in zip(legs,range(num_legs)):
                l.step()
        else:
            #print("turn 180")
            for (l,i) in zip(legs,range(num_legs)):
                l.reverse()
                l.step()
            ks["orientationBack"]=False
    elif ks["stateBackward"]==True:
        #print("hold s leg")
        if ks["orientationBack"]==False:
            #print("turn 180")
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
    ks["prev_stateLeft"] = ks["stateLeft"]
    ks["prev_stateBackward"] = ks["stateBackward"]
    ks["prev_stateRight"] = ks["stateRight"]

    os.system(clear_msg)
    for i in range(0,num_legs):
        print("Legs ",i)
        print("Step count: ", legs[i].step_count)
        print("Forward angle: ", legs[i].forward_angle/np.pi*180)

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

if __name__ == '__main__':

        FIRST_SEG_LEN = 3.9
        SECOND_SEG_LEN = 7.75
        THIRD_SEG_LEN = 12.8

        args = parse_arguments()
        path_data = args.path_data

        keyboard_states["forward_key"] = args.forward_key
        keyboard_states["backward_key"] = args.backward_key
        keyboard_states["left_key"] = args.left_key
        keyboard_states["right_key"] = args.right_key
        keyboard_states["turning_ang_per_int"] = args.turn_angle
        keyboard_states["update_interval"] = args.turn_interval

        x_offset = args.x_offset
        y_radius = args.y_radius
        z_radius = args.z_radius
        y_offset = args.y_offset
        z_offset = args.z_offset


        '''
        positions = np.genfromtxt(path_data, delimiter=",")
        positions = ps.scale_path(positions,FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN,0.7)
        num_points = positions.shape[0]
        '''

        '''
        for ind in range(0,50):
                positions[ind] = positions[ind]
                positions[ind] = positions[ind]

        positions = positions.tolist()
        '''

        A = 1;
        B = SECOND_SEG_LEN / FIRST_SEG_LEN;
        C = THIRD_SEG_LEN / FIRST_SEG_LEN;


        TOT_LEN = FIRST_SEG_LEN + SECOND_SEG_LEN + THIRD_SEG_LEN
        SECOND_THIRD_LEN = SECOND_SEG_LEN + THIRD_SEG_LEN

        positions = []
        
        # Ellipse
        '''
        k = 19;
        num_points = k;
        #theta = np.arccos((x_pos*TOT_LEN-FIRST_SEG_LEN)/(SECOND_SEG_LEN+THIRD_SEG_LEN));
        #radius = (SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(theta);
        for t in range(k):
            positions.append([x_offset,  y_radius*np.cos(-1*t/(k-1)*2*np.pi-np.pi/2)+y_offset,  z_radius*np.sin(t/(k-1)*2*np.pi-np.pi/2)+z_offset])
        '''

        # Semicircle
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

        legs = []
        for (i,b_loc,b_ang) in zip(range(num_legs),base_locs,base_angs):
            if i%2 == 1:
                step_offset = 0.5
            else:
                step_offset = 0
            legs.append(leg.leg(num_segs=3,lens=[FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN],base_location=b_loc,base_angle=b_ang,positions=positions,forward_angle=b_ang,leg_ID=i,step_offset=step_offset))
        print(legs)

        endpoints = []
        for l in legs:
            print(l)
            endpoints.append(np.array(l.get_3D_endpoints()))
            print(np.array(l.get_3D_endpoints()))
        print(endpoints)

        # Attaching 3D axis to the figure
        fig = plt.figure()
        ax = p3.Axes3D(fig)
        # NOTE: Can't pass empty arrays into 3d version of plot()

        lines = []
        for i in range(num_legs):
            lines.append([ax.plot(endpoints[i][0:2,0],endpoints[i][0:2,1],endpoints[i][0:2,2],'-',linewidth=5,color=(0.5,0.5,1))[0],ax.plot(endpoints[i][1:3,0],endpoints[i][1:3,1],endpoints[i][1:3,2],'-',linewidth=5,color=(1,0.5,0.5))[0],ax.plot(endpoints[i][2:4,0],endpoints[i][2:4,1],endpoints[i][2:4,2],'-',linewidth=5,color=(0.5,1,0.5))[0]])
        print(lines)

        texts = []
        for i in range(num_legs):
            texts.append([ax.text2D(endpoints[i][0,0],endpoints[i][0,1],"test",color='black',fontsize=15,weight='bold'),ax.text2D(endpoints[i][1,0],endpoints[i][1,1],"test",color='black',fontsize=15,weight='bold'),ax.text2D(endpoints[i][3,0],endpoints[i][3,1],"test",color='black',fontsize=15,weight='bold')])
        print(texts)

        # Setting the axes properties
        ax.set_xlim3d([-1.2*(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN), 1.2*(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)])
        ax.set_xlabel('X')

        ax.set_ylim3d([-1.2*(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN), 1.2*(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)])
        ax.set_ylabel('Y')

        ax.set_zlim3d([-1.2*(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN), 1.2*(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)])
        ax.set_zlabel('Z')

        ax.set_title('Multi Leg Test')

        # Creating the Animation object
        line_ani = animation.FuncAnimation(fig, update_legs, 1000, fargs=(legs, lines, texts, ax, positions,keyboard_states),
                                      interval=1, blit=False)

        plt.show()
