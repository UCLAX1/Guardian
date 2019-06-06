from adafruit_servokit import ServoKit

import argparse
import time

kit = ServoKit(channels=16)
#kit._pca.frequency = 50

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ang1",dest="ang1",type=float,default=1)
    parser.add_argument("--ang2",dest="ang2",type=float,default=1)
    parser.add_argument("--ang3",dest="ang3",type=float,default=1)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    increment = args.inc

    kit.servo[0].angle = 90
    kit.servo[1].angle = 90
    kit.servo[2].angle = 90
    time.sleep(1)
    kit.servo[0].angle = 90 + ang1
    kit.servo[1].angle = 90 + ang2
    kit.servo[2].angle = 90 + ang3 
    time.sleep(1)
    kit.servo[0].angle = 90
    kit.servo[1].angle = 90
    kit.servo[2].angle = 90

    print("Done")
    
