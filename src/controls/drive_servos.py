"""
./drive_sim_servos.py
Jingbin Huang
UCLA ASME X1 Robotics 2018-2019

Drives servos for one leg, using external path data.

"""

import argparse
import os
import time

import numpy as np
import leg

from adafruit_servokit import ServoKit


kit = ServoKit(channels=16)

def parse_arguments():

	parser = argparse.ArgumentParser()
	parser.add_argument("--path_data",dest="path_data",type=str,default="data.txt")

	return parser.parse_args()

def print_angs(angs):
	for ang in angs:
		print(ang)
	print("")


def update_angs(angs):
	for (ang,i) in zip(angs,range(3)):
		kit.servo[i].angle = int(ang)
	return None


if __name__ == '__main__':

	args = parse_arguments()
	path_data = args.path_data

	positions = np.genfromtxt(path_data, delimiter=",")
	positions = positions.tolist()

	FIRST_LEG_LEN = 1.7
	SECOND_LEG_LEN = 1
	THIRD_LEG_LEN = 2.25

	legs = leg.leg(3,[FIRST_LEG_LEN,SECOND_LEG_LEN,THIRD_LEG_LEN])
	angs = legs.get_angles_deg(mode='servo')+90
	print_angs(angs)
	update_angs(angs)

	for pos in positions:
		legs.follow_lsq([pos[0],pos[1],pos[2]])
		angs = legs.get_angles_deg(mode='servo')+90
		#import pdb; pdb.set_trace()
		update_angs(angs)
		print_angs(angs)
		time.sleep(0.1)
