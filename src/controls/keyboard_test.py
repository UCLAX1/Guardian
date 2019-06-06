import keyboard
import numpy as np
import time as t #for time.sleep

import leg
import path_scaling as ps

import os
import sys

CURSOR_UP_ONE = u"\u001b[{1}F"
ERASE_LINE = u"\u001b[{1}K"

def delete_last_lines(n=1):
    for _ in range(n):
        sys.stdout.write(u"\u001b[{1}F")
        sys.stdout.write(u"\u001b[{1}K")

#def keyboardcontrols()

print("Starting test keyboard script")



#pass in a leg object
def holdwasd():

	FIRST_SEG_LEN = 1
	SECOND_SEG_LEN = 1
	THIRD_SEG_LEN = 1

	positions = np.genfromtxt("data.txt", delimiter=",")
	positions = ps.scale_path(positions,FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN,0.7)
	num_points = positions.shape[0]

	l=leg.leg(3,[FIRST_SEG_LEN,SECOND_SEG_LEN,THIRD_SEG_LEN],[0,0,0],0,positions,0) #idk just borrowing this for now 

	#t=time.time()

	count = 0

	stateW = False
	stateA = False
	stateS = False
	stateD = False
	prev_stateW = False
	prev_stateA = False
	prev_stateS = False
	prev_stateD = False
	orientationBack=False

	a_time = 0
	a_time_dif = 0
	a_waiting = False
	d_time = 0
	d_time_dif = 0
	d_waiting = False

	turning_ang = 90*np.pi/180
	turning_time = 5
	turning_rate = turning_ang / turning_time
	update_interval = 0.1
	turning_ang_per_int = turning_rate*update_interval

	while True:
		try:
			if (keyboard.is_pressed('w')):
				stateW = True
			else:
				stateW = False
			if (keyboard.is_pressed('a')):
				stateA = True
			else:
				stateA = False
			if (keyboard.is_pressed('s')):
				stateS = True
			else:
				stateS = False
			if (keyboard.is_pressed('d')):
				stateD = True
			else:
				stateD = False

			if stateA==True:
				#print("hold a leg")
				if a_time_dif > update_interval or a_waiting == False:
					#print("Turn 10 deg CCW")
					l.turn(turning_ang_per_int) #positive is CW
					a_time = t.time()
					a_time_dif = 0
					a_waiting = True
				else:
					a_time_dif = t.time() - a_time

			if stateD==True:
				#print("hold d leg")
				if d_time_dif > update_interval or d_waiting == False:
					#print("Turn 10 deg CW")
					l.turn(-1*turning_ang_per_int) #positive is CW
					d_time = t.time()
					d_time_dif = 0
					d_waiting = True
				else:
					d_time_dif = t.time() - d_time

			if stateW==True:
				#print("hold w leg")
				if orientationBack==False:
					l.step()
				else:
					#print("turn 180")
					l.turn(np.pi)
					l.step()
					orientationBack=False
			elif stateS==True:
				#print("hold s leg")
				if orientationBack==False:
					#print("turn 180")
					l.turn(-1*np.pi)
					l.step()
					orientationBack=True
				else:
					l.step()

			if prev_stateW==True and stateW==False:
				count = count +1
				#print("you let go of w")
				#do leg.step()
			prev_stateW = stateW

			if prev_stateA==True and stateA==False:
				count = count +1
				#print("you let go of a")
				a_waiting = False
				#do leg.step()
			prev_stateA = stateA

			if prev_stateS==True and stateS==False:
				count = count +1
				#print("you let go of s")
				#do leg.step()
			prev_stateS = stateS

			if prev_stateD==True and stateD==False:
				count = count +1
				#print("you let go of d")
				d_waiting = False
				#do leg.step()
			prev_stateD = stateD

			if (keyboard.is_pressed('q')): #q is to exit immediately
				exit()

			os.system("cls")
			print("Step count: ", l.step_count)
			print("Forward angle: ", l.forward_angle/np.pi*180)
			

		except KeyboardInterrupt:
			exit()

holdwasd()


#import subprocess as sp
#sp.call('clear',shell=True)
