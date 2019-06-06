import numpy as np
np.set_printoptions(threshold=np.nan)
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import mpl_toolkits.mplot3d.proj3d as proj3d
import matplotlib.animation as animation

import argparse
import os

import leg

import path_scaling as ps

'''
num_legs = 4
base_locs = [[1,0,0],[0,-1,0],[-1,0,0],[0,1,0]]
base_angs = [0,np.pi/2,np.pi,-1*np.pi/2]
'''
num_legs = 1
base_locs = []
base_angs = []
angle_inc = 2*np.pi/num_legs
for i in range(num_legs):
    base_angs.append(i*angle_inc)
    base_locs.append([1*np.cos(base_angs[i]),-1*np.sin(base_angs[i]),0])

def parse_arguments():

	parser = argparse.ArgumentParser()
	parser.add_argument("--path_data",dest="path_data",type=str,default="data.txt")

	return parser.parse_args()

def update_legs(num, legs, lines, texts, ax, positions):
    if (num == 0):
        print("Animation reset")
    for (l,i) in zip(legs,range(num_legs)):
        if (num == 0):
            l.set_forward_angle(base_angs[i])
        #l.follow_lsq(positions[num])
        l.step()
        # if (num > 100 and num < 300):
        #    l.turn(np.radians(90/200))
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

        
        positions = np.genfromtxt(path_data, delimiter=",")
        positions = ps.scale_path(positions,FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN,0.7)
        num_points = positions.shape[0]
        

        '''
        for ind in range(0,50):
                positions[ind] = positions[ind]
                positions[ind] = positions[ind]

        positions = positions.tolist()
        '''

        TOT_LEN = FIRST_SEG_LEN + SECOND_SEG_LEN + THIRD_SEG_LEN
        SECOND_THIRD_LEN = SECOND_SEG_LEN + THIRD_SEG_LEN

        #positions = []

        # Demo path
        '''
        for t in range(50):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN,THIRD_SEG_LEN*np.cos(t*np.pi/2/49),0,THIRD_SEG_LEN*np.sin(t*np.pi/2/49)])
        for t in range(70):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN-SECOND_SEG_LEN*t/69,0,THIRD_SEG_LEN+SECOND_SEG_LEN*t/69])
        for t in range(100):
                positions.append([FIRST_SEG_LEN*np.cos(t*2*np.pi/99),FIRST_SEG_LEN*np.sin(t*2*np.pi/99),SECOND_SEG_LEN,THIRD_SEG_LEN])
        for t in range(100):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(-1*t*np.pi/99+np.pi/2),0,(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(-1*t*np.pi/99+np.pi/2)])
        for t in range(50):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(t*np.pi/2/49-np.pi/2),0,(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.sin(t*np.pi/2/49-np.pi/2)])
        '''

        # Point convergence test
        '''
        for t in range(10):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN,0,0])
        for t in range(10):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(np.pi/4),0,(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(np.pi/4)])
        for t in range(10):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN,0,0])
        for t in range(10):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(np.pi/4),0,-1*(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(np.pi/4)])
        '''

        # Circular crawl path
        '''
        for t in range(100):
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(np.pi/4),-1*(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(np.pi/4)*np.cos(t*2*np.pi/99-np.pi/2),1*(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(np.pi/4)*np.sin(t*2*np.pi/99-np.pi/2)])
        for t in range(100):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN,0,0])
        '''

        # Elliptical crawl path
        '''
        for t in range(5):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN,0,0])
        '''
        '''
        for k in range(5):
                t = 0
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(np.pi/4),-1/4*np.sqrt(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(t*2*np.pi/99-np.pi/2),1/4*(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(np.pi/4)*np.sin(t*2*np.pi/99-np.pi/2)-1])
        
        
        k = 100;
        num_points = k;

        pos_x = 0.8
        theta = np.arccos((pos_x*TOT_LEN-FIRST_SEG_LEN)/(SECOND_SEG_LEN+THIRD_SEG_LEN));
        radius = (SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(theta);
        # Scaling the radius
        y_scale = 1/4;
        z_scale = 1/4;
        # Offset specified as a factor of the scaled radius
        y_offset = 0;
        z_offset = -0.5;

        for t in range(k):
                positions.append([TOT_LEN*pos_x,y_scale*radius*np.cos(-1*t/(k-1)*2*np.pi-np.pi/2)+y_offset*y_scale*radius,z_scale*radius*np.sin(t/(k-1)*2*np.pi-np.pi/2)+z_offset*z_scale*radius])
        
        
        for k in range(5):
                t = 99
                positions.append([FIRST_SEG_LEN+(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(np.pi/4),-1/4*np.sqrt(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(t*2*np.pi/99-np.pi/2),1/4*(SECOND_SEG_LEN+THIRD_SEG_LEN)*np.cos(np.pi/4)*np.sin(t*2*np.pi/99-np.pi/2)-1])
        '''
        '''
        for t in range(5):
                positions.append([FIRST_SEG_LEN+SECOND_SEG_LEN+THIRD_SEG_LEN,0,0])
        '''
        # print(positions)

        # Up-down motion
        '''
        k = 50;
        num_points = 2*k
        for t in range(k):
            positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4),0,1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k-1))-0.5*TOT_LEN])
        for t in reversed(range(k)):
            positions.append([FIRST_SEG_LEN+(SECOND_THIRD_LEN)*np.cos(np.pi/4),0,1/2*(SECOND_THIRD_LEN)*np.cos(np.pi/4)*(t*2/(k-1))-0.5*TOT_LEN])
        '''

        # Side-to-side motion
        '''
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
        '''

        # Box motion
        '''
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
        '''

        legs = []
        for (i,b_loc,b_ang) in zip(range(num_legs),base_locs,base_angs):
            legs.append(leg.leg(3,[FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN],b_loc,b_ang,positions,b_ang,i))
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

        ax.set_title('Single Leg Test')

        # Creating the Animation object
        line_ani = animation.FuncAnimation(fig, update_legs, num_points, fargs=(legs, lines, texts, ax, positions),
                                      interval=1, blit=False)

        plt.show()
