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

import numpy as np
import leg

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d.proj3d as proj3d
import matplotlib.animation as animation

from adafruit_servokit import ServoKit

import path_scaling as ps


kit = ServoKit(channels=16)


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
            full_range_test_slow: runs each servo through full range of motion.
            full_range_test_fast: same as above, less path points.
            file name: used when path source is external.
            """))
    parser.add_argument("--num_points",dest="num_points",type=int,default=100,help="number of data points in path, deprecated")
    parser.add_argument("--wait_time",dest="wait_time",type=float,default=0,help="force sleep time between each data point")
    parser.add_argument("--num_legs",dest="num_legs",type=int,default=1,help="number of legs")

    return parser.parse_args()

def update_legs(num, legs, lines, texts, ax, positions):
    '''
    if (num == 0):
        print("Animation reset")
    '''

    for (l,i) in zip(legs,range(num_legs)):
        l.step()
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


def print_angs(num_legs,angs):
    for i in range(num_legs):
        print("Leg ",i)
        print(angs[i])
    print("")


def update_angs(num_legs,angs):
    '''
	for (ang,i) in zip(angs,range(3)):
		kit.servo[i].angle = ang
	return None
	'''
    for (i) in range(num_legs):
        kit.servo[3*i+0].angle = angs[i][0]
        kit.servo[3*i+1].angle = angs[i][1]
        kit.servo[3*i+2].angle = angs[i][2]+90


if __name__ == '__main__':

    args = parse_arguments()
    FIRST_SEG_LEN = args.seg1_len
    SECOND_SEG_LEN = args.seg2_len
    THIRD_SEG_LEN = args.seg3_len
    mode = args.mode
    path_source = args.path_source
    path_data = args.path_data
    num_points = args.num_points
    wait_time = args.wait_time
    num_legs = args.num_legs

    TOT_LEN = FIRST_SEG_LEN + SECOND_SEG_LEN + THIRD_SEG_LEN;
    SECOND_THIRD_LEN = SECOND_SEG_LEN + THIRD_SEG_LEN;

    base_locs = []
    base_angs = []
    angle_inc = 2*np.pi/num_legs
    for i in range(num_legs):
        base_angs.append(i*angle_inc)
        base_locs.append([1*np.cos(base_angs[i]),-1*np.sin(base_angs[i]),0])

    positions = []

    if (path_source == "internal"):
        
        if (path_data == "reset"):
            num_points = 10
            for t in range(10):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN,0,0])
                    
        elif (path_data == "ellipse"):
            k = 25;
            num_points = k;
            pos_x = 0.8
            theta = np.arccos((pos_x*TOT_LEN-FIRST_SEG_LEN)/(SECOND_SEG_LEN+THIRD_SEG_LEN));
            radius = (SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(theta);
            # Scaling the radius
            y_scale = 1/2;
            z_scale = 1/2;
            # Offset specified as a factor of the scaled radius
            y_offset = 0;
            z_offset = -0.5;

            for t in range(k):
                positions.append([TOT_LEN*pos_x,y_scale*radius*np.cos(-1*t/(k-1)*2*np.pi-np.pi/2)+y_offset*y_scale*radius,z_scale*radius*np.sin(t/(k-1)*2*np.pi-np.pi/2)+z_offset*z_scale*radius])
        
        elif (path_data == "full_range_test_slow"):
            num_points = 500
            for t in range(50):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN*np.cos(t*np.pi/4/49),0,THIRD_SEG_LEN*np.sin(t*np.pi/4/49)])
            for t in reversed(range(50)):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN*np.cos(t*np.pi/4/49),0,THIRD_SEG_LEN*np.sin(t*np.pi/4/49)])
            for t in range(50):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN*np.cos(-t*np.pi/4/49),0,THIRD_SEG_LEN*np.sin(-t*np.pi/4/49)])
            for t in reversed(range(50)):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN*np.cos(-t*np.pi/4/49),0,THIRD_SEG_LEN*np.sin(-t*np.pi/4/49)])
            for t in range(50):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(t*np.pi/4/49),0,(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(t*np.pi/4/49)])
            for t in reversed(range(50)):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(t*np.pi/4/49),0,(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(t*np.pi/4/49)])
            for t in range(50):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(-t*np.pi/4/49),0,(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(-t*np.pi/4/49)])
            for t in reversed(range(50)):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(-t*np.pi/4/49),0,(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(-t*np.pi/4/49)])
            for t in range(50):
                positions.append([(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(t*np.pi/4/49),(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(t*np.pi/4/49),0])
            for t in reversed(range(50)):
                positions.append([(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(t*np.pi/4/49),(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(t*np.pi/4/49),0])

        elif (path_data == "full_range_test_fast"):
            num_points = 100
            for t in range(10):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN*np.cos(t*np.pi/4/9),0,THIRD_SEG_LEN*np.sin(t*np.pi/4/9)])
            for t in reversed(range(10)):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN*np.cos(t*np.pi/4/9),0,THIRD_SEG_LEN*np.sin(t*np.pi/4/9)])
            for t in range(10):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN*np.cos(-t*np.pi/4/9),0,THIRD_SEG_LEN*np.sin(-t*np.pi/4/9)])
            for t in reversed(range(10)):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN*np.cos(-t*np.pi/4/9),0,THIRD_SEG_LEN*np.sin(-t*np.pi/4/9)])
            for t in range(10):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(t*np.pi/4/9),0,(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(t*np.pi/4/9)])
            for t in reversed(range(10)):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(t*np.pi/4/9),0,(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(t*np.pi/4/9)])
            for t in range(10):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(-t*np.pi/4/9),0,(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(-t*np.pi/4/9)])
            for t in reversed(range(10)):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(-t*np.pi/4/9),0,(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(-t*np.pi/4/9)])
            for t in range(10):
                positions.append([(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(t*np.pi/4/9),(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(t*np.pi/4/9),0])
            for t in reversed(range(10)):
                positions.append([(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(t*np.pi/4/9),(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(t*np.pi/4/9),0])
        
        elif (path_data == "up-down"):
            k = 50;
            num_points = 2*k
            for t in range(k):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4),0,1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k-1))-0.5*TOT_LEN])
            for t in reversed(range(k)):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4),0,1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k-1))-0.5*TOT_LEN])
            
        elif (path_data == "side"):
            k = 50
            num_points = 4*k
            for t in range(k):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4),1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k-1)),-0.23*TOT_LEN])
            for t in reversed(range(k)):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4),1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k-1)),-0.23*TOT_LEN])
            for t in range(k):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4),-1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k-1)),-0.23*TOT_LEN])
            for t in reversed(range(k)):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4),-1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k-1)),-0.23*TOT_LEN])
            
        elif (path_data == "box"):
            
            num_points = 4*50 + 4*25;
            k = 50;

            x_offset_factor = 0
            z_offset_factor = 0.3

            for t in range(k):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4)+x_offset_factor*TOT_LEN,0,1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k-1))-z_offset_factor*TOT_LEN])
            for t in range(int(k/2)):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4)+x_offset_factor*TOT_LEN,-1/4*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k/2-1)),1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(2)-z_offset_factor*TOT_LEN])
            for t in reversed(range(k)):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4)+x_offset_factor*TOT_LEN,-1/4*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(2),1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k-1))-z_offset_factor*TOT_LEN])
            for t in reversed(range(int(k/2))):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4)+x_offset_factor*TOT_LEN,-1/4*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k/2-1)),-z_offset_factor*TOT_LEN])
            for t in range(int(k/2)):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4)+x_offset_factor*TOT_LEN,1/4*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k/2-1)),-z_offset_factor*TOT_LEN])
            for t in range(k):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4)+x_offset_factor*TOT_LEN,1/4*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(2),1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k-1))-z_offset_factor*TOT_LEN])
            for t in reversed(range(int(k/2))):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4)+x_offset_factor*TOT_LEN,1/4*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k/2-1)),1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(2)-z_offset_factor*TOT_LEN])
            for t in reversed(range(k)):
                positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4)+x_offset_factor*TOT_LEN,0,1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k-1))-z_offset_factor*TOT_LEN])
                 
        else:
            print("Unrecognized internal data: ", path_data)
            quit()

    elif (path_source == "external"):
        '''
        positions = np.genfromtxt(path_data, delimiter=",")
        positions = positions.tolist()
        num_points = len(positions)
        '''
        positions = np.genfromtxt(path_data, delimiter=",")
        positions = ps.scale_path(positions,FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN,x=0.6,y_scale=1/2,z_scale=1/2,z_offset=-0.5)
        num_points = positions.shape[0]
    else:
        print("Unrecognized path source: ", path_source)
        quit()

    #legs = leg.leg(3,[FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN])
    legs = []
    for (i,b_loc,b_ang) in zip(range(num_legs),base_locs,base_angs):
        legs.append(leg.leg(3,[FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN],b_loc,b_ang,positions,b_ang))

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
        ax.set_xlim3d([-1*(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN), 1*(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)])
        ax.set_xlabel('X')

        ax.set_ylim3d([-1*(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN), 1*(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)])
        ax.set_ylabel('Y')

        ax.set_zlim3d([-1*(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN), 1*(FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN)])
        ax.set_zlabel('Z')

        ax.set_title('Single Leg Test')

        # Creating the Animation object
        line_ani = animation.FuncAnimation(fig, update_legs, 400, fargs=(legs, lines, texts, ax, positions),
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
                for (l,k) in zip(legs,range(num_legs)):
                    l.step()
                    angs[k] = l.get_angles_deg(mode='servo')+90
                    
                update_angs(num_legs,angs)
                print_angs(num_legs,angs)
                time.sleep(wait_time)

            except KeyboardInterrupt:
                exit()

        '''
        for i in range(5*num_points):
            for (l,k) in zip(legs,range(num_legs)):
                l.step()
                angs[k] = l.get_angles_deg(mode='servo')+90
            update_angs(num_legs,angs)
            print_angs(num_legs,angs)
            time.sleep(wait_time)
        '''

    else:
        print("Unrecognized mode: ", mode)
        quit()

